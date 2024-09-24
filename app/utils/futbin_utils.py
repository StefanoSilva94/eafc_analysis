from curl_cffi.requests import RequestsError
from curl_cffi import requests
from .. import schemas
from typing import Union
import pandas as pd

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
        # star from the last fb_player for cases where the player has moved club
        for fb_player in fb_players[::-1]:
            # Now compare the player stats with stats in the player_dict
            # futbin uses outfield stat names for gk as well so ok to use 'pac' and 'dri'
            fb_stats = ['rating', 'position', 'pac', 'dri']
            if player.position == 'GK':
                player_stats = ['rating', 'position', 'diving', 'reflexes']
            else:
                player_stats = ['rating', 'position', 'pace', 'dribbling']

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
                    player.price = fb_player.get('ps_MaxPrice')
                else:
                    # If price is 0 then the player should be extinct and sell for max price
                    player.price = fb_player.get('ps_LCPrice')
                break  # Stop checking once a match is found

    return items_batch


def adhoc_update_from_csv():
    """
    If any rows are missing a price, then this script cn be run to update them
    It requires a csv to be downloaded containing the incomplete data and save to the root directory and called
    'data.csv'.
    It will construct a query that can be used to update the missing values
    """
    BASE_URL = "https://www.futbin.org/futbin/api"

    df = pd.read_csv('../data.csv')

    # Create SQL queries
    query_start = 'UPDATE packed_items SET price = CASE \n '
    query_middle = ''
    query_end = '\n END WHERE id IN ('

    # Iterate through each row in the DataFrame
    for index, row in df.iterrows():
        id_value = row['id']
        name_value = row['name']
        rating = row['rating']
        position = row['position']

        last_name = name_value.split(' ')[-1]
        url = f"{BASE_URL}/searchPlayersByName?playername={last_name}"
        if int(id_value) == 99:
            pass
        try:
            request = requests.get(url, impersonate="chrome110")
            fb_players_data = request.json()
            fb_players = fb_players_data.get('data', [])
            if not fb_players:
                print(f"No FUTBIN data found for {last_name}")
                continue

            for fb_player in fb_players[::-1]:
                # Now compare the player stats with stats in the player_dict
                # futbin uses outfield stat names for gk as well so ok to use 'pac' and 'dri'
                fb_stats = ['rating', 'position']

                # If all the stats are the same then we have a match
                fb_rating = fb_player['rating']
                fb_pos = fb_player['position']
                if str(rating) == fb_rating and position == fb_pos:
                    # When there is a match, save the extra column values
                    price = fb_player.get('ps_LCPrice')
                    query_middle += f"WHEN id = {id_value} THEN {price} \n"
                    query_end += f"{id_value}, "
                    continue

        except RequestsError as e:
            print(f"Error fetching data for {last_name}: {e}")
            continue

    query_end += '100000)'
    query = query_start + query_middle + query_end

    print(query)
    return query
