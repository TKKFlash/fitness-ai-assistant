import { FormEvent, useState } from "react";
import { getProfile, Profile, ActivityLevel, Goal, Sex, saveProfile } from "../api/profile";
import { ApiError } from "../api/client";

const EMPTY_PROFILE: Profile = {
  birth_date: "",
  sex: "male",
  height_cm: 170,
  training_years: 0,
  activity_level: "moderate",
  goal: "maintain",
  equipment: [],
  injuries: [],
  chronic_conditions: [],
  medications: [],
  diet_restrictions: [],
  allergies: [],
  red_flags: [],
};

const LIST_FIELDS = [
  "equipment",
  "injuries",
  "chronic_conditions",
  "medications",
  "diet_restrictions",
  "allergies",
] as const;

const SEX_LABELS: Record<Sex, string> = { male: "男", female: "女" };
const GOAL_LABELS: Record<Goal, string> = {
  fat_loss: "减脂",
  muscle_gain: "增肌",
  maintain: "维持",
};
const ACTIVITY_LABELS: Record<ActivityLevel, string> = {
  sedentary: "久坐",
  light: "轻度活动",
  moderate: "中度活动",
  active: "高强度活动",
  very_active: "非常活跃",
};

function toList(text: string): string[] {
  return text
    .split(/[,，\n]/)
    .map((item) => item.trim())
    .filter(Boolean);
}

export function ProfilePage() {
  const [profile, setProfile] = useState<Profile>(EMPTY_PROFILE);
  const [listText, setListText] = useState<Record<string, string>>({});
  const [status, setStatus] = useState<string | null>(null);

  async function load() {
    try {
      const saved = await getProfile();
      setProfile(saved);
      setListText(
        Object.fromEntries(LIST_FIELDS.map((field) => [field, saved[field].join("、")])),
      );
    } catch (err) {
      if (!(err instanceof ApiError && err.status === 404)) {
        setStatus("读取档案失败");
      }
    }
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const payload: Profile = { ...profile };
    for (const field of LIST_FIELDS) {
      payload[field] = toList(listText[field] ?? "");
    }
    try {
      await saveProfile(payload);
      setStatus("已保存");
    } catch (err) {
      setStatus(
        err instanceof ApiError && err.status === 422 ? "有字段不合法，请检查" : "保存失败",
      );
    }
  }

  return (
    <main>
      <h1>我的档案</h1>
      <button type="button" onClick={load}>
        读取已保存的档案
      </button>
      <form onSubmit={handleSubmit}>
        <label>
          出生日期
          <input
            type="date"
            required
            value={profile.birth_date}
            onChange={(event) => setProfile({ ...profile, birth_date: event.target.value })}
          />
        </label>
        <label>
          性别
          <select
            value={profile.sex}
            onChange={(event) => setProfile({ ...profile, sex: event.target.value as Sex })}
          >
            {(Object.keys(SEX_LABELS) as Sex[]).map((value) => (
              <option key={value} value={value}>
                {SEX_LABELS[value]}
              </option>
            ))}
          </select>
        </label>
        <label>
          身高（cm）
          <input
            type="number"
            min={100}
            max={250}
            required
            value={profile.height_cm}
            onChange={(event) => setProfile({ ...profile, height_cm: Number(event.target.value) })}
          />
        </label>
        <label>
          训练年限
          <input
            type="number"
            min={0}
            max={60}
            step={0.5}
            value={profile.training_years}
            onChange={(event) =>
              setProfile({ ...profile, training_years: Number(event.target.value) })
            }
          />
        </label>
        <label>
          日常活动量
          <select
            value={profile.activity_level}
            onChange={(event) =>
              setProfile({ ...profile, activity_level: event.target.value as ActivityLevel })
            }
          >
            {(Object.keys(ACTIVITY_LABELS) as ActivityLevel[]).map((value) => (
              <option key={value} value={value}>
                {ACTIVITY_LABELS[value]}
              </option>
            ))}
          </select>
        </label>
        <label>
          目标
          <select
            value={profile.goal}
            onChange={(event) => setProfile({ ...profile, goal: event.target.value as Goal })}
          >
            {(Object.keys(GOAL_LABELS) as Goal[]).map((value) => (
              <option key={value} value={value}>
                {GOAL_LABELS[value]}
              </option>
            ))}
          </select>
        </label>
        <label>
          可用器械（用顿号或逗号分隔）
          <input
            value={listText.equipment ?? ""}
            onChange={(event) => setListText({ ...listText, equipment: event.target.value })}
          />
        </label>
        <label>
          伤病史
          <input
            value={listText.injuries ?? ""}
            onChange={(event) => setListText({ ...listText, injuries: event.target.value })}
          />
        </label>
        <label>
          慢性病
          <input
            value={listText.chronic_conditions ?? ""}
            onChange={(event) =>
              setListText({ ...listText, chronic_conditions: event.target.value })
            }
          />
        </label>
        <label>
          正在服用的药物
          <input
            value={listText.medications ?? ""}
            onChange={(event) => setListText({ ...listText, medications: event.target.value })}
          />
        </label>
        <label>
          饮食禁忌
          <input
            value={listText.diet_restrictions ?? ""}
            onChange={(event) =>
              setListText({ ...listText, diet_restrictions: event.target.value })
            }
          />
        </label>
        <label>
          过敏
          <input
            value={listText.allergies ?? ""}
            onChange={(event) => setListText({ ...listText, allergies: event.target.value })}
          />
        </label>
        <button type="submit">保存档案</button>
      </form>
      {status && <p role="status">{status}</p>}
    </main>
  );
}
