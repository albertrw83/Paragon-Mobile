import AsyncStorage from "@react-native-async-storage/async-storage";
import { storeData, getData } from "../utilities/StorageService";
import { getDataApi, postDataApi } from "./ApiService";
import { BASE_URL } from "./url";
import axios from "axios";

const config = {
  headers: {
    "Content-Type": "application/json",
  },
};

const defaultOptions = {
  baseURL: BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
};

// Create instance
let instance = axios.create(defaultOptions);
axios.defaults.baseURL = BASE_URL;
export const getAllJobs = () => {
  function thunk(dispatch) {
    fetch("http://127.0.0.1:8000/get_jobs_info")
      .then((response) => console.log(response, "cup"), response.json())
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
      .then((response) => console.log(response, "cup"), response.json())
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
    if (data.method === "PATCH") {
      response = await postDataApi(data);
    } else {
      response = await getDataApi(data);
    }
    console.log("responsehhhhh ", response.results);

    dispatch(data.actionType(response.results));
  } catch (error) {
    console.log("error in dispatcher ", error);
  }
};

export const updateJobName = async (payload) => {
  const { jobName, id } = payload;

  const body = jobName;

  const res = await instance.patch(`/get_jobs_info/${id}/`, body);
  console.log(res, "updateName");
  return res.data;
};
export const updateJob = async (payload) => {
  // const formData = new FormData();
  // formData.append("id", 1);
  // formData.append("job_name", jobName);
  // var requestOptions = {
  //   method: "POST",
  //   body: formData,
  //   redirect: "follow",
  // };
  // fetch(`${BASE_URL}/get_jobs_info/`, requestOptions)
  //   .then((response) => response)
  //   .then((result) => console.log(result))
  //   .catch((error) => console.log("error", error));
};
