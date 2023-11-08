// base.js -- Contains DOMContentloaded listener, global vars, show_message and user menu things.

const spar_green = "#157946"
const spar_green_darker = "#006431"

top_bar_background_color = spar_green;
top_bar_background_color_darker = spar_green_darker;

// Stuff to do after template loads
document.addEventListener("DOMContentLoaded", () => {
    // Show message contained in "init_message" as returned from the server in the template.
    if (init_message != "none") {
        show_message(init_message, "darkred");
    };

    // Make username clickable
    if (logged_in) {
        let user_menu = document.getElementById("user_menu");
        let user_name = document.getElementById("user_name");
        user_menu.style.display = "none";
        user_menu.addEventListener("focusout", () => {
            setTimeout (() => {
                user_menu.style.display = "none";
            }, 100)
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
    let user_name = document.getElementById("user_name");
    if (user_menu.style.display == "none") {
        user_menu.style.display = "block";
        user_menu.focus();
    }
}

// Function to show message for 4 seconds

function show_message(message, color="darkgreen") {
    let div = document.createElement("div");
    div.style.backgroundColor = color;
    div.innerHTML = message;
    div.className = "message";
    document.getElementById("message_container").appendChild(div);
    div.style.opacity = 100;
    //div.innerHTML += `<span style="margin-left:15px;">👍</span>`;
    div.addEventListener("click", () => {
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
    })
}


