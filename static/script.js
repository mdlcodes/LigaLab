// 1. Automatically fetch analytics on page load
fetch('/insights')
    .then(response => response.json())
    .then(data => {
        document.getElementById('total-players').innerText = data.total_active_players;
        document.getElementById('mvp').innerText = data.mvp_tracker;
        document.getElementById('elite-scorers').innerText = data.team_elite_scorers.join(', ');
    });

// 2. Send Registration data to backend via POST
function registerUser() {
    const user = document.getElementById('reg-username').value;
    const pass = document.getElementById('reg-password').value;
    
    fetch('/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: user, password: pass })
    })
    .then(res => res.json())
    .then(data => {
        const msgEl = document.getElementById('reg-message');
        msgEl.innerText = data.message || data.error;
    });
}

// 3. Send League Creation data to backend via POST
function createNewLeague() {
    const user = document.getElementById('league-mgr').value;
    const league = document.getElementById('league-name').value;
    
    fetch('/create_league', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: user, league_name: league })
    })
    .then(res => res.json())
    .then(data => {
        const msgEl = document.getElementById('league-message');
        msgEl.innerText = data.Message || data.error || data.Error;
    });
}

// 4. Send Team Creation data to backend via POST
function addNewTeam() {
    const user = document.getElementById('team-mgr').value;
    const league = document.getElementById('team-league').value;
    const team = document.getElementById('team-name').value;
    
    fetch('/add_team', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: user, league_name: league, team_name: team })
    })
    .then(res => res.json())
    .then(data => {
        const msgEl = document.getElementById('team-message');
        msgEl.innerText = data.message || data.error;
    });
}

// 5. Send Player Recruitment data to backend via POST
function addNewPlayer() {
    const user = document.getElementById('player-mgr').value;
    const league = document.getElementById('player-league').value;
    const team = document.getElementById('player-team').value;
    const player = document.getElementById('player-name').value;
    
    fetch('/add_player', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: user, league_name: league, team_name: team, player_name: player })
    })
    .then(res => res.json())
    .then(data => {
        const msgEl = document.getElementById('player-message');
        msgEl.innerText = data.message || data.error;
    });
}