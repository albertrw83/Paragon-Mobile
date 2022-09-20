import { SET_SERIAL, DELETE_FOOD } from "./types";

export const addFood = (newSerial) => ({
  type: SET_SERIAL,
  data: newSerial,
});
export const deleteFood = (key) => ({
  type: DELETE_FOOD,
  key: key,
});
