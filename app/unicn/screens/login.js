import { View, StyleSheet } from "react-native";
import { Text, Button } from "react-native-paper"
import AuthPageHeader from "../components/auth_header";
import {useState} from 'react'
import { colors } from "../constants";

export default function Login({navigation}) {

    function _login(){
      navigation.replace('BottomBarNav');
    }

    return (
        <View style={styles.base_container}>
          <AuthPageHeader title="WELCOME" description="SIGN IN"/>
          <View style={styles.form}>
              <Button onPress={_login}>LOGIN</Button>
          </View>
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
        backgroundColor: colors.light
    },
    form: {
        flex: 1,
        display: "flex",
        alignItems: "center",
        justifyContent: "start",
        width: '100%',
    }
});
