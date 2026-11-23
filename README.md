# Bus Complaint Sorter

## 1. Project Overview
The Bus Complaint Sorter is a Python-based console application that processes student bus complaints, classifies them into categories, identifies urgent safety issues, extracts route numbers, and generates reports.

## 2. Technologies Used
- Python 3
- CSV file handling
- Google Gemini API
- JSON
- python-dotenv
- VS Code

## 3. Project Features
- Reads complaints from complaints.csv.
- Reads route information from routes.csv.
- Classifies complaints into six categories:
  - delay
  - crowding
  - driver
  - vehicle
  - route_request
  - other
- Identifies urgent safety complaints.
- Extracts explicitly mentioned route numbers.
- Generates three output reports.
- Provides an offline demonstration mode.

## 4. Project Files
- main.py – Main Python program.
- complaints.csv – Student bus complaints.
- routes.csv – Bus route information.
- .env – Stores the Gemini API key privately.
- .gitignore – Prevents sensitive files from being committed.
- results.csv – Classification results.
- urgent.csv – Urgent safety complaints.
- summary.txt – Overall complaint report.

## 5. Installation
Install the required packages:

```bash
py -m pip install google-genai python-dotenv
```

## 6. API Configuration
Create a `.env` file and add:

```text
GEMINI_API_KEY=your_api_key_here
```

Never share your actual API key.

## 7. How to Run
Open the project folder in VS Code and execute:

```bash
py main.py
```

The program reads the CSV files, processes complaints, and generates the output reports.

## 8. Offline Demonstration Mode
The project includes a rule-based offline classifier. It is used as a backup when Gemini API access is unavailable.

The offline classifier uses keyword rules to identify complaint categories, urgent safety issues, route numbers, and summaries. It is not equivalent to LLM-based classification and requires human review for ambiguous complaints.

## 9. Output Files
1. results.csv
2. urgent.csv
3. summary.txt

## 10. Human Review
Urgent safety complaints must be reviewed by a transport officer. The system supports human decision-making and does not automatically take action against drivers or transport services.

## 11. Limitations
- Offline classification is based on predefined keywords.
- Ambiguous complaints may require manual review.
- Gemini API usage depends on available quota and service availability.
- Route extraction depends on route information explicitly provided in complaints.

## 12. Conclusion
The Bus Complaint Sorter demonstrates how Python, CSV processing, and LLM integration can help organize bus complaints and identify potential safety issues.