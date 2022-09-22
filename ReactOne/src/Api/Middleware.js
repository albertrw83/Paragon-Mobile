import AsyncStorage from "@react-native-async-storage/async-storage";
import { storeData, getData } from "../utilities/StorageService";
import { getDataApi, postDataApi } from "./ApiService";

export const getAllJobs = () => {
  function thunk(dispatch) {
    fetch("https://073c-119-152-135-145.ngrok.io/get_jobs_info")
      .then((response) => response.json())
      .then((responseJson) => {
        dispatch({
          type: "SET_JOB_INFO_DATA",
          payload: responseJson,
          meta: {
            retry: true,
          },
        });
      })
      .catch((error) => {
        console.error(error);
      });
  }

  thunk.interceptInOffline = true; // This is the important part
  return thunk; // Return it afterwards
};

export const fetchData = (data) => {
  function thunk(dispatch) {
    fetch(data.url)
      .then((response) => response.json())
      .then((responseJson) => {
        dispatch({
          type: "SET_JOB_INFO_DATA",
          payload: responseJson,
          meta: {
            retry: true,
          },
        });
      })
      .catch((error) => {
        console.error(error);
      });
  }

  thunk.interceptInOffline = true; // This is the important part
  return thunk; // Return it afterwards
};

export const dispatcher = (data) => async (dispatch) => {
  try {
    let response;
    if (!data.network) {
      const offlineList = await getData("offlineList");
      offlineList.push(data);
      storeData("offlineList", offlineList);
      return;
    }
    if (data.method === "POST") {
      response = await postDataApi(data);
    } else {
      response = await getDataApi(data);
    }
    console.log("response ", response);

    dispatch(data.actionType(response));
  } catch (error) {
    console.log("error in dispatcher ", error);
  }
};
