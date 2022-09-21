import React, { Component } from "react";
import { View, Text, StyleSheet, TouchableOpacity } from "react-native";
import { createStore } from "redux";
import CounterApp from "./src/CounterApp";
import foodForm from "./src/foodForm";
import { Provider } from "react-redux";
import FoodForm from "./src/foodForm";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import { store, persistor } from "./src/store";
import { PersistGate } from "redux-persist/integration/react";
import { ReduxNetworkProvider } from "react-native-offline";

/**
 * Store - holds our state - THERE IS ONLY ONE STATE
 * Action - State can be modified using actions - SIMPLE OBJECTS
 * Dispatcher - Action needs to be sent by someone - known as dispatching an action
 * Reducer - receives the action and modifies the state to give us a new state
 *  - pure functions
 *  - only mandatory argument is the 'type'
 * Subscriber - listens for state change to update the ui
 */
// const initialState = {
//   counter: 0,
// };
// const reducer = (state = initialState, action) => {
//   switch (action.type) {
//     case "INCREASE_COUNTER":
//       return { counter: state.counter + 1 };
//     case "DECREASE_COUNTER":
//       return { counter: state.counter - 1 };
//   }
//   return state;
// };

class App extends Component {
  render() {
    return (
      <Provider store={store}>
        <PersistGate loading={null} persistor={persistor}>
          {/* <ReduxNetworkProvider> */}
          <FoodForm />
          {/* </ReduxNetworkProvider> */}
        </PersistGate>
      </Provider>
    );
  }
}

export default App;

// export default App;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
  },
});
