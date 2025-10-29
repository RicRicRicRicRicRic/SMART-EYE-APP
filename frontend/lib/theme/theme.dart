import 'package:flutter/material.dart';

class SmartEyeTheme {
  static const Color primaryColor = Color(0xFF1E88E5);
  static const Color secondaryColor = Color(0xFF64B5F6);
  static const Color backgroundColor = Color(0xFFF5F5F5);
  static const Color surfaceColor = Color(0xFFFFFFFF);
  static const Color textPrimary = Color(0xFF212121);
  static const Color textSecondary = Color(0xFF9E9E9E);
  static const Color darkBackground = Color(0xFF0D1B2A);

  static final ThemeData lightMode = ThemeData(
    useMaterial3: true,
    brightness: Brightness.light,
    colorScheme: const ColorScheme.light(
      primary: primaryColor,
      secondary: secondaryColor,
      background: backgroundColor,
      surface: surfaceColor,
      onBackground: textPrimary,
      onSurface: textPrimary,
    ),
    scaffoldBackgroundColor: backgroundColor,
    fontFamily: 'Roboto',
    appBarTheme: const AppBarTheme(
      backgroundColor: primaryColor,
      foregroundColor: Colors.white,
    ),
  );
}