import { axiosClient } from "./ApiConfig";
export async function getDataApi(payload) {
  const { data } = await axiosClient.get(
    payload.url,
    JSON.stringify(payload.payload)
  );
  console.log(data, "coffee");
  return data;
}
export async function postDataApi(payload) {
  const { data } = await axiosClient.patch(
    payload.url,
    JSON.stringify(payload.payload)
  );
  return data;
}
