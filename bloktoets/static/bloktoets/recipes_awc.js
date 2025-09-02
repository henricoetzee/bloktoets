// Add_Window contents
// Create elements for add window


function create_add_window_contents(t, add_window_container, existing_item=false, response) {
    let content = document.createElement("div");
    content.className = "add-window";

    // Add close button
    const window_close_button = document.createElement("div");
    window_close_button.className = "window-close-button";
    window_close_button.innerHTML = "X";
    window_close_button.addEventListener("click", ()=>{add_window_container.remove()})
    add_window_container.append(window_close_button);
    // Observe window changes so that the close button move with the window
    const observer = new ResizeObserver(entries => {
        rect = content.getBoundingClientRect();
        window_close_button.style.top = rect.top - 10;
        window_close_button.style.left = rect.right - 12;
    })
    observer.observe(content);
    observer.observe(document.body);

    // Name input - common in all three models
    let input_name_label = document.createElement("label");
    input_name_label.className = "text-input-label";
    input_name_label.htmlFor = "new_name";
    input_name_label.innerHTML = "Name";
    content.appendChild(input_name_label);
    let input_name = document.createElement("input");
    input_name.id = "new_name";
    input_name.type = "text";
    input_name.className = "text-input";
    content.appendChild(input_name);

    // Scale code input - common in all three models
    let input_scale_label = document.createElement("label");
    input_scale_label.className = "text-input-label";
    input_scale_label.htmlFor = "new_scale";
    input_scale_label.innerHTML = "Scale code";
    content.appendChild(input_scale_label);
    let input_scale = document.createElement("input");
    input_scale.id = "new_scale";
    input_scale.type = "text";
    input_scale.className = "text-input";
    content.appendChild(input_scale);

    // Sub department input
    let sub_dept_input_label = document.createElement("label");
    sub_dept_input_label.className = "text-input-label";
    sub_dept_input_label.htmlFor = "sub_dept_input";
    sub_dept_input_label.innerHTML = "Sub. Dept.";
    content.appendChild(sub_dept_input_label);
    let sub_dept_input = document.createElement("input");
    sub_dept_input.id = "sub_dept";
    sub_dept_input.type = "text";
    sub_dept_input.className = "text-input";
    content.appendChild(sub_dept_input);

    // Split into two branches, one for recipes, and the other for
    // products and packaging
    if (t == "recipe") {
        // Create new recipe object
        r = new Recipe;
        let todo = "create";

        if (existing_item) {
            todo = "modify";
            r.id = response.id;
            r.name = response.name;
            r.scale_code = response.scale_code;
            r.recipe_ingredients = response.recipe_ingredients;
            r.ingredients = response.product_ingredients;
            r.packaging = response.packaging_ingredients;
            r.cost = response.cost_per_unit;
            r.selling = response.selling_price;
            r.yield = response.recipe_yield;
            r.stock_on_hand = response.stock_on_hand;
            r.sub_dept = response.sub_dept;
            sub_dept_input.value = r.sub_dept;
            input_name.value = r.name;
            input_scale.value = r.scale_code;
        }

        // Make window bigger and center display
        content.style.width = "1000px";
        content.style.textAlign = "center";
        // Add break before sub dept
        const break_before_sub_dept = document.createElement("br");
        content.insertBefore(break_before_sub_dept, sub_dept_input_label);

        // Add stock on hand input
        let input_stock_label = document.createElement("label");
        input_stock_label.className = "text-input-label";
        input_stock_label.htmlFor = "new_stock";
        input_stock_label.innerHTML = "Stock";
        content.appendChild(input_stock_label);
        let input_stock = document.createElement("input");
        input_stock.id = "new_cost";
        input_stock.type = "number";
        input_stock.min = 0;
        input_stock.step = 0.01;
        input_stock.className = "text-input";
        input_stock.value = r.stock_on_hand;
        content.appendChild(input_stock);

        // -------Add the +Recipe +Product +Packaging buttons
        let button_holder = document.createElement("div");
        // Recipe ingredients button
        let input_recipe_ingredient = document.createElement("button");
        input_recipe_ingredient.className = "button-green";
        input_recipe_ingredient.style.width = "fit-content";
        input_recipe_ingredient.innerHTML = "+ recipe";
        input_recipe_ingredient.onclick = function() {content.appendChild(render_add_contents_window(recipes, "recipes", r))};
        button_holder.appendChild(input_recipe_ingredient);
        // Product ingredient button
        let input_product_ingredient = document.createElement("button");
        input_product_ingredient.className = "button-green";
        input_product_ingredient.style.width = "fit-content";
        input_product_ingredient.innerHTML = "+ product";
        input_product_ingredient.onclick = function() {content.appendChild(render_add_contents_window(products, "products", r))};
        button_holder.appendChild(input_product_ingredient);
        // Packaging ingredient button
        let input_packaging_ingredient = document.createElement("button");
        input_packaging_ingredient.className = "button-green";
        input_packaging_ingredient.style.width = "fit-content";
        input_packaging_ingredient.innerHTML = "+ packaging";
        input_packaging_ingredient.onclick = function() {content.appendChild(render_add_contents_window(packaging, "packaging", r))};
        button_holder.appendChild(input_packaging_ingredient);
        // Add button holder
        content.appendChild(button_holder);

        // Add hr
        content.appendChild(document.createElement("hr"))

        // Render tables for all ingredients + Total price and selling price
        let ingredients_table_holder = document.createElement("div");
        ingredients_table_holder.id = "ingredients_table_holder";
        render_ingredients_table(ingredients_table_holder, r);

        content.appendChild(ingredients_table_holder);

        // Save button
        let save_button = document.createElement("button");
        save_button.className = "button-green";
        save_button.innerHTML = "Save";
        save_button.onclick = function() {
            add_window_container.remove();
            data = JSON.stringify({
                "what": "recipe",
                "todo": todo,
                "id": r.id,
                "recipe_book": current_recipebook,
                "scale_code": input_scale.value,
                "name": input_name.value,
                "cost_per_unit": parseFloat(r.cost),
                "selling_price": parseFloat(r.selling),
                "recipe_ingredients": r.recipe_ingredients,
                "ingredients": r.ingredients,
                "packaging": r.packaging,
                "recipe_yield": r.yield,
                "stock_on_hand": input_stock.value,
                "sub_dept": sub_dept_input.value
            });
            send_data(data, "Sending recipe to server...", () => {
                if (current_view == "stock") {
                    packaging = null;
                    recipes = null;
                    products = null;
                    setTimeout(render_stock, 100);
                }else{
                    get_data("recipes", "Getting recipes from server...", current_store, current_recipebook);
                }

            })
        }

        content.appendChild(save_button);

    } else {
        content.style.textAlign = "right";
        content.style.display = "grid";
        content.style.gridTemplateColumns = "1fr 1fr";
        content.style.width = "fit-content";
        content.style.alignItems = "center";

        // Product code input
        let product_code_input_label = document.createElement("label");
        product_code_input_label.className = "text-input-label";
        product_code_input_label.htmlFor = "new_product_code";
        product_code_input_label.innerHTML = "Product Code";
        content.appendChild(product_code_input_label);
        let product_code_input = document.createElement("input");
        product_code_input.id = "new_product_code";
        product_code_input.type = "text";
        product_code_input.className = "text-input";
        content.appendChild(product_code_input);


        // Packing qty input
        const input_packing_qty_label = document.createElement("label");
        input_packing_qty_label.className = "text-input-label";
        input_packing_qty_label.htmlFor = "new_packing_qty";
        input_packing_qty_label.innerHTML = "Packing quantity";
        content.appendChild(input_packing_qty_label);
        const input_packing_qty = document.createElement("input");
        input_packing_qty.id = "new_packing_qty";
        input_packing_qty.type = "number";
        input_packing_qty.min = 1;
        input_packing_qty.className = "text-input";
        content.appendChild(input_packing_qty);
        input_packing_qty.addEventListener("input", ()=>{update_cost_per_unit()});

        // Unit of measure input (Only for products)
        const uom_input_label = document.createElement("label");
        uom_input_label.className = "text-input-label";
        uom_input_label.htmlFor = "unit_of_measure";
        uom_input_label.innerHTML = "Unit of measure";
        const uom_input = document.createElement("input");
        uom_input.id = "unit_of_measure";
        uom_input.type = "text";
        uom_input.className = "text-input";
        uom_input.value = "unit";
        if (t == "product") {
            content.append(uom_input_label, uom_input);
        }
        uom_input.addEventListener("input", ()=>{update_cost_per_unit()});

        // Cost
        const input_cost_label = document.createElement("label");
        input_cost_label.className = "text-input-label";
        input_cost_label.htmlFor = "new_cost";
        input_cost_label.innerHTML = "Cost";
        content.appendChild(input_cost_label);
        const input_cost = document.createElement("input");
        input_cost.id = "new_cost";
        input_cost.type = "number";
        input_cost.min = 0;
        input_cost.step = 0.01;
        input_cost.className = "text-input";
        content.appendChild(input_cost);
        input_cost.addEventListener("input", ()=> {update_cost_per_unit()});

        // Cost per unit
        const cost_per_unit_label = document.createElement("label");
        cost_per_unit_label.className = "text-input-label";
        cost_per_unit_label.htmlFor = "cost_per_unit";
        cost_per_unit_label.innerHTML = "Cost per unit"
        const cost_per_unit = document.createElement("div");
        cost_per_unit.id = "cost_per_unit";
        cost_per_unit.style.fontSize = "medium";
        cost_per_unit.style.paddingRight = "10px";
        function update_cost_per_unit() {
            if (input_packing_qty.value > 0) {
                cost_per_unit.innerHTML = zar(input_cost.value / input_packing_qty.value) + " per " + uom_input.value;
            }
        }
        content.append(cost_per_unit_label, cost_per_unit);

        // Stock on hand
        let input_stock_label = document.createElement("label");
        input_stock_label.className = "text-input-label";
        input_stock_label.htmlFor = "new_stock";
        input_stock_label.innerHTML = "Stock on hand";
        content.appendChild(input_stock_label);
        let input_stock = document.createElement("input");
        input_stock.id = "new_cost";
        input_stock.type = "number";
        input_stock.min = 0;
        input_stock.step = 0.01;
        input_stock.className = "text-input";
        input_stock.value = 0;
        content.appendChild(input_stock);

        // Checkbox to check if item should be visible to whole store
        // THIS IS CURRENTLY HIDDEN BECAUSE IT IS NOT USED
        let input_checkbox = document.createElement("input")
        input_checkbox.id = "store_visible";
        input_checkbox.type = "checkbox";
        input_checkbox.hidden = true;
        content.appendChild(input_checkbox);
        let input_checkbox_label = document.createElement("label");
/* 
        input_checkbox_label.className = "text-input-label";
        input_checkbox_label.htmlFor = "store_visible";
        input_checkbox_label.innerHTML = "Visible for whole store?";
        content.appendChild(input_checkbox_label); */

        // TODO? Auto update field for price per quantity???
    
        // Populate items if we are rendering an existing item
        let todo = "create";
        let id = -1;
        if (existing_item) {
            todo = "modify";
            input_name.value = response.item.name;
            input_scale.value = response.item.scale_code;
            product_code_input.value = response.item.product_code;
            input_packing_qty.value = response.item.packing_qty;
            input_cost.value = response.item.cost;
            id = response.item.id;
            input_checkbox.checked = response.store_visible;
            input_checkbox.disabled = true;
            input_stock.value = response.item.stock_on_hand;
            sub_dept_input.value = response.item.sub_dept;
            uom_input.value = response.item.unit_of_measure;
            update_cost_per_unit();
        }

        // Save button
        let save_button = document.createElement("button");
        save_button.className = "button green-bg";
        save_button.innerHTML = "Save";
        save_button.onclick = function() {
            add_window_container.remove();
            const data = JSON.stringify({
                "todo": todo,
                "what": t,
                "id": id,
                "name": input_name.value,
                "scale_code": input_scale.value,
                "product_code": product_code_input.value,
                "packing_qty": input_packing_qty.value,
                "cost": input_cost.value,
                "store_visible": input_checkbox.checked,
                "store": current_store,
                "recipe_book": current_recipebook,
                "stock_on_hand": input_stock.value,
                "sub_dept": sub_dept_input.value,
                "unit_of_measure": uom_input.value
            });
            // let recipes = null;
            if (t == "product") {f = function() {get_data("products", "Getting products...", current_store, current_recipebook)}};
            if (t == "packaging") {f = function() {get_data("packaging", "Getting packaging...", current_store, current_recipebook)}};
            send_data(data, "Sending new item to server...", () => {
                if (current_view == "stock") {
                    packaging = null;
                    products = null;
                    setTimeout(render_stock, 100);
                }
                else (f())
            });
        }
        content.appendChild(save_button);

    }

    // Add used in and delete button for existing items:
    if (existing_item) {
        // Add used in button

        let used_in_button = document.createElement("button");
        used_in_button.innerHTML = "Not used in any recipes";
        used_in_button.className = "button disabled";
        content.appendChild(used_in_button);
        if (response.used_in.length > 0) {
            used_in_button.className = "button blue-bg";
            used_in_button.innerHTML = "Used in?";
            used_in_button.onclick = function() {show_popup(response.used_in.join("<br>"), true)};
        }
        // Add delete button
        let delete_button = document.createElement("button");
        delete_button.className = "button black-bg";
        delete_button.innerHTML = "Delete";
        delete_button.onclick = function() {
            let message = "Are you sure you want to delete this item?";
            if (response.used_in.length > 0) {
                message += "<br>This item is still used in " + response.used_in.length + " recipe(s).";
            }
            confirm_dialog(message, () => {
                add_window_container.remove();
                let id;
                if (t == "recipe") {id = response.id}
                else {id = response.item.id}
                recipes = null;
                packaging = null;
                products = null;
                let func;
                if (t == "product") {func = function() {get_data("products", "Getting products...", current_store, current_recipebook)}}
                if (t == "packaging") {func = function() {get_data("packaging", "Getting packaging...", current_store, current_recipebook)}}
                if (t == "recipe") {func = function() {get_data("recipes", "Getting recipes...", current_store, current_recipebook)}}
                data = JSON.stringify({
                    "todo": "delete",
                    "what": t,
                    "id": id,
                })
                send_data(data, "Deleting item...", () => {
                    setTimeout(func, 100);
                })
            });
        };
        content.appendChild(delete_button);
    }

    return content;
}

