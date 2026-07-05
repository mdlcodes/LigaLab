from flask import Flask, jsonify, render_template, request
# Import the function from ligalab.py
from ligalab import team_roster, generate_team_insights
import json
import os

app = Flask(__name__)

DB_FILE = 'database.json'

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

@app.route('/')
def home_gateway():
    # Show the clean Split Hero signup/login gate first
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/leagues')
def leagues():
    return render_template('leagues.html')

@app.route('/teams')
def teams():
    return render_template('teams.html')

@app.route('/players')
def players():
    return render_template('players.html')

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

@app.route('/create_league', methods=['POST'])
def create_league():
    league_data = request.get_json()
    username = league_data.get('username')
    league_name = league_data.get('league_name')

    if not username or not league_name:
        return jsonify({"Error": "Missing username or league anme"}), 400
    
    db = load_database()
    #Check if the username really exists
    if username not in db['users']:
        return jsonify({"error": "Username not found"}), 404
    #Avoid duplicate league 
    if league_name in db["users"][username]['custom_leagues']:
        return jsonify({"Error": "League name already exists"})
    
    db['users'][username]["custom_leagues"][league_name] = {
        "teams": {}
    }

    save_database(db)

    return jsonify({"Message" : f"League '{league_name}' create succesfully for user '{username}'!"}), 201

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