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
  FlatList,
  ScrollView,
} from "react-native";
import axios from "axios";
import { DataTable } from "react-native-paper";
import tableStyles from "../styles/tableStyles";
import * as ImagePicker from "expo-image-picker";
import * as DocumentPicker from "expo-document-picker";
import * as NetInfo from "@react-native-community/netinfo";
import Spinner from "react-native-loading-spinner-overlay";
import AsyncStorage from "@react-native-async-storage/async-storage";
// import { getEqInfoData } from "../src/Api/Middleware";
import { useDispatch } from "react-redux";

const DATA = [
  {
    id: "bd7acbea-c1b1-46c2-aed5-3ad53abb28ba",
    title: "First Item",
  },
  {
    id: "3ac68afc-c605-48d3-a4f8-fbd91aa97f63",
    title: "number2",
  },
  {
    id: "58694a0f-3da1-471f-bd96-145571e29d72",
    title: "Third Item",
  },
];

const Item = ({ title }) => (
  <View>
    <Text>{title}</Text>
  </View>
);
const TestItem = ({ eq }) => (
  <View>
    <Text>{eq}</Text>
  </View>
);
const EqItem = ({ eq }) => (
  <View>
    <Text>{eq}</Text>
  </View>
);
const Resources = () => {
  const dispatch = useDispatch();

  // const netInfo = NetInfo();
  const [image, setImage] = useState(null);
  const [isLoading, setLoading] = useState(false);
  const [testData, setTestData] = useState([]);
  const [eqData, setEqData] = useState([]);
  const [eqDataOffline, setEqDataOffline] = useState("empty4");
  const [sampleTestData, setsampleTestData] = useState("empty");
  const [retreivedData, setretreivedData] = useState("empty3");

  // // Subscribe
  // const unsubscribe = NetInfo.addEventListener((state) => {
  //   console.log("Connection type", state.type);
  //   console.log("Is connected?", state.isConnected);
  // });

  // useEffect(() => {
  //   getEQ();
  // }, []);

  // const getEQ = () => {
  //   dispatch(getEqInfoData(12));
  // };
  const _storeData = async () => {
    try {
      await AsyncStorage.setItem("@storage_key", "eqDataOffline");
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
        console.log("we have value");
        return value;
      }
    } catch (error) {
      // Error retrieving data
    }
  };
  const storeLocally = async () => {
    try {
      console.log(eqData);
      let jsonValue = JSON.stringify(eqData);
      await AsyncStorage.setItem("offlineValue", jsonValue);
    } catch (error) {
      console.log("error-async-storage", error);
    }
  };
  const eqPropertySet = async () => {
    let objectVal = await getfromlocal();
    setEqData(objectVal);
  };
  const getfromlocal = async () => {
    console.log("quickprint");
    console.log("catch22");
    try {
      let jsonValue = await AsyncStorage.getItem("offlineValue");
      console.log(jsonValue);

      return jsonValue != null ? JSON.parse(jsonValue) : null;
      // console.log({ jsonValue });
      // setStoredData(data);
      // setStatus(data);
    } catch (error) {
      console.log("error-async-storage", error);
    }
  };

  const getLocal = async () => {
    return;
    console.log("getlocal");
    try {
      axios
        .get("http://localhost:19004/get_eq_info/2171")
        .then((response) => {
          console.log("settingeqdata");
          setEqData(response.data);
        })
        .catch(() => {
          //failed to use API. Get from local storage
          eqPropertySet();
        })
        .finally(() => setLoading(false));
    } catch {
      console.log("catch22");
      try {
        let jsonValue = await AsyncStorage.getItem("offlineValue");
        // console.log(jsonValue);

        return jsonValue != null ? JSON.parse(jsonValue) : null;
        // console.log({ jsonValue });
        // setStoredData(data);
        // setStatus(data);
      } catch (error) {
        console.log("error-async-storage", error);
      }
    }
  };
  // const storeData = async (data) => {
  //   try {
  //     await AsyncStorage.setItem("someData", JSON.stringify(data));
  //   } catch (error) {
  //     console.log("error-async-storage", error);
  //   }
  // };

  // const getData = async () => {
  //   try {
  //     const data = await AsyncStorage.getItem("someData");
  //     setEqDataOffline(JSON.parse(data));
  //   } catch (error) {
  //     console.log("error-async-storage", error);
  //   }
  // };
  //   const changeProperty = (propert) => {

  //     NetInfo.fetch().then((state) => {
  //       console.log("Connection type", state.type);
  //       console.log("Is connected?", state.isConnected);
  //       if (state.isConnected) {
  //         console.log('connected. send to server and update databse')
  // getData()

  // eqDataOffline.propert
  //       } else {
  //       }
  //     });
  //   };
  // Unsubscribe
  // unsubscribe();
  const _pickDocument = async () => {
    let result = await DocumentPicker.getDocumentAsync({});
    alert(result.uri);
    console.log(result);
  };
  const getTestData = () => {
    fetch("http://localhost:19004/get_test_info/")
      .then((response) => response.json())
      .then((json) => setTestData(json))
      .catch((error) => console.log(error))
      .finally(() => setLoading(false));
  };

  const buttonPreessed = () => {
    // let x = _retrieveData();
    // setEqDataOffline(eqDataOffline);
    _storeData();
    // console.log(x);
  };
  const buttonPreessed2 = () => {
    console.log(_retrieveData());
    let x = _retrieveData();
    setEqDataOffline(x);
    console.log("x");
    console.log(x);
    console.log("x");
    // _storeData();
    // console.log(x);
  };
  const buttonPreessed3 = async () => {
    let localstuff = await getLocal();
    console.log(localstuff);
    // let x = _retrieveData();
    // console.log("pressed");
    // console.log(eqDataOffline);
    // console.log("pressed");
    // _storeData();
    // console.log(x);
  };
  const pickImage = async () => {
    // No permissions request is necessary for launching the image library
    let result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.All,
      allowsEditing: true,
      aspect: [4, 3],
      quality: 1,
    });

    if (!result.cancelled) {
      uploadImage(result);
    }
  };
  const uploadImage = (result) => {
    // ImagePicker saves the taken photo to disk and returns a local URI to it
    let localUri = result.uri;
    let filename = localUri.split("/").pop();

    // Infer the type of the image
    let match = /\.(\w+)$/.exec(filename);
    let type = match ? `image/${match[1]}` : `image`;

    let formData = new FormData();
    // Assume "photo" is the name of the form field the server expects
    formData.append("nameplateImage", { uri: localUri, name: filename, type });
    axios
      .post("myurl", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      })
      .then((response) => {
        // Set Image Url getting from Response
        console.log("data", response.data);
      })
      .catch((error) => console.log(error))
      .finally(() => setLoading(false));
  };
  const getEqData = () => {
    _retrieveData();
    setLoading(true);
    axios
      .get("http://localhost:19004/get_eq_info/2171")
      .then((response) => {
        setEqData(response.data);
      })
      .catch((error) => console.log(error))
      .finally(() => setLoading(false));
  };
  useEffect(() => {
    setLoading(true);
    getTestData();
  }, []);
  useEffect(() => {
    getEqData();
  }, []);
  useEffect(() => {
    // write your code here, it's like componentWillMount

    let storedData = _retrieveData();
    console.log("555");
    console.log(storedData);
    console.log("555");
  }, []);
  useEffect(() => {
    console.log(sampleTestData);
    console.log("data changed");
  }, [sampleTestData]);

  const renderItem = ({ item }) => <Item title={item.title} />;
  const renderTestItem = ({ item }) => <TestItem title={item.eq} />;
  const renderEqItem = ({ item }) => <TestItem title={item.eq} />;
  const editEqData = (text) => {
    console.log(eqData.site_id);
    console.log(eqData);
    // console.log(text);
    eqData.site_id = text;
  };
  useEffect(() => {
    console.log("eqdata", eqData);
  }, [eqData]);
  // NetInfo.fetch().then((state) => {
  //   console.log("Connection type", state.type);
  //   console.log("Is connected?", state.isConnected);
  // });
  return (
    <SafeAreaView style={styles.container}>
      <Spinner
        visible={isLoading}
        textContent={"Loading..."}
        textStyle={styles.spinnerTextStyle}
      />
      <ScrollView>
        <View style={{ padding: 20 }}>
          {isLoading ? (
            <Text>Loading...</Text>
          ) : (
            <FlatList
              data={DATA}
              renderItem={renderItem}
              keyExtractor={(item) => item.id}
            />
          )}
        </View>
        <View style={{ padding: 20 }}>
          {isLoading ? (
            <Text>Loading...</Text>
          ) : (
            <FlatList
              data={testData}
              renderTestItem={renderItem}
              keyExtractor={(item) => item.eq}
            />
          )}
        </View>
        <View>
          <TextInput onChangeText={setsampleTestData} value={sampleTestData} />
          <Button
            style={styles.button}
            title="store to local"
            color="#841584"
            accessibilityLabel="testing button"
            onPress={storeLocally}
          />
          <Button
            style={styles.button}
            title="get from local"
            color="#841584"
            accessibilityLabel="testing button2"
            onPress={getLocal}
          />
          <Button
            style={styles.button}
            title="current"
            color="#841584"
            accessibilityLabel="testing button3"
            onPress={buttonPreessed3}
          />
        </View>
        <DataTable>
          <DataTable.Row>
            <DataTable.Cell>Offfline expirement</DataTable.Cell>
            <DataTable.Cell>
              <Text>asdf</Text>
            </DataTable.Cell>
          </DataTable.Row>
          <DataTable.Row>
            <DataTable.Cell>sampleTestData</DataTable.Cell>
            <DataTable.Cell>
              <Text>{sampleTestData}</Text>
            </DataTable.Cell>
          </DataTable.Row>
          <DataTable.Row>
            <DataTable.Cell>sampleSavedData</DataTable.Cell>
            <DataTable.Cell>
              <Text>{eqDataOffline}</Text>
            </DataTable.Cell>
          </DataTable.Row>
          <DataTable.Row>
            <DataTable.Cell>Site Identification</DataTable.Cell>
            <DataTable.Cell>
              <TextInput
                onChangeText={(text) => editEqData(text)}
                value={eqData.site_id}
              />
              <Text>{eqData.site_id}</Text>
            </DataTable.Cell>
          </DataTable.Row>
          <DataTable.Row>
            <DataTable.Cell>Classification</DataTable.Cell>
            <DataTable.Cell>
              <Text>{eqData.classification}</Text>
            </DataTable.Cell>
          </DataTable.Row>
          <DataTable.Row>
            <DataTable.Cell>Serial Number</DataTable.Cell>
            <DataTable.Cell>
              <Text>{eqData.serial_number}</Text>
            </DataTable.Cell>
          </DataTable.Row>
          <DataTable.Row>
            <DataTable.Cell>Equipment Location</DataTable.Cell>
            <DataTable.Cell>
              <Text>23049SDLKFJ</Text>{" "}
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
              <TouchableOpacity
                style={{ backgroundColor: "red", padding: 5 }}
                // onPress={pickImage}
                onPress={_pickDocument}
              >
                <Text>Open Picker</Text>
              </TouchableOpacity>
            </DataTable.Cell>
          </DataTable.Row>
          <DataTable.Row>
            <DataTable.Cell>Scope Specifications</DataTable.Cell>
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
              <Text>23049SDLKFJ</Text>
            </DataTable.Cell>
          </DataTable.Row>
          <DataTable.Row>
            <DataTable.Cell>Scope Specifications</DataTable.Cell>
            <DataTable.Cell>
              <Text style={{ flex: 1, flexWrap: "wrap" }}>
                <View>
                  <Text>Refer asdfto Job Scope (Default)</Text>
                </View>
              </Text>
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

        <Text>{eqData.site_id}</Text>
      </ScrollView>
    </SafeAreaView>
  );
};

export default Resources;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    marginTop: 8,
  },
  input: {
    height: 80,
    margin: 12,
    borderWidth: 1,
    padding: 10,
  },
  row: {
    flexDirection: "row",
    flexWrap: "wrap",
  },
  enabled: {
    color: "green",
  },
  disabled: {
    color: "red",
  },
  box33: {
    width: "33%",
    height: "33%",
  },
  col50: {
    width: "50%",
  },

  spinnerTextStyle: {
    color: "#FFF",
  },
});
