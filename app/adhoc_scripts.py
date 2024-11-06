from curl_cffi import requests
player = "isco"
url = f"https://www.futbin.org/futbin/api/searchPlayersByName?playername={player}"
request = requests.get(url, impersonate="chrome110")
fb_players_data = request.json()
fb_players = fb_players_data.get('data', [])

print(fb_players)
