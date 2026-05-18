import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";

interface UploadBoxProps {
  disabled?: boolean;
  onUpload: (file: File) => void;
}

export const UploadBox = ({ disabled, onUpload }: UploadBoxProps) => {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Upload PDF</CardTitle>
        <CardDescription>Select one PDF file to index and chat.</CardDescription>
      </CardHeader>
      <CardContent>
        <Input
          accept="application/pdf"
          disabled={disabled}
          type="file"
          onChange={(event) => {
            const file = event.target.files?.[0];
            if (!file) return;
            onUpload(file);
            event.currentTarget.value = "";
          }}
        />
      </CardContent>
    </Card>
  );
};
