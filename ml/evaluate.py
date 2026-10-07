import os
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import joblib

def evaluate_models():
    base_dir = "e:/codepro2/spam-email-classifier"
    test_data_path = os.path.join(base_dir, "ml/dataset/test_data.csv")
    model_dir = os.path.join(base_dir, "backend/models")
    
    # Load test data
    print("Loading test data...")
    test_data = pd.read_csv(test_data_path)
    X_test = test_data['text']
    y_test = test_data['label']
    
    # Load vectorizer and models
    print("Loading vectorizer and trained models...")
    vectorizer = joblib.load(os.path.join(model_dir, "tfidf_vectorizer.joblib"))
    nb_classifier = joblib.load(os.path.join(model_dir, "spam_classifier_nb.joblib"))
    svm_classifier = joblib.load(os.path.join(model_dir, "spam_classifier_svm.joblib"))
    
    # Vectorize test data
    print("Vectorizing test data...")
    X_test_vec = vectorizer.transform(X_test)
    
    def evaluate(model, name):
        y_pred = model.predict(X_test_vec)
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred)
        rec = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        cm = confusion_matrix(y_test, y_pred)
        
        print(f"\n{'='*40}")
        print(f"Model: {name}")
        print(f"{'='*40}")
        print(f"Accuracy:  {acc:.4f}")
        print(f"Precision: {prec:.4f}")
        print(f"Recall:    {rec:.4f}")
        print(f"F1-score:  {f1:.4f}")
        print(f"Confusion Matrix:\n{cm}")
        
        return f1
    
    # Evaluate models
    f1_nb = evaluate(nb_classifier, "Multinomial Naive Bayes")
    f1_svm = evaluate(svm_classifier, "Linear SVM")
    
    # Select best model based on F1-score (balance of precision and recall)
    print("\n" + "="*40)
    print("MODEL SELECTION")
    print("="*40)
    
    if f1_svm > f1_nb:
        print("Linear SVM has a higher F1-score and is selected as the best practical model.")
        best_model = svm_classifier
    else:
        print("Multinomial Naive Bayes has a higher (or equal) F1-score and is selected as the best practical model.")
        best_model = nb_classifier
        
    # Save the selected model as the final classifier
    final_model_path = os.path.join(model_dir, "spam_classifier.joblib")
    joblib.dump(best_model, final_model_path)
    
    print(f"\nFinal Selected Classifier saved to: {final_model_path}")
    print(f"TF-IDF Vectorizer saved to: {os.path.join(model_dir, 'tfidf_vectorizer.joblib')}")

if __name__ == "__main__":
    evaluate_models()
