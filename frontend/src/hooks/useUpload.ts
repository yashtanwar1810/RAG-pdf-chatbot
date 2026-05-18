import { useMutation, useQueryClient } from "@tanstack/react-query";

import { uploadPdf } from "@/api/ragApi";

export const useUpload = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: uploadPdf,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["documents"] });
    }
  });
};
