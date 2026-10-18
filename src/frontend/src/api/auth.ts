import { request, setToken } from "./client";

export interface LoginResult {
  token: string;
  expires_at: number;
}

export function login(passcode: string): Promise<LoginResult> {
  return request<LoginResult>("/api/auth/login", {
    method: "POST",
    body: JSON.stringify({ passcode }),
  }).then((result) => {
    setToken(result.token);
    return result;
  });
}
