import { configureStore, combineReducers } from "@reduxjs/toolkit";
import { persistReducer, persistStore } from "redux-persist";
import thunk from "redux-thunk";
import AsyncStorage from "@react-native-async-storage/async-storage";
import {
  reducer as network,
  createNetworkMiddleware,
} from "react-native-offline";
import reducer from "./reducers/index";

const persistConfig = {
  key: "root",
  storage: AsyncStorage,
};

const reducers = {
  reducer,
  network,
};
const allReducers = combineReducers(reducers);
const networkMiddleware = createNetworkMiddleware({
  regexActionType: /^OTHER/,
  actionTypes: ["", ""],
  queueReleaseThrottle: 1000,
});

const persistedReducer = persistReducer(persistConfig, allReducers);

export const store = configureStore({
  reducer: persistedReducer,
  middleware: [thunk, networkMiddleware],
});

export const persistor = persistStore(store);
