import 'package:flutter/material.dart';


class DoctorsAppointment extends StatelessWidget {
  const DoctorsAppointment({super.key});
  @override
  Widget build(BuildContext context){
 return  Scaffold(
      appBar: AppBar(title: const Text("Doctors Appointment"),backgroundColor: const Color.fromARGB(255, 134, 115, 244),),
      
      body:Center(child: Text("Doctors Appointment")
      ),
      bottomNavigationBar: BottomNavigationBar(items:[ const 
      BottomNavigationBarItem(icon: Icon(Icons.home),label: 'Home'),
      BottomNavigationBarItem(icon: Icon(Icons.settings),label: 'Settings'),
      BottomNavigationBarItem(icon: Icon(Icons.question_answer),label: 'Help'),
      ]
      )
      );
}
}
  



