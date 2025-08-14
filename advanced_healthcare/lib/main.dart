  import 'package:advanced_healthcare/pages/home_page.dart';
import 'package:advanced_healthcare/pages/mainScaffold.dart';
  import 'package:flutter/material.dart';



  void main() {
    runApp(const MyApp());
  }

  class MyApp extends StatelessWidget {
    const MyApp({super.key});

    @override
    Widget build(BuildContext context) {
      return MaterialApp(
        title: 'Advanced Healthcare',
        debugShowCheckedModeBanner: false,
        home: const HomePage(),
      );
    }
  }