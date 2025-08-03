from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# IBM Credentials and Config
API_KEY = "9w9yQMBhq4VwVz0T9dZAoFW9KJy2G0Mvo35843uinZbh"
PROJECT_ID = "52e6b10f-a822-4468-9911-2f37f4a33524"
MODEL_ID = "ibm/granite-3-3-8b-instruct"

# IBM Token Service
def get_access_token(api_key):
    url = "https://iam.cloud.ibm.com/identity/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = f"grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey={api_key}"
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    return response.json()["access_token"]

# API Endpoint for meal plan generation
@app.route("/mealplan", methods=["POST"])
def meal_plan():
    data = request.get_json()
    prompt = data.get("prompt", "")
    
    if not prompt:
        return jsonify({"error": "Missing prompt in request body."}), 400

    try:
        token = get_access_token(API_KEY)

        url = "https://us-south.ml.cloud.ibm.com/ml/v1/text/chat?version=2023-05-29"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        body = {
            "messages": [
                {"role": "user", "content": [{"type": "text", "text": prompt}]}
            ],
            "project_id": PROJECT_ID,
            "model_id": MODEL_ID,
            "max_tokens": 2000,
            "temperature": 0.5,
            "top_p": 1
        }

        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        return jsonify(response.json())

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the app (for local testing only)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
