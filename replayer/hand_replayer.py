import streamlit as st
import os

# Ruta de la carpeta donde están las imágenes de las cartas
CARDS_FOLDER = os.path.join(os.path.dirname(__file__), "cards")
BACK_CARD_IMAGE = os.path.join(CARDS_FOLDER, "back.png")  # Imagen para cartas desconocidas

# Verificar si la carpeta de cartas existe y listar archivos
if not os.path.exists(CARDS_FOLDER):
    print(f"Error: La carpeta {CARDS_FOLDER} no existe.")
else:
    print(f"Contenido de {CARDS_FOLDER}: {os.listdir(CARDS_FOLDER)}")

def display_hand(hand):
    """
    Display a single hand in a user-friendly format.
    """
    st.write(f"Small Blind: {hand['smallblind']}, Big Blind: {hand['bigblind']}")

    # Mostrar las cartas del jugador en lugar del Hand ID
    st.write("### Your Cards:")
    player_hole_cards = get_player_hole_cards(hand)
    show_card_images(player_hole_cards)

    # Mostrar jugadores y sus cartas
    st.write("### Players")
    for player in hand["players"]:
        st.write(f"**{player['name']} (Seat {player['seat']})**")
        hole_cards = player.get("hole_cards", [])
        show_card_images(hole_cards, unknown_allowed=True)

    # Mostrar las rondas y sus cartas comunitarias
    st.write("### Rounds")
    for round_data in hand["rounds"]:
        st.write(f"#### Round {round_data['no']}")

        # Mostrar cartas comunitarias
        for cards in round_data["cards"]:
            if cards["type"] in ["Flop", "Turn", "River"]:
                st.write(f"**{cards['type']}:**")
                show_card_images(cards["cards"], unknown_allowed=False)

        # Mostrar acciones de los jugadores
        for action in round_data["actions"]:
            st.write(f"Player **{action['player']}**: **{action['type']}**, Bet: {action['sum']}")

def get_player_hole_cards(hand):
    """
    Obtener las cartas del jugador principal en la mano.
    """
    for player in hand["players"]:
        if player.get("is_hero", False):  # Suponiendo que haya una marca para identificar al jugador principal
            return player.get("hole_cards", [])
    return []

def show_card_images(cards, unknown_allowed=True):
    """
    Muestra imágenes de las cartas en la interfaz de Streamlit.
    """
    if not cards:  # Si no hay cartas para mostrar
        st.write("No hay cartas para mostrar.")
        return

    # Obtener las rutas de las imágenes de las cartas
    card_images = [get_card_image_path(card, unknown_allowed) for card in cards]

    # Filtrar imágenes vacías (por si acaso)
    card_images = [img for img in card_images if img]  # Eliminar rutas vacías

    if not card_images:  # Si no hay imágenes válidas
        st.write("No se encontraron imágenes válidas para mostrar.")
        return

    # Mostrar las imágenes en columnas
    num_columns = len(card_images)
    if num_columns > 0:  # Asegurarse de que hay al menos una columna
        cols = st.columns(num_columns)
        for col, img in zip(cols, card_images):
            col.image(img, width=100)
    else:
        st.write("No hay imágenes para mostrar.")

def get_card_image_path(card, unknown_allowed=True):
    """
    Construye la ruta del archivo de imagen de la carta basado en su nombre.
    Si la carta es desconocida y `unknown_allowed` es True, muestra una carta boca abajo.
    """
    suits = {"S": "spades", "H": "hearts", "D": "diamonds", "C": "clubs"}
    ranks = {
        "A": "ace", "K": "king", "Q": "queen", "J": "jack",
        "10": "10", "9": "9", "8": "8", "7": "7", "6": "6",
        "5": "5", "4": "4", "3": "3", "2": "2"
    }

    if not card or len(card) < 2:  # Si la carta es inválida
        return BACK_CARD_IMAGE if unknown_allowed else ""

    suit = card[0]  # Primer carácter: palo (S, H, D, C)
    rank = card[1:] # Resto de caracteres: rango (A, K, Q, J, 10, 9, ..., 2)

    # Verificar si el palo y el rango son válidos
    if suit in suits and rank in ranks:
        filename = f"{ranks[rank]}_of_{suits[suit]}.png"
        card_path = os.path.join(CARDS_FOLDER, filename)
        if os.path.exists(card_path):  # Verificar si la imagen existe
            return card_path
        else:
            print(f"Advertencia: No se encontró la imagen {filename} en {CARDS_FOLDER}")  # Depuración
    else:
        print(f"Advertencia: Carta inválida {card}")  # Depuración

    return BACK_CARD_IMAGE if unknown_allowed else ""
