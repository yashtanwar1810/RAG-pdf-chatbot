import type { DocumentInfo } from "@/types/api";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { cn } from "@/lib/utils";

interface DocumentListProps {
  activeDocumentId: string | null;
  documents: DocumentInfo[];
  loading?: boolean;
  onDelete: (documentId: string) => void;
  onSelect: (documentId: string) => void;
}

export const DocumentList = ({
  activeDocumentId,
  documents,
  loading,
  onDelete,
  onSelect
}: DocumentListProps) => {
  return (
    <Card className="h-full rounded-none border-x-0 border-y-0 lg:rounded-none lg:border-r lg:border-l-0 lg:border-y-0">
      <CardHeader>
        <CardTitle>Documents</CardTitle>
        <CardDescription>Choose a file to chat with.</CardDescription>
      </CardHeader>
      <CardContent className="space-y-3">
        {loading ? <p className="text-sm text-slate-500">Loading...</p> : null}
        {documents.length === 0 ? <p className="text-sm text-slate-500">No documents uploaded yet.</p> : null}
        <ul className="space-y-2">
          {documents.map((doc) => (
            <li key={doc.document_id} className="rounded-lg border border-slate-200 p-2">
              <div className="mb-2 flex items-center justify-between gap-2">
                <button
                  className={cn(
                    "truncate text-left text-sm font-medium",
                    activeDocumentId === doc.document_id ? "text-sky-700" : "text-slate-700"
                  )}
                  onClick={() => onSelect(doc.document_id)}
                  type="button"
                >
                  {doc.filename}
                </button>
                <Badge>{doc.chunk_count} chunks</Badge>
              </div>
              <div className="flex gap-2">
                <Button className="flex-1" size="sm" variant="outline" onClick={() => onSelect(doc.document_id)}>
                  Open
                </Button>
                <Button size="sm" variant="destructive" onClick={() => onDelete(doc.document_id)}>
                  Delete
                </Button>
              </div>
            </li>
          ))}
        </ul>
      </CardContent>
    </Card>
  );
};
