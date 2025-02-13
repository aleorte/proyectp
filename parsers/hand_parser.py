import xml.etree.ElementTree as ET
import os
from utils.currency_utils import clean_currency
from parsers.tournament_parser import parse_tournament_data

def safe_int(value, default=0):
    """
    Safely convert a value to an integer, returning a default value if conversion fails.
    """
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

def safe_float(value, default=0.0):
    """
    Safely convert a value to a float, returning a default value if conversion fails.
    """
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

def safe_find_text(element, tag, default=None):
    """
    Safely find and return the text of a tag, returning a default value if the tag is missing.
    """
    if element is None:
        return default
    child = element.find(tag)
    return child.text if child is not None else default

def parse_hand_history(game_element, tournamentcode):
    """
    Parse a single hand from a <game> tag and associate it with a tournament.
    """
    hand = {
        "gamecode": game_element.get("gamecode"),
        "startdate": safe_find_text(game_element.find("general"), "startdate", "Unknown"),
        "smallblind": safe_float(safe_find_text(game_element.find("general"), "smallblind", "0")),
        "bigblind": safe_float(safe_find_text(game_element.find("general"), "bigblind", "0")),
        "players": [],
        "rounds": [],
        "tournamentcode": tournamentcode  # Add tournament identifier
    }

    # Parse players
    players_element = game_element.find("general/players")
    if players_element is not None:
        for player in players_element.findall("player"):
            player_data = {
                "seat": safe_int(player.get("seat"), 0),
                "name": player.get("name", "Unknown"),
                "win": clean_currency(player.get("win", "0")),
                "bet": clean_currency(player.get("bet", "0")),
                "chips": clean_currency(player.get("chips", "0")),
                "dealer": safe_int(player.get("dealer"), 0),
                "hole_cards": []
            }
            hand["players"].append(player_data)

    # Parse rounds
    for round_element in game_element.findall("round"):
        round_data = {
            "no": safe_int(round_element.get("no"), 0),
            "cards": [],
            "actions": []
        }

        # Parse community cards
        for cards in round_element.findall("cards"):
            if cards.get("type") in ["Flop", "Turn", "River"]:
                round_data["cards"].append({
                    "type": cards.get("type"),
                    "cards": cards.text.split() if cards.text else []
                })

        # Parse player actions
        for action in round_element.findall("action"):
            round_data["actions"].append({
                "player": action.get("player", "Unknown"),
                "type": safe_int(action.get("type"), 0),
                "sum": clean_currency(action.get("sum", "0")),
                "no": safe_int(action.get("no"), 0)
            })

        hand["rounds"].append(round_data)

    # Parse hole cards
    for round_element in game_element.findall("round"):
        for cards in round_element.findall("cards"):
            if cards.get("type") == "Pocket":
                player_name = cards.get("player", "Unknown")
                for player in hand["players"]:
                    if player["name"] == player_name:
                        player["hole_cards"] = cards.text.split() if cards.text else []
                        break

    return hand

def parse_session(folder_path):
    """
    Parse all XML files in a folder and return tournament and hand data.
    """
    tournaments = []
    hand_histories = []

    for file_name in os.listdir(folder_path):
        if file_name.endswith(".xml"):
            file_path = os.path.join(folder_path, file_name)
            tree = ET.parse(file_path)
            root = tree.getroot()

            # Parse tournament data
            general_element = root.find("general")
            if general_element is not None:
                tournament_data = parse_tournament_data(general_element)
                tournaments.append(tournament_data)

                # Parse hand histories and associate them with the tournament
                for game_element in root.findall("game"):
                    hand_histories.append(parse_hand_history(game_element, tournament_data["tournamentcode"]))

    return tournaments, hand_histories