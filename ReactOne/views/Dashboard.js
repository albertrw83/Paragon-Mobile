import React, { Component, useState } from "react";
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Button,
  Switch,
  SafeAreaView,
  ActivityIndicator,
  StatusBar,
  TextInput,
  Pressable,
} from "react-native";
import { DataTable } from "react-native-paper";
import tableStyles from "../styles/tableStyles";
import { configureStore } from "@reduxjs/toolkit";
import { Provider } from "react-redux";
import store from "../redux/store";
import { useDispatch, useSelector } from "react-redux";

// import * as Picker from "expo-document-picker";

const Dashboard = () => {
  //functions
  return (
    //Content
    <SafeAreaView>
      <Text></Text>
    </SafeAreaView>
  );
};

export default Dashboard;