function render_add_contents_window(contents, content_type, recipe) {
    add_contents_window_container = document.createElement("div");
    add_contents_window_container.className = "add-window-container";
    add_contents_window = document.createElement("div");
    add_contents_window.className = "add-window";
    add_contents_window.style.width = "fit-content";
    add_contents_window_container.appendChild(add_contents_window);

    add_contents_window_container.addEventListener("keydown", (key)=> {
        if (key.key == "Escape") {
            add_contents_window_container.remove();
        }
    })

    // Add close button
    const window_close_button = document.createElement("div");
    window_close_button.className = "window-close-button";
    window_close_button.innerHTML = "X";
    window_close_button.addEventListener("click", ()=>{add_contents_window_container.remove()})
    add_contents_window_container.append(window_close_button);
    // Observe window changes so that the close button move with the window
    const observer = new ResizeObserver(entries => {
        rect = add_contents_window.getBoundingClientRect();
        window_close_button.style.top = rect.top - 10;
        window_close_button.style.left = rect.right - 12;
    })
    observer.observe(add_contents_window);
    observer.observe(document.body);

    // Create onclick functions
    if (content_type == "recipes") {
        onclickfunction = function(id) {
            recipe.add_recipe_ingredient(id);
            add_contents_window_container.remove();
            render_ingredients_table(document.getElementById("ingredients_table_holder"), recipe);
        }
    };
    if (content_type == "products") {
        onclickfunction = function(id) {
            recipe.add_ingredient(id);
            add_contents_window_container.remove();
            render_ingredients_table(document.getElementById("ingredients_table_holder"), recipe);
        }
    };
    if (content_type == "packaging") {
        onclickfunction = function(id) {
            recipe.add_packaging(id)
            add_contents_window_container.remove()
            render_ingredients_table(document.getElementById("ingredients_table_holder"), recipe);
        }
    };

    let table = document.createElement("table");
    table.className = "bt-table";

    // Create cancel button
    let close_button = document.createElement("button");
    close_button.className = "button red-bg";
    close_button.innerHTML = "Cancel";
    close_button.onclick = function() {add_contents_window_container.remove()};
    add_contents_window.appendChild(close_button);

    // Create filter input
    let thead = table.createTHead();
    let header_row = thead.insertRow();
    let header_cell = document.createElement("TH");
    let filterbox = document.createElement("input");
    filterbox.id = "filterbox";
    filterbox.placeholder = "Filter";
    filterbox.className = "text-input";
    
    // Focus on filter element
    setTimeout(()=>{filterbox.focus()}, 200);

    header_cell.style.textAlign = "center";
    header_cell.appendChild(filterbox);
    header_row.appendChild(header_cell);
    header_row.cells[0].colSpan = 2;
    
    // Create rows
    let tbody = table.createTBody();
    for (row in contents["data"]) {
        const new_row = tbody.insertRow();
        let id = contents.data[row]["id"];
        new_row.onclick = function() {onclickfunction(id)}
        for (cell in contents.data[row]) {
            if (cell == "name" || cell == "product_code") {
                const new_cell = new_row.insertCell();
                new_cell.innerHTML = contents.data[row][cell];
            }
        }
    }
    add_contents_window.appendChild(table);

    // Add filter function when filter input change
    filterbox.oninput = function() {
        for (row of tbody.childNodes) {
            if (!row.childNodes)
                continue
            let displayRow = false
            for (const e of row.childNodes) {
                if (e.innerHTML.toUpperCase().includes(filterbox.value.toUpperCase())) {
                    displayRow = true;
                    break
                }
            }
            if (displayRow)
                row.style.display = "table-row"
            else
                row.style.display = "none"
        }
    }

    return add_contents_window_container;
}

