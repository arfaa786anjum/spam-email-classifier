import os
import pandas as pd

def inspect():
    base_dir = "e:/codepro2/spam-email-classifier"
    dataset_path = os.path.join(base_dir, "ml/dataset/spam.csv")
    
    if not os.path.exists(dataset_path):
        print("Dataset not found. Please download it first.")
        return
        
    print(f"Loading dataset from: {dataset_path}")
    df = pd.read_csv(dataset_path)
    
    print("\n--- Dataset Info ---")
    print(f"Total Rows: {len(df)}")
    print(f"Columns: {list(df.columns)}")
    
    print("\n--- Missing Values ---")
    print(df.isnull().sum())
    
    print("\n--- Duplicates ---")
    print(f"Duplicate Rows: {df.duplicated(subset=['text']).sum()}")
    
    print("\n--- Class Distribution ---")
    print(df['label'].value_counts(normalize=True) * 100)
    print(df['label'].value_counts())
    
    print("\n--- Sample Data ---")
    print(df.head(3))

if __name__ == "__main__":
    inspect()
