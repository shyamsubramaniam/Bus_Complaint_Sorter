
import os
from dotenv import load_dotenv
from google import genai

# Load the API key from .env
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERROR: Gemini API key not found!")
    exit()

# Connect to Gemini
client = genai.Client(api_key=api_key)

# Test complaint
complaint = "Driver on route 7 was talking on the phone while driving."

# Ask Gemini to classify the complaint
prompt = """
You are a bus complaint classification assistant.

Classify this complaint and return JSON only.

Allowed categories:
delay, crowding, driver, vehicle, route_request, other

Rules:
1. urgent must be true only for a safety risk.
2. route must be the number mentioned in the complaint, or null.
3. Never guess a route.
4. Summary must contain 12 words or fewer.
5. Do not include people's names.

Required JSON format:
{
  "category": "driver",
  "urgent": true,
  "route": 7,
  "summary": "Route 7 driver used phone while driving"
}

Complaint:
""" + complaint

try:
    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json"
        }
    )

    print("\nGEMINI RESPONSE")
    print("----------------")
    print(response.text)

except Exception as error:
    print("Gemini API error:", error)

finally:
    client.close()
