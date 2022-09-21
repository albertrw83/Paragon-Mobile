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
