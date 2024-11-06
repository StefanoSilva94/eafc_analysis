from curl_cffi import requests

player = "isco"
url = f"https://www.futbin.org/futbin/api/searchPlayersByName?playername={player}"
request = requests.get(url, impersonate="chrome110")

# Check the status code and response content
print("Status code:", request.status_code)
print("Response content:", request.content)  # Print raw content to see if it's empty or non-JSON

# Parse JSON if the status code is 200 and content is not empty
if request.status_code == 200 and request.content:
    try:
        fb_players_data = request.json()
        fb_players = fb_players_data.get('data', [])
        print(fb_players)
    except requests.JSONDecodeError as e:
        print("JSON decoding error:", e)
else:
    print("Failed to retrieve data or empty response")
