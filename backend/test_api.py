from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def run_tests():
    with TestClient(app) as client:
        print("Testing /health endpoint...")
        response = client.get("/health")
        assert response.status_code == 200, response.text
        print(f"/health response: {response.json()}")
        
        print("\nTesting /predict with SPAM...")
        spam_data = {
            "subject": "Congratulations! You won a prize",
            "body": "Click here to claim your reward. Free entry to win!"
        }
        response = client.post("/predict", json=spam_data)
        assert response.status_code == 200, response.text
        print(f"SPAM response: {response.json()}")
        
        print("\nTesting /predict with LEGITIMATE email...")
        ham_data = {
            "subject": "Meeting agenda",
            "body": "Hi team, please find attached the agenda for tomorrow's sync. Best, John."
        }
        response = client.post("/predict", json=ham_data)
        assert response.status_code == 200, response.text
        print(f"LEGITIMATE response: {response.json()}")
        
        print("\nTesting /predict with empty input...")
        empty_data = {
            "subject": "",
            "body": "   "
        }
        response = client.post("/predict", json=empty_data)
        assert response.status_code == 422, response.text
        print(f"Empty input response: {response.json()}")

        print("\nTesting /predict with unusable text (only special chars)...")
        unusable_data = {
            "body": "--- *** ###"
        }
        response = client.post("/predict", json=unusable_data)
        assert response.status_code == 400, response.text
        print(f"Unusable text response: {response.json()}")
        
        print("\nAll tests passed successfully!")

if __name__ == "__main__":
    run_tests()
