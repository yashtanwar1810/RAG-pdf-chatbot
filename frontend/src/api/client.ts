import axios from "axios";

import { env } from "@/lib/env";

export class ApiError extends Error {
  public readonly status: number;
  public readonly detail: string;

  constructor(status: number, detail: string) {
    super(detail);
    this.status = status;
    this.detail = detail;
  }
}

export const apiClient = axios.create({
  baseURL: env.apiBaseUrl,
  timeout: 30_000,
  headers: {
    "Content-Type": "application/json"
  }
});

apiClient.interceptors.request.use((config) => {
  if (env.requireApiKey && env.appApiKey) {
    config.headers["x-api-key"] = env.appApiKey;
  }
  return config;
});

apiClient.interceptors.response.use(
  (response) => response,
  (error: unknown) => {
    if (axios.isAxiosError(error)) {
      const status = error.response?.status ?? 500;
      const detail = (error.response?.data as { detail?: string } | undefined)?.detail ?? error.message;
      return Promise.reject(new ApiError(status, detail));
    }
    return Promise.reject(new ApiError(500, "Unexpected network error"));
  }
);
