import { describe, expect, it } from "vitest";

import { ApiError } from "@/api/client";

describe("ApiError", () => {
  it("stores status and detail", () => {
    const err = new ApiError(401, "Unauthorized");
    expect(err.status).toBe(401);
    expect(err.detail).toBe("Unauthorized");
    expect(err.message).toBe("Unauthorized");
  });
});
