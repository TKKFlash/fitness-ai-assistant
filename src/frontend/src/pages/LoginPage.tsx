import { FormEvent, useState } from "react";
import { login } from "../api/auth";
import { ApiError } from "../api/client";

interface LoginPageProps {
  onLoggedIn: () => void;
}

export function LoginPage({ onLoggedIn }: LoginPageProps) {
  const [passcode, setPasscode] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setBusy(true);
    setError(null);
    try {
      await login(passcode);
      onLoggedIn();
    } catch (err) {
      if (err instanceof ApiError && err.status === 429) {
        setError("失败次数过多，请稍后再试");
      } else if (err instanceof ApiError && err.status === 401) {
        setError("口令不正确");
      } else {
        setError("无法连接服务器");
      }
    } finally {
      setBusy(false);
    }
  }

  return (
    <main>
      <h1>健身助手</h1>
      <form onSubmit={handleSubmit}>
        <label>
          口令
          <input
            type="password"
            value={passcode}
            onChange={(event) => setPasscode(event.target.value)}
            autoComplete="current-password"
            required
          />
        </label>
        <button type="submit" disabled={busy || passcode.length === 0}>
          登录
        </button>
      </form>
      {error && <p role="alert">{error}</p>}
    </main>
  );
}
