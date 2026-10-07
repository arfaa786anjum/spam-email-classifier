# System Workflow 🔄

This document outlines the step-by-step workflow of the SpamGuard application, from the moment a user submits an email to the moment they see the result.

## 1. User Interaction (Frontend)
1. **Input**: The user navigates to the SpamGuard web application. They type or paste text into the **Subject** and/or **Body** fields.
2. **Action**: The user clicks the **"Analyze Email"** button.
3. **State Change**: The UI immediately transitions to a **Loading** state, displaying a spinner. The "Analyze" button is disabled to prevent duplicate submissions.

## 2. API Request (Client to Server)
1. The React `api.js` service intercepts the request.
2. It constructs a JSON payload containing the `subject` and `body`.
3. It sends an HTTP `POST` request to the backend endpoint: `http://127.0.0.1:8000/predict`.

## 3. Backend Processing (FastAPI)
1. **Routing**: The FastAPI server receives the request at the `/predict` route.
2. **Validation**: Pydantic validates the request using the `PredictRequest` schema.
   - It checks data types.
   - It runs a custom validator to ensure that `subject` and `body` are not *both* empty. If they are, it instantly rejects the request with a `422 Unprocessable Entity` or `400 Bad Request`.
3. **Handoff**: The validated strings are passed to the `SpamPredictor` instance.

## 4. Machine Learning Inference (Predictor)
1. **Preprocessing**: 
   - The `preprocess_text` function combines the subject and body.
   - The text is converted to lowercase.
   - URLs are neutralized.
   - Unnecessary punctuation and noise are removed while preserving key indicators (like `$`, `!`, `?`).
   - Multiple spaces are compressed.
2. **Edge-Case Check**: If the text becomes completely empty after noise removal (e.g., if the user only entered `"---"`), a `ValueError` is raised, causing the API to return a `400 Bad Request`.
3. **Vectorization**: The cleaned text string is passed through the pre-fitted **TF-IDF Vectorizer** (loaded from memory) to convert it into a sparse numerical matrix.
4. **Prediction**: The numerical matrix is passed into the **Linear SVM Model** (loaded from memory).
5. **Confidence Scoring**: The `decision_function` of the SVM calculates the distance from the decision boundary. This value is run through a **sigmoid function** to map it smoothly to a pseudo-probability between `0.0` and `1.0`.

## 5. API Response (Server to Client)
The `SpamPredictor` constructs a dictionary containing:
- `prediction`: `"spam"` or `"not_spam"`
- `confidence`: The calculated probability (e.g., `0.9421`)
- `message`: A human-readable summary.

FastAPI serializes this dictionary into JSON via the `PredictResponse` schema and sends it back to the client with a `200 OK` status.

## 6. UI Update (Frontend)
1. **Success**: The React app receives the data.
2. **State Change**: The loading spinner disappears.
3. **Rendering**:
   - If `spam`, the Right Panel turns **Red** with a warning icon (`🚨`).
   - If `not_spam`, the Right Panel turns **Green** with a success icon (`✓`).
   - The progress bar smoothly animates to fill up to the exact percentage of the `confidence` score.
4. **Conclusion**: The user can now view the result or click "Clear" to analyze another email.
