import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import App from "./App";
import store from "./redux/store";
import { Provider } from "react-redux";
import configureStore from "./src/store";

// const store = configureStore();

const reduxTutorial = () => (
  <Provider store={store}>
    <App />
  </Provider>
);

// As of React 18
const root = ReactDOM.createRoot(document.getElementById("root"));

root.render(<App />);
