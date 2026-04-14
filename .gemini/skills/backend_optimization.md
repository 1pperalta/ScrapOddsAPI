# Backend Optimization Skill

This skill enforces high-performance, robust, and clean Python backend code practices, specifically tailored for the ScrapOddsAPI architecture.

## Core Mandates

1. **Strict Type Hinting:**
   - **MUST** use comprehensive type hints (`typing` module) for ALL function arguments, return values, and complex variable assignments.
   - Example: `def process_data(items: List[Dict[str, Any]]) -> Optional[str]:`

2. **Robust Logging:**
   - **NEVER** use `print()` for error handling or debugging in production-ready backend code.
   - **MUST** use the standard Python `logging` module or Flask's built-in logger (`app.logger`).
   - Include contextual information in logs (e.g., function names, variable states) to aid in tracing issues. 

3. **Resource & Connection Management:**
   - **MUST** utilize Connection Pooling for database interactions (e.g., via `psycopg2.pool` or SQLAlchemy). Do not instantiate fresh database connections on every request unless strictly necessary.
   - Ensure all database connections, API sessions, and file handlers are properly closed using `try...finally` blocks or context managers (`with` statement).

4. **Performance & Concurrency:**
   - **CONSIDER** caching strategies (like in-memory LRU or Redis) for expensive, repetitive operations (e.g., retrieving odds for high-profile matches).
   - If migrating or adding new endpoints that involve heavy I/O operations (like LLM calls), structure the code to allow for future asynchronous refactoring (e.g., keeping business logic separate from the routing layer).

5. **Error Handling:**
   - Catch specific exceptions rather than broad `Exception` clauses where possible.
   - Always return well-structured JSON error responses with appropriate HTTP status codes (e.g., 400 for bad requests, 500 for internal server errors).
