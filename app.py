import json
import os
from flask import Flask, jsonify, render_template, request, redirect, url_for
# Import the function from ligalab.py
from ligalab import team_roster, generate_team_insights


app = Flask(__name__)

DB_FILE = 'database.json'
TEAMS_FILE = 'teams.json'
PLAYERS_FILE = 'players.json'
LEAGUES_FILE = 'leagues.json'

#reads the json text file
def load_database():
    #To check if the file exist on personal hard drive
    if not os.path.exists(DB_FILE):
        return {"users": {}, 
                "custom_leagues": {}}
    
    with open(DB_FILE, 'r') as file: 
        return json.load(file)
    
def save_database(data):
    #write the updated dictionary into the physical json file
    with open(DB_FILE, 'w') as file:
        # json.dump writes it into string literal, indent = 4 for spacing
        json.dump(data, file, indent = 4)

#Load data from the hard drive (TEAMS)
def load_teams():
    if not os.path.exists(TEAMS_FILE):
        return []
    with open(TEAMS_FILE, 'r') as file:
        return json.load(file)
    
def save_teams(data):
    with open(TEAMS_FILE, 'w') as file:
        json.dump(data, file, indent=4)

#Load data from the hard drive (PLAYERS)
def load_players():
    if not os.path.exists(PLAYERS_FILE):
        return []
    with open(PLAYERS_FILE, 'r') as file:
        return json.load(file)
    
def save_players(data):
    with open(PLAYERS_FILE, 'w') as file:
        json.dump(data, file, indent=4)


#LOAD DATA AND SAVE(LEAGUESS)
def load_leagues():
    if not os.path.exists(LEAGUES_FILE):
        return []
    with open(LEAGUES_FILE, 'r') as file:
        return json.load(file)

def save_leagues(data):
    with open(LEAGUES_FILE, 'w') as file:
        json.dump(data, file, indent=4)
    

@app.route('/')
def home_gateway():
    # Show the clean Split Hero signup/login gate first
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/leagues', methods=['GET', 'POST'])
def leagues():
    
    leagues_database = load_leagues()
    teams_database = load_teams()
    players_database = load_players()

    for league in leagues_database: 
        # get the teams whose league is the same with the league looping
        matching_teams = [t for t in teams_database if t.get('league') == league['name']]
        # saves the number of teams on teams.json
        league['teams'] = len(matching_teams)

        allowed_teams = [t['name'] for t in matching_teams]
        league['players'] = len([p for p in players_database if p.get('team') in allowed_teams])
    
    return render_template('leagues.html', leagues=leagues_database)

@app.route('/leagues/create', methods=['GET', 'POST'])
def create_league():
    if request.method == 'POST':
        league_name = request.form.get('league_name')
        league_season = request.form.get('league_season')
        league_type = request.form.get('league_type')
        league_status = request.form.get('league_status')

        if league_name and league_season:

            leagues_db = load_leagues()
            teams_db = load_teams()
            players_db = load_players()

            new_league = {
                "id": f"LG-{101 + len(leagues_db)}",
                "name": league_name, 
                "season": league_season,
                "type": league_type,
                "status": league_status if league_status else "Registration Open"
            }

            leagues_db.append(new_league)
            save_leagues(leagues_db)

            team_names = request.form.getlist('team_name[]')
            team_coaches = request.form.getlist('team_coach[]')
            team_colors = request.form.getlist('team_colors[]')

            for i in range(len(team_names)):
                current_team_name = team_names[i]
                if current_team_name:
                    new_team={
                        "id": f"TM-2026-{101+len(teams_db)}",
                        "name": current_team_name,
                        "coach": team_coaches[i] if i < len(team_coaches) else "TBA",
                        "color": team_colors[i] if i < len(team_colors) else "Default",
                        "league": league_name
                    }

                    teams_db.append(new_team)

            player_names = request.form.getlist('player_name[]')
            player_positions = request.form.getlist('player_position[]')
            player_numbers = request.form.getlist('player_number[]')
            player_teams = request.form.getlist('player_team[]')

            for i in range(len(player_names)):
                if player_names[i]:
                    new_player = {
                        "name": player_names[i],
                        "position": player_positions[i] if i < len(player_positions) else "Unknown",
                        "number": player_numbers[i] if i < len(player_numbers) else "00",
                        "team": player_teams[i] if i < len(player_teams) else "Unknown",
                        "status": "Active"

                    }
                    players_db.append(new_player)

            save_teams(teams_db)
            save_players(players_db)

            return redirect(url_for('leagues'))
    return render_template('create_league.html')
                        



@app.route('/teams', methods=['GET', 'POST'])
def teams():
    teams_database = load_teams()
    players_database = load_players()

    for team in teams_database:
        matching_players = [p for p in players_database if p.get('team') == team['name']]
        team['roster_size'] = len(matching_players)
    
    return render_template('teams.html', teams=teams_database)

