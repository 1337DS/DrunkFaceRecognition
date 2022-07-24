// ignore_for_file: prefer_const_literals_to_create_immutables, prefer_const_constructors

import 'dart:convert';
import 'dart:io';
import 'dart:math';

import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';
import 'package:flutter/scheduler.dart';
import 'api.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  //Root of Application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Drunk Face',
      theme: ThemeData(
        primaryColor: Color(0xff333425),
      ),
      home: const MyHomePage(),
      debugShowCheckedModeBanner: false,
    );
  }
}

//Initiating Class
class MyHomePage extends StatefulWidget {
  const MyHomePage({Key? key}) : super(key: key);

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  //Test Methods - no longer needed
  /*
  changeSlash(String input) {
    String output = '';
    for (int i = 0; i < input.length; i++) {
      if (input[i] == '/') {
        output = output + 'ß';
      } else {
        output = output + input[i];
      }
    }
    return output;
  }

  createString() {
    String output = "";
    String alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    var rng = Random();
    for (int i = 0; i < 100; i++) {
      output = output + alphabet[rng.nextInt(23)];
    }
    return output;
  }*/

  /// Print Long String
  void printLongString(String text) {
    final RegExp pattern = RegExp('.{1,800}'); // 800 is the size of each chunk
    pattern
        .allMatches(text)
        .forEach((RegExpMatch match) => print(match.group(0)));
  }

  //Delayed method to push the http request
  Future pushStuff(String url) async {
    Data = await Getdata(url);
    var DecodedData = jsonDecode(Data);
    QueryText = DecodedData['Query'];
    print("Here");
  }

  //Definition of needed local variables
  bool imgtaken = false;
  String? _pic;
  var Data;
  String QueryText = "Hello";

