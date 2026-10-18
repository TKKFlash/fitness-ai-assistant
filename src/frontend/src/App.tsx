import { useState } from "react";
import { clearToken, getToken } from "./api/client";
import { LoginPage } from "./pages/LoginPage";
import { ProfilePage } from "./pages/ProfilePage";
import { RedFlagPage } from "./pages/RedFlagPage";
import type { RedFlagResult } from "./api/safety";

type Tab = "profile" | "safety";

export function App() {
  const [loggedIn, setLoggedIn] = useState(() => getToken() !== null);
  const [tab, setTab] = useState<Tab>("profile");
  const [redFlagResult, setRedFlagResult] = useState<RedFlagResult | null>(null);

  if (!loggedIn) {
    return <LoginPage onLoggedIn={() => setLoggedIn(true)} />;
  }

  return (
    <>
      <nav>
        <button type="button" onClick={() => setTab("profile")} aria-pressed={tab === "profile"}>
          档案
        </button>
        <button type="button" onClick={() => setTab("safety")} aria-pressed={tab === "safety"}>
          安全自查
        </button>
        <button
          type="button"
          onClick={() => {
            clearToken();
            setLoggedIn(false);
          }}
        >
          退出
        </button>
      </nav>
      {tab === "profile" && <ProfilePage />}
      {tab === "safety" && (
        <>
          <RedFlagPage onResult={setRedFlagResult} />
          {redFlagResult && (
            <section>
              {redFlagResult.triggered ? (
                <p role="alert">
                  检测到需要医生评估的情况：{redFlagResult.reasons.join("、")}。
                  在咨询医生之前，助手不会给出训练强度或热量建议。
                </p>
              ) : (
                <p role="status">自查未发现需要优先就医的情况。</p>
              )}
            </section>
          )}
        </>
      )}
    </>
  );
}
