import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { Message } from "@/components/Chat/Message";

describe("Message", () => {
  it("renders assistant content", () => {
    render(<Message message={{ id: "1", role: "assistant", content: "hello" }} />);
    expect(screen.getByText("hello")).toBeInTheDocument();
  });
});
