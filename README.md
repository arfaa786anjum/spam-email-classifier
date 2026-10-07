# SpamGuard 🛡️

SpamGuard is a complete, beginner-friendly yet professional full-stack web application that uses Machine Learning (Natural Language Processing) to predict whether an email or SMS is SPAM or NOT SPAM (HAM).

## 🚀 Features
- **AI-Powered Analysis**: Accurately detects spam using a trained Linear SVM model.
- **Beautiful Interface**: A modern, responsive, premium UI built with React and Tailwind CSS.
- **Real-Time Feedback**: Provides immediate classification and a confidence percentage.
- **Robust Preprocessing**: Cleans URLs, special characters, and normalizes text before inference.
- **RESTful API**: Fast and fully documented backend powered by FastAPI.

## 🛠️ Technology Stack
- **Machine Learning**: Python, pandas, scikit-learn, TF-IDF, Linear SVM.
- **Backend**: FastAPI, Uvicorn, Pydantic, Joblib.
- **Frontend**: React (Vite), Tailwind CSS (v4), Lucide React.

## 🏗️ Architecture
1. **Frontend (React)**: Captures user input (Subject & Body). Sends a JSON payload via an HTTP POST request to the backend.
2. **Backend (FastAPI)**: Receives the payload, validates it using Pydantic, and passes it to the ML Predictor.
3. **ML Predictor**: Preprocesses the text (lowercasing, URL removal, noise reduction), applies the loaded TF-IDF vectorizer, and passes it through the trained Linear SVM model. It calculates a pseudo-probability using the decision function.
4. **Response**: The backend returns the classification (spam/not_spam), confidence score, and a user-friendly message back to the frontend to render the appropriate UI state.

## 📊 Dataset & ML Metrics
- **Dataset**: UCI SMS Spam Collection Dataset.
- **Class Distribution**: 86.6% Legitimate (Ham), 13.4% Spam.
- **Selected Model**: Linear SVM (Chosen over Naive Bayes for its superior F1-Score).
- **Performance**:
  - **Accuracy**: 98.65%
  - **Precision**: 98.35%
  - **Recall**: 90.84%
  - **F1-Score**: 94.44%

## 📖 API Documentation
The API provides two main endpoints:
- `GET /health`: Checks if the API is running and the ML models are loaded.
- `POST /predict`: Predicts spam probability.
  **Request Body:**
  ```json
  {
    "subject": "Optional subject string",
    "body": "Required email body string"
  }
  ```
  **Response:**
  ```json
  {
    "prediction": "spam" | "not_spam",
    "confidence": 0.0 - 1.0,
    "message": "String explanation"
  }
  ```

## 💻 Installation & Run Instructions

### 1. Python Environment & Backend
```bash
# Create and activate virtual environment
python -m venv venv
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# (Optional) Retrain models
python ml/train.py
python ml/evaluate.py

# Start Backend Server
uvicorn backend.app.main:app --reload
```
*Backend will run on http://127.0.0.1:8000. Access Swagger docs at http://127.0.0.1:8000/docs.*

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
*Frontend will typically run on http://localhost:5173.*

## 🚧 Limitations
- The model was trained heavily on SMS data, which is shorter than typical emails. For production email filtering, a large corpus of standard emails (like Enron) would yield better long-form accuracy.
- Contextual meaning and HTML-heavy email structures are lost since the vectorization is purely Bag-of-Words (TF-IDF).

## 🔮 Future Enhancements
- Switch to deep learning (e.g., fine-tuning BERT) for better semantic understanding.
- Support file uploads (.eml, .txt) directly into the UI.
- Add user feedback loops (e.g., "Report as Incorrect") to continually retrain the model.
