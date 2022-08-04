import { StyleSheet, View } from "react-native";
import { Text, Button } from "react-native-paper";

export default function Dashboard({navigation}) {
    function  _logout() {
        navigation.replace("Login");
    }
    return (
        <View style={styles.base_container}>
            <Text>Dashboard</Text>
            <Button onPress={_logout}>Logout!</Button>
        </View>
    )
}


const styles = StyleSheet.create({
    base_container: {
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        flex: 1,
        minHeight: "100%",
    }
});
