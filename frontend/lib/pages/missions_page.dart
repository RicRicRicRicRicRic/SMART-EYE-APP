import 'package:flutter/material.dart';

class MissionScreen extends StatelessWidget {
  const MissionScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(
          'Mission Control',
          style: TextStyle(
            fontFamily: 'Times New Roman',
            fontSize: 22,
            fontWeight: FontWeight.bold,
          ),
        ),
      ),
      body: ListView(
        children: const [
          ListTile(leading: Icon(Icons.visibility), title: Text('Surveillance Mode')),
          ListTile(leading: Icon(Icons.local_hospital), title: Text('Emergency Response Mode')),
          ListTile(leading: Icon(Icons.search), title: Text('Search & Rescue Mode')),
        ],
      ),
    );
  }
}