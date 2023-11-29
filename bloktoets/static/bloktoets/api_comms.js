// --------------------------API fetcher--------------------------------------
function get_data(what, loading_message="Loading...", id=false, recipebook=false, render=true) {
    // ID is used for store ID or product ID
    let popup = show_popup(loading_message)
    url = "/bt_api?get=" + what;
    if (id) {url += "&id=" + id}
    if (recipebook) {url += "&recipebook=" + recipebook}
    fetch(url)
    .then(response => response.json())
    .then(response => {
        popup.remove();
        if (response["status"] == "failed") {
            show_message(response["error"],)
        };
        if (what == "stores") {
            stores = response;
            if (render) {render_stores(response)};
        }
        if (what == "recipebook") {
            recipebooks = response;
            if (render) {render_recipebooks(response)};
        }
        if (what == "recipes") {
            recipes = response;
            if (render) {render_recipes(response)};
        }
        if (what == "products") {
            products = response;
            if (render) {render_products(response)};
        }
        if (what == "packaging") {
            packaging = response;
            if (render) {render_packaging(response)};
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
    })
    .catch(error => {
        console.error(error);
        popup.remove();
        show_message("Error getting data from server",);
    })
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
        else if (response['status'] == "failed") {show_message(response['error'])}
        else {show_message("Error may have occurred. Check data.")};
        f();
    })
    .catch(error => {
        console.error(error);
        popup.remove();
        show_message("Error sending data to the server");
    })




}