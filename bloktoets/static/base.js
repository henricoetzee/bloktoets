// base.js -- Contains DOMContentloaded listener, global vars, show_message and user menu things.

const spar_green = "#157946"
const spar_green_darker = "#006431"

top_bar_background_color = spar_green;
top_bar_background_color_darker = spar_green_darker;

// Stuff to do after template loads
document.addEventListener("DOMContentLoaded", () => {
    // Show message contained in "init_message" as returned from the server in the template.
    if (init_message != "none") {
        show_message(init_message);
    };

    // Make username clickable
    if (logged_in) {
        let user_menu = document.getElementById("user_menu");
        let user_name = document.getElementById("user_name");
        user_menu.style.display = "none";
        user_menu.addEventListener("focusout", () => {
            setTimeout (() => {
                user_menu.style.display = "none";
            }, 500)
        })
        user_name.addEventListener("click", () => {
            usermenu_toggle();
        })
    }

});
// User menu things
// Show / hide user menu
function usermenu_toggle() {
    let user_menu = document.getElementById("user_menu");
    if (user_menu.style.display == "none") {
        user_menu.style.display = "block";
        user_menu.focus();
    }
}

// Function to show message (notification)
function show_message(message, color="#F9CB40") {
    let div = document.createElement("div");
    div.style.backgroundColor = color;
    div.innerHTML = message;
    div.className = "message";
    document.getElementById("message_container").appendChild(div);
    div.style.opacity = 100;
    // Close Button
    let close_button = document.createElement("button");
    close_button.innerHTML = "X";
    close_button.className = "message-button";
    div.appendChild(close_button);
    close_button.addEventListener("click", () => {close_message()})

    if (color != "#EC1B24") {setTimeout(() => {close_message()}, 5000)}

    function close_message() {
        setTimeout(() => {
            div.style.opacity = 0;
        }, 0);
        setTimeout(() => {
            div.style.marginBottom = 0;
            div.style.height = 0;
            div.style.padding = 0;
        }, 500)
        setTimeout(() => {
            div.remove();
        }, 1000)
    }

}

function capitilize_first_letter(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}


// Get CSRF cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');


function confirm_dialog(message, func) {
    let container = document.createElement("div");
    container.className = "popup-container";
    document.body.appendChild(container);

    let dialog = document.createElement("div");
    dialog.style.width = "360px";
    dialog.innerHTML = message;
    container.appendChild(dialog);

    let confirm_button = document.createElement("button");
    confirm_button.className = "button red-bg";
    confirm_button.style.cursor = "not-allowed";
    confirm_button.innerHTML = "Confirm";
    confirm_button.style.cursor = "pointer";
    confirm_button.onclick = function() {
        container.remove();
        func();
    }
    dialog.appendChild(confirm_button);

    let cancel_button = document.createElement("button");
    cancel_button.className = "button blue-bg";
    cancel_button.innerHTML = "Cancel";
    cancel_button.onclick = function() {container.remove()};
    dialog.appendChild(cancel_button);


}