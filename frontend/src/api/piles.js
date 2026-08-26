import api from "./axios";

export const createPile = async () => {
  const response = await api.post("/piles" ,{
    name,
  });
  return response.data;
};

export const uploadDocuments = async (pileId, files) => {
  const formData = new FormData();

  files.forEach((file) => {
    formData.append("files", file);
  });

  const response = await api.post(
    `/piles/${pileId}/documents`,
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    }
  );

  return response.data;
};

export const searchDocuments = async (pileId, query) => {
  const response = await api.get(
    `/piles/${pileId}/search`,
    {
      params: { query },
    }
  );

  return response.data;
};

export const askDocuments = async (pileId, query) => {
  const response = await api.get(
    `/piles/${pileId}/ask`,
    {
      params: { query },
    }
  );

  return response.data;
};