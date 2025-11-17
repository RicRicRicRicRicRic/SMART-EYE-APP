import 'package:flutter/material.dart';

class AlertsScreen extends StatelessWidget {
  final List<String> alerts = [
    'Fire hazard at 12:45 (Lat: 14.553, Lng: 121.047)',
    'Person detected at 12:50 (Lat: 14.554, Lng: 121.048)',
  ];

  AlertsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Emergency Alerts')),
      body: ListView.builder(
        itemCount: alerts.length,
        itemBuilder: (context, index) => Card(
          child: ListTile(
            leading: const Icon(Icons.warning, color: Colors.red),
            title: Text(alerts[index]),
          ),
        ),
      ),
    );
  }
}