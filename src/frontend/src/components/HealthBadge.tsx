import { useEffect, useState } from "react";

type Health = "checking" | "ok" | "down";

export function HealthBadge() {
  const [health, setHealth] = useState<Health>("checking");

  useEffect(() => {
    fetch("/healthz")
      .then((response) => setHealth(response.ok ? "ok" : "down"))
      .catch(() => setHealth("down"));
  }, []);

  const label = health === "checking" ? "检查中" : health === "ok" ? "正常" : "不可用";
  return <p>后端状态：{label}</p>;
}
