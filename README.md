# FormForge 

**Your AI-Powered Form Builder** : A real-time fitness coaching app that watches your form through your webcam and gives you live, spoken feedback, like having a personal trainer right in the room.

## What it does

FormForge uses computer vision to track your body movements during a workout and tells you, in real time, whether your form is correct. Pick an exercise, set your goals, and start your session — the app analyzes your posture frame by frame, tracks your reps and sets, and an AI voice coach checks in on you as you go.

It currently supports:
- Squats
- Push-ups
- Bicep Curls (Dumbbells)
- Shoulder Press
- Lunges

Each exercise has its own set of form checks. for example, knee and back angle for squats, or elbow angle and swing detection for bicep curls, so the feedback is actually relevant to what you're doing.

## How it works

1. **Plan your workout** — choose an exercise, number of sets, and reps in the sidebar.
2. **Start the session** — your webcam turns on, and a pose-detection model starts tracking your joints in real time.
3. **Get live feedback** — as you move, the app calculates angles and posture metrics and flags issues with your form.
4. **Hear from your coach** — an AI voice coach (powered by Groq's LLM) gives you spoken feedback at key moments, like starting or finishing a workout.
5. **Track your progress** — every session is saved, and your workout history is summarized in a table so you can see your progress over time.

## Tech Stack

- **Frontend/App Framework:** Streamlit
- **Real-time Video:** streamlit-webrtc
- **Computer Vision / Pose Estimation:** OpenCV + ML pose landmark model
- **AI Coaching:** Groq LLM API
- **Voice Feedback:** Text-to-Speech pipeline
- **Data Handling:** Pandas
- **Persistence:** SQLite
- **Styling:** Custom CSS + custom fonts

## Project Structure

```
FormForge/
├── core/              # Base exercise logic
├── detectors/         # Per-exercise pose/form detectors
├── ml_models/         # Pose landmark model
├── services/
│   ├── auth/          # Login wall
│   ├── coaching/      # LLM + TTS + voice pipeline
│   ├── config/        # Exercise options & config
│   ├── persistence/   # Database access
│   ├── state/         # Session state defaults
│   ├── tracking/       # Metrics sync
│   └── vision/         # Video processing
├── static/            # CSS & fonts
├── main.py            # App entry point
└── requirements.txt
```

## Getting Started

### Prerequisites
- Python 3.9+
- A Groq API key (for AI voice coaching)

### Installation

```bash
git clone https://github.com/Famous077/FormForge.git
cd FormForge
pip install -r requirements.txt
```

### Set up your environment

Create a `.env` file in the project root and add:

```
GROQ_API_KEY=your_api_key_here
```

### Run the app

```bash
streamlit run main.py
```

Then open the local URL Streamlit gives you, log in, set up your workout plan, and start training.

## Why I built this

I wanted to combine my interest in computer vision and AI to build something genuinely useful — a tool that gives people the kind of real-time form correction you'd normally only get from a personal trainer, but accessible from a laptop webcam. It's an ongoing project, and there's plenty more I plan to add — more exercises, better feedback, and a more personalized coaching experience.

## License

This project is open for learning and personal use. Feel free to explore the code and adapt it for your own projects.
