# NeoGuardian - AI-Powered Neonatal Care Assistant

## Overview
NeoGuardian is a web application that uses AI (Google Gemini) to analyze baby symptoms and provide recommendations. It supports multiple languages and includes features like chat interface, voice input, and clinic locator.

## Features
- Symptom analysis with risk assessment
- Multilingual support (English, Yoruba, Hausa, Pidgin)
- Voice input
- Dark mode
- Chat download
- Feedback system
- Nearby clinic locator for urgent cases
- Enhanced landing page with 3D animations

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Set GOOGLE_API_KEY in app.py
3. Run: `python app.py`
4. Access at http://localhost:5000

## Ethical Note
This app is not a substitute for professional medical advice. Always consult a doctor.

## Architecture
- Flask backend
- Gemini API for analysis
- Three.js for landing page animations
- Web Speech API for voice input
- Google Maps API for location services 