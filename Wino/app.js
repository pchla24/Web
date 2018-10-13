var password = document.getElementById("password"),
confirm_password = document.getElementById("confirm_password");

var passText = document.getElementById("passText");

function validatePassword() {
    if (password.value != confirm_password.value) {
        confirm_password.setCustomValidity("Hasła nie są identyczne");
    } else {
        confirm_password.setCustomValidity('');
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

password.onkeyup = checkPassword;
password.onchange = validatePassword;
confirm_password.onkeyup = validatePassword;
