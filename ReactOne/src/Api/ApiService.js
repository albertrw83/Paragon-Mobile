import { axiosClient } from "./ApiConfig";
export async function getDataApi(payload) {
  const { data } = await axiosClient.get(
    payload.url,
    JSON.stringify(payload.payload)
  );
  return data;
}
export async function postDataApi(payload) {
  const { data } = await axiosClient.post(
    payload.url,
    JSON.stringify(payload.payload)
  );
  return data;
}