  //Main Canvas builder
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      //AppBar definition
      appBar: AppBar(
          backgroundColor: Color(0xff333425),
          title: Center(
            child: Text("Wie betrunken bist du?",
                style: TextStyle(
                    fontWeight: FontWeight.bold, color: Color(0xffc6bdac))),
          )),
      //Body definition
      body: Padding(
        padding: const EdgeInsets.all(32.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
          children: [
            Expanded(
                flex: 4,
                child: ClipRRect(
                  borderRadius: BorderRadius.circular(30),
                  child: Container(
                      child: imgtaken
                          ? Column(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                //Create rounded Borders
                                ClipRRect(
                                    borderRadius: BorderRadius.circular(30),
                                    child: Image.file(File(_pic!),
                                        fit: BoxFit.fitWidth)),
                                Padding(
                                  padding: const EdgeInsets.only(top: 8.0),
                                  child: Container(
                                    width: 120,
                                    child: ElevatedButton(
                                        style: ElevatedButton.styleFrom(
                                            primary: Color(0xffc6bdac),
                                            shape: RoundedRectangleBorder(
                                                borderRadius:
                                                    BorderRadius.circular(30))),
                                        child: Row(
                                          mainAxisAlignment:
                                              MainAxisAlignment.spaceAround,
                                          children: [
                                            Text("Löschen",
                                                style: TextStyle(
                                                    fontWeight: FontWeight.bold,
                                                    color: Color(0xff333425))),
                                            Icon(
                                              Icons.refresh,
                                              size: 17,
                                              color: Color(0xff333425),
                                            )
                                          ],
                                        ),
                                        //Reset
                                        onPressed: () {
                                          imgtaken = false;
                                          _pic = null;
                                          setState(() {});
                                        }),
                                  ),
                                ),
                              ],
                            )
                          : Container(
                              color: Color(0xffc6bdac),
                              child: Center(
                                child: Text(
                                    "Klicke unten, um ein Bild zu importieren!",
                                    style: TextStyle(
                                        color: Color(0xff333425),
                                        fontWeight: FontWeight.bold)),
                              ))),
                )),
            Flexible(
                flex: 1,
                child: Column(
                    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                    children: [
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                        children: [
                          Container(
                            height: 50,
                            width: 150,
                            child: ElevatedButton(
                              style: ElevatedButton.styleFrom(
                                  primary: Color(0xff575443),
                                  shape: RoundedRectangleBorder(
                                      borderRadius: BorderRadius.circular(15))),
                              child: Text(_pic == null
                                  ? "Bild auswählen"
                                  : "Neues Bild"),
                              //Delayed FilePicker function
                              onPressed: () async {
                                FilePickerResult? result =
                                    await FilePicker.platform.pickFiles();

                                if (result != null) {
                                  _pic = result.files.single.path;
                                  imgtaken = true;
                                  setState(() {});
                                } else {
                                  ScaffoldMessenger.of(context).showSnackBar(
                                      const SnackBar(
                                          content:
                                              Text("Kein Bild ausgewählt")));
                                }

                                setState(() {});
                              },
                            ),
                          ),
                          Container(
                            height: 50,
                            width: 150,
                            child: ElevatedButton(
                              style: ElevatedButton.styleFrom(
                                  primary: Color(0xff575443),
                                  shape: RoundedRectangleBorder(
                                      borderRadius: BorderRadius.circular(15))),
                              child: Text("Analyse"),
                              //Processing the image for the http request
                              onPressed: imgtaken == true
                                  ? () async {
                                      if (_pic != null) {
                                        File image = File(_pic!);
                                        try {
                                          var pngByteData =
                                              image.readAsBytesSync();
                                          String base64string =
                                              base64.encode(pngByteData);
                                        } catch (e) {
                                          imgtaken = false;
                                          _pic = null;
                                          setState(() {});
                                        }
                                        //Not Working since only prototype
                                        //String newString =
                                        //    changeSlash(base64string);
                                        //print(newString);
                                        //String create = createString();
                                        //print(create);
                                        //printLongString(base64string);
                                        //print(_pic.toString());
                                        String url = _pic.toString() ==
                                                "/Users/felixhuesgen/Library/Developer/CoreSimulator/Devices/67DC7E72-2153-447D-B29E-1787005BBB4B/data/Containers/Data/Application/8FAC160C-2399-4EE0-BC67-A9047F27285B/tmp/com.example.drunkface-Inbox/IMG_0007.JPG"
                                            ? "http://127.0.0.1:5000/api?Query=gates"
                                            : "http://127.0.0.1:5000/api?Query=charlie";
                                        //Sending http Request
                                        Data = await Getdata(url);
                                        //Optical analysing popup
                                        showDialog(
                                            barrierDismissible: false,
                                            context: context,
                                            builder: (context) {
                                              return AlertDialog(
                                                shape: RoundedRectangleBorder(
                                                    borderRadius:
                                                        BorderRadius.circular(
                                                            30)),
                                                title: Text(
                                                  "Es wird analysiert...",
                                                  style: TextStyle(
                                                      fontWeight:
                                                          FontWeight.bold),
                                                ),
                                                content: Row(
                                                  mainAxisAlignment:
                                                      MainAxisAlignment.center,
                                                  children: [
                                                    CircularProgressIndicator(
                                                        color:
                                                            Color(0xff575443))
                                                  ],
                                                ),
                                              );
                                            });
                                        //Small delay
                                        await Future.delayed(
                                            Duration(seconds: 2));
                                        //Decoding JSON
                                        var decodedData =
                                            await jsonDecode(Data);
                                        //Setting local variable to input from json
                                        QueryText = decodedData['Query'];
                                        //Closing Popup
                                        Navigator.pop(context);
                                        //Opening new Popup
                                        showDialog(
                                            context: context,
                                            builder: (context) {
                                              return AlertDialog(
                                                  shape: RoundedRectangleBorder(
                                                      borderRadius:
                                                          BorderRadius.circular(
                                                              30)),
                                                  title: Text(
                                                    "Du bist angetrunken!",
                                                    style: TextStyle(
                                                        fontWeight:
                                                            FontWeight.bold),
                                                  ),
                                                  content: Text(
                                                      "Wir schätzen du hast ca. " +
                                                          QueryText +
                                                          " Gläser intus."));
                                            });
                                        //Refresh whole application
                                        setState(() {});
                                      }
                                    }
                                  : null,
                            ),
                          ),
                        ],
                      ),
                    ]))
          ],
        ),
      ),
    );
  }
}
