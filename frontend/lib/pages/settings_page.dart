import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import 'signin_page.dart';
import '../constants/api_constants.dart';

class SettingsScreen extends StatefulWidget {
  const SettingsScreen({super.key});

  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  Map<String, dynamic>? userData;
  bool isLoading = true;
  String? errorMessage;

  @override
  void initState() {
    super.initState();
    _fetchUserInfo();
  }

  // Updated _fetchUserInfo with enhanced debugging
  Future<void> _fetchUserInfo() async {
    setState(() {
      isLoading = true;
      errorMessage = null;
    });

    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('access_token');

    print("=== SETTINGS DEBUG ===");
    print("Token exists: ${token != null}");
    if (token != null && token.length > 20) {
      print("Token preview: ${token.substring(0, 20)}...");
    }

    if (token == null || token.isEmpty) {
      print("No token → redirecting to login");
      _redirectToLogin();
      return;
    }

    try {
      final response = await http.get(
        Uri.parse('$baseUrl/me'),
        headers: {
          'Authorization': 'Bearer $token',
          'Content-Type': 'application/json',
        },
      );

      print(" /me response status: ${response.statusCode}");

      if (response.statusCode == 200) {
        setState(() {
          userData = jsonDecode(response.body);
          isLoading = false;
        });
        print("User data loaded successfully");
      } else if (response.statusCode == 401) {
        print("401 Unauthorized - Token invalid/expired");
        errorMessage = "Session expired. Please login again.";
        _redirectToLogin();
      } else {
        print("Other error: ${response.statusCode}");
        errorMessage = "Failed to load profile";
        setState(() => isLoading = false);
      }
    } catch (e) {
      print("Exception in _fetchUserInfo: $e");
      errorMessage = "Connection error";
      setState(() => isLoading = false);
    }
  }

  void _redirectToLogin() {
    Navigator.pushAndRemoveUntil(
      context,
      MaterialPageRoute(builder: (context) => SignInPage()),
          (route) => false,
    );
  }

  Future<void> _logout() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('access_token');
    print("DEBUG LOGOUT: Token removed.");
    _redirectToLogin();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('User Settings',
            style: TextStyle(fontFamily: 'Times New Roman', fontSize: 22, fontWeight: FontWeight.bold)),
      ),
      body: isLoading
          ? const Center(child: CircularProgressIndicator())
          : errorMessage != null
          ? _buildErrorView()
          : _buildProfileContent(),
    );
  }

  Widget _buildErrorView() {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          const Icon(Icons.error_outline, color: Colors.red, size: 48),
          const SizedBox(height: 16),
          Text(errorMessage!, style: const TextStyle(color: Colors.red, fontSize: 16)),
          const SizedBox(height: 20),
          ElevatedButton(
            onPressed: _redirectToLogin,
            child: const Text('Go to Login'),
          ),
        ],
      ),
    );
  }

  Widget _buildProfileContent() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        children: [
          Card(
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
            child: Padding(
              padding: const EdgeInsets.all(20.0),
              child: Column(
                children: [
                  const CircleAvatar(
                      radius: 45,
                      backgroundImage: AssetImage('assets/images/profile.jpg')
                  ),
                  const SizedBox(height: 12),
                  Text(userData?['full_name'] ?? 'User',
                      style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
                  Text(userData?['email'] ?? '',
                      style: const TextStyle(fontSize: 16, color: Colors.grey)),
                ],
              ),
            ),
          ),
          const SizedBox(height: 20),
          _buildInfoCard('Account Information', [
            _buildInfoRow('Responder ID', userData?['responder_id']?.toString()),
            _buildInfoRow('Full Name', userData?['full_name']),
            _buildInfoRow('Email', userData?['email']),
            _buildInfoRow('Contact Number', userData?['contact_number'] ?? 'Not provided'),
            _buildInfoRow('Approval Status', userData?['approval_status']),
            _buildInfoRow('Account Status', userData?['is_active']?.toString()),
            _buildInfoRow('Member Since', userData?['created_at']?.toString().substring(0, 10)),
          ]),
          const SizedBox(height: 30),
          SizedBox(
            width: double.infinity,
            child: ElevatedButton.icon(
              onPressed: _logout,
              icon: const Icon(Icons.logout),
              label: const Text('Logout'),
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.red,
                foregroundColor: Colors.white,
                padding: const EdgeInsets.symmetric(vertical: 16),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildInfoCard(String title, List<Widget> children) {
    return Card(
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(title, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const Divider(height: 20),
            ...children,
          ],
        ),
      ),
    );
  }

  Widget _buildInfoRow(String label, String? value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8.0),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SizedBox(
              width: 140,
              child: Text(label, style: const TextStyle(fontWeight: FontWeight.w500, color: Colors.grey))
          ),
          Expanded(child: Text(value ?? 'N/A', style: const TextStyle(fontSize: 16))),
        ],
      ),
    );
  }
}