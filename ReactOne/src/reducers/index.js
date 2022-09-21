const initialState = {
  jobInfoData: [],
};

export default appReducer = (state = initialState, action) => {
  switch (action.type) {
    case "SET_JOB_INFO_DATA":
      return { ...state, jobInfoData: action.payload };
    default:
      return state;
  }
};
