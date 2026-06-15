team_roster = {
    '7': {'name': 'Michelle', 'position': 'Point Guard', 'scores' : [18, 22, 15, 26]},
    '1': {'name': 'Wemby', 'position': 'Shooting Guard', 'scores': [8, 2, 32, 12]},
    '90':{'name' : 'Brunson', 'position': 'Point Guard', 'scores': [50, 20, 10, 20]}
}

def add_game_performance(roster, jersey, points):
    if jersey in roster:
        if points >= 0:
            roster[jersey]['scores'].append(points)
            return f"Added {points} pts to {roster[jersey]['name']}'s record successfully!"
        else:
            return "Invalid score value!"
    else: 
        return "Player not found!"
def generate_team_insights(roster):
    total_active_players = len(roster)
    team_elite_scorers = [p['name'] for p in roster.values() if (sum(p['scores']) / len(p['scores']) >= 15)]

    highest_score = -1
    mvp_tracker = "None"
    for p in roster.values():
        if max(p['scores']) > highest_score:
            highest_score = max(p['scores'])
            mvp_tracker = p['name']
    return {
        'total_active_players': total_active_players,
        'team_elite_scorers': team_elite_scorers,
        'mvp_tracker': mvp_tracker
    }