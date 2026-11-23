
import csv
import os
import json
import time

from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Select project mode
USE_GEMINI = False
client = None

# Get Gemini API key
api_key = os.getenv("GEMINI_API_KEY")

# Connect to Gemini
if not api_key:
    raise ValueError("Gemini API key not found in .env file!")

client = genai.Client(api_key=api_key)


# Offline demonstration classifier
def classify_offline(complaint):

    import re

    text = complaint.lower()

    category = "other"
    urgent = False
    route = None

    # Extract only explicitly mentioned route numbers
    match = re.search(r"\broute\s+(\d+)\b", text)

    if match:
        route = int(match.group(1))

    # Identify safety risks
    safety_words = [
        "phone while driving",
        "footboard",
        "rashly",
        "rash driving",
        "high speed",
        "smoke",
        "burning smell",
        "does not close properly",
        "damaged and unsafe"
    ]

    if any(word in text for word in safety_words):
        urgent = True

    
    # Identify complaint category

    if any(word in text for word in [
        "add a stop",
        "provide a bus stop", "bus stop",
        "missed our usual stop", "missed the stop",
        "usual stop", "railway station"
    ]):
        category = "route_request"

    elif any(word in text for word in [
        "crowded", "crowding", "overcrowded",
        "no space", "cannot get seats", "cannot get a seat"
    ]):
        category = "crowding"

    elif any(word in text for word in [
        "late", "delay", "waiting", "on time",
        "did not arrive"
    ]):
        category = "delay"

    elif any(word in text for word in ["driver", "driving"]):
        category = "driver"

    elif any(word in text for word in [
        "tyre", "engine", "door", "brake",
        "smoke", "window", "air conditioning", " ac "
    ]):
        category = "vehicle"


    # Generate meaningful summaries
    if "phone while driving" in text:
        summary = "Driver used a phone while driving"

    elif "footboard" in text:
        summary = "Students standing on the footboard due to overcrowding"

    elif "rashly" in text or "high speed" in text:
        summary = "Driver was driving at an unsafe speed"

    elif "smoke" in text or "burning smell" in text:
        summary = "Smoke and burning smell reported inside the bus"

    elif "door" in text:
        summary = "Front bus door does not close properly"

    elif "tyre" in text:
        summary = "Bus tyre appears damaged and unsafe"

    elif "window" in text:
        summary = "Broken bus window allows rainwater inside"

    elif "air conditioning" in text or " ac " in text:
        summary = "Bus air conditioning is not working"

    elif any(word in text for word in ["late", "delay", "on time", "did not arrive"]):
        summary = "Bus arrived late at the scheduled pickup point"

    elif "crowd" in text or "seats" in text:
        summary = "Bus overcrowding and insufficient seating reported"

    elif "stop" in text:
        summary = "Passenger reports a bus stop or route issue"

    elif len(text.split()) <= 3:
        summary = "Vague complaint; more details required"

    else:
        summary = "Complaint requires further review"

    return {
        "category": category,
        "urgent": urgent,
        "route": route,
        "summary": summary
    }
   

# Function 3: Classify complaints using Gemini
def classify(complaint):

    prompt = f"""
    You are a bus complaint classification assistant.

    Classify the complaint and return JSON only.

    Allowed categories:
    delay, crowding, driver, vehicle, route_request, other

    Rules:
    1. urgent must be true only for a safety risk.
    2. route must be the number mentioned in the complaint, or null.
    3. Never guess a route.
    4. Summary must contain 12 words or fewer.
    5. Do not include people's names.

    Required JSON format:
    {{
        "category": "driver",
        "urgent": true,
        "route": 7,
        "summary": "Route 7 driver used phone while driving"
    }}

    Complaint: {complaint}
    """

    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt,
            config={
                "response_mime_type": "application/json"
            }
        )

        result = json.loads(response.text)

        return result

    except Exception as error:
        print("Gemini classification error:", error)
        return None
    
    # Function 4: Validate Gemini response
def is_valid(result):

    if not isinstance(result, dict):
        return False

    required_keys = ["category", "urgent", "route", "summary"]

    for key in required_keys:
        if key not in result:
            return False

    allowed_categories = [
        "delay",
        "crowding",
        "driver",
        "vehicle",
        "route_request",
        "other"
    ]

    if result["category"] not in allowed_categories:
        return False

    if not isinstance(result["urgent"], bool):
        return False

    if result["route"] is not None:
        if type(result["route"]) is not int:
            return False

    if not isinstance(result["summary"], str):
        return False

    if len(result["summary"].split()) > 12:
        return False

    return True

# Function 5: Check route validity
def check_route(result, complaint, routes):

    route = result["route"]

    if route is None:
        return result

    # Check whether the route exists in routes.csv
    if route not in routes:
        result["route"] = None
        return result

    # Check whether the route number appears in the complaint
    if str(route) not in complaint:
        result["route"] = None

    return result