// Render recipe table.  e = element to render to, select_item = ID of element that should be selected after rendering
function render_ingredients_table(e, recipe, select_item) {
    // Clear e.innerHTML
    e.innerHTML = "";

    // Reset recipe cost, will be calculated during table creation
    recipe.total_cost = 0.0;

    // ----------RECIPE INGREDIENTS----------------
    // Title and table header
    if (recipe.recipe_ingredients.length > 0) {
        let recipe_ingredients_header = document.createElement("h3");
        recipe_ingredients_header.innerHTML = "Recipe Ingrediens:";
        e.appendChild(recipe_ingredients_header);
        let recipe_ingredients_table = document.createElement("table")
        recipe_ingredients_table.className = "bt-table";
        let recipe_ingredients_table_header = create_headers(false);
        recipe_ingredients_table.appendChild(recipe_ingredients_table_header)
        // Table
        recipe_ingredients_table_body = create_body(recipe, "recipe_ingredients");
        recipe_ingredients_table.appendChild(recipe_ingredients_table_body);
        e.appendChild(recipe_ingredients_table);
    }
    // ---------PRODUCT INGREDIENTS----------------
    if (recipe.ingredients.length > 0) {
        let product_ingredients_header = document.createElement("h3");
        product_ingredients_header.innerHTML = "Product Ingrediens:";
        e.appendChild(product_ingredients_header);
        let product_ingredients_table = document.createElement("table")
        product_ingredients_table.className = "bt-table";
        let product_ingredients_table_header = create_headers(true);
        product_ingredients_table.appendChild(product_ingredients_table_header)
        // Table
        product_ingredients_table_body = create_body(recipe, "ingredients");
        product_ingredients_table.appendChild(product_ingredients_table_body);
        e.appendChild(product_ingredients_table);   
    }
    // ---------PACKAGING INGREDIENTS---------------
    if (recipe.packaging.length > 0) {
        let packaging_ingredients_header = document.createElement("h3");
        packaging_ingredients_header.innerHTML = "Packaging Ingrediens:";
        e.appendChild(packaging_ingredients_header);
        let packaging_ingredients_table = document.createElement("table")
        packaging_ingredients_table.className = "bt-table";
        let packaging_ingredients_table_header = create_headers(true);
        packaging_ingredients_table.appendChild(packaging_ingredients_table_header)
        // Table
        packaging_ingredients_table_body = create_body(recipe, "packaging");
        packaging_ingredients_table.appendChild(packaging_ingredients_table_body);
        e.appendChild(packaging_ingredients_table);
    }

    // Add yield input and label
    let yield_input_label = document.createElement("label");
    yield_input_label.className = "text-input-label";
    yield_input_label.style.fontSize = "large";
    yield_input_label.htmlFor = "yield_input";
    yield_input_label.innerHTML = "Recipe yield: ";
    e.appendChild(yield_input_label);
    let yield_input = document.createElement("input");
    yield_input.id = "selling_input";
    yield_input.className = "text-input";
    yield_input.style.width = "100px";
    yield_input.value = recipe.yield;
    e.appendChild(yield_input);

    // Divide recipe cost by yield to get cost per unit
    recipe.cost = (recipe.total_cost - recipe.packaging_cost) / recipe.yield + recipe.packaging_cost;

    // Render costs
    let costs_div = document.createElement("div");
    e.appendChild(costs_div);
    create_costs(costs_div);

    // Add VAT exclusive selling price
    let selling_without_vat = document.createElement("div");
    selling_without_vat.className = "recipe-totals";
    selling_without_vat.style.fontWeight = "bold";
    selling_without_vat.innerHTML = "Selling without VAT: " + zar(recipe.selling / 1.15);
    e.appendChild(selling_without_vat);

    // Add selling price input and label
    let selling_input_label = document.createElement("label");
    selling_input_label.className = "text-input-label";
    selling_input_label.style.fontSize = "larger";
    selling_input_label.htmlFor = "sellling_input";
    selling_input_label.innerHTML = "Selling price: R";
    e.appendChild(selling_input_label);
    let selling_input = document.createElement("input");
    selling_input.id = "selling_input";
    selling_input.className = "text-input";
    selling_input.style.width = "100px";
    selling_input.style.fontSize = "larger";
    selling_input.value = recipe.selling;
    e.appendChild(selling_input);

    // Add GP amount and %
    let gp_output = document.createElement("h3");
    create_totals(gp_output, selling_input.value, recipe);
    e.appendChild(gp_output);

    // Select the item specified in select_item
    if (select_item) {
        document.getElementById(select_item).focus();
    }

    selling_input.onkeyup = function(key) {
        let keys = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "Enter", "Tab", "Backspace"]
        if (keys.includes(key.key)) {
            create_totals(gp_output, selling_input.value, recipe);
        }
    }
    yield_input.onkeyup = function(key) {
        let keys = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "Enter", "Tab", "Backspace"]
        if (keys.includes(key.key)) {
            recipe.yield = yield_input.value;
            recipe.cost = (recipe.total_cost - recipe.packaging_cost) / recipe.yield + recipe.packaging_cost;
            create_costs(costs_div);
        }
    }


    // ---------------FUNCTIONS--------------------
    // Function to render recipe costs
    function create_costs(e) {
        // Add cost without packaging
        e.innerHTML = "";
        let total_without_packaging = document.createElement("div");
        total_without_packaging.className = "recipe-totals";
        total_without_packaging.innerHTML = "Cost without packaging: ";
        total_without_packaging.innerHTML += zar(recipe.cost - recipe.packaging_cost);
        e.appendChild(total_without_packaging);
        // Add cost grand total
        let grand_total = document.createElement("div");
        grand_total.className = "recipe-totals";
        grand_total.innerHTML = "Cost with packaging: ";
        grand_total.innerHTML += zar(recipe.cost);
        e.appendChild(grand_total);
    }

    // Function to calculate and render GP totals
    function create_totals(e, selling, recipe) {
        e.innerHTML = "";
        let gp = (selling / 1.15) - recipe.cost;
        let gp_percent = 0;
        if (selling > 0) {gp_percent = gp / (selling / 1.15) * 100};
        e.innerHTML = "GP = " + zar(gp) + " (" + gp_percent.toFixed(1) + "%)";
        recipe.selling = selling;
        selling_without_vat.innerHTML = "Selling without VAT: " + zar(recipe.selling / 1.15);
    }

    // Function to create table headers
    function create_headers(has_product_code) {
        let headers = document.createElement("THEAD");
        let header_row = headers.insertRow();
        let header_names = [];
        if (has_product_code)
            header_names.push("Product code");
        header_names.push("Item", "Cost", "Qty", "Total", "Delete");
        for (h in header_names) {
            let cell = document.createElement("TH");
            cell.innerHTML = header_names[h];
            header_row.appendChild(cell);
        }
        return headers;
    }
    // Function to create table body
    function create_body(recipe, what) {
        let body = document.createElement("TBODY");
        let data = null;
        let items = null;
        if (what == "recipe_ingredients") {
            data = recipe.recipe_ingredients;
            items = recipes;
        };
        if (what == "ingredients") {
            data = recipe.ingredients;
            items = products;
        };
        if (what == "packaging") {
            data = recipe.packaging;
            items = packaging;
        };
        let total = 0.0;
        let total_qty = 0.0;
        for (line in data) {
            let line_item = get_item(data[line][0], items)
            let row = body.insertRow();
            row.className = "recipe-ingredient-row"
            row.style.cursor = "default"     //TODO
            // Product Code for products and packaging
            if (what != "recipe_ingredients") {
                const product_code_cell = row.insertCell();
                const product_code_input = document.createElement("input");
                let product_code = line_item["product_code"] == "undefined" ? "" : line_item["product_code"];
                product_code_cell.style.display = "flex";
                product_code_input.className = "text-input";
                product_code_input.style.width = "150px";
                product_code_input.value = product_code;
                product_code_cell.append(product_code_input)

                product_code_input.addEventListener("input", (event)=>{
                    if (event.target.value != product_code) {
                        product_code_input.style.borderColor = "blue";
                    }else{
                        product_code_input.style.borderColor = "#157946";
                    }
                })

                product_code_input.addEventListener("focusout", ()=>{update_product_code()})

                function update_product_code() {
                    if (product_code == product_code_input.value) {return}  // Only update if value is different
                    product_code = product_code_input.value;                // Update product code, else this update will run again even if value did not change
                    line_item["product_code"] = product_code               // Update local data
                    product_code_input.style.borderColor = "#157946";
                    data = JSON.stringify({
                        "todo": "modify",
                        "what": what == "packaging" ? what : "product",
                        "id": line_item["id"],
                        "name": line_item["name"],
                        "scale_code": line_item["scale_code"],
                        "product_code": product_code_input.value,
                        "sub_dept": line_item["sub_dept"],
                        "packing_qty": line_item["packing_qty"],
                        "cost": line_item["cost"],
                        "stock_on_hand": line_item["stock_on_hand"],
                        "unit_of_measure": line_item["unit_of_measure"]
                    })
                    send_data(data, "", (success)=>{
                        if (!success) {
                            product_code_input.style.borderColor = "red";
                        }
                    }, "Updating product code...")
                }
            }

            // Name
            let cell = row.insertCell();
            cell.innerHTML = line_item["name"];
            // Cost
            cell = row.insertCell();
            let line_total = line_item["unit_price"]
            if (what == "recipe_ingredients") {line_total = line_item["cost_per_unit"]}
            cell.innerHTML = zar(line_total)
            // Qty input
            cell = row.insertCell();
            let qty_input = document.createElement("input");
            qty_input.type = "number";
            qty_input.className = "text-input";
            qty_input.id = what + line_item["id"]
            qty_input.style.width = "90px";
            qty_input.style.margin = "0px";
            qty_input.value = data[line][1];
            total_qty += data[line][1];

            qty_input.onchange = function() {qty_changed()}

            // Function to re-render table and alter recipe object after qty of item is changed
            function qty_changed() {
                if (what == "recipe_ingredients") {recipe.change_recipe_ingredient(line_item["id"], parseFloat(qty_input.value))};
                if (what == "ingredients") {recipe.change_ingredient(line_item["id"], parseFloat(qty_input.value))};
                if (what == "packaging") {recipe.change_packaging(line_item["id"], parseFloat(qty_input.value))};
                render_ingredients_table(e, recipe, what + line_item["id"]);
            }

            line_total *= data[line][1];
            cell.append(qty_input);

            // Unit of measure for qty input, if products
            if (what == "ingredients") {
                uom_div = document.createElement("div");
                uom_div.innerHTML = line_item["unit_of_measure"];
                cell.style.display = "grid";
                cell.style.gridTemplateColumns = "1fr 1fr";
                cell.style.alignItems = "center";
                cell.style.gridColumnGap = "8px";
                cell.append(uom_div);
            }
            qty_input.onchange = function() {qty_changed();}
            // Line total
            cell = row.insertCell();
            cell.innerHTML = zar(line_total);
            total += line_total;

            // Delete ingredient button
            cell = row.insertCell();
            let delete_button = document.createElement("button");
            delete_button.className = "button red-bg";
            delete_button.style.width = "28px";
            delete_button.innerHTML = "X";
            delete_button.onclick = function() {
                if (what == "recipe_ingredients") {recipe.remove_recipe_ingredient(line_item["id"])};
                if (what == "ingredients") {recipe.remove_ingredient(line_item["id"])};
                if (what == "packaging") {recipe.remove_packaging(line_item["id"])};  
                render_ingredients_table(e, recipe);  
            }
            cell.appendChild(delete_button);
        }

        // TOTAL ROW
        let row = body.insertRow();
        row.style.fontWeight = "bold";
        // One blank cells for total row
        let cell = row.insertCell();
        // Total label cell
        cell = row.insertCell();
        cell.innerHTML = "Total";
        // Total qty cell
        cell = row.insertCell();
        cell.innerHTML = parseFloat(total_qty.toFixed(3));
        // Total amount cell
        cell = row.insertCell();
        cell.innerHTML = zar(total);
        // Add to total recipe cost
        recipe.total_cost += total;
        // Extra blank cell
        cell = row.insertCell();

        // If we calculated packaging cos, add that to recipe object
        if (what == "packaging") {recipe.packaging_cost = total};

        return body;

        // Function that returns the line item that matched the id.
        function get_item(id, items) {
            for (let item in items.data) {
                if (items.data[item]["id"] == id) {
                    return items.data[item];
                }
            }
        }
    }
}


