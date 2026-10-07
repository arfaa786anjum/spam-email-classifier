import os
import urllib.request
import zipfile
import pandas as pd

def download_dataset():
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00228/smsspamcollection.zip"
    dataset_dir = "e:/codepro2/spam-email-classifier/ml/dataset"
    zip_path = os.path.join(dataset_dir, "smsspamcollection.zip")
    txt_path = os.path.join(dataset_dir, "SMSSpamCollection")
    csv_path = os.path.join(dataset_dir, "spam.csv")

    if not os.path.exists(csv_path):
        print("Downloading dataset...")
        urllib.request.urlretrieve(url, zip_path)
        
        print("Extracting dataset...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(dataset_dir)
            
        print("Converting to CSV...")
        df = pd.read_csv(txt_path, sep='\t', names=["label", "text"])
        df.to_csv(csv_path, index=False)
        print("Saved to CSV.")
        
        # Cleanup
        os.remove(zip_path)
        os.remove(txt_path)
        if os.path.exists(os.path.join(dataset_dir, "readme")):
            os.remove(os.path.join(dataset_dir, "readme"))
    else:
        print("Dataset already exists.")

if __name__ == "__main__":
    download_dataset()
