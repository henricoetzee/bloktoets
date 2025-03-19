// --------------------------API fetcher--------------------------------------
function get_data(what, loading_message="Loading...", id=false, recipebook=false, render=true) {
    // ID is used for store ID or product ID
    let popup = show_popup(loading_message);
    let url = "/bt_api/?get=" + what;
    if (id) {url += "&id=" + id}
    if (recipebook) {url += "&recipebook=" + recipebook}

    let request = new XMLHttpRequest;
    request.open("GET", url, false);
    request.onreadystatechange
    request.onload = () => {
        if (request.status == 200) {
            response = JSON.parse(request.responseText);
            popup.remove();
            if (response["status"] == "failed") {
                show_message(response["error"], "#EC1B24")
            };
            if (what == "stores") {
                stores = response;
                if (render) {setTimeout(render_stores, 100)};
            }
            if (what == "recipebook") {
                recipebooks = response;
                if (render) {setTimeout(render_recipebooks, 100)};
            }
            if (what == "recipes") {
                recipes = response;
                if (render) {setTimeout(render_recipes, 100)};
            }
            if (what == "products") {
                products = response;
                if (render) {setTimeout(render_products, 100)};
            }
            if (what == "packaging") {
                packaging = response;
                if (render) {setTimeout(render_packaging, 100)};
            }
            if (what == "product") {
                render_add_window("product", true, response)
            }
            if (what == "package") {
                render_add_window("packaging", true, response)
            }
            if (what == "recipe") {
                render_add_window("recipe", true, response)
            }
        }else{
            console.error(request.responseText);
            popup.remove();
            show_message("Error getting data from server", "#EC1B24");
        }
    }
    request.send(null)
    
}

//-----------------------------SEND DATA----------------------------//
function send_data(data, loading_message="Sending data...", f) {
    popup = show_popup(loading_message)
    fetch("/bt_api/", {
        method: "PUT",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: data,
        mode: 'same-origin'
    })
    .then(response => response.json())
    .then(response => {
        popup.remove();
        if (response['status'] == "success") {
            if (response['message']) {show_message(response['message'])
            }else{
                show_message("Success")
            }
        }
        else if (response['status'] == "failed") {show_message(response['error'], "#EC1B24")}
        else {show_message("Error may have occurred. Check data.")};
        if (f) {f();};
    })
    .catch(error => {
        console.error(error);
        popup.remove();
        show_message("Error sending data to the server");
    })
}