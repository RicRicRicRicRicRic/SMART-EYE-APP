import 'package:flutter/material.dart';
import 'screens/splash_screen.dart';
import '../theme/theme.dart';

void main() {
  runApp(const SmartEyeApp());
}

class SmartEyeApp extends StatelessWidget {
  const SmartEyeApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'SMART-EYE',
      debugShowCheckedModeBanner: false,
      theme: SmartEyeTheme.lightMode,
      home: SplashScreen(),
    );
  }
}