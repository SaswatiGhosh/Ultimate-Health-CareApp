import 'package:flutter/material.dart';
import 'package:advanced_healthcare/pages/feature_cards.dart';
import 'package:advanced_healthcare/pages/symptom_checker.dart';
import 'package:advanced_healthcare/pages/doctors_appointment.dart';
import 'package:advanced_healthcare/pages/upload_lab_records.dart';
import 'package:advanced_healthcare/pages/offline_records.dart';


// This is a named constructor that initializes the widget with a title and icon.
// const improves performance if the values don’t change.
// super(key: key) allows this widget to take an optional key for widget tree optimizatio
class HomePage extends StatefulWidget {   
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  @override


  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea
      (
        child: Column(
          children: 
          [
            //app bar
            Padding(
              padding: const EdgeInsets.all(25.0),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text("Hello", style: TextStyle(fontSize: 15, color: Colors.blue, fontWeight: FontWeight.bold),),
                      Text("Miss Best", style: TextStyle(fontSize:25, color:Colors.blue, fontWeight: FontWeight.bold),),
                    ],
                  ),
                  //profile picture
                  
                  Container(
              
                    padding: EdgeInsets.all(12),
                    decoration: BoxDecoration(color: Colors.deepPurpleAccent, borderRadius: BorderRadius.circular(12)),
                    child: Icon(Icons.person),
                  )
                ],
              ),
            ),
            //how do you feel about today
            SizedBox(height: 25),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 25.0),
              child: Container(
                padding: EdgeInsets.all(12),
                decoration: BoxDecoration(color: const Color.fromARGB(255, 236, 193, 243),borderRadius: BorderRadius.circular(12)),
                child: Row(
                  children: [
                    Container(
                      height: 100,
                      width: 100,
                      color: Colors.deepPurple,
                      
                    ),
                    SizedBox(width: 20),
                    Column(
                      children: [
                        Text("How do you feel about today?",style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),),
                        SizedBox(height: 8),
                        Text("Fill out the medical forms"),
                        SizedBox(height: 8),
                        Container(
                          padding: EdgeInsets.all(12),
                          decoration: BoxDecoration(color: Colors.indigoAccent,borderRadius: BorderRadius.circular(12)),
                        
                          child: Center(
                            child: Text('Get Started',style: TextStyle(color: Colors.white),),
                          ),
                        )
                      ],
                    )
                  ],
                ),
              ),
            ),

            //search bar
            SizedBox(height: 25),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 25.0),
              child: Container(
                padding: EdgeInsets.all(12),
                decoration: BoxDecoration(color:  const Color.fromARGB(255, 236, 193, 243), borderRadius: BorderRadius.circular(12)),
                child: TextField(
                  decoration: InputDecoration(
                    prefixIcon: Icon(Icons.search),
                    border: InputBorder.none,
                    hintText: 'How can we help you today?',
                    hintStyle: TextStyle(fontWeight: FontWeight.bold),
                )
                ),
              ),
            ),
            // Service list we are offering  Buttons:  Symptom Checker  Upload Lab Report  Offline Records  Settings (language, sync, etc.)  Shall I put this 4 as buttons or as cards in Flutter homepage
            SizedBox(height: 25),
            Expanded(
              child: Padding(
                padding: const EdgeInsets.symmetric(horizontal: 25.0),
                child: GridView.count(
                  crossAxisCount: 2,
                  children: [
                    FeatureCard(title: "Symptom Checker", icon: Icons.health_and_safety,onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => SymptomCheckerPage())), ),
                    FeatureCard(title: "Upload Lab Report", icon: Icons.upload_file , onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => UploadLabReport())),),
                    FeatureCard(title: "Offline Records", icon: Icons.folder_off , onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => OfflineRecords())),),
                    FeatureCard(title: "Doctors appointment", icon: Icons.medical_services_outlined , onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => DoctorsAppointment())),),
                    ],
              )
              
              ),
            ),
        
        
        
        ]
        ),
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