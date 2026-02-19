import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { GoogleOAuthProvider } from "@react-oauth/google";
import { AuthProvider } from "../contexts/AuthContext";
import ErrorBoundary from "../components/ErrorBoundary";

function ThrowingComponent() {
  throw new Error("Test error");
}

describe("ErrorBoundary", () => {
  it("renders children when no error", () => {
    render(
      <ErrorBoundary>
        <div data-testid="child">Hello</div>
      </ErrorBoundary>
    );
    expect(screen.getByTestId("child")).toBeDefined();
  });

  it("renders fallback UI on error", () => {
    // Suppress React error boundary console output during test
    const spy = vi.spyOn(console, "error").mockImplementation(() => {});
    render(
      <ErrorBoundary>
        <ThrowingComponent />
      </ErrorBoundary>
    );
    expect(screen.getByText("Something went wrong")).toBeDefined();
    spy.mockRestore();
  });
});

describe("App smoke test", () => {
  it("renders without crashing", async () => {
    // Dynamically import to avoid side-effect issues
    const { default: App } = await import("../App");
    // App includes splash screen, so we just ensure no throw
    expect(() => render(<App />)).not.toThrow();
  });
});
