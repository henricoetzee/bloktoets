
// ------------------------------RENDER FUNCTIONS----------------------------//
function render_recipes(response, hist=true) {
    if (hist) {history.pushState({"where": "recipes", "data": response}, "")};
    // Update breadcrumb
    let recipebook_name = "";
    for (r in recipebooks.data) {
        if (recipebooks.data[r].id == current_recipebook) {recipebook_name = recipebooks.data[r].name}
    }
    breadcrumbs[1] = recipebook_name;
    render_breadcrumbs();

    // Render selector on breadcrumb
    render_selector("recipes");
    
    // Render add button on breadcrumb
    render_button("Add recipe", () => {render_add_window("recipe")});

    // Get products and packaging that is needed for recipes
    if (products == null) {get_data("products", "Getting products", current_store, current_recipebook, false)}
    if (packaging == null) {get_data("packaging", "Getting products", current_store, current_recipebook, false)}

    render_table(response, function(id) {get_data("recipe", "Getting recipe...", id)});
}

function render_products(response, hist=true) {
    if (hist) {history.pushState({"where": "products", "data": response}, "")};
    // Update breacrumb
    render_breadcrumbs();

    // Render selector on breadcrumb
    render_selector("products");

    // Render add button on breadcrumb
    render_button("Add product", () => {render_add_window("product")});

    render_table(response, function(id) {get_data("product", "Getting product...", id)});
}

function render_packaging(response, hist=true) {
    if (hist) {history.pushState({"where": "packaging", "data": response}, "")};
    // Update breacrumb
    render_breadcrumbs();

    // Render selector on breadcrumb
    render_selector("packaging");

    // Render add button on breadcrumb
    render_button("Add packaging", () => {render_add_window("packaging")});

    render_table(response, function(id) {get_data("package", "Getting package...", id)});
}


// Renders a drop down selector to choose between recipes, products and packing materials.
function render_selector(selected_component) {
    let elem = document.getElementById("app_name");
    let selector_container = document.createElement("span");
    selector_container.className = "breadcrumb";
    selector_container.innerHTML = " > ";
    selector_container.style.marginLeft = "10px";
    
    let select_options = ["recipes", "products", "packaging"]
    let selector = document.createElement("select");
    selector.className = "component-selector";
    
    for (i in select_options) {
        var option = document.createElement("option");
        option.value = select_options[i];
        option.text = capitilize_first_letter(select_options[i]);
        selector.appendChild(option);
        if (select_options[i] == selected_component) {option.selected = true};
    }

    selector.addEventListener("change", () => {
        switch_component(selector.value);
    })

    selector_container.appendChild(selector);
    elem.appendChild(selector_container);
}

// Used by the render_selector function
function switch_component(component) {
    if (component == "recipes") {
        if (recipes == null) {get_data("recipes", "Getting recipes...", current_store, current_recipebook)}
        else {render_recipes(recipes)}
    }
    if (component == "products") {
        if (products == null) {get_data("products", "Getting products...", current_store, current_recipebook)}
        else {render_products(products)}
    }
    if (component == "packaging") {
        if (packaging == null) {get_data("packaging", "Getting packaging...", current_store, current_recipebook)}
        else (render_packaging(packaging))
    }
    
}

// Renders a button on the nav toolbar.  Will be deleted by the render_breadcrumbs button, so
// this function should be called after that function.
function render_button(button_name, button_function) {
    let elem = document.getElementById("app_name");
    let new_button = document.createElement("span");
    new_button.className = "breadcrumb";
    new_button.style.marginLeft = "30px";
    new_button.style.backgroundColor = "#BCED09";
    new_button.style.color = "#000000";
    new_button.style.borderRadius = "10px";
    new_button.innerHTML = button_name;
    new_button.onclick = function() {button_function()}
    elem.appendChild(new_button);
}


function render_add_window(t, existing_item = false, response = null) {
    let add_window_container = document.createElement("div");
    add_window_container.className = "add-window-container";
    
    let add_window = create_add_window_contents(t, add_window_container, existing_item, response);
    
    let close_button = document.createElement("button");
    close_button.className = "button red-bg";
    close_button.innerHTML = "Cancel";
    close_button.onclick = function() {add_window_container.remove()};

    add_window.appendChild(close_button);
    add_window_container.appendChild(add_window);
    document.body.appendChild(add_window_container);
}