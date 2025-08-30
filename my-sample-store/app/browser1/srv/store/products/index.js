
//
// convert
//

const trueBoolStrings = ['1', 'true', 't', 'yes', 'y', 'on'];

function convertListElementBool(input) {
    return trueBoolStrings.includes(input.toLowerCase());
}

function convertListElementInt(input) {
    return parseInt(input);
}

function convertListElementFloat(input) {
    const split = input.split('.');
    if (split.length > 2) {
        throw new Error('Invalid float');
    }
    let result = parseFloat(input)
    if (parseInt(split[1]) === 0) {
        result += 0.0000001;
    }
    
    return result;
}

function convertListElementEnum(input) {
    return input;
}

function convertListElementStr(str) {
    return str;
}

function convertListElementDatetime(input) {
    const date = new Date(input);
    if (isNaN(date.getTime())) {
        throw new Error('Invalid datetime');
    }
    return date;
}

//
// defs
//



//
// data functions
//

function initProducts(data) {
    let result = {
        product_name: data.product_name,

        price: data.price,

        in_stock: data.in_stock,


    }

    if (typeof data.id !== 'undefined') {
        result.id = data.id;
    }
    return result;
}

function exampleProducts() {
    const data = {
			product_name: 'Laptop',
			price: 999.99,
			in_stock: true
    }
    return {...data}
}

function randomProducts() {
    return {
		product_name: random_thing_name(),
		'price': randomFloat(),

		'in_stock': randomBool(),

    }
}

function verifyProducts(data) {

    let result = {
        valid: true,
        errors: {}
    }

    if (typeof data.product_name !== 'string') {
        result.error.product_name = 'product_name must be a string';
        result.valid = false;
    }


    if (typeof data.price !== 'number') {
        result.error.price = 'price must be a float';
        result.valid = false;
    }


    if (typeof data.in_stock !== 'boolean') {
        result.error.in_stock = 'in_stock must be a boolean';
        result.valid = false;
    }




    return result

}

function productsFromInputTBody(tbody) {   
    console.log('productsFromInputTBody', tbody);
    const data = {};

    // parse id if exists

    const idInput = tbody.querySelector('input[name="id"]');
    if (idInput) {
        data.id = idInput.value;
    }

    const product_nameInput = tbody.querySelector('input[name="product_name"]');
    data.product_name = product_nameInput.value;


    const priceInput = tbody.querySelector('input[name="price"]');
    data.price = parseFloat(priceInput.value);


    const in_stockInput = tbody.querySelector('input[name="in_stock"]');
    data.in_stock = in_stockInput.checked;




    return data;
}

function productsToInputTBody(data, tbody) {
    tbody.innerHTML = '';

    // show id if present

    if (typeof data.id !== 'undefined') {
        const idTdKey = document.createElement('td');
        idTdKey.textContent = 'id';

        const idTdInput = document.createElement('td');
        const idInput = document.createElement('input');
        idInput.name = 'id';
        idInput.value = data.id;
        idInput.size = 35;
        idInput.readOnly = true;
        idTdInput.appendChild(idInput);

        const idTdOther = document.createElement('td');
        idTdOther.textContent = '-';

        const idTr = document.createElement('tr');
        idTr.appendChild(idTdKey);
        idTr.appendChild(idTdInput);
        idTr.appendChild(idTdOther);

        tbody.appendChild(idTr);
    }


    //
    // product_name - str
    //

    const product_nameTdKey = document.createElement('td');
    product_nameTdKey.textContent = 'product_name';

    const product_nameTdInput = document.createElement('td');
    const product_nameInput = document.createElement('input');
    product_nameInput.name = 'product_name';
    product_nameInput.value = data.product_name || '';
    product_nameInput.size = 35;
    product_nameTdInput.appendChild(product_nameInput);

    const product_nameTdOther = document.createElement('td');
    product_nameTdOther.textContent = '-';

    const product_nameTr = document.createElement('tr');
    product_nameTr.appendChild(product_nameTdKey);
    product_nameTr.appendChild(product_nameTdInput);
    product_nameTr.appendChild(product_nameTdOther);

    tbody.appendChild(product_nameTr);


    //
    // price - float
    //

    const priceTdKey = document.createElement('td');
    priceTdKey.textContent = 'price';

    const priceTdInput = document.createElement('td');
    const priceInput = document.createElement('input');
    priceInput.name = 'price';
    priceInput.type = 'number';
    priceInput.size = 5;
    priceInput.value = parseFloat(data.price).toFixed(2);
    priceInput.step = '.01';
    priceTdInput.appendChild(priceInput);

    const priceTdOther = document.createElement('td');
    priceTdOther.textContent = '-';

    const priceTr = document.createElement('tr');
    priceTr.appendChild(priceTdKey);
    priceTr.appendChild(priceTdInput);
    priceTr.appendChild(priceTdOther);

    tbody.appendChild(priceTr);


    //
    // in_stock - bool
    //

    const in_stockTdKey = document.createElement('td');
    in_stockTdKey.textContent = 'in_stock';

    const in_stockTdInput = document.createElement('td');
    const in_stockInput = document.createElement('input');
    in_stockInput.name = 'in_stock';
    in_stockInput.type = 'checkbox';
    in_stockInput.checked = data.in_stock;
    in_stockTdInput.appendChild(in_stockInput);

    const in_stockTdOther = document.createElement('td');
    in_stockTdOther.textContent = '-';

    const in_stockTr = document.createElement('tr');
    in_stockTr.appendChild(in_stockTdKey);
    in_stockTr.appendChild(in_stockTdInput);
    in_stockTr.appendChild(in_stockTdOther);

    tbody.appendChild(in_stockTr);




    return tbody;

}

