import 'package:advanced_healthcare/pages/doctors_appointment.dart';
import 'package:flutter/material.dart';

class SymptomCheckerPage extends StatefulWidget {   
  const SymptomCheckerPage({super.key});

  @override
  State<SymptomCheckerPage> createState() => _SymptomCheckerPageState();
}

class _SymptomCheckerPageState extends State<SymptomCheckerPage> {
   


  @override
  Widget build(BuildContext context) => 
  Scaffold(
      appBar: AppBar(title: const Text("Symptom Checker"), backgroundColor: const Color.fromARGB(255, 134, 115, 244),),
      
      body:SafeArea(
      child: Padding(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
        children: [
          Text("Hey, It seems you are not doing good. Tell me how do you feel?", style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),),
          SizedBox(height: 20),
          TextField(
            minLines: 1,
            maxLines: 25,
            decoration: InputDecoration(
              hintText: " I am feeling.....",
              labelStyle: TextStyle(fontWeight: FontWeight.bold , fontSize: 25),
              border: OutlineInputBorder(),
              // icon: const Icon(Icons.clear)
            ),
          ),
          // SizedBox(height: 20),
          Expanded(
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children : [
              ElevatedButton(
              onPressed: () {},
              child: Text("Submit"),
            ),
              ElevatedButton(onPressed: () => Navigator.push(context, MaterialPageRoute(builder: (_) => DoctorsAppointment())),
              // style:ElevatedButton.styleFrom(backgroundColor:  Colors.purple[100]),
              child: Text("Doctor Appointment"),
              )
            ]
            )
          )



        ],
      )
    )
  ),
  bottomNavigationBar: BottomNavigationBar(items:[ const 
      BottomNavigationBarItem(icon: Icon(Icons.home),label: 'Home'),
      BottomNavigationBarItem(icon: Icon(Icons.settings),label: 'Settings'),
      BottomNavigationBarItem(icon: Icon(Icons.question_answer),label: 'Help'),
      ]
      )
  );
}




