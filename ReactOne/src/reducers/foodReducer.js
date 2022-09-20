import { ActionSheetIOS } from "react-native";

const SET_SERIAL = "SET_SERIAL";
const DELETE_FOOD = "DELETE_FOOD";
// const initialState = {
//   serialNumber: { svalue: "empty" },
// };
export const setSerial = (newSerial) => ({
  type: SET_SERIAL,
  newSerial,
});

const foodReducer = (state = { newSerial: "empty" }, action) => {
  switch (action.type) {
    case SET_SERIAL:
      return {
        ...state,
        newSerial: action.newSerial,
      };
    default:
      return state;
  }
};

export default foodReducer;
