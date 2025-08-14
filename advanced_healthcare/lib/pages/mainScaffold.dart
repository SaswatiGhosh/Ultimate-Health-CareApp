import 'package:flutter/material.dart';
import 'package:advanced_healthcare/pages/symptom_checker.dart';
import 'package:advanced_healthcare/pages/doctors_appointment.dart';
import 'package:advanced_healthcare/pages/upload_lab_records.dart';
import 'package:advanced_healthcare/pages/offline_records.dart';
import 'package:advanced_healthcare/pages/home_page.dart';
import 'package:advanced_healthcare/pages/settingspage.dart';


class MainScaffold extends StatefulWidget {
  const MainScaffold({super.key});

  @override
  State<MainScaffold> createState() => _MainScaffoldState();
}

class _MainScaffoldState extends State<MainScaffold> {
  int _selectedIndex = 0;

  final List<Widget> _pages = [
    HomePage(),
    DoctorsAppointment(),
    SettingsPage()
  
  ];
  final List<String> _titles = [
    'Home',
    'Doctor_Appointment',
    'Settings'
  ];


  void _onItemTapped(int index) {
    setState(() {
      _selectedIndex = index;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(_titles[_selectedIndex]),
        backgroundColor: const Color.fromARGB(255, 84, 159, 197),
      ),
      body: _pages[_selectedIndex],  // 👈 Dynamically display selected screen
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _selectedIndex,
        onTap: _onItemTapped,
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.home), label: 'Home'),
          BottomNavigationBarItem(icon: Icon(Icons.local_hospital), label: 'Doctor Appointment'),
          BottomNavigationBarItem(icon: Icon(Icons.settings), label: 'Settings'),
          
        ],
      ),
    );
  }
}