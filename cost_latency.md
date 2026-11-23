# Cost and Latency Note

## API Cost
The project uses the Google Gemini API for AI-based complaint classification when API access is enabled.

API usage may depend on the selected model, number of complaints, and current pricing or free-tier limits.

The project also provides an offline rule-based mode to demonstrate complaint processing when API access is unavailable.

## Latency
Each Gemini API request takes time to process. Processing many complaints may increase the total execution time.

Offline classification is generally faster because it uses local keyword rules and does not require an internet connection.

## Limitations
- API quota limits may prevent some requests.
- Network problems may affect response time.
- Offline classification may not understand every complaint correctly.
- Results should be checked by a human transport officer.