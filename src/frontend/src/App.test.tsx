import { render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { App } from "./App";
import { HealthBadge } from "./components/HealthBadge";

describe("HealthBadge", () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("shows healthy when backend responds ok", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ ok: true }));
    render(<HealthBadge />);
    expect(await screen.findByText(/正常/)).toBeInTheDocument();
  });

  it("shows unavailable when backend is unreachable", async () => {
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new Error("down")));
    render(<HealthBadge />);
    await waitFor(() => expect(screen.getByText(/不可用/)).toBeInTheDocument());
  });
});

describe("App login gate", () => {
  beforeEach(() => {
    localStorage.clear();
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("shows the login page when no token is stored", () => {
    render(<App />);
    expect(screen.getByRole("button", { name: "登录" })).toBeInTheDocument();
  });

  it("shows the main navigation when a token is stored", () => {
    localStorage.setItem("fitness.token", "t");
    render(<App />);
    expect(screen.getByRole("button", { name: "退出" })).toBeInTheDocument();
  });
});
