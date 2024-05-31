# MoodMatch
<p align="center">
  <img src="app\static\img\Mood match Log.png" />
</p>



**MoodMatch: Where feelings meet recommendations.**

## Overview

MoodMatch is a comprehensive emotional wellness project designed to understand your current mood, provide personalized recommendations, and offer a touch of digital companionship.

## Key Features

1. **Emotion Recognition**
   - Utilizes webcam technology to analyze your facial expressions and identify your current emotional state.
   - Leverages pre-trained models to recognize a range of emotions (e.g., happiness, sadness, anger, surprise).

2. **Personalized Recommendations**
   - **MoodMatch Music**: Curates a personalized Spotify playlist based on your detected mood.
   - **Storytelling Integration**: Recommends stories that align with your emotional state (e.g., funny stories for happy moods, suspenseful stories for excitement).

3. **Voice Recognition and Interaction**
   - Integrates speech-to-text conversion to understand your spoken commands.
   - Allows you to request specific types of recommendations (e.g., "play me a happy song" or "recommend a story").

4. **Chatbot for Mood Moderation**
   - Offers supportive conversation based on your mood.
   - Provides tailored advice or guides you towards helpful resources (self-help articles, relaxation techniques) if needed.

## Goals

1. **Enhance Emotional Awareness**: Help users gain a better understanding of their current emotions.
2. **Improve Emotional Well-being**: Create a positive impact on a user's emotional state through personalized recommendations and supportive conversations.
3. **Offer Personalized User Experience**: Tailor recommendations and interactions based on a user's mood for a more engaging and relevant experience.

## Technologies

- **Backend**: Flask
- **Emotion Recognition**: OpenCV with a pre-trained emotion recognition model (Keras)
- **Webcam Integration**: OpenCV
- **Speech Recognition**: SpeechRecognition or a cloud-based API like Google Speech-to-Text
- **Music Recommendation**: Spotipy
- **Storytelling Integration**: APIs from services like Project Gutenberg or user-created story databases
- **Chatbot**: Rasa or Dialogflow

### Additional Considerations
- **UI**: HTML, CSS, and potentially React
- **Database (Optional)**: SQLAlchemy or mysqldb

## Challenge Statement

MoodMatch aims to address the challenge of limited self-awareness of one's emotional state and the difficulty of finding personalized recommendations or support based on current emotions.

## Who Will Benefit from MoodMatch

- Users interested in improving emotional self-awareness.
- Users seeking personalized recommendations based on their emotional state.
- Users exploring ways to manage emotions.

## Locale Relevance

MoodMatch is a web-based application accessible globally. Integration with location-specific story repositories and support for multiple languages may be considered in future updates.

## Risks

### Technical Risks
- **Emotion Recognition Accuracy**
- **Integration Challenges**
- **Data Security and Privacy**

### Non-Technical Risks
- **User Adoption**
- **Misuse of Recommendations**

## Infrastructure

### Branching and Merging Strategy

- **Version Control**: Git (https://github.com/jeid12/Alx-portfolio)
- **Branching Strategy**: Feature Branch Workflow
  - **Master Branch**: Stable, deployed version.
  - **Feature Branches**: For new functionalities.
  - **Pull Requests**: For code review and merging.

### Deployment Strategy

- **CI/CD**: Jenkins or GitHub Actions
- **Steps**: Building, testing, and deploying the application.

### Data Population

- **Initial Data**: Manually added sample data for testing.
- **User-Generated Data**: Stored in a database to personalize future recommendations.

### Testing Strategy

- **Unit Tests**: Testing individual functionalities.
- **Integration Tests**: Verifying system functionality.
- **End-to-End Tests (Optional)**: Simulating user interactions.
- **Automation**: Using pytest or unittest.

## Existing Solutions

### Emotion Recognition Apps
- Similar: Emoleap, Feeling
- Different: MoodMatch integrates music and story APIs for personalized recommendations.

### Music Recommendation Services
- Similar: Spotify, Apple Music
- Different: MoodMatch uses real-time emotion detection for dynamic recommendations.

### Chatbots for Mental Wellbeing
- Similar: Woebot, Koko
- Different: MoodMatch tailors conversation and recommendations based on real-time emotion detection.

## Disclaimer

MoodMatch is not a replacement for professional therapy or mental health services. It cannot diagnose or treat mental health conditions. Emotion recognition may not always be accurate, and users should not rely solely on MoodMatch for critical decisions.

## Week1 Work

**Figma Design**: https://www.figma.com/design/iwH8uMNgbvheqiJKp6NU61/Moodmatch?node-id=0-1&t=pmJyMb7W0oVVwOca-1
**setting up structure**
**testing first functionality** 
## week2 Work
** backend design, with emotion intergration,music recomandation,story recormation.**
**collaboratively debugging some isuues**
**front end integration with backend separatively**
**current progress : 70%**

##Week 3 work 
** designing Landing page**
**understanding functionality**
**backend integration with mysqldb **
**login and sign up authentication**
**organizing folders and document**
**final deployment**
**presentation on 6 or 7 may 2024**


## Contact

**Team Member:**
- **NIYOKWIZERA JEAN D AMOUR**
  - **Role**: CEO/Developer
  - **Email**: niyokwizerajd123@gmail.com
  - **tel**: +250784422138
- **Orojo Oluwatobi Ann**
  - **Role**: Developer
  - **Email**:tobiadesiyan007@gmail.com
  - **tel**:+234 706 526 4560

---

Developed by Bro Jeid Ltd, KN 7 Ave, Kigali, Rwanda &
Annalexbaby, Nigeria

