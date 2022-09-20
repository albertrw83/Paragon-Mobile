import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import General from "../views/General";
import TestReport from "../views/TestReport";
import WorkingData from "../views/WorkingData";
import Resources from "../views/Resources";
import SpecialistSupport from "../views/SpecialistSupport";

const Tab = createBottomTabNavigator();
const Tabs = () => {
  return (
    <Tab.Navigator screenOptions={{}}>
      <Tab.Screen name="General" component={General} />
      {/* <Tab.Screen name="Report" component={TestReport} /> */}
      <Tab.Screen name="Working" component={WorkingData} />
      <Tab.Screen name="Resources" component={Resources} />
      <Tab.Screen name="Support" component={SpecialistSupport} />
    </Tab.Navigator>
  );
};
export default Tabs;
