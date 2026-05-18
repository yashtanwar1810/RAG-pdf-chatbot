import { z } from "zod";

const envSchema = z.object({
  VITE_API_BASE_URL: z.string().url().default("http://localhost:8000/api/v1"),
  VITE_REQUIRE_API_KEY: z.enum(["true", "false"]).default("false"),
  VITE_APP_API_KEY: z.string().default("")
});

const parsed = envSchema.parse({
  VITE_API_BASE_URL: import.meta.env.VITE_API_BASE_URL,
  VITE_REQUIRE_API_KEY: import.meta.env.VITE_REQUIRE_API_KEY,
  VITE_APP_API_KEY: import.meta.env.VITE_APP_API_KEY
});

export const env = {
  apiBaseUrl: parsed.VITE_API_BASE_URL,
  requireApiKey: parsed.VITE_REQUIRE_API_KEY === "true",
  appApiKey: parsed.VITE_APP_API_KEY
};
