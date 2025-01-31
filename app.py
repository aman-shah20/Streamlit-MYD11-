import streamlit as st
import pandas as pd

st.set_page_config(layout='wide', page_title='MYD11')

def load_myd11():
    st.subheader("Enter Player Details")
    
    # Get number of players
    number_of_players = st.number_input('Enter the number of players:', min_value=11, step=1)
    
    d11_list = []
    for player in range(number_of_players):  
        player_name = st.text_input(f"Enter player {player + 1} name:", key=f"player_{player}")
        if player_name:
            d11_list.append(player_name)

    if len(d11_list) < 11:
        st.warning("You need at least 11 players to create teams.")
        return None
    
    df = pd.DataFrame(d11_list, columns=['Players'])

    # Get number of teams
    num_of_teams = st.number_input('Enter the number of teams:', min_value=1, step=1)
    
    st.subheader("Generated Teams")

    # Create teams
    teams = []
    for i in range(1, num_of_teams + 1):
        if len(df) < 11:
            st.error("Not enough players to create a full team!")
            break
        sample = df.sample(n=11, replace=False)
        teams.append(sample.reset_index(drop=True))  # Reset index for clean display

    # Display teams in 5 columns
    if teams:
        cols = st.columns(10)  # Create 5 columns
        for i, team in enumerate(teams):
            col_index = i % 10  # Determine column position
            with cols[col_index]:  
                st.write(f"### Team {i + 1}")
                st.write(team)

    return df

st.title('Welcome to My Dream 11 Site')
st.header('Create Your Random Teams of Players')

option = st.selectbox('Select One', ['Click to select', 'Customise Team', 'Nothing'])

if option == 'Customise Team':
    players_df = load_myd11()
    if players_df is not None:
        st.write("### All Players Entered")
        st.write(players_df)

st.sidebar.title('Contents')
st.sidebar.title('About Us')
st.sidebar.title('Contact')
st.sidebar.title('Join')
st.sidebar.title('Logout')

