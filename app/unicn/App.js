import { View } from 'react-native';
import { ActivityIndicator, Provider } from 'react-native-paper';
import { useState } from 'react';
import 'react-native-gesture-handler';
import AppNavigation from './core/app_navigator';

export default function App() {
  const [is_loading, setIsLoading] = useState(false);

  if (is_loading)
    return (
      <View
      style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        flex: 1,
        minHeight: "100%",
      }}>
        <ActivityIndicator
          size="large"
          style={{marginTop: -20}}
          animating={true}
          color="#044df5"
        />
      </View>
    )

  return (
    <Provider>
        <AppNavigation/>
    </Provider>
  );
}
