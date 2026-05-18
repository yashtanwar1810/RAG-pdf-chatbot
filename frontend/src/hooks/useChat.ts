import { useMutation } from "@tanstack/react-query";

import { sendChat } from "@/api/ragApi";

export const useChat = () => {
  return useMutation({
    mutationFn: sendChat
  });
};
