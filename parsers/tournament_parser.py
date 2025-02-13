from utils.currency_utils import clean_currency

def safe_int(value, default=0):
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

def safe_float(value, default=0.0):
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

def safe_find_text(element, tag, default=None):
    if element is None:
        return default
    child = element.find(tag)
    return child.text if child is not None else default

def parse_tournament_data(general_element):
    if general_element is None:
        return None

    tournament_data = {
        "sessioncode": general_element.get("sessioncode", "Unknown"),
        "client_version": safe_find_text(general_element, "client_version", "Unknown"),
        "gametype": safe_find_text(general_element, "gametype", "Unknown"),
        "tablename": safe_find_text(general_element, "tablename", "Unknown"),
        "tournamentcurrency": safe_find_text(general_element, "tournamentcurrency", "Unknown"),
        "duration": safe_find_text(general_element, "duration", "Unknown"),
        "gamecount": safe_int(safe_find_text(general_element, "gamecount", "0")),
        "startdate": safe_find_text(general_element, "startdate", "Unknown"),
        "currency": safe_find_text(general_element, "currency", "Unknown"),
        "nickname": safe_find_text(general_element, "nickname", "Unknown"),
        "bets": clean_currency(safe_find_text(general_element, "bets", "0")),
        "wins": clean_currency(safe_find_text(general_element, "wins", "0")),
        "chipsin": clean_currency(safe_find_text(general_element, "chipsin", "0")),
        "chipsout": clean_currency(safe_find_text(general_element, "chipsout", "0")),
        "statuspoints": safe_find_text(general_element, "statuspoints", "Unknown"),
        "awardpoints": safe_find_text(general_element, "awardpoints", "Unknown"),
        "ipoints": safe_find_text(general_element, "ipoints", "Unknown"),
        "tablesize": safe_int(safe_find_text(general_element, "tablesize", "0")),
        "tournamentcode": safe_find_text(general_element, "tournamentcode", "Unknown"),
        "tournamentname": safe_find_text(general_element, "tournamentname", "Unknown"),
        "rewarddrawn": clean_currency(safe_find_text(general_element, "rewarddrawn", "0")),
        "place": safe_int(safe_find_text(general_element, "place", "0")),
        "buyin": safe_find_text(general_element, "buyin", "Unknown"),
        "totalbuyin": clean_currency(safe_find_text(general_element, "totalbuyin", "0")),
        "win": clean_currency(safe_find_text(general_element, "win", "0")),
    }
    return tournament_data
