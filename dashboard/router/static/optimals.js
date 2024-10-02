let optimals = []

function get_optimal_from_name(name) {
    return optimals.find(optimal => optimal.name == name);
}

class Optimals {
    constructor(id, name, description, image_uri, value) {
        this.id = id
        this.name = name;
        this.description = description;
        this.image_uri = image_uri;
        this.value = value;
    }

    toString() {
        return `Optimals.${this.name}`;
    }

    toHtml() {
        return `<div class="card"  id="${this.id}Card">
                    <img src="${this.image_uri}" class="card-img-top h-100 rounded" alt="...">
                </div>`;
    }
}
