import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
import joblib
from preprocessing import preprocess_text

def train_models():
    base_dir = "e:/codepro2/spam-email-classifier"
    dataset_path = os.path.join(base_dir, "ml/dataset/spam.csv")
    model_dir = os.path.join(base_dir, "backend/models")
    
    # 1. Load the dataset
    print("Loading dataset...")
    df = pd.read_csv(dataset_path)
    
    # 2. Handle missing values
    print("Handling missing values...")
    df = df.dropna(subset=['text', 'label'])
    
    # 3. Remove duplicates
    print(f"Removing duplicates... (Original shape: {df.shape})")
    df = df.drop_duplicates(subset=['text'])
    print(f"Shape after removing duplicates: {df.shape}")
    
    # 4. Normalize labels (spam -> 1, ham -> 0)
    print("Normalizing labels...")
    df['label_num'] = df['label'].map({'ham': 0, 'spam': 1})
    
    # 5. Preprocess text
    # In this dataset, there is no separate 'subject' column, so we just use the body.
    print("Preprocessing text...")
    df['clean_text'] = df['text'].apply(lambda x: preprocess_text(body=x))
    
    # Drop rows that became empty after cleaning
    df = df[df['clean_text'].str.strip() != '']
    print(f"Final shape for training: {df.shape}")
    
    # 6. Split into train/test sets
    print("Splitting into train/test sets...")
    X = df['clean_text']
    y = df['label_num']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # 7. Apply TF-IDF Vectorization
    print("Applying TF-IDF vectorization...")
    vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    
    # 8. Train Multinomial Naive Bayes
    print("Training Multinomial Naive Bayes classifier...")
    nb_classifier = MultinomialNB()
    nb_classifier.fit(X_train_vec, y_train)
    
    # 9. Optionally train Linear SVM
    print("Training Linear SVM classifier...")
    svm_classifier = LinearSVC(random_state=42, dual='auto')
    svm_classifier.fit(X_train_vec, y_train)
    
    # 10. Save the models and vectorizer for evaluate script
    print("Saving vectorizer and models...")
    os.makedirs(model_dir, exist_ok=True)
    joblib.dump(vectorizer, os.path.join(model_dir, "tfidf_vectorizer.joblib"))
    joblib.dump(nb_classifier, os.path.join(model_dir, "spam_classifier_nb.joblib"))
    joblib.dump(svm_classifier, os.path.join(model_dir, "spam_classifier_svm.joblib"))
    
    # Save test set for evaluate.py
    test_data = pd.DataFrame({'text': X_test, 'label': y_test})
    test_data.to_csv(os.path.join(base_dir, "ml/dataset/test_data.csv"), index=False)
    
    print("Training phase complete. Run evaluate.py to calculate metrics and select the best model.")

if __name__ == "__main__":
    train_models()
