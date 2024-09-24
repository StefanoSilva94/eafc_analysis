from curl_cffi.requests import RequestsError
from curl_cffi import requests
from .. import schemas
from typing import Union


def update_player_data_with_price(items_batch: Union[schemas.ItemCreateBatch, schemas.PlayerPickCreateBatch]):
    """
    This recieve player_dict where each element is the player data scraped from ea fc web app.
    It will iterate through each player in the dict
    It will extract their name and use the FUTBIN api to search for this player using their last name
    Multiple players can be returned, so it will check that the name, position and rating of the
    FUTBIN data matches the scraped player data.
    If it is a match it will update the scraped player data with the futbin price data.
    Otherwise, it will compare to the next player
    """

    BASE_URL = "https://www.futbin.org/futbin/api"

    # start the comparison process for each scraped player data
    for player in items_batch.items:
        last_name = player.name.split(' ')[-1]
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
            if player.position == 'GK':
                player_stats = ['rating', 'position', 'diving', 'reflexes']
            else:
                player_stats = ['rating', 'position', 'pace', 'dribbling']

                # Compare the scraped player to FUTBIN data and update if matched
                for fb_player in fb_players:
                    fb_stats = ['rating', 'position', 'pac', 'dri']
                    if player.position == 'GK':
                        fb_stats = ['rating', 'position', 'diving', 'reflexes']

                    if all(getattr(player, stat1) == fb_player.get(stat2) for stat1, stat2 in
                           zip(player_stats, fb_stats)):
                        # Update the player with FUTBIN data
                        player.base_id = fb_player.get('playerid')
                        player.resource_id = fb_player.get('resource_id')
                        player.league = fb_player.get('league')
                        player.nation = fb_player.get('nation')
                        player.raretype = fb_player.get('raretype')
                        player.rare = fb_player.get('rare')
                        if fb_player.get('ps_LCPrice') == 0:
                            player.price = fb_player.get('ps_LCPrice')
                        else:
                            # If price is 0 then the player should be extinct and sell for max price
                            player.price = fb_player.get('ps_MaxPrice')
                        break  # Stop checking once a match is found

    return items_batch
