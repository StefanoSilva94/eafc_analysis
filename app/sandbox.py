from curl_cffi.requests import RequestsError
from curl_cffi import requests

BASE_URL = "https://www.futbin.org/futbin/api"


def update_player_data_with_price(player_dict):
    """
    This recieve player_dict where each element is the player data scraped from ea fc web app.
    It will iterate through each player in the dict
    It will extract their name and use the FUTBIN api to search for this player using their last name
    Multiple players can be returned, so it will check that the name, position and rating of the
    FUTBIN data matches the scraped player data.
    If it is a match it will update the scraped player data with the futbin price data.
    Otherwise, it will compare to the next player
    """
    # start the comparison process for each scraped player data
    for player in player_dict.values():
        last_name = player['name'].split(' ')[-1]
        url = f"{BASE_URL}/searchPlayersByName?playername={last_name}"
        try:
            request = requests.get(url, impersonate="chrome110")
        except RequestsError as e:
            print(f"Error fetching data for {last_name}: {e}")
            continue

        try:
            # save futbin players data
            fb_players_data = request.json()
            fb_players = fb_players_data.get('data', [])
            if not fb_players:
                print(f"No FUTBIN data found for {last_name}")
                continue
        except ValueError:
            print(f"Invalid JSON response for {last_name}")
            continue

        # now compare the scraped player data to each fb_player until a match is found
        for fb_player in fb_players:
            # Now compare the player stats with stats in the player_dict
            # futbin uses outfield stat names for gk as well so ok to use 'pac' and 'dri'
            fb_stats = ['rating', 'position', 'pac', 'dri']
            if player['position'] == 'GK':
                player_stats = ['rating', 'position', 'diving', 'reflexes']
            else:
                player_stats = ['rating', 'position', 'pace', 'dribbling']

            # If all the stats are the same then we have a match
            if all(player[stat1] == fb_player[stat2] for stat1, stat2 in zip(player_stats, fb_stats)):
                # When there is a match, save the extra column values
                player.update({
                    'base_id': fb_player.get('playerid'),
                    'resource_id': fb_player.get('resource_id'),
                    'league': fb_player.get('league'),
                    'nation': fb_player.get('nation'),
                    'raretype': fb_player.get('raretype'),
                    'rare': fb_player.get('rare'),
                    'price': fb_player.get('ps_LCPrice')
                })
                print(player['price'])
                break

    return player_dict




data = {
    0: {"name": 'Asun Martínez', "rating": '74', "position": 'RW', "is_tradeable": False, "pace": '84', "dribbling": '75'},
    1: {"name": 'Maikuma', 'rating': '70', 'position': 'RB', 'is_tradeable': True, "pace": '74', "dribbling": '67'}
}

new_data = update_player_data_with_price(data)
print(type(new_data[0]['price']))
