import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import '../widgets/custom_scaffold.dart';
import '../theme/theme.dart';
import 'welcome_page.dart';
import '../constants/api_constants.dart';

class SignUpPage extends StatelessWidget {
  final TextEditingController emailController = TextEditingController();
  final TextEditingController passwordController = TextEditingController();
  final TextEditingController registerIDController = TextEditingController();
  final TextEditingController usernameController = TextEditingController();

  SignUpPage({super.key});

  @override
  Widget build(BuildContext context) {
    return CustomScaffold(
      child: SafeArea(
        child: Stack(
          children: [
            Center(
              child: SingleChildScrollView(
                padding: const EdgeInsets.all(24.0),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    const SizedBox(height: 40),
                    Image.asset(
                      'assets/images/logo.png',
                      width: 120,
                      height: 80,
                      fit: BoxFit.contain,
                    ),
                    const Text(
                      'Sign Up',
                      style: TextStyle(
                        fontSize: 32,
                        fontWeight: FontWeight.bold,
                        color: Colors.black87,
                      ),
                    ),
                    const SizedBox(height: 30),
                    _buildTextField(registerIDController, 'Responder ID'),
                    const SizedBox(height: 15),
                    _buildTextField(usernameController, 'Full name'),
                    const SizedBox(height: 15),
                    _buildTextField(emailController, 'Email'),
                    const SizedBox(height: 15),
                    _buildTextField(passwordController, 'Password', isPassword: true),
                    const SizedBox(height: 20),
                    ElevatedButton(
                      onPressed: () => _handleRegister(context),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: SmartEyeTheme.primaryColor,
                        padding: const EdgeInsets.symmetric(vertical: 14, horizontal: 80),
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                      ),
                      child: const Text('Register', style: TextStyle(color: Colors.white)),
                    ),
                  ],
                ),
              ),
            ),
            Positioned(
              top: 16,
              left: 16,
              child: IconButton(
                icon: const Icon(Icons.arrow_back, color: Colors.black87),
                onPressed: () => Navigator.pop(context),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildTextField(TextEditingController controller, String label, {bool isPassword = false}) {
    return TextField(
      controller: controller,
      obscureText: isPassword,
      textAlign: TextAlign.center,
      decoration: InputDecoration(
        labelText: label,
        filled: true,
        fillColor: Colors.white,
        border: OutlineInputBorder(borderRadius: BorderRadius.circular(16)),
      ),
    );
  }

  Future<void> _handleRegister(BuildContext context) async {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Registering...'), duration: Duration(seconds: 1)),
    );

    try {
      final response = await http.post(
        Uri.parse('$baseUrl/register'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'responder_id': registerIDController.text.trim(),
          'full_name': usernameController.text.trim(),
          'contact_number': null,
          'email': emailController.text.trim(),
          'password': passwordController.text,
        }),
      );

      if (response.statusCode == 201) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Registration successful! Waiting for admin approval.'), backgroundColor: Colors.green),
        );
        Navigator.pop(context);
      } else {
        final msg = jsonDecode(response.body)['detail'] ?? 'Registration failed';
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(msg), backgroundColor: Colors.red));
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Cannot connect to server.'), backgroundColor: Colors.red),
      );
    }
  }
}