class Recipe {
    constructor() {
        this.recipe_ingredients = [];
        this.ingredients = [];
        this.packaging = [];
        this.cost = 0.0;
        this.total_costs = 0.0;
        this.packaging_cost = 0.0;
        this.selling = 0.0;
        this.id = -1;
        this.yield = 1;
        this.stock_on_hand = 0;
    }
    add_recipe_ingredient(id) {
        for (let i in this.recipe_ingredients) {
            if (id == this.recipe_ingredients[i][0]) {
                show_message("Cannot add ingredient twice")
                id = -1;
                break;
            }
        }
        if (id >= 0) {this.recipe_ingredients.push([id, 1])}
    }
    add_ingredient(id) {
        for (let i in this.ingredients) {
            if (id == this.ingredients[i][0]) {
                show_message("Cannot add ingredient twice")
                id = -1;
                break;
            }
        }
        if (id >= 0) {this.ingredients.push([id, 1])}
    }
    add_packaging(id) {
        for (let i in this.packaging) {
            if (id == this.packaging[i][0]) {
                show_message("Cannot add ingredient twice")
                id = -1;
                break;
            }
        }
        if (id >= 0) {this.packaging.push([id, 1])}
    }

    remove_recipe_ingredient(id) {
        for (let i = 0; i < this.recipe_ingredients.length; i++) {
            if (this.recipe_ingredients[i][0] == id) {
                this.recipe_ingredients.splice(i,1);
            }
        }
    }
    remove_ingredient(id) {
        for (let i = 0; i < this.ingredients.length; i++) {
            if (this.ingredients[i][0] == id) {
                this.ingredients.splice(i,1);
            }
        }
    }
    remove_packaging(id) {
        for (let i = 0; i < this.packaging.length; i++) {
            if (this.packaging[i][0] == id) {
                this.packaging.splice(i,1);
            }
        }
    }

    change_recipe_ingredient(id, amount) {
        for (let i = 0; i < this.recipe_ingredients.length; i++) {
            if (this.recipe_ingredients[i][0] == id) {
                this.recipe_ingredients[i][1] = amount;
            }
        }
    }
    change_ingredient(id, amount) {
        for (let i = 0; i < this.ingredients.length; i++) {
            if (this.ingredients[i][0] == id) {
                this.ingredients[i][1] = amount;
            }
        }
    }
    change_packaging(id, amount) {
        for (let i = 0; i < this.packaging.length; i++) {
            if (this.packaging[i][0] == id) {
                this.packaging[i][1] = amount;
            }
        }
    }
}