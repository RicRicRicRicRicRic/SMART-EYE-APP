import 'package:flutter/material.dart';
import 'settings_page.dart';
import 'map_page.dart';
import 'alerts_page.dart';
import 'missions_page.dart';

class DashboardScreen extends StatelessWidget {
  const DashboardScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('SMART-EYE Dashboard'),
        centerTitle: true,
        automaticallyImplyLeading:
          false, // ✅ This removes the back button completely
        actions: [
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
            // Drone status card
            Card(
              shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(16)),
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text('Drone Status',
                        style: TextStyle(
                            fontSize: 18, fontWeight: FontWeight.bold)),
                    const SizedBox(height: 8),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: const [
                        Text('Battery: 87%'),
                        Text('Altitude: 120m'),
                        Text('Speed: 15 km/h'),
                      ],
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 16),

            // Emergency alert
            Card(
              shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(16)),
              child: const Padding(
                padding: EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text('Latest Emergency Alert',
                        style: TextStyle(
                            fontSize: 18, fontWeight: FontWeight.bold)),
                    SizedBox(height: 8),
                    Text('Type: Fire Hazard'),
                    Text('Location: Lat 14.553, Lng 121.047'),
                    Text('Time: 12:45 PM'),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 16),

            // Action buttons
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                ElevatedButton.icon(
                  onPressed: () {},
                  icon: const Icon(Icons.flight_takeoff),
                  label: const Text('Launch'),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.green,
                    foregroundColor: Colors.white, // ✅ Makes text & icon white
                  ),
                ),
                ElevatedButton.icon(
                  onPressed: () {},
                  icon: const Icon(Icons.flight_land),
                  label: const Text('Land'),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.orange,
                    foregroundColor: Colors.white, // ✅ Makes text & icon white
                  ),
                ),
                ElevatedButton.icon(
                  onPressed: () {},
                  icon: const Icon(Icons.warning),
                  label: const Text('Emergency'),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.red,
                    foregroundColor: Colors.white, // ✅ Makes text & icon white
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),

            // Navigation shortcuts
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                _buildNavButton(context, 'Map', Icons.map, const MapScreen()),
                _buildNavButton(context, 'Alerts', Icons.notifications, AlertsScreen()),
                _buildNavButton(context, 'Missions', Icons.flag, const MissionScreen()),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildNavButton(BuildContext context, String label, IconData icon, Widget screen) {
    return ElevatedButton.icon(
      onPressed: () => Navigator.push(context, MaterialPageRoute(builder: (context) => screen)),
      icon: Icon(icon),
      label: Text(label),
    );
  }
}