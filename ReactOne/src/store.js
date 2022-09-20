import { configureStore, combineReducers } from "@reduxjs/toolkit";
import foodReducer from "./reducers/foodReducer";

const rootReducer = combineReducers({
  foods: foodReducer,
});

export default configureStore({
  reducer: {
    foods: foodReducer,
  },
});