# Function 1: Load complaints
def load_complaints():
    complaints = []

    with open("complaints.csv", "r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        for row in reader:
            complaints.append(row)

    return complaints


# Function 2: Load routes
def load_routes():
    routes = {}

    with open("routes.csv", "r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        reader.fieldnames = [name.strip() for name in reader.fieldnames]

        for row in reader:
            route_number = int(row["route"].strip())
            area_name = row["area"].strip()
            routes[route_number] = area_name

    return routes

# Function 6: Process all complaints
def process_complaints(complaints, routes):

    results = []

    for complaint_data in complaints:

        complaint_text = complaint_data["complaint"]

        print("\nProcessing complaint:", complaint_data["id"])

        # Select classification method
        if USE_GEMINI:

            print("Using Gemini AI...")
            result = classify(complaint_text)

            if not is_valid(result):
                print("Invalid response. Retrying...")
                time.sleep(10)
                result = classify(complaint_text)

        else:

            print("Using offline demonstration mode...")
            result = classify_offline(complaint_text)

        # Manual review if response is invalid
        if not is_valid(result):

            print("Needs manual review!")

            result = {
                "category": "needs_manual_review",
                "urgent": False,
                "route": None,
                "summary": "Manual review required"
            }

        else:
            result = check_route(result, complaint_text, routes)

        # Store result
        results.append({
            "id": complaint_data["id"],
            "date": complaint_data["date"],
            "complaint": complaint_text,
            "category": result["category"],
            "urgent": result["urgent"],
            "route": result["route"],
            "summary": result["summary"]
        })

    return results

# Function 7: Write results to CSV

def write_results(results):

    with open("results.csv", "w", newline="", encoding="utf-8") as file:

        fieldnames = [
            "id",
            "category",
            "urgent",
            "route",
            "summary"
        ]

        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

        for result in results:
            writer.writerow({
                "id": result["id"],
                "category": result["category"],
                "urgent": result["urgent"],
                "route": result["route"],
                "summary": result["summary"]
            })

    print("\nresults.csv created successfully!")

    # Function 8: Write urgent complaints
def write_urgent(results, routes):

    with open("urgent.csv", "w", newline="", encoding="utf-8") as file:

        fieldnames = [
            "id",
            "date",
            "route",
            "area",
            "original_complaint",
            "summary"
        ]

        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

        for result in results:

            if result["urgent"] is True:

                route = result["route"]

                area = routes.get(route, "Unknown") if route is not None else "Unknown"

                writer.writerow({
                    "id": result["id"],
                    "date": result["date"],
                    "route": route,
                    "area": area,
                    "original_complaint": result["complaint"],
                    "summary": result["summary"]
                })

    print("urgent.csv created successfully!")

    # Function 9: Generate summary report
def write_summary(results, routes):

    category_counts = {}
    route_counts = {}

    urgent_complaints = []

    for result in results:

        # Count categories
        category = result["category"]

        category_counts[category] = category_counts.get(category, 0) + 1

        # Count routes
        route = result["route"]

        if route is not None:
            route_counts[route] = route_counts.get(route, 0) + 1

        # Collect urgent complaints
        if result["urgent"] is True:
            urgent_complaints.append(result)

    with open("summary.txt", "w", encoding="utf-8") as file:

        file.write("BUS COMPLAINT SORTER REPORT\n")
        file.write("===========================\n\n")

        file.write("CATEGORY COUNTS\n")
        file.write("----------------\n")

        for category, count in category_counts.items():
            file.write(f"{category}: {count}\n")

        file.write("\nROUTE-WISE COMPLAINT COUNTS\n")
        file.write("---------------------------\n")

        sorted_routes = sorted(
            route_counts.items(),
            key=lambda item: item[1],
            reverse=True
        )

        for route, count in sorted_routes:
            area = routes.get(route, "Unknown")
            file.write(f"Route {route} - {area}: {count}\n")

        file.write("\nURGENT SAFETY COMPLAINTS\n")
        file.write("------------------------\n")

        for result in urgent_complaints:
            file.write(
                f"{result['id']}: {result['summary']}\n"
            )

    print("summary.txt created successfully!")

# Main program
def main():

    try:
        complaints = load_complaints()
        routes = load_routes()

        print("\nBUS COMPLAINT SORTER")
        print("--------------------")

        print("Total complaints:", len(complaints))
        print("Total routes:", len(routes))

        print("\nCSV FILES LOADED SUCCESSFULLY!")

        print("\nStarting complaint classification...")

        results = process_complaints(complaints, routes)
        write_results(results)
        write_urgent(results, routes)
        write_summary(results, routes)

        print("\nALL TASKS COMPLETED SUCCESSFULLY!")
        print("Check results.csv, urgent.csv and summary.txt")

    except FileNotFoundError as error:
        print("CSV file not found:", error)

    except Exception as error:
        print("Program error:", error)


# Start the program only once
if __name__ == "__main__":
    main()