import 'package:flutter/material.dart';

class CustomScaffold extends StatelessWidget {
  final Widget child;
  final String? backgroundImage;

  const CustomScaffold({
    super.key,
    required this.child,
    this.backgroundImage,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        width: double.infinity,
        height: double.infinity,
        decoration: backgroundImage != null
            ? BoxDecoration(
          image: DecorationImage(
            image: AssetImage(backgroundImage!),
            fit: BoxFit.cover,
          ),
        )
            : const BoxDecoration(
          color: Colors.white,
        ),
        child: child,
      ),
    );
  }
}