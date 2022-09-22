import { configureStore, combineReducers } from "@reduxjs/toolkit";
import { persistReducer, persistStore } from "redux-persist";
import thunk from "redux-thunk";
import AsyncStorage from "@react-native-async-storage/async-storage";
import {
  reducer as network,
  createNetworkMiddleware,
} from "react-native-offline";
import homeReducer from "./reducers/index";

const persistConfig = {
  key: "root",
  storage: AsyncStorage,
};

const reducers = {
  homeReducer,
  network,
};
const allReducers = combineReducers(reducers);
const networkMiddleware = createNetworkMiddleware({
  queueReleaseThrottle: 200,
});

const persistedReducer = persistReducer(persistConfig, allReducers);

export const store = configureStore({
  reducer: persistedReducer,
  middleware: [networkMiddleware, thunk],
});

export const persistor = persistStore(store);
