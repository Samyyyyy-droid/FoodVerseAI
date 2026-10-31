# Food Verse AI 🍃

### Multimodal AI-Powered Food Intelligence Platform

Food Verse AI is an AI-powered food intelligence platform designed to make food-related decisions smarter and easier. It combines computer vision, image analysis, and Large Language Models (LLMs) to provide food recognition, nutritional insights, freshness assessment, restaurant hygiene monitoring, recipe generation, and personalized meal planning.

## 🚀 Features

### 1. Food Recognition & Nutrition Analysis
- Recognizes food items from uploaded images.
- Identifies food categories and serving sizes.
- Estimates calories, protein, carbohydrates, fats, fiber, and sugar.
- Generates health scores and nutritional recommendations.

### 2. Food Freshness Detection
- Processes food images using OpenCV.
- Extracts image features such as brightness, saturation, and edge density.
- Provides preliminary freshness assessments.
- Generates food safety recommendations.

### 3. Restaurant Hygiene Monitoring
- Analyzes kitchen images using AI.
- Identifies visible hygiene concerns.
- Evaluates visible food-handling practices.
- Provides hygiene observations and improvement recommendations.

### 4. Smart Kitchen & Recipe Generation
- Generates recipes from ingredients or dish names.
- Provides ingredient quantities and cooking instructions.
- Suggests cooking tips and nutritional information.

### 5. Personalized Meal Planner
- Generates personalized meal plans based on user profiles.
- Considers age, dietary preferences, fitness goals, and activity levels.
- Supports calorie targets and meal frequency.
- Provides estimated nutritional summaries.

## 🛠️ Technology Stack

| Component | Technologies |
|---|---|
| Frontend | React.js, Vite, CSS |
| Backend | Python, FastAPI |
| AI Integration | Groq API, Qwen Model |
| Image Processing | OpenCV, Pillow, NumPy |
| API Communication | Axios, REST API |
| Data Validation | Pydantic |
| Development Tools | VS Code, Git, GitHub |

## 📁 Project Structure

```text
FoodVerseAI/
│
├── backend/
│   ├── routers/
│   │   ├── food_recognition.py
│   │   ├── freshness_detector.py
│   │   ├── hygiene_monitor.py
│   │   ├── kitchen_assistant.py
│   │   └── meal_planner.py
│   │
│   ├── services/
│   │   ├── food_ai.py
│   │   ├── freshness_ai.py
│   │   ├── freshness_classifier.py
│   │   ├── hygiene_ai.py
│   │   ├── hygiene_classifier.py
│   │   ├── recipe_ai.py
│   │   └── meal_planner.py
│   │
│   ├── requirements.txt
│   ├── main.py
│   └── .env
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   ├── package.json
│   └── index.html
│
├── .gitignore
└── README.md
```

*The structure above shows the main application files; additional test and configuration files may also be present.*

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.9 or higher
- Node.js and npm
- Git
- Groq API key

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd FoodVerseAI
```

### 2. Backend Setup

```bash
cd backend

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file inside the `backend` directory:

```env
GROQ_API_KEY=your_groq_api_key
```

Replace `your_groq_api_key` with your actual Groq API key.

**Important:** Never upload your `.env` file or expose your API key publicly.

### 4. Start the Backend

From the `backend` directory:

```bash
uvicorn main:app --reload
```

Backend URL:

`http://127.0.0.1:8000`

Interactive API documentation:

`http://127.0.0.1:8000/docs`

### 5. Frontend Setup

Open another terminal:

```bash
cd frontend

npm install
npm install axios lucide-react react-router-dom

npm run dev
```

Frontend URL:

`http://localhost:5173`

## 🔗 API Endpoints

| Module | Method | Endpoint |
|---|---|---|
| Food Recognition | POST | `/api/food-recognition/analyze` |
| Freshness Detection | POST | `/api/freshness/analyze` |
| Hygiene Monitoring | POST | `/api/hygiene/analyze` |
| Recipe Generation | POST | `/api/kitchen/recipe` |
| Meal Planner | POST | `/api/meal-planner/generate` |
| Health Check | GET | `/health` |

## 🧪 Testing

The application can be tested through:

- FastAPI Swagger UI (`/docs`)
- Frontend dashboard
- Image uploads for food, freshness, and hygiene analysis
- Recipe generation using ingredients
- Personalized meal plan generation using user profiles

## 🔮 Future Enhancements

- Real-time food recognition through camera input.
- Video-based restaurant hygiene monitoring.
- Improved freshness classification using trained machine learning models.
- Voice-assisted cooking instructions.
- User authentication and profile management.
- Meal history and nutritional tracking.
- Cloud deployment and database integration.

## ⚠️ Disclaimer

Food recognition, nutritional values, freshness assessments, and hygiene observations are AI-generated estimates. They should not be treated as scientifically verified food-safety inspections, medical advice, or laboratory results.

## 👨‍💻 Project

**Food Verse AI — Multimodal AI-Powered Food Intelligence Platform**

Developed as part of the SmartBridge SkillWallet project.