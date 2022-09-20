import React, { Component, useEffect, useState } from "react";
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
import AsyncStorage from "@react-native-async-storage/async-storage";
import axios from "axios";
import { DataTable } from "react-native-paper";
import tableStyles from "../styles/tableStyles";
import * as ImagePicker from "expo-image-picker";
import * as DocumentPicker from "expo-document-picker";
import { NetInfoStateType, useNetInfo } from "@react-native-community/netinfo";
import Spinner from "react-native-loading-spinner-overlay";

let sampleJson = require("../sample_files/sample-file.json");

const SpecialistSupport = () => {
  const [status, setStatus] = useState();
  const [storedData, setStoredData] = useState("");
  const netInfo = useNetInfo();

  const storeLocally = async () => {
    try {
      await AsyncStorage.setItem("statusValue", status);
    } catch (error) {
      console.log("error-async-storage", error);
    }
  };

  const getLocal = async () => {
    console.log("getlocal");
    try {
      const data = await AsyncStorage.getItem("statusValue");
      console.log({ data });
      setStoredData(data);
      setStatus(data);
    } catch (error) {
      console.log("error-async-storage", error);
    }
  };
  // lastChjange = "01-05-2022-41503945"
  useEffect(() => {
    if (status !== undefined) {
      console.log({ status });
      storeLocally();
    }
  }, [status]);
  useEffect(() => {
    if (netInfo.isConnected && netInfo.type == NetInfoStateType.wifi) {
      console.log("Get DATA from API");
      // get data from API
    } else {
      getLocal();
    }
  }, [netInfo]);
  return (
    <SafeAreaView style={styles.container}>
      <TextInput
        style={{ backgroundColor: "lightgray" }}
        onChangeText={setStatus}
        value={status}
      />
      <Button
        title="Store in Local"
        color="#841584"
        accessibilityLabel="testing button"
        onPress={storeLocally}
      />
      <Button
        title="Retreive from Local"
        color="#841584"
        accessibilityLabel="testing button"
        onPress={getLocal}
      />
      {/*<Button
        title="print local"
        color="#841584"
        accessibilityLabel="testing button"
        onPress={printLocal}
  />*/}
      <Text>{storedData}</Text>
    </SafeAreaView>
  );
};

export default SpecialistSupport;

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
