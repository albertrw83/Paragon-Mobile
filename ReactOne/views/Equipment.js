import React, { Component, useState, useEffect } from "react";
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
import { DataTable, Card, Title, Paragraph } from "react-native-paper";
import tableStyles from "../styles/tableStyles";
import { configureStore } from "@reduxjs/toolkit";
import { Provider } from "react-redux";
import store from "../redux/store";
import * as NetInfo from "@react-native-community/netinfo";
import AsyncStorage from "@react-native-async-storage/async-storage";
import axios from "axios";
// import * as Picker from "expo-document-picker";

const Equipment = () => {
  //set up variable states
  const [apiData, setApiData] = useState([]);

  //functions

  const _storeData = async () => {
    try {
      await AsyncStorage.setItem("@storage_key", JSON.stringify(apiData));
    } catch (error) {
      console.log(error);
      // Error saving data
    }
  };
  const _retrieveData = async () => {
    try {
      const value = await AsyncStorage.getItem("@storage_key");
      if (value !== null) {
        // We have data!!
        // console.log(value);
        return JSON.parse(value);
      }
    } catch (error) {
      // Error retrieving data
    }
  };
  const getApiData = () => {
    // _retrieveData();
    // setLoading(true);
    axios
      .get("http://localhost:19004/get_job_info/127")
      .then((response) => {
        // console.log(response.data);
        setApiData(response.data);
      })
      .catch((error) => console.log(error))
      .finally(() => console.log("setLoading(false)"));
    // console.log("asdfh");
  };
  const printOut = () => {
    // console.log(apiData);
  };
  // .then((response) => response.json())
  // .then((json) => setTestData(json))

  useEffect(() => {
    getApiData();
  }, []);
  let sampleElement = (
    <View>
      <Text>stuffsdaf</Text> <Text>stuffsdaf</Text>
    </View>
  );
  // need to loop through each equipment in the job and then display properties from those equipment in card format
  let eqsObject = {
    job_number: "abc123",
    job_names: [{ name1: "super job", name2: "superduper job" }],
  };
  let eqCompiler = (
    <Card>
      <Card.Title title="Card Title" subtitle="Card Subtitle" />
      <Card.Content>
        <Title>{apiData.job_name}</Title>
      </Card.Content>
      <Card.Cover source={{ uri: "https://picsum.photos/700" }} />
      <Card.Actions>
        <Button
          title="store locally"
          color="#841584"
          accessibilityLabel="testing button"
          onPress={console.log("button pressed")}
        />
      </Card.Actions>
    </Card>
  );
  // apiData.map((jobInfo) => (
  //   <View>
  //     {" "}
  //     <Text>{jobInfo.job_name}</Text>
  //   </View>
  // ));

  // () => {
  //   console.log(apiData.equipment.length);
  //   for (i = 0; i < apiData.equipment.length; i++) {
  //     console.log(apiData.equipment[0].site_id);
  //     // loopData += `<li>${data[i].name}</li>`
  //   }
  // };

  return (
    //Content
    <SafeAreaView>
      <Text></Text>
      <Text>{apiData.job_number}</Text>
      <View>
        <Button
          title="store locally"
          color="#841584"
          accessibilityLabel="testing button"
          onPress={_storeData}
        />
        <Button
          title="retrieve"
          color="#841584"
          accessibilityLabel="testing button"
          onPress={_retrieveData}
        />
        {eqCompiler}
      </View>
    </SafeAreaView>
  );
};

export default Equipment;
