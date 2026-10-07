# SpamGuard Project TODO

## Phase 1: Project Setup and Dataset
- [x] Create the complete project folder structure
- [x] Set up Python virtual environment
- [x] Create requirements.txt
- [x] Set up React + Vite frontend
- [x] Install required frontend dependencies
- [x] Add .gitignore
- [x] Find/use a suitable public labeled spam/ham dataset
- [x] Place the dataset inside ml/dataset/
- [x] Inspect the dataset
- [x] Identify text column, label column
- [x] Check missing values, duplicates, class distribution
- [x] Create a small dataset inspection script
- [x] Create initial README
- [x] Create TODO.md
- [x] Verify Python environment
- [x] Verify frontend starts
- [x] Verify dataset can be loaded and statistics

## Phase 2: Machine Learning Pipeline
- [x] Create NLP preprocessing pipeline
- [x] Apply TF-IDF Vectorization
- [x] Train Multinomial Naive Bayes classifier
- [x] Evaluate model
- [x] Save trained model and vectorizer

## Phase 3: Backend API
- [x] Set up FastAPI project structure
- [x] Create `/health` and `/predict` endpoints
- [x] Load trained model and vectorizer
- [x] Implement prediction logic and error handling

## Phase 4: Frontend UI
- [x] Design main screen layout with two panels
- [x] Implement Left Panel (Input fields and buttons)
- [x] Implement Right Panel (Results, loading state)
- [x] Connect Frontend to Backend

## Phase 5: Final Validation and Documentation
- [x] Test with spam/legitimate examples
- [x] Update README with architecture and usage
- [x] Final polish
