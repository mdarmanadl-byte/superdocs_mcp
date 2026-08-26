import api from "./axios";

export const getRun = async (runId) => {
  const response = await api.get(`/piles/runs/${runId}`);
  return response.data;
};

export const getRunDetails = async (runId) => {
  const response = await api.get(
    `/piles/runs/${runId}/details`

  );

  return response.data;
};

export const reviewRun = async (runId, approved) => {
    console.log("REVIEW RUN CLICKED:", approved);
  const response = await api.post(
    `/piles/runs/${runId}/review`,

     null,
    {
      params: {
        approved,
      },
    }
  );

  return response.data;
};

export const getRunFindings = async (runId) => {
  const response = await api.get(
    `/piles/runs/${runId}/findings`
  );

  return response.data;
};

export const reviewFinding = async (
  runId,
  findingId,
  approved
) => {
  const response = await api.post(
    `/piles/runs/${runId}/findings/${findingId}/review`,
    {
      approved,
    }
  );

  return response.data;
};