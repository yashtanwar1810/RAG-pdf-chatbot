export interface UploadResponse {
  document_id: string;
  filename: string;
  chunks_created: number;
  status: string;
  message: string;
}

export interface DocumentInfo {
  document_id: string;
  filename: string;
  file_url: string;
  chunk_count: number;
}

export interface DocumentsResponse {
  items: DocumentInfo[];
}

export interface ChatRequest {
  document_id: string;
  question: string;
  top_k?: number;
}

export interface ChatSource {
  document_id: string;
  file_name: string;
  page: number;
  chunk_id: string;
  text: string;
  score: number;
}

export interface ChatResponse {
  answer: string;
  sources: ChatSource[];
}
