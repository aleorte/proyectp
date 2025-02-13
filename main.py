import os
import streamlit as st
from datetime import datetime
from parsers.hand_parser import parse_session
from replayer.hand_replayer import display_hand  # Import the display_hand function
import plotly.express as px  # For timeline/graph

def main():
    st.title("Poker Hand Analyzer")
    st.sidebar.button("Recargar Datos", on_click=lambda: st.experimental_rerun())

    # Load and parse data
    st.write("### Load Hand Histories")
    folder_path = st.text_input("Enter the path to the folder with XML files:")
    if folder_path and os.path.exists(folder_path):
        tournaments, hand_histories = parse_session(folder_path)
        st.session_state["tournaments"] = tournaments
        st.session_state["hand_histories"] = hand_histories
        st.write(f"Loaded {len(tournaments)} tournaments and {len(hand_histories)} hands.")

    # Display tournaments
    if "tournaments" in st.session_state:
        st.write("### Tournaments")

        # Add a date filter for tournaments
        st.write("#### Filter by Date")
        min_date = min([datetime.strptime(t["startdate"], "%Y-%m-%d %H:%M:%S") for t in st.session_state["tournaments"]])
        max_date = max([datetime.strptime(t["startdate"], "%Y-%m-%d %H:%M:%S") for t in st.session_state["tournaments"]])
        date_range = st.date_input("Select a date range:", [min_date, max_date])

        # Filter tournaments by date range
        filtered_tournaments = [
            t for t in st.session_state["tournaments"]
            if date_range[0] <= datetime.strptime(t["startdate"], "%Y-%m-%d %H:%M:%S").date() <= date_range[1]
        ]

        # Display tournament dropdown with concise information
        tournament_options = [
            f"{t['tournamentname'].replace('Twister ', '')} | {t['startdate']} | {t['gamecount']}"
            for t in filtered_tournaments
        ]
        selected_tournament_index = st.selectbox(
            "Select a tournament:",
            range(len(filtered_tournaments)),
            format_func=lambda x: tournament_options[x]
        )

        # Display hands for the selected tournament
        if selected_tournament_index is not None:
            selected_tournament = filtered_tournaments[selected_tournament_index]
            st.write(f"Total Buy-in: {selected_tournament['totalbuyin']}")

            # Filter hands for the selected tournament using tournamentcode
            tournament_hands = [
                hand for hand in st.session_state["hand_histories"]
                if hand["tournamentcode"] == selected_tournament["tournamentcode"]
            ]
            if tournament_hands:
                st.write("#### Hands in this Tournament")

                # Display hand dropdown with only hole cards
                hand_options = [
                    f"{', '.join(hand['players'][0]['hole_cards'])}"  # Only show hole cards
                    for hand in tournament_hands
                ]
                selected_hand_index = st.selectbox(
                    "Select a hand:",
                    range(len(tournament_hands)),
                    format_func=lambda x: hand_options[x]
                )

                # Add "Next" and "Previous" buttons
                col1, col2 = st.columns(2)
                with col1:
                    if selected_hand_index > 0:
                        if st.button("Previous Hand"):
                            selected_hand_index -= 1
                with col2:
                    if selected_hand_index < len(tournament_hands) - 1:
                        if st.button("Next Hand"):
                            selected_hand_index += 1

                # Display the selected hand
                selected_hand = tournament_hands[selected_hand_index]
                display_hand(selected_hand)

                # Add a timeline of actions
                st.write("#### Timeline of Actions")
                timeline_data = []
                for round_data in selected_hand["rounds"]:
                    for action in round_data["actions"]:
                        timeline_data.append({
                            "Round": round_data["no"],
                            "Player": action["player"],
                            "Action": action["type"],
                            "Sum": action["sum"]
                        })
                if timeline_data:
                    fig = px.timeline(
                        timeline_data,
                        x_start=[0] * len(timeline_data),
                        x_end=[1] * len(timeline_data),
                        y="Player",
                        color="Action",
                        title="Action Timeline"
                    )
                    st.plotly_chart(fig)
                else:
                    st.write("No actions recorded for this hand.")
            else:
                st.write("No hands found for this tournament.")

if __name__ == "__main__":
    main()