// Main.js
// get_data()  - Gets data from server and calls relevent function depending on request type
// Render functions
// render stores, recipebooks, recipes
// render_table - Renders table with data.

var current_store = -1;
var current_recipebook = -1;
var stores;
var breadcrumbs = [0,0];

// --------------------------API fetcher--------------------------------------
function get_data(what, loading_message="Loading...", store_id=false, recipebook=false) {
    popup = show_popup(loading_message)
    url = "/bt_api?get=" + what;
    if (store_id) {url += "&store_id=" + store_id}
    if (recipebook) {url += "&recipebook=" + recipebook}
    fetch(url)
    .then(response => response.json())
    .then(response => {
        popup.remove();
        if (what == "stores") {render_stores(response)}
        if (what == "recipebook") {render_recipebooks(response)}
        if (what == "recipes") {render_recipes(response)}
    })
    .catch(error => {
        console.error(error);
        popup.remove();
        show_message("Error getting data from server", "darkred");
    })
}

// --------------------------RENDER FUNCTIONS--------------------------------
function render_stores(response, hist=true) {
    if (hist) {history.pushState({"where": "stores", "data": response}, "")};
    stores = response;
    breadcrumbs = [0,0];
    render_breadcrumbs();
    render_table(response, function(id) {
        current_store = id;
        get_data("recipebook", "Getting recipebooks...", id);

    });
}
function render_recipebooks(response, hist=true) {
    if (hist) {history.pushState({"where": "recipebooks", "data": response}, "")};
    recipebooks = response;
    let store_name = "";
    for (s in stores.data) {
        if (stores.data[s].id == current_store) {store_name = stores.data[s].name}
    }
    breadcrumbs = [store_name,0]
    render_breadcrumbs();
    render_table(response, function(id) {
        current_recipebook = id;
        get_data("recipes", "Getting recipes...", 0, id)
    });
}
function render_recipes(response, hist=true) {
    if (hist) {history.pushState({"where": "recipes", "data": response}, "")};
    let recipebook_name = "";
    for (r in recipebooks.data) {
        if (recipebooks.data[r].id == current_recipebook) {recipebook_name = recipebooks.data[r].name}
    }
    breadcrumbs[1] = recipebook_name;
    render_breadcrumbs();
    render_table(response, function(id) {get_data("recipe", "Getting recipe...", id)});
}

//Render table
function render_table(data, onclickfunction=false, clear_main=true, where="main_view") {
    let table = document.createElement("table");
    table.className = "bt-table";
    // Create headers
    let thead = table.createTHead();
    let header_row = thead.insertRow();
    for (header in data['headers']) {
        const header_cell = document.createElement("TH");
        header_cell.innerHTML = data.headers[header];
        header_row.appendChild(header_cell);
    }
    // Create rows
    tbody = table.createTBody();
    for (row in data["data"]) {
        const new_row = tbody.insertRow();
        let id = data.data[row]["id"];
        if (onclickfunction) {new_row.onclick = function() {onclickfunction(id)}}
        for (cell in data.data[row]) {
            if (cell != "id") {
                const new_cell = new_row.insertCell();
                new_cell.innerHTML = data.data[row][cell];
            }
        }
    }
    // Render
    render_to = document.getElementById(where);
    if (clear_main) {render_to.innerHTML = ""};
    render_to.appendChild(table);
}

//-------------------------------BREADCRUMBS----------------------------------
function render_breadcrumbs() {
    elem = document.getElementById("app_name");
    if (breadcrumbs[0] == 0) {elem.innerHTML = "Bloktoets"}
    else {
        elem.innerHTML = "";
        bc1 = document.createElement("span");
        bc1.className = "breadcrumb";
        bc1.innerHTML = breadcrumbs[0];
        bc1.onclick = function() {
            get_data("stores");
        };
        elem.appendChild(bc1);
    }
    if (breadcrumbs[1] != 0) {
        bc2 = document.createElement("span");
        bc2.className = "breadcrumb";
        bc2.innerHTML = " > " + breadcrumbs[1];
        bc2.style.marginLeft = "10px"
        bc2.onclick = function() {
            get_data("recipebook", "Getting recipebooks...", current_store)
            breadcrumbs[1] = 0;
            render_breadcrumbs();
        };
        elem.appendChild(bc2);
    }
    
}

//-----------------------------SHOW POPUP WINDOW---------------------------
function show_popup(message) {
    popup_container = document.createElement("div");
    popup_container.className = "popup-container";
    popup = document.createElement("div");
    popup.innerHTML = message;
    popup_container.appendChild(popup);
    close_button = document.createElement("button");
    close_button.className = "close-button";
    close_button.innerHTML = "Close";
    close_button.onclick = function() {popup_container.remove();}
    document.body.appendChild(popup_container);
    setTimeout(() => {popup.appendChild(close_button)},4000);
    return popup_container;
}

//-------------------------------HISTORY----------------------------------
window.onpopstate = function(event) {
    if (event.state) {
        if (event.state.where == "stores") {render_stores(event.state.data, false)};
        if (event.state.where == "recipebooks") {render_recipebooks(event.state.data, false)};
        if (event.state.where == "recipes") {render_recipes(event.state.data, false)};
    }
}