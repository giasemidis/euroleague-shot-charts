import requests
import pandas as pd


MADE_ACTIONS = ['2FGM', '3FGM', 'LAYUPMD', 'DUNK']
MISSES_ACTIONS = ['2FGA', '2FGAB', '3FGA', '3FGAB', 'LAYUPATT']


def get_game_shot_data(gamecode, season):
    """
    Get the shot data of a single game in the season
    """
    url = (
        f"https://live.euroleague.net/api/Points?gamecode={gamecode}"
        f"&seasoncode=E{season}"
    )
    r = requests.get(url)

    if r.status_code != 200:
        print("something went wrong while fetching the data")

    if r.text == '':
        shots_df = None
        print(
            f"No available data found for game-code {gamecode} and season "
            f"{season}"
        )
    else:
        data = r.json()
        shots_df = pd.DataFrame(data['Rows'])
        # team id, player id and action id contain trailing white space
        shots_df['TEAM'] = shots_df['TEAM'].str.strip()
        shots_df['ID_PLAYER'] = shots_df['ID_PLAYER'].str.strip()
        shots_df['ID_ACTION'] = shots_df['ID_ACTION'].str.strip()
        shots_df.insert(0, 'Season', season)
        shots_df.insert(1, 'Gamecode', gamecode)
    return shots_df


def get_season_shot_data(season=2021):
    """
    Get the shot data of all games in a season
    """
    data_list = []
    gamecode = 0
    while True:
        gamecode += 1
        shots_df = get_game_shot_data(gamecode, season)

        if shots_df is None:
            print("No more available game data for this season, beak and exit")
            break

        data_list.append(shots_df)

    data_df = None
    if data_list:
        data_df = pd.concat(data_list, axis=0)
    return data_df


def get_player_shot_data(data, name, season=None):
    '''
    Get a player's shot data from the dataset.
    '''
    name = name.upper()
    if season is not None:
        data = data[data['Season'] == season]
    player_data = data[data['PLAYER'].str.startswith(name)]
    made_df = player_data[
        player_data['ID_ACTION'].isin(MADE_ACTIONS)
    ].reset_index()
    missed_df = player_data[
        player_data['ID_ACTION'].isin(MISSES_ACTIONS)
    ].reset_index()
    total_df = player_data[player_data['ID_ACTION'] != 'FTM'].reset_index()
    return made_df, missed_df, total_df
