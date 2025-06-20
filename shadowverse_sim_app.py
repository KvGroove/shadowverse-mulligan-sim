import streamlit as st
import random
import copy

def simulate_mulligan_draw(
    copies_of_target=3,
    num_simulations=100_000,
    mulligan_size=4,
    avg_cards_kept=2,
    turn_to_check=5,
    force_mulligan_target=True,
):
    deck_size=40
    hits = 0

    for _ in range(num_simulations):
        # Create deck
        deck = ["target"] * copies_of_target + ["other"] * (deck_size - copies_of_target)
        random.shuffle(deck)

        # Draw mulligan hand (4 cards)
        mulligan_hand = deck[:mulligan_size]
        remaining_deck = deck[mulligan_size:]

        # Determine how many to mulligan (assume avg_cards_kept)
        if force_mulligan_target:
            cards_kept = [card for card in mulligan_hand if card != "target"]
            if len(cards_kept) > avg_cards_kept:
                cards_kept = random.sample(cards_kept, avg_cards_kept)
        else:
            cards_kept = random.sample(mulligan_hand, avg_cards_kept)

        cards_to_mulligan = copy.deepcopy(mulligan_hand)
        for card in cards_kept:
            cards_to_mulligan.remove(card)

        # Draw replacements
        random.shuffle(remaining_deck)
        replacement_cards = remaining_deck[:len(cards_to_mulligan)]
        post_mulligan_hand = cards_kept + replacement_cards

        # Draw 5th starting card
        remaining_deck = remaining_deck[len(cards_to_mulligan):]
        if remaining_deck:
            post_mulligan_hand.append(remaining_deck.pop(0))

        # Draw one card at the start of each turn from 2 to the specified turn
        for _ in range(turn_to_check - 1):
            if remaining_deck:
                post_mulligan_hand.append(remaining_deck.pop(0))

        # Check if target card is in final hand
        if "target" in post_mulligan_hand:
            hits += 1

    probability = hits / num_simulations
    return probability

# Streamlit App
st.title("Shadowverse Mulligan Draw Simulator")

st.markdown("""
Use this tool to simulate the probability of drawing at least one copy of a target card in your Shadowverse deck by a specific turn.
""")

copies_of_target = st.slider("Copies of target card", 0, 40, 3)
turn_to_check = st.slider("Turn to check by", 1, 15, 5)
avg_cards_kept = st.slider("Average cards kept in mulligan", 0, 4, 2)
num_simulations = st.number_input("Number of simulations", min_value=1000, max_value=1_000_000, value=100_000, step=1000)
force_mulligan_target = st.checkbox("Force mulligan target away", value=True)

if st.button("Run Simulation"):
    with st.spinner("Running simulation..."):
        prob = simulate_mulligan_draw(
            copies_of_target=copies_of_target,
            num_simulations=num_simulations,
            avg_cards_kept=avg_cards_kept,
            turn_to_check=turn_to_check,
            force_mulligan_target=force_mulligan_target,
        )
    st.success(f"Probability of drawing at least one target card by turn {turn_to_check}: {prob:.2%}")
