import {
  View,
  Text,
  TouchableOpacity,
  FlatList,
  Image,
  StyleSheet,
} from "react-native";
import React from "react";
import Theme from "../assets/theme/Theme";

export default function JobsList({ allJobs, setSelectedJob, showJobDetail }) {
  return (
    <View>
      <FlatList
        showsVerticalScrollIndicator={false}
        data={allJobs}
        keyExtractor={(job, i) => `id-${i}`}
        renderItem={({ item }) => {
          return (
            <TouchableOpacity
              activeOpacity={0.9}
              onPress={() => {
                showJobDetail(true);
                setSelectedJob(item);
              }}
            >
              <View style={styles.container}>
                <Text style={styles.jobName}>{item?.job_name}</Text>
                <Image style={styles.icon} source={Theme.icons.rightArrow} />
              </View>
            </TouchableOpacity>
          );
        }}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    width: "100%",
    height: 50,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
  },
  jobName: {
    fontSize: 16,
  },
  icon: {
    width: 20,
    height: 20,
    resizeMode: "contain",
  },
});
