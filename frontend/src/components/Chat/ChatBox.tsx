import type { ChatMessage } from "@/types/chat";

import { Card, CardContent } from "@/components/ui/card";

import { Message } from "./Message";

interface ChatBoxProps {
  messages: ChatMessage[];
}

export const ChatBox = ({ messages }: ChatBoxProps) => {
  return (
    <Card>
      <CardContent className="max-h-[60vh] min-h-[360px] space-y-3 overflow-y-auto p-4">
        {messages.length === 0 ? (
          <p className="text-sm text-slate-500">Your conversation will appear here.</p>
        ) : (
          messages.map((message) => <Message key={message.id} message={message} />)
        )}
      </CardContent>
    </Card>
  );
};
