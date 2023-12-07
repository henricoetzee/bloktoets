// Main.js
// get_data()  - Gets data from server and calls relevent function depending on request type
// Render functions
// render stores, recipebooks, recipes
// render_table - Renders table with data.

var current_store = -1;
var current_recipebook = -1;
var stores = null;
var recipebooks = null;
var recipes = null;
var products = null;
var packaging = null;
var stock = null;
var current_view = null;

// Array for breadcrumbs. There can be two breadcrumbs. 0 means no breadcrumbs.
var breadcrumbs = [0,0];



// --------------------------RENDER FUNCTIONS--------------------------------
function render_stores(response, hist=true) {
    if (hist) {history.pushState({"where": "stores", "data": response}, "")};
    if (response == null) {response = stores};
    current_view = "stores";

    // We are rendering the stores, so reset all data that comes after selecting the store
    recipebooks = null;
    recipes = null;
    products = null;
    packaging = null;

    // Render breadcrumbs
    breadcrumbs = [0,0];
    render_breadcrumbs();
    // Render table
    render_table(response, function(id) {
        current_store = id;
        get_data("recipebook", "Getting recipebooks...", id);

    });
}
function render_recipebooks(response, hist=true) {
    if (hist) {history.pushState({"where": "recipebooks", "data": response}, "")};
    if (response == null) {response = recipebooks};
    current_view = "recipebooks";

    // We are rendering the recipe books, so reset all data that comes after
    recipes = null;
    products = null;
    packaging = null;

    // Render breadcrumbs
    // Find store name for breadcrumbs
    let store_name = "";
    for (s in stores.data) {
        if (stores.data[s].id == current_store) {store_name = stores.data[s].name}
    }
    breadcrumbs = [store_name,0]
    render_breadcrumbs();
    // Render table
    render_table(response, function(id) {
        current_recipebook = id;
        get_data("recipes", "Getting recipes...", 0, id)
    });
}


//Render table
function render_table(data, onclickfunction=false, clear_main=true, where="main_view") {
    let table = document.createElement("table");
    table.className = "bt-table";
    // Create filter, will be added to first header cell
    filter_input = document.createElement("input");
    filter_input.className = "text-input";
    filter_input.style.width = "auto";
    filter_input.style.marginLeft = "15px";
    filter_input.placeholder = "Filter"

    // Create headers
    let thead = table.createTHead();
    let header_row = thead.insertRow();
    for (header in data['headers']) {
        const header_cell = document.createElement("TH");
        header_cell.innerHTML = data.headers[header];

        // Append filter on first (name) cell:
        if (header == 0) {header_cell.appendChild(filter_input)};

        header_row.appendChild(header_cell);
    }
    // Create rows
    let tbody = table.createTBody();
    for (row in data["data"]) {
        const new_row = tbody.insertRow();
        let id = data.data[row]["id"];
        if (onclickfunction) {new_row.onclick = function() {onclickfunction(id)}}
        for (cell in data.data[row]) {
            if (cell != "id" && cell != "stock_on_hand") {
                const new_cell = new_row.insertCell();
                // Render currency for certain columns:
                if (cell == "cost" || cell == "unit_price" || cell == "cost_per_unit") {
                    new_cell.innerHTML = zar(data.data[row][cell]);
                    new_cell.style.textAlign = "right";
                }else if (cell == "gross_profit"){
                    new_cell.innerHTML = data.data[row][cell].toFixed(1) + "%";
                }else{
                    new_cell.innerHTML = data.data[row][cell];
                }
            }
        }
    }

    // Filter input listener
    filter_input.oninput = function() {
        for (row in tbody.childNodes) {
            if (!Number.isInteger(parseInt(row))) {continue}  // Skip methods in table
            if (!tbody.childNodes[row].childNodes[0].innerHTML.toUpperCase().includes(filter_input.value.toUpperCase())) {
                tbody.childNodes[row].style.display = "none";
            } else {
                tbody.childNodes[row].style.display = "table-row";
            }          
        }
    }
    
    // Render
    render_to = document.getElementById(where);
    if (clear_main) {render_to.innerHTML = ""};
    render_to.appendChild(table);
}

