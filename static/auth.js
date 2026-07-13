// Account Registration manager
function registerUser(){
    const user = document.getElementById('reg-username').value;
    const pass = document.getElementById('reg-password').value;

    fetch('/register', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({username: user, password: pass})
    })
    .then(res => res.json())
    .then(data =>{
        const msgEl = document.getElementById('reg-message');
        msgEl.innerText = data.message || data.error;
    });

}



function loginManager(){
    const user = document.getElementById('login-username').value;
    const pass = document.getElementById('login-password').value;
    const errorEl = document.getElementById('login-error');

    errorEl.innerText = "";

    if (!user || !pass){
        errorEl.innerText = "Please fill out all fields, coach!";
        return;
    }

    fetch('/api/login', {
        method: 'POST', 
        headers: { 'Content-Type': 'application/json'},
        body: JSON.stringify({username: user, password: pass})
    })
    .then(res => res.json())
    .then(data => {
        if(data.status == "success"){
            window.location.href = '/dashboard';
        } else {
            errorEl.innerText = data.message;
        }
    })
    .catch(error => {
        console.error('Error logging in:', error);
        errorEl.innerText = "System error, please try again."
    })
}


