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
      backgroundImage: 'assets/images/auth_bg.png', // 👈 Make sure this exists
      child: SafeArea(
        child: Column(
          children: [
            const Spacer(), // Push everything down
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 40.0),
              child: RichText(
                textAlign: TextAlign.center,
                text: const TextSpan(
                  children: [
                    TextSpan(
                      text: 'Welcome to SMART-EYE\n',
                      style: TextStyle(
                        fontSize: 42.0,
                        fontWeight: FontWeight.w700,
                        color: Colors.white,
                      ),
                    ),
                    TextSpan(
                      text:
                      '\nYour emergency alert drone assistant.\n\nSign in to continue.',
                      style: TextStyle(
                        fontSize: 18,
                        color: Colors.white70,
                      ),
                    ),
                  ],
                ),
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