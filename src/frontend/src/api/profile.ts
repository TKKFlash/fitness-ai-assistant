import { request } from "./client";

export type Sex = "male" | "female";
export type Goal = "fat_loss" | "muscle_gain" | "maintain";
export type ActivityLevel = "sedentary" | "light" | "moderate" | "active" | "very_active";

export interface Profile {
  birth_date: string;
  sex: Sex;
  height_cm: number;
  training_years: number;
  activity_level: ActivityLevel;
  goal: Goal;
  equipment: string[];
  injuries: string[];
  chronic_conditions: string[];
  medications: string[];
  diet_restrictions: string[];
  allergies: string[];
  red_flags: string[];
}

export interface ProfileOut extends Profile {
  updated_at: string;
}

export function getProfile(): Promise<ProfileOut> {
  return request<ProfileOut>("/api/profile");
}

export function saveProfile(profile: Profile): Promise<ProfileOut> {
  return request<ProfileOut>("/api/profile", {
    method: "PUT",
    body: JSON.stringify(profile),
  });
}
