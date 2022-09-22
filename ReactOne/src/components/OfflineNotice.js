import { View, Text } from "react-native";
import React, { useState, useEffect } from "react";
import NetInfo from "@react-native-community/netinfo";
import { useDispatch } from "react-redux";
import { dispatcher } from "../Api/Middleware";
import { setNetworkAvailble } from "../reducers";
import { storeData, getData } from "../utilities/StorageService";
let emptyList = [];

export default function OfflineNotice() {
  const [netInfo, setNetInfo] = useState("");
  const dispatch = useDispatch();
  useEffect(() => {
    // Subscribe to network state updates
    createOfflineList();
    getAllOfflineData();
    const unsubscribe = NetInfo.addEventListener((state) => {
      setNetInfo({
        type: state.type,
        isConnected: state.isConnected,
        isInternetReachable: state.isInternetReachable,
      });
    });

    return () => {
      // Unsubscribe to network state updates
      unsubscribe();
    };
  }, []);

  const createOfflineList = async () => {
    const offlineList = await getData("offlineList");
    console.log("data in offline ", offlineList);
    if (!offlineList) {
      storeData("offlineList", emptyList);
      return;
    }
  };

  useEffect(() => {
    fetchOfflineStoredData(netInfo.isConnected);
  }, [netInfo]);

  const fetchOfflineStoredData = (data) => {
    dispatch(setNetworkAvailble(data));
  };

  const getAllOfflineData = async () => {
    if (netInfo.isConnected) {
      const offlineData = await getData("offlineList");
      console.log("offlineData getAllOfflineData");
      if (offlineData.length > 0) {
        for (let index = 0; index < offlineData.length; index++) {
          const offlineItem = offlineData[index];
          offlineItem.network = true;
          console.log("offlineItem ", offlineItem);
          dispatch(dispatcher(offlineItem));
          console.log("offlineList conditional ", offlineData);
        }
        storeData("offlineList", emptyList);
      }
    }
  };

  return <View />;
}
