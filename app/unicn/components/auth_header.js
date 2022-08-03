import {View, StyleSheet, Text} from 'react-native'

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
      width: '100%',
      height: 250,
      position: 'relative',
      top: 0,
      left: 0,
      backgroundColor: '#093EF9',
    },
    header: {
      height: 150,
      width: '100%',
      borderTopLeftRadius: 50,
      borderTopRightRadius: 50,
      position: 'absolute',
      top: 200,
      elevation: 10,
      backgroundColor: '#ffffff',
    },
    header_title: {
       left: 20,
       top: 40,
       width: '100%',
       position: 'absolute',
    },
    body: {
        top: 80,
        left: 20,
        flex: 1,
        borderWidth: 1,
        width: '90%',
        borderColor: 'black'
    }
  });