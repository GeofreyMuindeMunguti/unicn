import { createStackNavigator } from '@react-navigation/stack';
import { NavigationContainer } from '@react-navigation/native';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import Profile from '../screens/profile';
import { createMaterialBottomTabNavigator } from '@react-navigation/material-bottom-tabs';
import Login from '../screens/login';
import { useState } from 'react';
import Dashboard from '../screens/dashboard';
import Chat from '../screens/chat';
import { StyleSheet } from 'react-native';
import { colors } from '../constants';


const Tab = createMaterialBottomTabNavigator()



const BottomBarNavigator = () => {
    return (
        <Tab.Navigator 
            activeColor={colors.primary}
            inactiveColor="#95a5a6"
            barStyle={{ backgroundColor: colors.light }}
        >
            <Tab.Screen name="Dashboard" component={Dashboard} />
            <Tab.Screen name="Chat" component={Chat} />
            <Tab.Screen name="profile" component={Profile} />
        </Tab.Navigator>
    )
}


const AppNavigation = () => {

    const Stack = createStackNavigator();

    return (
        <NavigationContainer>
            <Stack.Navigator
                screenOptions={{ headerShown: false }}
                initialRouteName="Login"
            >
                <Stack.Screen name="Login" component={Login} />
                <Stack.Screen name="BottomBarNav" component={BottomBarNavigator} />
        </Stack.Navigator>
        </NavigationContainer>
    )
}

export default AppNavigation;


const styles = StyleSheet.create({
    bottombarnav: {
        backgroundColor: colors.light,
    }
})