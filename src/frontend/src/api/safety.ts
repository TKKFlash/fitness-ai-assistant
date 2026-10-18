import { request } from "./client";

export interface RedFlagAnswers {
  chest_pain_or_pressure: boolean;
  fainting_or_near_fainting: boolean;
  shortness_of_breath_at_rest: boolean;
  palpitations_or_irregular_heartbeat: boolean;
  unexplained_weight_loss: boolean;
  persistent_joint_pain_or_swelling: boolean;
  numbness_or_tingling: boolean;
  pregnant_or_postpartum_under_6_months: boolean;
  under_18: boolean;
  eating_disorder_history_or_current: boolean;
  diagnosed_heart_kidney_liver_or_thyroid_disease: boolean;
  diabetes_on_insulin_or_sulfonylurea: boolean;
  taking_anticoagulants_or_immunosuppressants: boolean;
  free_text: string;
}

export interface RedFlagResult {
  triggered: boolean;
  reasons: string[];
  severity: "refer_to_clinician" | "stop_training_advice" | null;
}

export function checkRedFlags(answers: RedFlagAnswers): Promise<RedFlagResult> {
  return request<RedFlagResult>("/api/safety/red-flags", {
    method: "POST",
    body: JSON.stringify(answers),
  });
}