function productsToDisplayTBody(data, tbody) {
    tbody.innerHTML = '';

    // id - string

    const idTdKey = document.createElement('td');
    idTdKey.textContent = 'id';

    const idTdValue = document.createElement('td');
    idTdValue.textContent = data.id;

    const idTr = document.createElement('tr');
    idTr.appendChild(idTdKey);
    idTr.appendChild(idTdValue);

    tbody.appendChild(idTr);

    //
    // product_name - str
    //

    const product_nameTdKey = document.createElement('td');
    product_nameTdKey.textContent = 'product_name';

    const product_nameTdValue = document.createElement('td');
    product_nameTdValue.textContent = data.product_name;

    const product_nameTr = document.createElement('tr');
    product_nameTr.appendChild(product_nameTdKey);
    product_nameTr.appendChild(product_nameTdValue);

    tbody.appendChild(product_nameTr);


    //
    // price - float
    //

    const priceTdKey = document.createElement('td');
    priceTdKey.textContent = 'price';

    const priceTdValue = document.createElement('td');
    priceTdValue.textContent = data.price;
    
    const priceTr = document.createElement('tr');
    priceTr.appendChild(priceTdKey);
    priceTr.appendChild(priceTdValue);

    tbody.appendChild(priceTr);


    //
    // in_stock - bool
    //

    const in_stockTdKey = document.createElement('td');
    in_stockTdKey.textContent = 'in_stock';

    const in_stockTdValue = document.createElement('td');
    in_stockTdValue.textContent = (data.in_stock) ? 'yes' : 'no';

    const in_stockTr = document.createElement('tr');
    in_stockTr.appendChild(in_stockTdKey);
    in_stockTr.appendChild(in_stockTdValue);

    tbody.appendChild(in_stockTr);




    return tbody;
}

function productsToTableRow(data) {

    const tr = document.createElement('tr');
    tr.style.cursor = 'pointer';
    tr.onclick = () => window.location.href = `/store/products/${data.id}`

    // id - string

    const idTd = document.createElement('td');
    idTd.textContent = data.id;
    tr.appendChild(idTd);

    //
    // product_name - str
    //

    const product_nameTd = document.createElement('td');
    product_nameTd.textContent = data.product_name;
    tr.appendChild(product_nameTd);


    //
    // price - float
    //

    const priceTd = document.createElement('td');
    priceTd.textContent = data.price;
    tr.appendChild(priceTd);


    //
    // in_stock - bool
    //

    const in_stockTd = document.createElement('td');
    in_stockTd.textContent = (data.in_stock) ? 'yes' : 'no';
    tr.appendChild(in_stockTd);




    return tr;

}

function productsListToDisplayTBody(productsList, tbody) {

    tbody.innerHTML = '';

    for (const products of productsList) {
        tbody.appendChild(productsToTableRow(products));
    }

    return tbody;

}

//
// serialize functions
//

function productsForJSON(data) {
    // convert an items types to be ready to JSON

    let result = {}
    for (const field in data) {
        if (Object.prototype.toString.call(data[field]) === '[object Date]') {
            result[field] = data[field].toISOString().split('.')[0];
        }else if (Array.isArray(data[field])) {
            result[field] = data[field].map((item) => {
                if (Object.prototype.toString.call(item) === '[object Date]') {
                    return item.toISOString().split('.')[0];
                }else{
                    return item;
                }
            });
        }else{
            result[field] = data[field];
        }
    }
    return result;
}

//
// client functions
//

function clientCreateProducts(data) {
    
    return fetch('/api/store/products', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
}

function clientReadProducts(id) {

    return fetch(`/api/store/products/${id}`, {
        method: 'GET',
    })
}

function clientUpdateProducts(id, data) {

    return fetch(`/api/store/products/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })

}

function clientDeleteProducts(id) {

    return fetch(`/api/store/products/${id}`, {
        method: 'DELETE',
    })

}

function clientListProductss(offset, size) {

    return fetch(`/api/store/products?offset=${offset}&size=${size}`, {
        method: 'GET',
    })
}