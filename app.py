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
def home():
    return "Welcome to LigaLab"

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