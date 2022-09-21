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
} from "react-native";
import { DataTable, Card, Title, Paragraph } from "react-native-paper";

import AsyncStorage from "@react-native-async-storage/async-storage";
import { useDispatch, useSelector } from "react-redux";
import JobsList from "../src/components/JobsList";
import JobModal from "../src/components/JobModal";
import { getAllJobs } from "../src/Api/Middleware";

const Equipment = () => {
  const jobInfoData = useSelector((state) => state.reducer.jobInfoData);
  const [isModalVisible, setModalVisible] = useState(false);
  const [selectedJob, setSelectedJob] = useState({});

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

  useEffect(() => {
    getJobs();
  }, []);

  const getJobs = () => {
    dispatch(getAllJobs());
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
          allJobs={jobInfoData}
        />
      </Card.Content>
    </Card>
  );

  return (
    //Content
    <SafeAreaView>
      <JobModal
        job={selectedJob}
        showModal={isModalVisible}
        setShowModal={setModalVisible}
      />
      <Text></Text>
      <Text>{jobInfoData?.job_number}</Text>
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
