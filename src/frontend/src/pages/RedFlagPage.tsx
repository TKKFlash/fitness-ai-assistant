import { FormEvent, useState } from "react";
import { checkRedFlags, RedFlagAnswers, RedFlagResult } from "../api/safety";

const QUESTIONS: { field: keyof Omit<RedFlagAnswers, "free_text">; label: string }[] = [
  { field: "chest_pain_or_pressure", label: "运动或日常时有胸痛、胸闷" },
  { field: "fainting_or_near_fainting", label: "有过晕厥或接近晕厥" },
  { field: "shortness_of_breath_at_rest", label: "静息时也气短" },
  { field: "palpitations_or_irregular_heartbeat", label: "心悸或心律不齐" },
  { field: "unexplained_weight_loss", label: "近期体重下降但原因不明" },
  { field: "persistent_joint_pain_or_swelling", label: "持续的关节疼痛或肿胀" },
  { field: "numbness_or_tingling", label: "肢体麻木或刺痛" },
  { field: "pregnant_or_postpartum_under_6_months", label: "孕期或产后 6 个月内" },
  { field: "under_18", label: "未满 18 岁" },
  { field: "eating_disorder_history_or_current", label: "有饮食失调史或当前症状" },
  { field: "diagnosed_heart_kidney_liver_or_thyroid_disease", label: "已确诊心、肾、肝或甲状腺疾病" },
  { field: "diabetes_on_insulin_or_sulfonylurea", label: "糖尿病并使用胰岛素或磺脲类药物" },
  { field: "taking_anticoagulants_or_immunosuppressants", label: "正在服用抗凝药或免疫抑制剂" },
];

const EMPTY_ANSWERS: RedFlagAnswers = {
  chest_pain_or_pressure: false,
  fainting_or_near_fainting: false,
  shortness_of_breath_at_rest: false,
  palpitations_or_irregular_heartbeat: false,
  unexplained_weight_loss: false,
  persistent_joint_pain_or_swelling: false,
  numbness_or_tingling: false,
  pregnant_or_postpartum_under_6_months: false,
  under_18: false,
  eating_disorder_history_or_current: false,
  diagnosed_heart_kidney_liver_or_thyroid_disease: false,
  diabetes_on_insulin_or_sulfonylurea: false,
  taking_anticoagulants_or_immunosuppressants: false,
  free_text: "",
};

interface RedFlagPageProps {
  onResult: (result: RedFlagResult) => void;
}

export function RedFlagPage({ onResult }: RedFlagPageProps) {
  const [answers, setAnswers] = useState<RedFlagAnswers>(EMPTY_ANSWERS);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    try {
      onResult(await checkRedFlags(answers));
    } catch {
      setError("提交失败，请检查网络后重试");
    }
  }

  return (
    <main>
      <h1>安全自查</h1>
      <p>以下任一项为是，助手将停止强度和热量建议，并建议你先咨询医生。</p>
      <form onSubmit={handleSubmit}>
        {QUESTIONS.map(({ field, label }) => (
          <label key={field}>
            <input
              type="checkbox"
              checked={answers[field]}
              onChange={(event) =>
                setAnswers((prev) => ({ ...prev, [field]: event.target.checked }))
              }
            />
            {label}
          </label>
        ))}
        <label>
          其他补充（可选）
          <textarea
            maxLength={1000}
            value={answers.free_text}
            onChange={(event) =>
              setAnswers((prev) => ({ ...prev, free_text: event.target.value }))
            }
          />
        </label>
        <button type="submit">提交自查</button>
      </form>
      {error && <p role="alert">{error}</p>}
    </main>
  );
}
