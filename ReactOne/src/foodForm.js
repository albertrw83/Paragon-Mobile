import React, { Component, useState } from "react";
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  TextInput,
  Button,
  Switch,
  SafeAreaView,
  ActivityIndicator,
  StatusBar,
} from "react-native";
import { connect } from "react-redux";
import { NavigationContainer } from "@react-navigation/native";
import Tabs from "../navigation/tabs";
import JobView from "../navigation/jobView";
import { SET_SERIAL, DELETE_FOOD } from "./actions/types";

const mapStateToProps = (state) => ({ serialn: state.serialn });
const mapDispatchToProps = () => ({
  editSerial: (serialNumber) =>
    dispatchEvent({
      type: ActionTypes.SET_SERIAL,
      payload: {
        serialNumber,
      },
    }),
});

// const connectComponent = connectreac(mapStateToProps, mapDispatchToProps);
const FoodList = () => {
  return (
    <NavigationContainer>
      <JobView />
    </NavigationContainer>
  );
};

export default FoodList;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
  },
  input: {
    height: 80,
    margin: 12,
    borderWidth: 1,
    padding: 10,
  },
  enabled: {
    color: "green",
  },
  disabled: {
    color: "red",
  },
});
