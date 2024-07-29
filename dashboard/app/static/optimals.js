const image_base_uri = 'static/assets/';
const json_base_uri = 'static/assets/';

class Optimals {
    static Slider = new Optimals('slider', 'Use slider', 'slider.png', null);
    static Matrix1 = new Optimals('matrix1', 'Use this optimal matrix', 'om_1.png', 'om_1.json');
    static Matrix2 = new Optimals('matrix2', 'Use this optimal matrix', 'om_2.png', 'om_2.json');

    constructor(name, description, image_uri, value_uri) {
        this.name = name;
        this.image_uri = image_base_uri + image_uri;
        this.value_uri = json_base_uri + value_uri;
        this.description = description;
    }

    toString() {
        return `Optimals.${this.name}`;
    }

    toHtml() {
        return `<div class="card"  id="${this.name}Card">
                    <img src="${this.image_uri}" class="card-img-top h-100" alt="...">
                    <div class="card-body">
                        <p class="card-text">${this.description}</p>
                    </div>
                </div>`;
    }

    static foreach(callback) {
        callback(this.Slider);
        callback(this.Matrix1);
        callback(this.Matrix2);
    }
}
