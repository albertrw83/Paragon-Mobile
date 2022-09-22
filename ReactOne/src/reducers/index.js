// const initialState = {
//   jobInfoData: [],
// };

// export default appReducer = (state = initialState, action) => {
//   switch (action.type) {
//     case "SET_JOB_INFO_DATA":
//       return { ...state, jobInfoData: action.payload };
//     default:
//       return state;
//   }
// };

import { createSlice } from "@reduxjs/toolkit";
const initialState = {
  isLoading: false,
  allJobs: [],
  isNetworkAvailble: false,
};

export const homeReducer = createSlice({
  name: "home",
  initialState,
  reducers: {
    setLoading: (state, { payload }) => {
      state.isLoading = payload;
    },
    setAllJobs: (state, { payload }) => {
      state.allJobs = payload;
    },
    setNetworkAvailble: (state, { payload }) => {
      state.isNetworkAvailble = payload;
    },
  },
});
// Action creators are generated for each case reducer function
export const { setLoading, setNetworkAvailble, setAllJobs } =
  homeReducer.actions;
export default homeReducer.reducer;
