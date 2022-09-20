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
// import * as Picker from "expo-document-picker";

const pool = {
  siteid: "someid",
};
const General = () => {
  // const pool = {
  //   siteid: "someid",
  //   classfication: "someclass",
  // };

  const [isEnabled, setIsEnabled] = useState(false);
  const [hidden, setHidden] = useState(false);
  const [hiddenEqLocation, sethiddenEqLocation] = useState(false);
  const [hiddenEqLocationText, sethiddenEqLocationText] = useState(true);
  const [text, setText] = useState("This is the homescreen");
  const [textInput, setTextInput] = useState("");
  const [numberOne, setnumberOne] = useState(6);
  const [numberTwo, setnumberTwo] = useState(8);
  const [equipmentLocation, setEquipmentLocation] = useState("Undefined");
  const [jobSite, setJobSite] = useState("Undefined");
  const [editJobSite, enableEditJobSite] = useState(false);

  // const onLongPress = () => {
  //   setCount(count + 1);
  // };
  const toggleSwitch = () => {
    setIsEnabled((previousState) => !previousState);
    if (isEnabled) {
      setText(textInput);
      setHidden(true);
    } else {
      setText("not enabled");
      setHidden(false);
    }
  };
  const changeEqLocation = () => {
    sethiddenEqLocation(true);
    sethiddenEqLocationText(false);
  };
  const editValue = () => {
    sethiddenEqLocation(true);
    sethiddenEqLocationText(false);
  };
  const doEditJobSite = () => {
    console.log("clicked");
    enableEditJobSite(true);
  };
  const onChangeNumber = () => {
    setHidden(true);
  };

  return (
    <SafeAreaView>
      <Text style={tableStyles.textcheck}>This is green text</Text>
      <TextInput value={jobSite} onChangeText={setJobSite} />
      <Pressable onLongPress={() => enableEditJobSite(true)}>
        <View pointerEvents="none">
          <Button
            style={styles.button}
            title="Add Sub Equipment"
            color="#841584"
            accessibilityLabel="Add Sub Equipment"
            onPress={doEditJobSite}
          />
        </View>
      </Pressable>
      {HidableText()}
      <DataTable>
        <DataTable.Row>
          <DataTable.Cell>Site Identification</DataTable.Cell>
          <DataTable.Cell>{pool.siteid}</DataTable.Cell>
        </DataTable.Row>
        <DataTable.Row>
          <DataTable.Cell>Classification</DataTable.Cell>
          <DataTable.Cell>
            <Text>{pool.classification}</Text>
          </DataTable.Cell>
        </DataTable.Row>
        <DataTable.Row>
          <DataTable.Cell>Serial Number</DataTable.Cell>
          <DataTable.Cell>
            <Text>23049SDLKFJ</Text>
          </DataTable.Cell>
        </DataTable.Row>
        <DataTable.Row>
          <DataTable.Cell>Equipment Location</DataTable.Cell>
          <DataTable.Cell>
            {hiddenEqLocationText ? (
              <Text onLongPress={changeEqLocation}>{equipmentLocation}</Text>
            ) : null}
            {hiddenEqLocation ? (
              <TextInput
                value={equipmentLocation}
                placeholder="useless placeholder"
                keyboardType="numeric"
                onChangeText={setEquipmentLocation}
              />
            ) : null}
          </DataTable.Cell>
        </DataTable.Row>
        <DataTable.Row>
          <DataTable.Cell>Job Site</DataTable.Cell>
          <DataTable.Cell>
            <Text>Valero Anadarko</Text>
          </DataTable.Cell>
        </DataTable.Row>
        <DataTable.Row>
          <DataTable.Cell>Manufacturer Nameplate Photo</DataTable.Cell>
          <DataTable.Cell>
            <Text>Photo Input</Text>
          </DataTable.Cell>
        </DataTable.Row>
        <DataTable.Row>
          <DataTable.Cell>Scope Specifications</DataTable.Cell>
          <DataTable.Cell>
            <Text> Refer to Job Scope (Default)</Text>
          </DataTable.Cell>
        </DataTable.Row>
        <DataTable.Row>
          <DataTable.Cell>Scope Specifications</DataTable.Cell>
          <DataTable.Cell>
            <Text> Refer to Job Scope (Default)</Text>
          </DataTable.Cell>
        </DataTable.Row>
        <DataTable.Row>
          <DataTable.Cell>Scope Specifications</DataTable.Cell>
          <DataTable.Cell>
            <Text style={tableStyles.textcheck}>
              {" "}
              Refer to Job Scope (Default)
            </Text>
          </DataTable.Cell>
        </DataTable.Row>
        <DataTable.Row>
          <DataTable.Cell>Scope Specifications</DataTable.Cell>
          <DataTable.Cell>
            <Text> Refer to Job Scope (Default)</Text>
          </DataTable.Cell>
        </DataTable.Row>
        <DataTable.Row>
          <DataTable.Cell>Required Test Sets</DataTable.Cell>
          <DataTable.Cell>
            <Text>Relay Test Set Fluke 87 Multimeter</Text>
          </DataTable.Cell>
        </DataTable.Row>
        <DataTable.Row>
          <DataTable.Cell>Status</DataTable.Cell>
          <DataTable.Cell>
            <Text> Refer to Job Scope (Default)</Text>
          </DataTable.Cell>
        </DataTable.Row>
        <DataTable.Row>
          <DataTable.Cell>Scope Specifications</DataTable.Cell>
          <DataTable.Cell>
            <Text> Refer to Job Scope (Default)</Text>
          </DataTable.Cell>
        </DataTable.Row>
        <DataTable.Row>
          <DataTable.Cell>Scope Specifications</DataTable.Cell>
          <DataTable.Cell>
            <Text> Refer to Job Scope (Default)</Text>
          </DataTable.Cell>
        </DataTable.Row>
      </DataTable>
      <Text style={numberOne > numberTwo ? styles.enabled : styles.disabled}>
        {text}
      </Text>
      {isEnabled ? <Text>{pool.siteid}</Text> : null}
      <TextInput
        value={textInput}
        placeholder="sample"
        onChangeText={setTextInput}
      />

      <TextInput
        value={"7"}
        placeholder="useless placeholder"
        keyboardType="numeric"
      />
      <StatusBar backgroundColor="green" />
      {isEnabled ? <StatusBar backgroundColor="green" /> : null}
    </SafeAreaView>
  );
};

const HidableText = () => {
  return <Text>This is the homescreenponent</Text>;
};

export default General;

// function mapStateToPropers(state)

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
  separator: {
    marginVertical: 8,
    borderBottomColor: "#737373",
    borderBottomWidth: StyleSheet.hairlineWidth,
  },
  head: { height: 40, backgroundColor: "#808B97" },
  text: { margin: 6 },
  row: { flexDirection: "row", backgroundColor: "#FFF1C1" },
  btn: { width: 58, height: 18, backgroundColor: "#78B7BB", borderRadius: 2 },
  btnText: { textAlign: "center", color: "#fff" },
});
