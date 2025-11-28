import 'package:flutter/material.dart';
import 'signin_page.dart';
import 'signup_page.dart';
import '../theme/theme.dart';
import '../widgets/custom_scaffold.dart';
import '../widgets/welcome_button.dart';

class WelcomePage extends StatelessWidget {
  const WelcomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return CustomScaffold(
      backgroundImage: 'assets/images/auth_bg.png',
      child: SafeArea(
        child: Column(
          children: [
            const Spacer(),


// 🛸 Drone-enhanced welcome text
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 40.0),
              child: Column(
                children: [
                  const Text(
                    'Welcome to SMART-EYE',
                    textAlign: TextAlign.center,
                    style: TextStyle(
                      fontSize: 42.0,
                      fontWeight: FontWeight.w700,
                      color: Colors.white,
                    ),
                  ),


                  const SizedBox(height: 20),

                  Image.asset(
                    'assets/images/logo.png',
                    width: 120,
                    height: 120,
                    fit: BoxFit.contain,
                  ),

                  const SizedBox(height: 20),

                  const Text(
                    'Your emergency alert drone assistant. Sign in to continue.',
                  textAlign: TextAlign.center,
                    style: TextStyle(
                      fontSize: 18,
                      color: Colors.white70,
                    ),
                  ),
                ],
              ),
            ),
            const Spacer(),
            // 👇 Buttons now sit at the bottom
            Row(
              children: [
                Expanded(
                  child: WelcomeButton(
                    buttonText: 'Sign In',
                    onTap: SignInPage(), // 👈 Make it const
                    color: Colors.transparent,
                    textColor: Colors.white,
                  ),
                ),
                Expanded(
                  child: WelcomeButton(
                    buttonText: 'Sign Up',
                    onTap: SignUpPage(),
                    color: Colors.white,
                    textColor: SmartEyeTheme.textPrimary,
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}