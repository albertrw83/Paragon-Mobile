import { axiosClient } from "./ApiConfig";
const jobId1 = 1;
export async function getJobInfoApi(jobId) {
  const { data } = await axiosClient.get(`get_job_info/${jobId}`);
  return data;
}
export function getEqInfoApi(eqId) {
  return axiosClient.get(`get_eq_info/2`, JSON.stringify(payload));
}
