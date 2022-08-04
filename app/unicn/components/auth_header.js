import {View, StyleSheet} from 'react-native'
import {Text} from "react-native-paper"
import { colors } from '../constants';

export default function AuthPageHeader({title, description}) {
    return (
    <>
    <View style={styles.background} />
      <View style={styles.header}>
        <View style={styles.header_title}>
            <Text style={{fontSize: 20, fontWeight: 'bold', color: '#093EF9'}}>{title}</Text>
            <Text style={{fontSize: 16, fontWeight: '400', color: '#838383', paddingTop: 10}}>{description}</Text>
            <View
              style={{
                borderBottomColor: '#808080',
                borderBottomWidth: 1.5,
                paddingTop: 10,
                width: '90%'
              }}
            />
        </View>
      </View>
      </>
    );
}

const styles = StyleSheet.create({
    background: {
      flex:3/4,
      width: '100%',
      backgroundColor: '#093EF9',
    },
    header: {
      flex: 1,
      justifyContent: "start",
      width: '100%',
      borderTopLeftRadius: 50,
      borderTopRightRadius: 50,
      position: 'relative',
      top: -50,
      backgroundColor: colors.light,
    },
    header_title: {
       top: 40,
       left: 20,
       width: '100%',
       position: 'relative',
    },
    body: {
        flex: 1,
        borderWidth: 1,
        width: '90%',
        borderColor: 'black'
    }
  });