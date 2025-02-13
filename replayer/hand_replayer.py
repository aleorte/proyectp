import streamlit as st
import os

# Ruta de la carpeta donde están las imágenes de las cartas
CARDS_FOLDER = "./cards"

def display_hand(hand):
    """
    Display a single hand in a user-friendly format.
    """
    st.write(f"### Start Date: {hand['startdate']}")
    st.write(f"Small Blind: {hand['smallblind']}, Big Blind: {hand['bigblind']}")

    # Mostrar las cartas del jugador en lugar del Hand ID
    st.write("#### Your Cards:")
    player_hole_cards = get_player_hole_cards(hand)
    if player_hole_cards:
        show_card_images(player_hole_cards)
    else:
        st.write("No hole cards available.")

    # Mostrar jugadores y sus cartas
    st.write("#### Players")
    for player in hand["players"]:
        hole_cards = player["hole_cards"]
        st.write(f"{player['name']} (Seat {player['seat']}):")
        if hole_cards:
            show_card_images(hole_cards)
        else:
            st.write("Cards not available")

    # Mostrar las rondas y sus cartas comunitarias
    st.write("#### Rounds")
    for round_data in hand["rounds"]:
        st.write(f"--- Round {round_data['no']} ---")

        # Mostrar cartas comunitarias
        for cards in round_data["cards"]:
            if cards["type"] in ["Flop", "Turn", "River"]:
                st.write(f"{cards['type']}:")
                show_card_images(cards["cards"])

        # Mostrar acciones de los jugadores
        for action in round_data["actions"]:
            st.write(f"Player {action['player']}: Action {action['type']}, Sum {action['sum']}")

def get_player_hole_cards(hand):
    """
    Obtener las cartas del jugador principal en la mano.
    """
    for player in hand["players"]:
        if player.get("is_hero", False):  # Suponiendo que haya una marca para identificar al jugador principal
            return player["hole_cards"]
    return None

def show_card_images(cards):
    """
    Muestra imágenes de las cartas en la interfaz de Streamlit.
    """
    card_images = []
    for card in cards:
        card_path = get_card_image_path(card)
        if os.path.exists(card_path):
            card_images.append(card_path)
        else:
            st.write(f"Card image not found: {card}")

    if card_images:
        st.image(card_images, width=100)  # Ajusta el tamaño según sea necesario

def get_card_image_path(card):
    """
    Construye la ruta del archivo de imagen de la carta basado en su nombre.
    """
    suits = {"S": "spades", "H": "hearts", "D": "diamonds", "C": "clubs"}
    ranks = {"A": "ace", "K": "king", "Q": "queen", "J": "jack", "10": "10",
             "9": "9", "8": "8", "7": "7", "6": "6", "5": "5", "4": "4",
             "3": "3", "2": "2"}

    if len(card) < 2:
        return ""

    rank = ranks.get(card[:-1], card[:-1])
    suit = suits.get(card[-1], "")

    if suit:
        filename = f"{rank}_of_{suit}.png"
        return os.path.join(CARDS_FOLDER, filename)
    return ""