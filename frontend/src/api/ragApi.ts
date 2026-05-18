import { apiClient } from "@/api/client";
import type { ChatRequest, ChatResponse, DocumentInfo, DocumentsResponse, UploadResponse } from "@/types/api";

export const uploadPdf = async (file: File): Promise<UploadResponse> => {
  const formData = new FormData();
  formData.append("file", file);
  const { data } = await apiClient.post<UploadResponse>("/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" }
  });
  return data;
};

export const fetchDocuments = async (): Promise<DocumentInfo[]> => {
  const { data } = await apiClient.get<DocumentsResponse>("/documents");
  return data.items;
};

export const deleteDocument = async (documentId: string): Promise<void> => {
  await apiClient.delete(`/documents/${documentId}`);
};

export const sendChat = async (payload: ChatRequest): Promise<ChatResponse> => {
  const { data } = await apiClient.post<ChatResponse>("/chat", payload);
  return data;
};
