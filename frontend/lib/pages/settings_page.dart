import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:image_picker/image_picker.dart';
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
  bool isLoading = true, isEditing = false, isSaving = false;
  bool _obscurePassword = true;

  final ImagePicker _picker = ImagePicker();
  late TextEditingController _nameController = TextEditingController();
  late TextEditingController _contactController = TextEditingController();
  late TextEditingController _emailController = TextEditingController();
  late TextEditingController _passwordController = TextEditingController();

  @override
  void initState() {
    super.initState();
    _fetchUserInfo();
  }

  @override
  void dispose() {
    _nameController.dispose();
    _contactController.dispose();
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  Future<String?> _getToken() async => (await SharedPreferences.getInstance()).getString('access_token');

  void _showSnack(String msg, Color color) => ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(msg), backgroundColor: color));

  void _redirectToLogin() => Navigator.pushAndRemoveUntil(context, MaterialPageRoute(builder: (context) => SignInPage()), (route) => false);

  Future<void> _fetchUserInfo() async {
    setState(() => isLoading = true);
    final token = await _getToken();
    if (token == null || token.isEmpty) return _redirectToLogin();

    try {
      final response = await http.get(Uri.parse('$baseUrl/me'), headers: {'Authorization': 'Bearer $token'});
      if (response.statusCode == 200) {
        setState(() {
          userData = jsonDecode(response.body);
          _nameController.text = userData?['full_name'] ?? '';
          _contactController.text = userData?['contact_number'] ?? '';
          _emailController.text = userData?['email'] ?? '';
          _passwordController.text = '';
          isLoading = false;
        });
      } else {
        if (response.statusCode == 401) _redirectToLogin();
        setState(() => isLoading = false);
      }
    } catch (_) {
      setState(() => isLoading = false);
    }
  }

  Future<void> _saveProfileChanges() async {
    setState(() => isSaving = true);
    final token = await _getToken();

    // Prevent passing validation breaking empty strings into the payload body
    final String? fullNameParam = _nameController.text.trim().isEmpty ? null : _nameController.text.trim();
    final String? contactParam = _contactController.text.trim().isEmpty ? null : _contactController.text.trim();
    final String? emailParam = _emailController.text.trim().isEmpty ? null : _emailController.text.trim();
    final String? passwordParam = _passwordController.text.trim().isEmpty ? null : _passwordController.text.trim();

    try {
      final response = await http.put(
        Uri.parse('$baseUrl/me/'),
        headers: {'Authorization': 'Bearer $token', 'Content-Type': 'application/json'},
        body: jsonEncode({
          'full_name': fullNameParam,
          'contact_number': contactParam,
          'email': emailParam,
          'password': passwordParam,
        }),
      );

      if (response.statusCode == 200) {
        _showSnack('Profile updated successfully!', Colors.green);
        setState(() => isEditing = false);
        await _fetchUserInfo();
      } else {
        final errorData = jsonDecode(response.body);
        _showSnack(errorData['detail']?.toString() ?? 'Failed to update profile', Colors.red);
      }
    } catch (_) {
      _showSnack('Connection error', Colors.red);
    } finally {
      setState(() => isSaving = false);
    }
  }

  Future<void> _pickAndUploadImage() async {
    final pickedFile = await _picker.pickImage(source: ImageSource.gallery);
    if (pickedFile == null) return;

    setState(() => isLoading = true);
    final token = await _getToken();

    try {
      var request = http.MultipartRequest('POST', Uri.parse('$baseUrl/me/profile-picture'))
        ..headers['Authorization'] = 'Bearer $token'
        ..files.add(await http.MultipartFile.fromPath('file', pickedFile.path));

      var response = await request.send();
      if (response.statusCode == 200) {
        _showSnack('Profile picture updated!', Colors.green);
        await _fetchUserInfo();
      } else {
        setState(() => isLoading = false);
        _showSnack('Upload failed', Colors.red);
      }
    } catch (_) {
      setState(() => isLoading = false);
      _showSnack('Upload error', Colors.red);
    }
  }

  void _toggleEditMode() {
    setState(() {
      isEditing = !isEditing;
      if (!isEditing) {
        _nameController.text = userData?['full_name'] ?? '';
        _contactController.text = userData?['contact_number'] ?? '';
        _emailController.text = userData?['email'] ?? '';
        _passwordController.text = '';
      }
    });
  }

  Future<void> _logout() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('access_token');
    _redirectToLogin();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('User Settings', style: TextStyle(fontFamily: 'Times New Roman', fontSize: 22, fontWeight: FontWeight.bold)),
        actions: [if (!isLoading) IconButton(icon: Icon(isEditing ? Icons.close : Icons.edit), onPressed: _toggleEditMode)],
      ),
      body: isLoading
          ? const Center(child: CircularProgressIndicator())
          : SingleChildScrollView(
        padding: const EdgeInsets.all(10.0),
        child: Column(
          children: [
            Card(
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
              child: Padding(
                padding: const EdgeInsets.all(10.0),
                child: Column(
                  children: [
                    GestureDetector(
                      onTap: _pickAndUploadImage,
                      child: Stack(
                        alignment: Alignment.bottomRight,
                        children: [
                          CircleAvatar(
                            radius: 45,
                            backgroundImage: userData?['profile_picture_url'] != null
                                ? NetworkImage(userData!['profile_picture_url'])
                                : const AssetImage('assets/images/profile.jpg') as ImageProvider,
                          ),
                          const CircleAvatar(radius: 18, backgroundColor: Colors.blue, child: Icon(Icons.camera_alt, size: 18, color: Colors.white)),
                        ],
                      ),
                    ),
                    const SizedBox(height: 12),
                    Text(userData?['full_name'] ?? 'User', style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
                    Text(userData?['email'] ?? '', style: const TextStyle(color: Colors.grey)),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 10),

            Card(
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text('Account Information', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                    const Divider(height: 20),
                    _buildRow('Full Name', controller: _nameController),
                    _buildRow('Contact Number', controller: _contactController),
                    _buildRow('Email', controller: _emailController),
                    _buildRow('Password', controller: _passwordController, isPassword: true),
                    _buildRow('Responder ID', value: userData?['responder_id']?.toString()),
                    _buildRow('Role', value: userData?['responder_role']),
                    _buildRow('Approval Status', value: userData?['approval_status']),
                    _buildRow('Account Status', value: userData?['is_active']?.toString()),
                    _buildRow('Member Since', value: userData?['created_at']?.toString().substring(0, 10)),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 25),

            SizedBox(
              width: double.infinity,
              child: ElevatedButton.icon(
                onPressed: isEditing ? (isSaving ? null : _saveProfileChanges) : _logout,
                icon: Icon(isEditing ? Icons.save : Icons.logout),
                label: Text(isEditing ? (isSaving ? 'Saving...' : 'Save Changes') : 'Logout'),
                style: ElevatedButton.styleFrom(backgroundColor: isEditing ? Colors.green : Colors.red),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildRow(String label, {TextEditingController? controller, String? value, bool isPassword = false}) {
    final useTextField = controller != null && isEditing;
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 5.0),
      child: Row(
        children: [
          SizedBox(width: 140, child: Text(label, style: const TextStyle(fontWeight: FontWeight.w500, color: Colors.grey))),
          Expanded(
            child: useTextField
                ? TextField(
              controller: controller,
              obscureText: isPassword && _obscurePassword,
              decoration: InputDecoration(
                isDense: true,
                contentPadding: const EdgeInsets.symmetric(vertical: 10.0, horizontal: 12.0),
                border: OutlineInputBorder(borderRadius: BorderRadius.circular(12.0)),
                hintText: 'Enter $label',
                suffixIcon: isPassword
                    ? IconButton(
                  padding: EdgeInsets.zero,
                  constraints: const BoxConstraints(),
                  icon: Icon(_obscurePassword ? Icons.visibility : Icons.visibility_off, size: 20),
                  onPressed: () => setState(() => _obscurePassword = !_obscurePassword),
                )
                    : null,
                suffixIconConstraints: isPassword
                    ? const BoxConstraints(minWidth: 36, minHeight: 20)
                    : null,
              ),
              keyboardType: isPassword
                  ? TextInputType.visiblePassword
                  : (label.contains('Number') ? TextInputType.phone : TextInputType.text),
            )
                : Text(
              isPassword
                  ? '••••••••••'
                  : (controller != null ? (controller.text.isNotEmpty ? controller.text : 'Not provided') : (value ?? 'N/A')),
              style: const TextStyle(fontSize: 16),
            ),
          ),
        ],
      ),
    );
  }
}