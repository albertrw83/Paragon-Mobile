import {
  View,
  Text,
  StyleSheet,
  Dimensions,
  Image,
  TouchableOpacity,
  Modal,
} from "react-native";
import React from "react";
// import Modal from "react-native-modal";
import Theme from "../assets/theme/Theme";
const WINDOW_WIDTH = Dimensions.get("window").width;
const WINDOW_HEIGHT = Dimensions.get("window").height;

export default function JobModal({ job, showModal, setShowModal }) {
  const closeModal = () => {
    setShowModal(!showModal);
  };
  const JobDetail = ({ text1, text2 }) => {
    return (
      <View style={styles.container}>
        <Text style={styles.heading}>{text1} | </Text>
        <Text style={styles.jobDetail}>{text2}</Text>
      </View>
    );
  };
  return (
    <View style={styles.centeredView}>
      <Modal
        // animationType="slide"
        transparent={true}
        visible={showModal}
        onRequestClose={closeModal}
      >
        <View style={styles.centeredView}>
          <View style={styles.modalContainer}>
            <TouchableOpacity style={styles.crossTouch} onPress={closeModal}>
              <Image style={styles.crossIcon} source={Theme.icons.closeIcon} />
            </TouchableOpacity>
            <Text style={styles.jobDetailTxt}> Job Detail</Text>
            <JobDetail
              text1={"Customer Name"}
              text2={
                job?.customer_name === null
                  ? "Name not available"
                  : job?.customer_name
              }
            />
            <JobDetail text1={"Job Name"} text2={job?.job_name} />
            <JobDetail text1={"Job Number"} text2={job?.job_number} />
            <JobDetail
              text1={"Total Equipments"}
              text2={job?.equipment?.length}
            />
          </View>
        </View>
      </Modal>
    </View>
  );
}

const styles = StyleSheet.create({
  modalContainer: {
    width: "100%",
    padding: 5,
    backgroundColor: Theme.colors.white,
    borderRadius: 10,
    borderColor: Theme.colors.primary,
    borderWidth: 4,
  },
  jobDetailTxt: {
    textAlign: "center",
    textAlignVertical: "center",
    fontSize: 16,
    fontWeight: "bold",
    color: Theme.colors.primary,
  },
  container: {
    width: "90%",
    minHeight: 30,
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: Theme.colors.white,
    paddingHorizontal: 5,
    alignSelf: "center",
  },
  heading: {
    fontSize: 15,
    fontWeight: "bold",
    color: Theme.colors.primary,
  },
  jobDetail: {
    fontSize: 14,
    fontWeight: "500",
  },
  crossIcon: {
    width: 25,
    height: 25,
    resizeMode: "contain",
  },
  crossTouch: { alignSelf: "flex-end", marginRight: 5 },
  centeredView: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "rgba(0,0,0,0.5)",
  },
});
