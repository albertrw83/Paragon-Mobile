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
  FlatList,
  Image,
  Alert,
} from "react-native";
import { DataTable, Card, Title, Paragraph } from "react-native-paper";
import * as ImagePicker from "expo-image-picker";

import AsyncStorage from "@react-native-async-storage/async-storage";
import { useDispatch, useSelector } from "react-redux";
import JobsList from "../src/components/JobsList";
import JobModal from "../src/components/JobModal";
import { dispatcher, getAllJobs } from "../src/Api/Middleware";
import { setAllJobs } from "../src/reducers";

const Equipment = () => {
  const RefreshInterval = 60000;

  const isNetworkAvailble = useSelector(
    (state) => state.homeReducer.isNetworkAvailble
  );
  const allJobs = useSelector((state) => state.homeReducer.allJobs);
  console.log(allJobs, "lo");
  const [pickedImagePath, setPickedImagePath] = useState("");
  const [isModalVisible, setModalVisible] = useState(false);
  const [selectedJob, setSelectedJob] = useState({});
  const [picture, setPicture] = useState();
  const dispatch = useDispatch();

  //functions

  const _storeData = async () => {
    try {
      await AsyncStorage.setItem("@storage_key", JSON.stringify(apiData));
    } catch (error) {
      console.log(error);
    }
  };
  const _retrieveData = async () => {
    try {
      const value = await AsyncStorage.getItem("@storage_key");
      if (value !== null) {
        return JSON.parse(value);
      }
    } catch (error) {}
  };

  const selectionBtn = () => {
    Alert.alert("Picture upload Selection", "", [
      {
        text: "Camera",
        onPress: () => openCamera(),
        style: "cancel",
      },
      { text: "Gallery", onPress: () => showImagePicker() },
      { text: "Exit", onPress: () => console.log() },
    ]);
  };
  useEffect(() => {
    getJobs(); // this function is fetching all the jobs data
  }, []);

  useEffect(() => {
    const interval = setInterval(() => {
      getJobs();
    }, RefreshInterval);

    return () => clearInterval(interval);
  }, []);

  // This function is triggered when the "Select an image" button pressed
  const showImagePicker = async () => {
    // Ask the user for the permission to access the media library
    const permissionResult =
      await ImagePicker.requestMediaLibraryPermissionsAsync();

    if (permissionResult.granted === false) {
      alert("You've refused to allow this appp to access your photos!");
      return;
    }

    const result = await ImagePicker.launchImageLibraryAsync();

    // Explore the result
    console.log(result);

    if (!result.cancelled) {
      setPickedImagePath(result.uri);
      console.log(result.uri);
    }
  };

  // This function is triggered when the "Open camera" button pressed
  const openCamera = async () => {
    // Ask the user for the permission to access the camera
    const permissionResult = await ImagePicker.requestCameraPermissionsAsync();

    if (permissionResult.granted === false) {
      alert("You've refused to allow this appp to access your camera!");
      return;
    }

    const result = await ImagePicker.launchCameraAsync();

    // Explore the result
    console.log(result);
    setPicture(result.uri);
    if (!result.cancelled) {
      setPickedImagePath(result.uri);
      console.log(result.uri);
    }
  };
  const getJobs = () => {
    dispatch(
      dispatcher({
        payload: "",
        method: "GET",
        url: "get_jobs_info",
        network: isNetworkAvailble,
        actionType: setAllJobs,
      })
    );
  };
  let sampleElement = (
    <View>
      <Text>stuffsdaf</Text> <Text>stuffsdaf</Text>
    </View>
  );
  let eqsObject = {
    job_number: "abc123",
    job_names: [{ name1: "super job", name2: "superduper job" }],
  };
  let eqCompiler = (
    <Card>
      <Card.Title title="All Jobs" subtitle="" />
      <Card.Content>
        <JobsList
          showJobDetail={setModalVisible}
          setSelectedJob={setSelectedJob}
          allJobs={allJobs}
          onPress={selectionBtn}
        />
      </Card.Content>
    </Card>
  );

  return (
    //Content
    <SafeAreaView>
      <Image source={{ uri: picture }} style={{ height: 50, width: 50 }} />
      <JobModal
        job={selectedJob}
        showModal={isModalVisible}
        setShowModal={setModalVisible}
      />
      <Text></Text>
      <Text>{allJobs?.job_number}</Text>
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
      </View>
      {eqCompiler}
    </SafeAreaView>
  );
};

export default Equipment;
