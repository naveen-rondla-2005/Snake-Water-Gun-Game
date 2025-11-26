import streamlit as st
from random import choice
import time

def get_com_input():
    """Returns a random choice for the computer."""
    return choice(['snake', 'water', 'gun'])

def determine_winner(user_input, com_input):
    """Determines the winner of a single round."""
    if user_input == com_input:
        return 'draw'
    elif (
        (user_input == 'snake' and com_input == 'water') or
        (user_input == 'water' and com_input == 'gun') or
        (user_input == 'gun' and com_input == 'snake')
    ):
        return 'user'
    else:
        return 'computer'

def play_game():
    st.title("🐍💧🔫 Snake, Water, Gun Game")
    st.write("Welcome to Snake, Water, Gun game!")

    # Initialize session state variables. We use 'total_rounds' to determine the state.
    if 'total_rounds' not in st.session_state:
        st.session_state.total_rounds = None
        st.session_state.user_score = 0
        st.session_state.com_score = 0
        st.session_state.round = 1

    # Section 1: Ask for the number of rounds (visible only when the game has not started)
    if st.session_state.total_rounds is None:
        st.write("Please select the number of rounds you want to play.")
        
        # We use a variable for the default value
        default_rounds = 5
        
        with st.form(key='setup_form'):
            # The 'value' parameter sets the default number. The user's actual input is captured by 'rounds_input'.
            rounds_input = st.number_input(
                "Number of rounds", 
                min_value=1, 
                value=default_rounds, 
                step=1,
                help="Enter a number like 5, 10, 21, etc."
            )
            
            submit_button = st.form_submit_button("Start Game")

        if submit_button:
            st.session_state.total_rounds = rounds_input
            st.rerun() 
        return

    # Section 2: The Main Game Loop (visible once the game has started)
    if st.session_state.round <= st.session_state.total_rounds:
        st.header(f"Round {st.session_state.round} of {st.session_state.total_rounds}")
        st.write("Choose your move:")

        col1, col2, col3 = st.columns(3)
        user_choice = None
        if col1.button("Snake 🐍"):
            user_choice = 'snake'
        if col2.button("Water 💧"):
            user_choice = 'water'
        if col3.button("Gun 🔫"):
            user_choice = 'gun'

        if user_choice:
            com_choice = get_com_input()
            
            # Display effects and determine winner
            if user_choice == 'snake':
                st.write("🐍🐍🐍🐍🐍")
            elif user_choice == 'water':
                st.write("💧🌊💦💧🌊")
            else:
                st.write("🔫💥🔫💥🔫")
            
            time.sleep(0.5)

            st.write(f"You chose **{user_choice.capitalize()}**.")
            st.write(f"The computer chose **{com_choice.capitalize()}**.")
            
            if com_choice == 'snake':
                st.write("Computer's move: 🐍")
            elif com_choice == 'water':
                st.write("Computer's move: 💧")
            else:
                st.write("Computer's move: 🔫")

            result = determine_winner(user_choice, com_choice)

            if result == 'draw':
                st.info("It's a TIE!")
            elif result == 'user':
                st.success("🎉 You win this round!")
                st.session_state.user_score += 1
            else:
                st.error("🤖 Computer wins this round.")
                st.session_state.com_score += 1
            
            st.session_state.round += 1
            
            time.sleep(1)
            st.rerun()

        st.subheader("Current Score")
        st.write(f"Your Score: **{st.session_state.user_score}** | Computer Score: **{st.session_state.com_score}**")
        
    # Section 3: Final Results
    else:
        st.subheader("Final Results!")
        if st.session_state.user_score > st.session_state.com_score:
            st.balloons()
            st.success("Congratulations! You won the game!")
        elif st.session_state.user_score < st.session_state.com_score:
            st.error("Better luck next time! The computer won the game.")
        else:
            st.info("The game is a tie!")
        
        st.write("---")
        if st.button("Play Again?"):
            st.session_state.total_rounds = None
            st.session_state.user_score = 0
            st.session_state.com_score = 0
            st.session_state.round = 1
            st.rerun()

if __name__ == '__main__':
    play_game()