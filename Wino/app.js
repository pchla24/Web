var password = document.getElementById("password"),
confirm_password = document.getElementById("confirm_password");

var login = document.getElementById("login");

var pesel = document.getElementById("pesel");

function validatePassword() {
    if (password.value != confirm_password.value) {
        confirm_password.setCustomValidity("Hasła nie są identyczne");
    } else {
        confirm_password.setCustomValidity("");
    }
}

function checkPassword() {
    var strenghtBar = document.getElementById("passMeter")
    var strength = 0;
    if (password.value.match(/[a-zA-Z0-9][a-zA-Z0-9]+/)) {
        strength += 1
    }
    if (password.value.match(/[~<>?]+/)) {
        strength += 1
    }
    if (password.value.match(/[!@$%^&*()]+/)) {
        strength += 1
    }
    if (password.value.length > 5) {
        strength += 1
    }
    switch(strength) {
        case 0:
            strenghtBar.value = 0;
            break
        case 1:
            strenghtBar.value = 1;
            break
        case 2:
            strenghtBar.value = 2;
            break
        case 3:
            strenghtBar.value = 3;
            break
        case 4:
            strenghtBar.value = 4;
            break 
    }
}

function validateLogin() {
    fetch("http://edi.iem.pw.edu.pl/chaberb/register/check/<" + login.value + ">")
    .then(response => response.text())
    .then(data => {
        console.log(data)
        if (data.includes("false")) {
            console.log("Jest false")
        } else {
            ;
        }
  });
}

function validatePESEL() {
    if (pesel.value.length == 0) {
        pesel.setCustomValidity("");
    } else if (pesel.value.length == 11) {
        if (pesel.value.match(/^[0-9]+$/) != null) {
            pesel.setCustomValidity("");
        } else { 
            pesel.setCustomValidity("PESEL musi zawierać same cyfry");
        }
    } else {
        pesel.setCustomValidity("PESEL musi składać się z 11 cyfr");
    }
}


login.onkeyup = validateLogin;
password.onkeyup = checkPassword;
password.onchange = validatePassword;
confirm_password.onkeyup = validatePassword;
pesel.onkeyup = validatePESEL;

