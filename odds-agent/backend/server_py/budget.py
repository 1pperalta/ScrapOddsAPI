import json
import os
from datetime import datetime, date
from pathlib import Path
from threading import Lock


BUDGET_STATE_FILE = Path(__file__).parent / "budget_state.json"

INPUT_COST_PER_TOKEN = 0.15 / 1_000_000
OUTPUT_COST_PER_TOKEN = 0.75 / 1_000_000


class BudgetExhaustedError(Exception):
    pass


class BudgetTracker:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "_initialized"):
            return
        self._initialized = True
        self._file_lock = Lock()
        self.total_limit = float(os.getenv("BUDGET_LIMIT_USD", "5.0"))
        self.daily_limit = float(os.getenv("DAILY_LIMIT_USD", "1.0"))
        self.max_output_tokens = int(os.getenv("MAX_OUTPUT_TOKENS", "800"))
        self._state = self._load_state()

    def _default_state(self) -> dict:
        return {
            "total_spent_usd": 0.0,
            "daily_spent_usd": 0.0,
            "current_date": date.today().isoformat(),
            "total_requests": 0,
            "total_input_tokens": 0,
            "total_output_tokens": 0,
        }

    def _load_state(self) -> dict:
        if BUDGET_STATE_FILE.exists():
            try:
                with open(BUDGET_STATE_FILE, "r") as f:
                    state = json.load(f)
                if state.get("current_date") != date.today().isoformat():
                    state["daily_spent_usd"] = 0.0
                    state["current_date"] = date.today().isoformat()
                return state
            except (json.JSONDecodeError, KeyError):
                return self._default_state()
        return self._default_state()

    def _save_state(self):
        with open(BUDGET_STATE_FILE, "w") as f:
            json.dump(self._state, f, indent=2)

    def check_budget(self):
        with self._file_lock:
            self._state = self._load_state()

            if self._state["total_spent_usd"] >= self.total_limit:
                raise BudgetExhaustedError(
                    f"Total budget exhausted: ${self._state['total_spent_usd']:.4f} / ${self.total_limit:.2f}"
                )
            if self._state["daily_spent_usd"] >= self.daily_limit:
                raise BudgetExhaustedError(
                    f"Daily budget exhausted: ${self._state['daily_spent_usd']:.4f} / ${self.daily_limit:.2f}"
                )

    def record_usage(self, input_tokens: int, output_tokens: int):
        cost = (input_tokens * INPUT_COST_PER_TOKEN) + (output_tokens * OUTPUT_COST_PER_TOKEN)

        with self._file_lock:
            self._state = self._load_state()
            self._state["total_spent_usd"] += cost
            self._state["daily_spent_usd"] += cost
            self._state["total_requests"] += 1
            self._state["total_input_tokens"] += input_tokens
            self._state["total_output_tokens"] += output_tokens
            self._save_state()

        return cost

    def get_status(self) -> dict:
        with self._file_lock:
            self._state = self._load_state()
            return {
                "total_spent_usd": round(self._state["total_spent_usd"], 6),
                "total_remaining_usd": round(self.total_limit - self._state["total_spent_usd"], 6),
                "daily_spent_usd": round(self._state["daily_spent_usd"], 6),
                "daily_remaining_usd": round(self.daily_limit - self._state["daily_spent_usd"], 6),
                "total_limit_usd": self.total_limit,
                "daily_limit_usd": self.daily_limit,
                "total_requests": self._state["total_requests"],
                "total_input_tokens": self._state["total_input_tokens"],
                "total_output_tokens": self._state["total_output_tokens"],
                "date": self._state["current_date"],
            }


def get_budget_tracker() -> BudgetTracker:
    return BudgetTracker()
