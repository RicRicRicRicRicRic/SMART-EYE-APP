import 'package:flutter/material.dart';
import '../widgets/custom_scaffold.dart';
import '../theme/theme.dart';
import 'welcome_page.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

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
            // Main scrollable content
            Center(
              child: SingleChildScrollView(
                padding: const EdgeInsets.all(24.0),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  crossAxisAlignment: CrossAxisAlignment.center,
                  children: [
                    const SizedBox(height: 40), // space for back button

                    // LOGO
                    Image.asset(
                      'assets/images/logo.png',
                      width: 120,
                      height: 80,
                      fit: BoxFit.contain,
                    ),



                    const Text(
                      'Sign Up',
                      textAlign: TextAlign.center,
                      style: TextStyle(
                        fontSize: 32,
                        fontWeight: FontWeight.bold,
                        color: Colors.black87,
                      ),
                    ),

                    const SizedBox(height: 30),

                    // Responder ID
                    TextField(
                      controller: registerIDController,
                      textAlign: TextAlign.center,
                      decoration: InputDecoration(
                        labelText: 'Responder ID',
                        labelStyle: const TextStyle(color: Colors.black54),
                        filled: true,
                        fillColor: Colors.white,
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(16),
                        ),
                      ),
                    ),

                    const SizedBox(height: 15),

                    // Full Name
                    TextField(
                      controller: usernameController,
                      textAlign: TextAlign.center,
                      decoration: InputDecoration(
                        labelText: 'Full name',
                        labelStyle: const TextStyle(color: Colors.black54),
                        filled: true,
                        fillColor: Colors.white,
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(16),
                        ),
                      ),
                    ),

                    const SizedBox(height: 15),

                    // Email
                    TextField(
                      controller: emailController,
                      textAlign: TextAlign.center,
                      decoration: InputDecoration(
                        labelText: 'Email',
                        labelStyle: const TextStyle(color: Colors.black54),
                        filled: true,
                        fillColor: Colors.white,
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(16),
                        ),
                      ),
                    ),

                    const SizedBox(height: 15),

                    // Password
                    TextField(
                      controller: passwordController,
                      obscureText: true,
                      textAlign: TextAlign.center,
                      decoration: InputDecoration(
                        labelText: 'Password',
                        labelStyle: const TextStyle(color: Colors.black54),
                        filled: true,
                        fillColor: Colors.white,
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(16),
                        ),
                      ),
                    ),

                    const SizedBox(height: 20),

                    // Register Button
                    ElevatedButton(
                      onPressed: () async {
                        // ... collect values ...

                        final response = await http.post(
                          Uri.parse('http://localhost:8000/api/register'),  // or your real backend URL
                          headers: {'Content-Type': 'application/json'},
                          body: jsonEncode({
                            'responder_id': registerIDController.text.trim(),
                            'full_name': usernameController.text.trim(),
                            'contact_number': '', // optional — add field if needed
                            'email': emailController.text.trim(),
                            'password': passwordController.text,
                          }),
                        );

                        if (response.statusCode == 201) {
                          // success → show message, go to login or welcome
                          ScaffoldMessenger.of(context).showSnackBar(
                            const SnackBar(content: Text('Registration submitted! Waiting for approval.')),
                          );
                          Navigator.pop(context);
                        } else {
                          // error
                          final msg = jsonDecode(response.body)['detail'] ?? 'Registration failed';
                          ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(msg)));
                        }
                      },
                      style: ElevatedButton.styleFrom(
                        backgroundColor: SmartEyeTheme.primaryColor,
                        padding: const EdgeInsets.symmetric(vertical: 14, horizontal: 80),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(16),
                        ),
                      ),
                      child: const Text(
                        'Register',
                        style: TextStyle(color: Colors.white),
                      ),
                    ),
                  ],
                ),
              ),
            ),

            // Back button at top-left
            Positioned(
              top: 16,
              left: 16,
              child: IconButton(
                icon: const Icon(Icons.arrow_back, color: Colors.black87),
                onPressed: () {
                  Navigator.pushReplacement(
                    context,
                    MaterialPageRoute(builder: (context) => const WelcomePage()),
                  );
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}
