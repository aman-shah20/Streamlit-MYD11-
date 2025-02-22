import streamlit as st
import pandas as pd
import itertools
import random

st.set_page_config(layout='wide', page_title='MYD11')

def is_valid_team(team):
    """Check if a team has at least one player from each category."""
    roles = [player[1] for player in team]  
    return all(roles.count(role) > 0 for role in ["Wicket Keeper", "Batsman", "All Rounder", "Bowler"])

def assign_captain_vc(team):
    """Randomly assign Captain (C) and Vice-Captain (VC) in the team."""
    captain = random.choice(team)
    vice_captain = random.choice([p for p in team if p != captain])  

    team_with_roles = [
        (p[0], p[1], "C" if p == captain else "VC" if p == vice_captain else "") 
        for p in team
    ]
    
    return team_with_roles

def load_myd11():
    st.subheader("Enter Player Details")
    
    total_players = 22  
    
    positions = {
        "Wicket Keeper": st.number_input('Number of Wicket Keepers:', min_value=0, max_value=total_players, step=1),
        "Batsman": st.number_input('Number of Batsmen:', min_value=0, max_value=total_players, step=1),
        "All Rounder": st.number_input('Number of All Rounders:', min_value=0, max_value=total_players, step=1),
        "Bowler": st.number_input('Number of Bowlers:', min_value=0, max_value=total_players, step=1)
    }
    
    players_list = []
    
    for role, count in positions.items():
        for i in range(count):
            player_name = st.text_input(f"Enter {role} {i + 1} name:", key=f"{role}_{i}")
            if player_name:
                players_list.append((player_name, role))
    
    if len(players_list) < 11:
        st.error("At least 11 players are required to form a team!")
        return None
    
    df_players = pd.DataFrame(players_list, columns=["Players", "Role"])
    
    # Generate all valid team combinations
    all_combinations = itertools.combinations(players_list, 11)
    valid_teams = [team for team in all_combinations if is_valid_team(team)]
    
    # Display the exact number of possible teams
    st.success(f"✅ Total valid teams possible: {len(valid_teams)}")
    
    if not valid_teams:
        st.error("No valid teams can be formed. Ensure at least one player per category.")
        return None
    
    num_of_teams = st.number_input('Enter the number of teams to generate:', 
                                   min_value=1, 
                                   max_value=len(valid_teams), 
                                   step=1)

    st.subheader("Generated Teams")
    
    teams = random.sample(valid_teams, min(num_of_teams, len(valid_teams)))
    
    if teams:
        cols = st.columns(5)  
        for i, team in enumerate(teams):
            col_index = i % 5
            with cols[col_index]:  
                st.write(f"### Team {i + 1}")
                
                team_with_captains = assign_captain_vc(team)
                
                st.write(pd.DataFrame(team_with_captains, columns=["Players", "Role", "Captaincy"]))
    
    return df_players

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
