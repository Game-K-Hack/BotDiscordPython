const loginForm = document.getElementById("login-form");
const loginButton = document.getElementById("login-form-submit");
const loginErrorMsg = document.getElementById("bar-user");
const loginErrorMsg2 = document.getElementById("bar-pwd");

loginButton.addEventListener("click", (e) => {
    e.preventDefault();
    const username = loginForm.username.value;
    const password = loginForm.password.value;

    if (username === 'admin' && password === '75321456kelian' || username === 'kojhyy#5962' && password === 'minecraft2003') {
        if (username === 'admin' && password === '75321456kelian') {
            //alert("admin")
            }
        loginErrorMsg.style.borderBottomColor = "#5cad00";
        loginErrorMsg2.style.borderBottomColor = "#5cad00";
        window.open("https://botdiscordpython.gamek.repl.co/search.html");
    }
    else {
        loginErrorMsg.style.borderBottomColor = "#ff2222";
        loginErrorMsg2.style.borderBottomColor = "#ff2222";
    }
})