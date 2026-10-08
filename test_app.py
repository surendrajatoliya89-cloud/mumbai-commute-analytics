"""
test_app.py
-----------
Automated test suite verifying that all Flask routes render without error.
"""

from app import app

def test_routes():
    client = app.test_client()
    routes = [
        ("/", 200),
        ("/dashboard", 200),
        ("/comparison", 200),
        ("/data", 200),
        ("/analytics", 200),
        ("/prediction", 200),
        ("/about", 200),
        ("/api/summary", 200)
    ]

    all_passed = True
    print("Testing Flask Web Routes:")
    for route, expected_code in routes:
        resp = client.get(route)
        if resp.status_code == expected_code:
            print(f"  [PASS] {route} -> Status {resp.status_code}")
        else:
            print(f"  [FAIL] {route} -> Expected {expected_code}, got {resp.status_code}")
            all_passed = False

    # Test Prediction POST
    post_data = {
        "distance": "14.0",
        "travel_time": "30",
        "waiting_time": "4",
        "cost": "35",
        "peak_hour": "No",
        "crowd_level": "Medium",
        "weather": "Clear",
        "delay": "1",
        "comfort": "4"
    }
    resp_post = client.post("/prediction", data=post_data)
    if resp_post.status_code == 200 and b"Predicted by Decision Tree" in resp_post.data:
        print("  [PASS] POST /prediction -> Successful inference and response rendered!")
    else:
        print(f"  [FAIL] POST /prediction -> Status {resp_post.status_code}")
        all_passed = False

    if all_passed:
        print("\nALL FLASK APPLICATION TESTS PASSED PERFECTLY!")
    else:
        print("\nSOME TESTS FAILED.")

if __name__ == "__main__":
    test_routes()

