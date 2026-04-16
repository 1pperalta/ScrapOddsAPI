# Frontend Testing & Reliability Skill

This skill enforces a robust, test-driven approach to React component development and promotes high UI reliability.

## Core Mandates

1. **Test-Driven Component Development (TDD):**
   - **MUST** provide or update a corresponding test file whenever you create or modify a React component.
   - Use **Vitest** as the test runner and **React Testing Library (@testing-library/react)** for rendering components.

2. **Behavioral Testing over Implementation:**
   - **FOCUS** tests on user interactions (clicking, typing) and observable state changes (loading spinners, error messages, rendered data).
   - **DO NOT** test internal component state, hook implementations, or CSS classes directly unless they are crucial for functionality (e.g., accessibility roles).

3. **API Mocking:**
   - **MUST** mock all external API calls and side effects.
   - Use `vi.mock()` or standard mock response objects when simulating the backend `/api/agent/...` endpoints to ensure tests run quickly and deterministically without requiring a live server.

4. **Error Boundaries & Graceful Degradation:**
   - When building complex UI components (especially those rendering Markdown or parsing AI responses), suggest or implement React Error Boundaries.
   - Ensure the UI degrades gracefully: if an AI response is malformed, display a friendly fallback message rather than crashing the application.

5. **Accessibility (a11y) First:**
   - Ensure components include appropriate `aria-labels`, `roles`, and maintain keyboard navigability. Tests should verify these attributes when querying the DOM (e.g., using `getByRole`).
