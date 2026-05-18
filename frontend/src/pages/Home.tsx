import { useMemo, useState } from "react";

import { ApiError } from "@/api/client";
import { ChatBox } from "@/components/Chat/ChatBox";
import { ChatInput } from "@/components/Chat/ChatInput";
import { DocumentList } from "@/components/Sidebar/DocumentList";
import { UploadBox } from "@/components/Upload/UploadBox";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useChat } from "@/hooks/useChat";
import { useDeleteDocument, useDocuments } from "@/hooks/useDocuments";
import { useUpload } from "@/hooks/useUpload";
import type { ChatMessage } from "@/types/chat";

const errorMessage = (error: unknown) => {
  if (error instanceof ApiError) return error.detail;
  if (error instanceof Error) return error.message;
  return "Unexpected error";
};

export const Home = () => {
  const [activeDocumentId, setActiveDocumentId] = useState<string | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);

  const documentsQuery = useDocuments();
  const uploadMutation = useUpload();
  const deleteMutation = useDeleteDocument();
  const chatMutation = useChat();

  const documents = documentsQuery.data ?? [];

  const statusText = useMemo(() => {
    if (uploadMutation.isPending) return "Uploading and indexing";
    if (chatMutation.isPending) return "Generating answer";
    if (documentsQuery.isFetching) return "Refreshing documents";
    return "Ready";
  }, [chatMutation.isPending, documentsQuery.isFetching, uploadMutation.isPending]);

  const handleUpload = (file: File) => {
    uploadMutation.mutate(file, {
      onSuccess: (result) => {
        setActiveDocumentId(result.document_id);
      }
    });
  };

  const handleDelete = (documentId: string) => {
    deleteMutation.mutate(documentId, {
      onSuccess: () => {
        if (activeDocumentId === documentId) {
          setActiveDocumentId(null);
          setMessages([]);
        }
      }
    });
  };

  const handleAsk = (question: string) => {
    if (!activeDocumentId) return;

    const userMessage: ChatMessage = {
      id: crypto.randomUUID(),
      role: "user",
      content: question
    };

    setMessages((prev) => [...prev, userMessage]);

    chatMutation.mutate(
      { document_id: activeDocumentId, question },
      {
        onSuccess: (res) => {
          setMessages((prev) => [
            ...prev,
            {
              id: crypto.randomUUID(),
              role: "assistant",
              content: res.answer
            }
          ]);
        }
      }
    );
  };

  const blockingError =
    documentsQuery.error ?? uploadMutation.error ?? deleteMutation.error ?? chatMutation.error;

  return (
    <main className="grid min-h-screen grid-cols-1 bg-slate-50 lg:grid-cols-[340px_1fr]">
      <DocumentList
        activeDocumentId={activeDocumentId}
        documents={documents}
        loading={documentsQuery.isLoading}
        onDelete={handleDelete}
        onSelect={setActiveDocumentId}
      />

      <section className="space-y-4 p-4 lg:p-6">
        <Card>
          <CardHeader className="flex-row items-center justify-between space-y-0">
            <CardTitle className="text-2xl">PDF RAG Assistant</CardTitle>
            <Badge aria-live="polite">{statusText}</Badge>
          </CardHeader>
          <CardContent className="text-sm text-slate-500">
            Upload a document, select it, and ask grounded questions with source-backed responses.
          </CardContent>
        </Card>

        <UploadBox disabled={uploadMutation.isPending} onUpload={handleUpload} />

        {blockingError ? (
          <Card className="border-rose-200 bg-rose-50">
            <CardContent className="p-4 text-sm text-rose-700">{errorMessage(blockingError)}</CardContent>
          </Card>
        ) : null}

        {activeDocumentId ? (
          <>
            <ChatBox messages={messages} />
            <ChatInput disabled={chatMutation.isPending} onSubmit={handleAsk} />
          </>
        ) : (
          <Card>
            <CardContent className="p-4 text-sm text-slate-600">
              Select or upload a PDF to start chatting.
            </CardContent>
          </Card>
        )}
      </section>
    </main>
  );
};
