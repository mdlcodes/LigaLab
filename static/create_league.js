function toggleSection(sectionId){
    const section = document.getElementById(sectionId);
    section.classList.toggle('active');
}

function updateTeamDropdowns(){
    console.log("The function is running!");
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
    const wrapper = document.getElementById('teams-container-wrapper');
    const newRow = document.createElement('div');
    newRow.className = 'team-builder-row';
    
    newRow.innerHTML = `
        <div class="sub-input-row">
            <input type="text" name="team_name[]" placeholder="Enter team name" oninput="updateTeamDropdowns()" required>
            <input type="text" name="team_coach[]" placeholder="Enter coach name" required>
            <input type="text" name="team_colors[]" placeholder="Enter team colors" required>
            <button type="button" onclick="this.parentElement.parentElement.remove(); updateTeamDropdowns();" style="background-color: #ef4444; color: white;">-</button>
        </div>
    `;

    wrapper.appendChild(newRow);
    updateTeamDropdowns();
                            
}

function addPlayerRow() {
    const wrapper = document.getElementById('players-container-wrapper');
    const newRow = document.createElement('div');
    newRow.className = 'team-builder-row';
    
    newRow.innerHTML = `
        <div class="sub-input-row">
            <input type="text" name="player_name[]" placeholder="Enter player name" required>
            <input type="text" name="player_position[]" placeholder="Enter player position" required>
            <input type="text" name="player_number[]" placeholder="Enter player number" required>
            <select name="player_team[]">
                <option value="">Select team</option>
            </select>
            <button type="button" onclick="this.parentElement.parentElement.remove()" style="background-color: #ef4444; color: white;">-</button>
        </div>
    `;
    wrapper.appendChild(newRow);
    updateTeamDropdowns();
}