// Render stock table
function render_stock_table(clear_main=true, where="main_view") {
    render_to = document.getElementById(where);
    if (clear_main) {render_to.innerHTML = ""};

    // Create recipe header
    let recipe_ingredients_header = document.createElement("h4");
    recipe_ingredients_header.innerHTML = "Recipes:";
    recipe_ingredients_header.style.textAlign = "center";
    render_to.appendChild(recipe_ingredients_header);

    // Create recipe table
    render_to.appendChild(render_items_table(recipes, (id) => {get_data("recipe", "Getting recipe...", id)}));

    // Create products header
    let product_ingredients_header = document.createElement("h4");
    product_ingredients_header.innerHTML = "Products:";
    product_ingredients_header.style.textAlign = "center";
    render_to.appendChild(product_ingredients_header);

    // Create products table
    render_to.appendChild(render_items_table(products, (id) => {get_data("product", "Getting product...", id)}));

    // Create packaging header
    let packaging_ingredients_header = document.createElement("h4");
    packaging_ingredients_header.innerHTML = "Packaging:";
    packaging_ingredients_header.style.textAlign = "center";
    render_to.appendChild(packaging_ingredients_header);

    // Create packaging table
    render_to.appendChild(render_items_table(packaging, (id) => {get_data("package", "Getting package...", id)}));

    // Helper function
    function render_items_table(data, onclickfunction = false) {
        let table = document.createElement("table");
        table.className = "bt-table";

        // Create table headers
        let thead = table.createTHead();
        let header_row = thead.insertRow();
        let headers = ["Name", "Unit price", "Stock on hand", "Total"]
        for (header in headers) {
            const header_cell = document.createElement("TH");
            header_cell.innerHTML = headers[header];
            header_row.appendChild(header_cell);
        }

        // Create table rows
        let tbody = table.createTBody();
        let grand_total = 0.0;
        for (row in data["data"]) {
            // Only render items with more than 0 stock
            if (parseFloat(data.data[row]["stock_on_hand"]) <= 0) {continue}

            const new_row = tbody.insertRow();
            let id = data.data[row]["id"];
            if (onclickfunction) {new_row.onclick = function() {onclickfunction(id)}}
            let row_cost = 0;

            // Name cell
            let new_cell = new_row.insertCell();
            new_cell.innerHTML = data.data[row]["name"];

            // Unit price cell
            new_cell = new_row.insertCell();
            new_cell.innerHTML = zar(data.data[row]["unit_price"]);

            // Stock on hand
            new_cell = new_row.insertCell();
            new_cell.innerHTML = data.data[row]["stock_on_hand"];

            // Totals cell and calculations
            row_cost = parseFloat(data.data[row]["unit_price"]) * parseFloat(data.data[row]["stock_on_hand"]);
            grand_total += row_cost;
            new_cell = new_row.insertCell();
            new_cell.innerHTML = zar(row_cost);
            new_cell.style.textAlign = "right";
        }
        // Create totals row
        const new_row = tbody.insertRow();
        new_row.style.fontWeight = "bold";

        let new_cell = new_row.insertCell(); // Extra black cell
        new_cell = new_row.insertCell() // Extra blank cell
        new_cell = new_row.insertCell();
        new_cell.innerHTML = "Total";
        new_cell = new_row.insertCell();
        new_cell.innerHTML = zar(grand_total);

        return table;
    }
}

//-------------------------------BREADCRUMBS----------------------------------
function render_breadcrumbs() {
    elem = document.getElementById("app_name");
    if (breadcrumbs[0] == 0) {elem.innerHTML = "Bloktoets"}
    else {
        elem.innerHTML = "";
        let bc1 = document.createElement("span");
        bc1.className = "breadcrumb";
        bc1.innerHTML = breadcrumbs[0];
        bc1.onclick = function() {
            get_data("stores");
        };
        elem.appendChild(bc1);
    }
    if (breadcrumbs[1] != 0) {
        let bc2 = document.createElement("span");
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

//-----------------------------SHOW POPUP MESSAGE---------------------------
function show_popup(message, show_close_button_immediately) {
    let popup_container = document.createElement("div");
    popup_container.className = "popup-container";
    let popup = document.createElement("div");
    popup.innerHTML = message;
    popup_container.appendChild(popup);
    let close_button = document.createElement("button");
    close_button.className = "close-button";
    close_button.innerHTML = "Close";
    close_button.onclick = function() {popup_container.remove();}
    document.body.appendChild(popup_container);
    if (show_close_button_immediately) {popup.appendChild(close_button)}
    else {setTimeout(() => {popup.appendChild(close_button)},4000)};
    return popup_container;
}

//-------------------------------HISTORY----------------------------------
window.onpopstate = function(event) {
    if (event.state) {
        if (event.state.where == "stores") {render_stores(event.state.data, false)};
        if (event.state.where == "recipebooks") {render_recipebooks(event.state.data, false)};
        if (event.state.where == "recipes") {render_recipes(event.state.data, false)};
        if (event.state.where == "products") {render_products(event.state.data, false)};
        if (event.state.where == "packaging") {render_packaging(event.state.data, false)};
        if (event.state.where == "stock") {render_stock(false)};
    }
}

//------------------------------Render currency-------------------------
function zar(amount){
    return "R " + amount.toFixed(2);
}