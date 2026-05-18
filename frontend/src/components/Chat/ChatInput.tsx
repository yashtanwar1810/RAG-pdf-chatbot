import { FormEvent, useState } from "react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

interface ChatInputProps {
  disabled?: boolean;
  onSubmit: (question: string) => void;
}

export const ChatInput = ({ disabled, onSubmit }: ChatInputProps) => {
  const [value, setValue] = useState("");

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const trimmed = value.trim();
    if (!trimmed) return;
    onSubmit(trimmed);
    setValue("");
  };

  return (
    <form className="flex gap-2" onSubmit={handleSubmit}>
      <Input
        aria-label="Ask question"
        disabled={disabled}
        placeholder="Ask a question about your document"
        value={value}
        onChange={(event) => setValue(event.target.value)}
      />
      <Button disabled={disabled || value.trim().length < 3} type="submit">
        Send
      </Button>
    </form>
  );
};
