import api from "./axios";

export const askDocuments = async (pileId, query) => {
  const { data } = await api.get(`/piles/${pileId}/ask`, {
    params: {
      query,
    },
  });

  return data;
};