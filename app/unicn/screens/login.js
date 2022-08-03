import { View, StyleSheet, Text } from "react-native";
import AuthPageHeader from "../components/auth_header";

export default function Login() {
    return (
        <View style={styles.page}>
        <AuthPageHeader title="WELCOME" description="SIGN IN"/>
        <View style={styles.body}>
            <Text>FORM</Text>
        </View>
      </View>
      );
}

const styles = StyleSheet.create({
    page: {
      flex: 1,
      backgroundColor: 'white',
    },
    body: {
        top: 80,
        left: 20,
        flex: 1,
        width: '90%',
    }
  });