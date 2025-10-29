import 'package:flutter/material.dart';

class MapScreen extends StatelessWidget {
  const MapScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Drone Map'),
        backgroundColor: Colors.white,
        foregroundColor: Colors.black, // Makes app bar text/icon dark
        elevation: 1,
      ),
      body: Center(
        child: Container(
          margin: const EdgeInsets.all(20),
          padding: const EdgeInsets.all(20),
          decoration: BoxDecoration(
            color: Colors.grey[100], // Light background
            borderRadius: BorderRadius.circular(16),
            boxShadow: [
              BoxShadow(
                color: Colors.grey.withOpacity(0.2),
                blurRadius: 8,
                offset: const Offset(0, 4),
              ),
            ],
          ),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: const [
              Icon(Icons.map, size: 80, color: Colors.blueAccent),
              SizedBox(height: 20),
              Text(
                'Map Preview Placeholder',
                style: TextStyle(fontSize: 18, color: Colors.black87),
              ),
              SizedBox(height: 10),
              Text(
                'Drone Position: Lat 14.5534, Lng 121.0471',
                style: TextStyle(color: Colors.black54),
              ),
            ],
          ),
        ),
      ),
      backgroundColor: Colors.white, // Optional: lightens full background
    );
  }
}