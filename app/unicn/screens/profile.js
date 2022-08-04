import { View, StyleSheet } from "react-native";
import { Text } from "react-native-paper";

export default function Profile() {
    return (
        <View style={styles.base_container}>
            <Text>Profile</Text>
        </View>
    );
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
