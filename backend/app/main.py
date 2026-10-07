from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from .schemas import PredictRequest, PredictResponse
from .predictor import SpamPredictor

app = FastAPI(title="SpamGuard API", description="API for Spam Email Classifier")

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

predictor = None

@app.on_event("startup")
def startup_event():
    global predictor
    try:
        predictor = SpamPredictor()
        print("SpamPredictor loaded successfully.")
    except Exception as e:
        print(f"Error loading model: {e}")

@app.get("/health")
def health_check():
    if predictor is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Model not loaded. Please train models first.")
    return {"status": "ok", "message": "SpamGuard API is running and model is loaded."}

@app.post("/predict", response_model=PredictResponse)
def predict_spam(request: PredictRequest):
    if predictor is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Model not loaded.")
        
    try:
        result = predictor.predict(body=request.body, subject=request.subject)
        return PredictResponse(**result)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred during prediction: {str(e)}")
