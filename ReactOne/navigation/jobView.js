import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import Equipment from "../views/Equipment";
import Dashboard from "../views/Dashboard";
import Site from "../views/Site";
import Preparation from "../views/Preparation";
import Scope from "../views/Scope";
import Safety from "../views/Safety";
import Internal from "../views/Internal";
import Notes from "../views/Notes";
import Files from "../views/Files";

const Tab = createBottomTabNavigator();
const JobView = () => {
  return (
    <Tab.Navigator screenOptions={{}}>
      <Tab.Screen name="Equipment" component={Equipment} />
      {/* <Tab.Screen name="Report" component={TestReport} /> */}
      <Tab.Screen name="Dashboard" component={Dashboard} />
      <Tab.Screen name="Site" component={Site} />
      <Tab.Screen name="Preparation" component={Preparation} />
      <Tab.Screen name="Scope" component={Scope} />
      <Tab.Screen name="Safety" component={Safety} />
      <Tab.Screen name="Internal" component={Internal} />
      <Tab.Screen name="Notes" component={Notes} />
      <Tab.Screen name="Files" component={Files} />
    </Tab.Navigator>
  );
};
export default JobView;
