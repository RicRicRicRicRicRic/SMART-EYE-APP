import 'package:flutter/material.dart';
import 'package:flutter_spinkit/flutter_spinkit.dart';
import '../pages/welcome_page.dart';
import '../theme/theme.dart';

class SplashScreen extends StatefulWidget {
  const SplashScreen({super.key});

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> {
  @override
  void initState() {
    super.initState();
    Future.delayed(const Duration(seconds: 3), () {
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (context) => const WelcomePage()),
      );
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Theme.of(context).colorScheme.background, // ✅ uses F5F5F5
      body: Column(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          const SizedBox(height: 100),

          // Center logo + branding
          Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Image.asset("assets/images/logo.png", width: 150),
              const SizedBox(height: 20),
              Image.asset("assets/images/branding.png", width: 120),
            ],
          ),

          // Bottom loading animation
          const Padding(
            padding: EdgeInsets.only(bottom: 50),
            child: SpinKitFadingCube(
              color: SmartEyeTheme.primaryColor,
              size: 40.0,
            ),
          ),
        ],
      ),
    );
  }
}