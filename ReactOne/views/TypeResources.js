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

const TypeResources = () => {
  return (
    <SafeAreaView style={styles.container}>
      <Text>toggle switch</Text>
    </SafeAreaView>
  );
};

export default TypeResources;

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
