import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import '../constants/api_constants.dart';
import 'settings_page.dart';
import 'map_page.dart';
import 'alerts_page.dart';
import 'missions_page.dart';

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({super.key});

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  double? altitude;
  double? speed;
  int? battery;
  bool isLive = false;
  bool isLoading = true;
  String? errorMessage;

  @override
  void initState() {
    super.initState();
    _fetchDroneStatus();
  }

  Future<void> _fetchDroneStatus() async {
    setState(() {
      isLoading = true;
      errorMessage = null;
    });

    try {
      final prefs = await SharedPreferences.getInstance();
      final token = prefs.getString('access_token');

      final response = await http.get(
        Uri.parse('$baseUrl/drone/status'),
        headers: {'Authorization': 'Bearer $token'},
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);

        setState(() {
          if (data['status'] == 'no_live_data') {
            altitude = null;
            speed = null;
            battery = null;
            isLive = false;
          } else {
            altitude = (data['altitude'] as num?)?.toDouble();
            speed = (data['speed'] as num?)?.toDouble();
            battery = data['battery'] as int?;
            isLive = true;
          }
          isLoading = false;
        });
      } else {
        setState(() {
          errorMessage = "Failed to load telemetry";
          isLoading = false;
        });
      }
    } catch (e) {
      print("Dashboard Fetch Error: $e");
      setState(() {
        errorMessage = "Connection error";
        isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(
          'Dashboard',
          style: TextStyle(
            fontFamily: 'Times New Roman',
            fontSize: 22,
            fontWeight: FontWeight.bold,
          ),
        ),
        centerTitle: true,
        automaticallyImplyLeading: false,
        leading: Padding(
          padding: const EdgeInsets.all(8.0),
          child: Image.asset(
            'assets/images/logo.png',
            width: 120,
            height: 120,
            fit: BoxFit.contain,
          ),
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: _fetchDroneStatus,
          ),
          IconButton(
            icon: const Icon(Icons.settings),
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const SettingsScreen()),
              );
            },
          ),
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Card(
              shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(16)),
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        const Text(
                          'Drone Status',
                          style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                        ),
                        if (isLoading)
                          const SizedBox(
                            width: 16,
                            height: 16,
                            child: CircularProgressIndicator(strokeWidth: 2),
                          ),
                      ],
                    ),
                    const SizedBox(height: 8),
                    errorMessage != null
                        ? Text(
                      errorMessage!,
                      style: const TextStyle(color: Colors.red, fontSize: 14),
                    )
                        : !isLive
                        ? const Padding(
                      padding: EdgeInsets.symmetric(vertical: 4.0),
                      child: Row(
                        children: [
                          Icon(
                            Icons.signal_cellular_connected_no_internet_4_bar,
                            color: Colors.orange,
                            size: 16,
                          ),
                          SizedBox(width: 8),
                          Text(
                            'Drone Offline - No Data Available',
                            style: TextStyle(
                              color: Colors.orange,
                              fontWeight: FontWeight.w500,
                            ),
                          ),
                        ],
                      ),
                    )
                        : Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text('Battery: ${battery != null ? "$battery%" : "N/A"}'),
                        Text('Altitude: ${altitude != null ? "${altitude!.toStringAsFixed(1)}m" : "N/A"}'),
                        Text('Speed: ${speed != null ? "${speed!.toStringAsFixed(1)} m/s" : "N/A"}'),
                      ],
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 16),

            Card(
              shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(16)),
              child: const Padding(
                padding: EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Latest Emergency Alert',
                      style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                    ),
                    SizedBox(height: 8),
                    Text('Type: Fire Hazard'),
                    Text('Location: Lat 14.553, Lng 121.047'),
                    Text('Time: 12:45 PM'),
                  ],
                ),
              ),
            ),

            const Spacer(),

            Row(
              children: [
                Expanded(
                  child: _buildNavButton(
                    context,
                    'Map',
                    Icons.map,
                    const MapScreen(),
                    const Color(0xFF1E88E5),
                  ),
                ),
                const SizedBox(width: 10),
                Expanded(
                  child: _buildNavButton(
                    context,
                    'Alerts',
                    Icons.notifications,
                    AlertsScreen(),
                    Colors.red,
                  ),
                ),
                const SizedBox(width: 10),
                Expanded(
                  child: _buildNavButton(
                    context,
                    'Missions',
                    Icons.flag,
                    MissionScreen(),
                    Colors.green,
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildNavButton(
      BuildContext context,
      String label,
      IconData icon,
      Widget screen,
      Color backgroundColor,
      ) {
    return ElevatedButton.icon(
      onPressed: () => Navigator.push(context, MaterialPageRoute(builder: (_) => screen)),
      icon: Icon(icon),
      label: Text(label),
      style: ElevatedButton.styleFrom(
        backgroundColor: backgroundColor,
        foregroundColor: Colors.white,
        padding: const EdgeInsets.symmetric(vertical: 14),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(8),
        ),
      ),
    );
  }
}