import 'package:advanced_healthcare/pages/offline_records.dart';
import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import 'package:advanced_healthcare/pages/offline_records.dart';

class UploadLabReport extends StatefulWidget {
  const UploadLabReport({super.key});
  @override
  State<UploadLabReport> createState() => _UploadLabReportState();
}

class _UploadLabReportState extends State<UploadLabReport> {
  File? _selectedFile; // Stores the selected file
  String? _fileName; // Stores the name of the selected file

  // Picks a file using the File Picker
  Future<void> _pickFile() async {
    final result = await FilePicker.platform.pickFiles(
      allowedExtensions: ['pdf', 'docx', 'png'],
      type: FileType.custom,
    );

    if (result != null && result.files.single.path != null) {
      File file = File(result.files.single.path!);
      String name = result.files.single.name;

      
      // await prefs.setString('offline_file_path', file.path);
      // await prefs.setString('offline_file_name', name);
      setState(() {
        _selectedFile = file;
        _fileName = name;
      });
    }
  }

  Future<void> _uploadFile() async {
    if (_selectedFile == null) return;
    final name = _fileName!;
    final file = _selectedFile!;
    final path=file.path;

    final prefs = await SharedPreferences.getInstance();
    List<String> storedPaths = prefs.getStringList('uploaded_files') ?? [];
    storedPaths.add('$name|${file.path}');// Store as "name|path"
    await prefs.setStringList('uploaded_files', storedPaths);

    final uri = Uri.parse('https://your-api-endpoint.com/upload');

    // Create multipart request
    var request = http.MultipartRequest('POST', uri)
      ..files.add(
        await http.MultipartFile.fromPath('file', _selectedFile!.path),
      );

    // Send the request

    var response = await request.send();
    
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(
          response.statusCode == 200
              ? 'File uploaded successfully!'
              : 'Failed to upload file.',
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) => 
  Scaffold(
      appBar: AppBar(title: const Text("Upload Lab Records"), backgroundColor: const Color.fromARGB(255, 134, 115, 244),),
      
      body:SafeArea(
      child: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
          const  Text("Upload your lab reports here",style: TextStyle(fontWeight: FontWeight.bold, fontSize: 20),),
            const SizedBox(height: 30,),
            if (_fileName != null)
            Padding(
              padding: const EdgeInsets.all(16.0),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                      Text('Selected file: $_fileName'),
                      const SizedBox(height: 20),
                      
                    ],
                  ),
              ),
          
                // if (_fileName != null)
                //   Text('Selected file: $_fileName'),
                // const SizedBox(height: 20),
                // Padding(
                //   padding: const EdgeInsets.all(8.0),
                //   child: ElevatedButton(
                //     onPressed: _pickFile,
                //     child: const Text('Pick File'),
                //   ),
                // ),
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Padding(
                      padding: const EdgeInsets.all(8.0),
                      child: ElevatedButton(
                        onPressed: _pickFile,
                        child: const Text('Pick File'),
                      ),
                    ),
                    const SizedBox(height: 20),
                    ElevatedButton(
                      onPressed: _selectedFile != null ? _uploadFile : null,
                      child: const Text('Upload File'),
                    ),
                  ],
                ),
              ],
            ),
          ),
    )
      
      );
}
