const loginForm = document.getElementById("login-form");
const loginButton = document.getElementById("login-form-submit");
const loginErrorMsg = document.getElementById("bar-user");

loginButton.addEventListener("click", (e) => {
    e.preventDefault();
    const search = loginForm.username.value;

    if (search === 'admin') {
        if (search === 'admin') {
            //alert("admin")
            }
        loginErrorMsg.style.borderBottomColor = "#5cad00";
        window.open("https://botdiscordpython.gamek.repl.co/search.html");
    }
    else {
        loginErrorMsg.style.borderBottomColor = "#ff2222";
    }
})