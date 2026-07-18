function toggleSection(sectionId){
    const section = document.getElementById(sectionId);
    const header = section.previousElementSibling;

    section.classList.toggle('active');

    if(header && header.classList.contains('accordion-header')){
        header.classList.toggle('active');
    }
}

function addPlayerRow(){
    const playerName = document.getElementsByName('player_name[]');
    const errorEl = document.getElementById('player-add-error');

    if(playerName.length > 0){
        const lastPlayerName = playerName[playerName.length - 1].value.trim();

        if(lastPlayerName === ''){
            errorEl.innerText = "Please fill out the player name";
            return;
        }
    }

    if(errorEl) errorEl.innerText = "";

    const wrapper = document.getElementById('players-container-wrapper');
    const newRow = document.createElement('div');
    newRow.className = 'team-builder-row';

    newRow.innerHTML = `
        <button type="button" class="btn-remove-row" onclick="this.parentElement.remove()" title="Remove Player">✕</button>
        <div class="dynamic-grid">
            <div class="input-group">
                <label>Player Name</label>
                <input type="text" name="player_name[]" placeholder="Enter player name">
            </div>
            <div class="input-group">
                <label>Player Position</label>
                <input type="text" name="player_position[]" placeholder="Enter player position">
            </div>
            <div class="input-group">
                <label>Player Number</label>
                <input type="text" name="player_number[]" placeholder="Enter player number">
            </div>
        </div>
    `;

    wrapper.appendChild(newRow);
}

function validateTeamForm(event){
    const teamNameInput = document.querySelector('input[name="team_name"]');
    const errorEl = document.getElementById('team-error');

    if(teamNameInput && teamNameInput.value.trim() === ''){
        evert.prevetnDefault();
        if(errorEl) errorEl.innerText = "Please fill out team name";
        return false;
    }

    if(errorEl) errorEl.innerText = "";
    return true;
}