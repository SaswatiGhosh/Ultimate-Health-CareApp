import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';
import 'dart:io';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:open_file/open_file.dart';
import 'package:advanced_healthcare/pages/upload_lab_records.dart';

class OfflineRecords extends StatelessWidget {

  const OfflineRecords({super.key});
  Future<List<Map<String, String>>> _loadAllSavedFile() async 
  {
    final prefs = await SharedPreferences.getInstance();
    List<String> stored = prefs.getStringList('uploaded_files') ?? [];
    return stored.map((entry) {
        final parts = entry.split('|');
        return {'name': parts[0], 'path': parts[1]};
      }).toList();
  }
  


  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Offline Records'),backgroundColor: const Color.fromARGB(255, 134, 115, 244),),
      body:FutureBuilder<List<Map<String, String>>>(

      future: _loadAllSavedFile(),
      builder: (context, snapshot) {
        if (!snapshot.hasData) {
          return const Center(child: CircularProgressIndicator(),
          );
        }
        final files = snapshot.data!;
        if (files.isEmpty){
          return const Center(child: Text("No files uploaded"));
        }
        return ListView.separated(

          itemCount: files.length,
          separatorBuilder: (BuildContext context, int index) => const Divider(),
          itemBuilder: (context,index){
            final filename=files[index]['name']!;
            final filepath=files[index]['path']!;
            final file=File(filepath);
            return ListTile(
              leading: const Icon(Icons.insert_drive_file),
              title: Text(filename),
              onTap: () {
                  OpenFile.open(filepath);
                },

            );
          }
          );
      },
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
