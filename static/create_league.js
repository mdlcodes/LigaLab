function toggleSection(sectionId){
    const section = document.getElementById(sectionId);
    section.classList.toggle('active');
}

function updateTeamDropdowns(){
    const teamInputs = document.querySelectorAll('input[name="team_name[]"]');
    const currentTeams = [];

    teamInputs.forEach(input => {
        if (input && input.value && input.value.trim() !== ''){
            currentTeams.push(input.value.trim())
        }
    });

    const dropdowns = document.querySelectorAll('select[name="player_team[]"]');

    dropdowns.forEach(select => {
        const previousSelection = select.value || "";

        select.innerHTML = '<option value="">Select team</option>';

        currentTeams.forEach(teamName => {
            const option = document.createElement('option');
            option.value = teamName;
            option.textContent = teamName;

            if(teamName === previousSelection){
                option.selected = true;
            }

            select.appendChild(option);
        });
    });

}

function addTeamRow(){
    const teamNames = document.getElementsByName('team_name[]');
    const lastTeamName = teamNames[teamNames.length -1].value.trim();
    const errorEl = document.getElementById('team-add-error');

    if(lastTeamName === ''){
        errorEl.innerText = "Please fill in the team name first before adding a new team, Coach!.";
        return;
    }

    errorEl.innerText = "";

    const wrapper = document.getElementById('teams-container-wrapper');
    const newRow = document.createElement('div');
    newRow.className = 'team-builder-row';
    
    newRow.innerHTML = `
        <button type="button" class="btn-remove-row" onclick="this.parentElement.remove(); updateTeamDropdowns();" title="Remove Team">✕</button>
        <div class="dynamic-grid">
            <div class="input-group">
                <label>Team Name</label>
                <input type="text" name="team_name[]" placeholder="Enter team name" oninput="updateTeamDropdowns()" required>
            </div>
            <div class="input-group">
                <label>Coach Name</label>
                <input type="text" name="team_coach[]" placeholder="Enter coach name" required>
            </div>
            <div class="input-group">
                <label>Team Colors</label>
                <input type="text" name="team_colors[]" placeholder="Enter team colors" required>
            </div>
        </div>
    `;

    wrapper.appendChild(newRow);
    updateTeamDropdowns();
                            
}

function addPlayerRow() {
    const playerNames = document.getElementsByName('player_name[]');
    const lastPlayerName = playerNames[playerNames.length - 1].value.trim();
    const errorEl = document.getElementById('player-add-error');

    if(lastPlayerName === ''){
        errorEl.innerText = "Please fill in the player name first before adding a new player, Coach!.";
        return;
    }

    errorEl.innerText = "";

    const wrapper = document.getElementById('players-container-wrapper');
    const newRow = document.createElement('div');
    newRow.className = 'team-builder-row';
    
    newRow.innerHTML = `
        <button type="button" class="btn-remove-row" onclick="this.parentElement.remove()" title="Remove Player">✕</button>
        <div class="dynamic-grid">
            <div class="input-group">
                <label>Player Name</label>
                <input type="text" name="player_name[]" placeholder="Enter player name" required>
            </div>
            <div class="input-group">
                <label>Position</label>
                <input type="text" name="player_position[]" placeholder="Enter player position" required>
            </div>
            <div class="input-group">
                <label>Jersey Number</label>
                <input type="text" name="player_number[]" placeholder="Enter player number" required>
            </div>
            <div class="input-group">
                <label>Select Team</label>
                <select name="player_team[]">
                    <option value="">Select team</option>
                </select>
            </div>
        </div>
    `;

    wrapper.appendChild(newRow);
    updateTeamDropdowns();
}

function validateLeagueForm(event) {
    const leagueName = document.querySelector('input[name="league_name"]').value.trim();
    const errorEl = document.getElementById('league-error');

    if(leagueName === ''){
        event.preventDefault();
        errorEl.innerText = "Please fill in the League Name, Coach!"
        return false;
    }

    errorEl.innerText = "";
    return true;
}