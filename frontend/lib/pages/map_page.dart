import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import '../constants/api_constants.dart';

class MapScreen extends StatefulWidget {
  const MapScreen({super.key});

  @override
  State<MapScreen> createState() => _MapScreenState();
}

class _MapScreenState extends State<MapScreen> {
  final MapController mapController = MapController();
  LatLng? dronePosition;
  bool isLoading = true;
  String? errorMessage;

  static const LatLng _initialPosition = LatLng(14.5534, 121.0471);

  @override
  void initState() {
    super.initState();
    _fetchDroneLocation();
  }

  void _zoomMap(bool zoomIn) {
    final currentZoom = mapController.camera.zoom;
    final targetZoom = zoomIn ? currentZoom + 1.0 : currentZoom - 1.0;

    if (targetZoom >= 5.0 && targetZoom <= 18.0) {
      mapController.move(mapController.camera.center, targetZoom);
    }
  }

  Future<void> _fetchDroneLocation() async {
    setState(() {
      isLoading = true;
      errorMessage = null;
    });

    try {
      final prefs = await SharedPreferences.getInstance();
      final token = prefs.getString('access_token');

      final response = await http.get(
        Uri.parse('$baseUrl/drone/location'),
        headers: {'Authorization': 'Bearer $token'},
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        final lat = (data['latitude'] as num).toDouble();
        final lng = (data['longitude'] as num).toDouble();

        setState(() {
          dronePosition = LatLng(lat, lng);
        });

        if (mounted) {
          mapController.move(dronePosition!, mapController.camera.zoom);
        }
      } else {
        setState(() {
          errorMessage = "Failed to load location";
        });
      }
    } catch (e) {
      print("Error: $e");
      setState(() {
        errorMessage = "Connection error";
      });
    } finally {
      setState(() => isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Drone Map', style: TextStyle(fontFamily: 'Times New Roman')),
        backgroundColor: const Color(0xFF1E88E5),
        foregroundColor: Colors.white,
      ),
      body: Stack(
        children: [
          Positioned.fill(
            child: FlutterMap(
              mapController: mapController,
              options: MapOptions(
                initialCenter: dronePosition ?? _initialPosition,
                initialZoom: 15,
                minZoom: 5,
                maxZoom: 18,
              ),
              children: [
                TileLayer(
                  urlTemplate: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
                  subdomains: const ['a', 'b', 'c'],
                  userAgentPackageName: 'com.example.smarteye',
                ),
                if (dronePosition != null)
                  MarkerLayer(
                    markers: [
                      Marker(
                        point: dronePosition!,
                        width: 60,
                        height: 60,
                        child: const Icon(
                          Icons.flight,
                          color: Colors.red,
                          size: 45,
                        ),
                      ),
                    ],
                  ),
              ],
            ),
          ),
          Positioned(
            top: 16,
            right: 16,
            child: FloatingActionButton(
              heroTag: "btn_refresh_map",
              onPressed: _fetchDroneLocation,
              backgroundColor: const Color(0xFF1E88E5),
              child: const Icon(Icons.refresh, color: Colors.white),
            ),
          ),
          Positioned(
            bottom: 24,
            right: 16,
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                FloatingActionButton.small(
                  heroTag: "btn_zoom_in",
                  onPressed: () => _zoomMap(true),
                  backgroundColor: Colors.white,
                  child: const Icon(Icons.add, color: Colors.black87),
                ),
                const SizedBox(height: 8),
                FloatingActionButton.small(
                  heroTag: "btn_zoom_out",
                  onPressed: () => _zoomMap(false),
                  backgroundColor: Colors.white,
                  child: const Icon(Icons.remove, color: Colors.black87),
                ),
              ],
            ),
          ),
          if (isLoading)
            const Center(child: CircularProgressIndicator()),
          if (errorMessage != null)
            Center(
              child: Padding(
                padding: const EdgeInsets.all(20),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    const Icon(Icons.error_outline, color: Colors.red, size: 50),
                    const SizedBox(height: 10),
                    Text(errorMessage!, textAlign: TextAlign.center),
                    const SizedBox(height: 10),
                    ElevatedButton(
                      onPressed: _fetchDroneLocation,
                      child: const Text('Retry'),
                    ),
                  ],
                ),
              ),
            ),
        ],
      ),
    );
  }
}