@app.route('teams/create', methods=['GET', 'POST'])
def create_teams():
    leagues_database = load_leagues()

    if request.method == 'POST':
        teams_database = load_teams()
        players_database = load_players()

        team_name = request.form.get('team_name')
        team_coach = request.form.get('team_coach')
        team_color = request.form.get('team_color')
        team_league = request.form.get('team_league')

        if team_name:
            new_team = {
                "name": team_name,
                "coach": team_coach,
                "color": team_color,
                "league": team_league 
            }

        teams_database.append(new_team)
        save_teams(teams_database)

        player_names = request.form.getlist('player_name[]')
        player_positions = request.form.getlist('player_position[]')
        player_numbers = request.form.getlist('player_number[]')

        for i in range(len(player_names)):
                if player_names[i].strip():
                    new_player = {
                        "name": player_names[i].strip(),
                        "position": player_positions[i] if i < len(player_positions) else "Unknown",
                        "number": player_numbers[i] if i < len(player_numbers) else "00",
                        "team": team_name, 
                        "status": "Active"
                    }
                    players_database.append(new_player)
        save_players(players_database)

        return redirect(url_for('teams'))
    return render_template('create_teams.html', leagues=leagues_database)
#PLAYER
@app.route('/players', methods=['GET', 'POST'])
def players():
    
    players_database = load_players()
    teams_database = load_teams()

    if request.method == 'POST':
        player_name = request.form.get('ligalab-player-name')
        player_number = request.form.get('ligalab-player-number')
        player_team = request.form.get('ligalab-player-team')

        if player_name and player_number and player_team:

            new_player={
                "name": player_name,
                "number": player_number,
                "teams": player_team,
                "status": "Active Roster"
            }

            players_database.append(new_player)
            save_players(players_database)

            return redirect(url_for('players'))

    return render_template('players.html', players=players_database, teams=teams_database)


@app.route('/schedules')
def schedules():
    return render_template('schedule.html')

@app.route('/dashboard')
def dashboard_view():
    # This is the actual inner tournament control center panel
    return render_template('index.html')

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '')

    if not username or not password:
        return jsonify({"status": "error", "message": "Missing username or password"})
    
    db = load_database()

    if "users" in db and username in db["users"]:
        if db["users"][username]["password"] == password:
            return jsonify({"status": "success", "message": "Authentication sucessful"})
        else:
            return jsonify({"status": "error", "message": "Incorrect password or username"})
    else:
        return jsonify({"status": "error", "message": "Username not found.Please try again"})

@app.route('/insights')
def get_insights():
    insights_data = generate_team_insights(team_roster)
    return jsonify(insights_data)



@app.route('/add_team', methods=['POST'])
def add_team():
    #add a basketball team
    team_data = request.get_json()
    username = team_data.get('username')
    league_name = team_data.get('league_name')
    team_name = team_data.get('team_name')

    #ensure all fields are filled out
    if not all([username, league_name, team_name]):
        return jsonify({"error":"Missing, username, league name, or team name"}), 400
    
    db = load_database()
    #ensure the user and league exist
    if username not in db["users"]:
        return jsonify({"error": "User profile not found"}), 404
    if league_name not in db['users'][username]["custom_leagues"]:
        return jsonify({"error": "League is not found in this user profile"}), 404
    
    if team_name in db["users"][username]["custom_leagues"][league_name]["teams"]:
        return jsonify({"error":"Team name already exist in this league "}), 400
    
    db["users"][username]["custom_leagues"][league_name]["teams"][team_name] = {
        "players" : {},
        "team_wins": 0,
        "team_losses": 0
    }

    save_database(db)

    return jsonify({"message": f"Team '{team_name}' successfully added to '{league_name}'"}), 201

@app.route('/add_player', methods=['POST'])
def add_player():
    player_data = request.get_json()
    username = player_data.get('username')
    league_name = player_data.get('league_name')
    team_name = player_data.get('team_name')
    player_name = player_data.get('player_name')

    if not all([username, league_name, team_name, player_name]):
        return jsonify({"error":"Missing username, league name, team name, player name"}), 400
    
    db = load_database()

    #verify and no dupli

    if username not in db['users']:
        return jsonify({"error": "Manager Profile not found"}), 404
    if league_name not in db['users'][username]['custom_leagues']:
        return jsonify({"error": f"The {league_name} does not exist"}), 404
    if team_name not in db['users'][username]['custom_leagues'][league_name]['teams']:
        return jsonify({"error": "Team profile not found in this league"})
    
    #Ensure the player does not exist in the team yet
    current_team_player = db["users"][username]['custom_leagues'][league_name]["teams"][team_name]['players']

    if player_name in current_team_player:
        return jsonify({"error": "This player already exist"}), 400
    
    #Inject player record slot
    db["users"][username]["custom_leagues"][league_name]['teams'][team_name]["players"][player_name] = {
        "scores": [], 
        "assists": [],
        "rebounds": []
    }

    save_database(db)

    return jsonify({"message": f"Player '{player_name}' signed successfully"}), 201


@app.route('/register', methods=['POST'])
def register():
    #Grab the JSON data from the user's input
    user_data = request.get_json()
    username = user_data.get('username')
    password = user_data.get('password')

    if not username or not password:
        return jsonify({"error" : "Missing username or password"}), 400
    
    db = load_database()

    #Check for name duplicate
    if username in db["users"]:
        return jsonify({"error": "Username already taken"}), 400

    #Insert the inputed user records into out text file in a dictionary structure
    db["users"][username] = {
        "password" : password,
        "custom_leagues" : {} 
    }     
    # save the updated dictionary to text file
    save_database(db)

    return jsonify({"message": f"User {username} registered successfully!"}), 201

if __name__ == '__main__':
    app.run(debug=True, port=5000)