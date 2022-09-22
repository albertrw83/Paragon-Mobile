import AsyncStorage from "@react-native-async-storage/async-storage";
export const storeData = async (key, value) => {
  try {
    const jsonValue = JSON.stringify(value);
    await AsyncStorage.setItem(key, jsonValue);
  } catch (e) {
    console.log("error storing data ", e);
  }
};
export const getData = async (key) => {
  try {
    const value = await AsyncStorage.getItem(key);
    if (value !== null) {
      return JSON.parse(value);
    } else {
      return "";
    }
  } catch (e) {
    console.log("error while retrieving data ", e);
  }
};
export const removeData = async (key) => {
  try {
    await AsyncStorage.removeItem(key);
  } catch (e) {
    console.log("error while removing data ", e);
  }
};
export const deleteAllData = async () => {
  try {
    await AsyncStorage.clear();
  } catch (e) {
    console.log("error while deleting all data ", e);
  }
};
