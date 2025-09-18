
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

function initCustomers(data) {
    let result = {
        customer_name: data.customer_name,

        email: data.email,

        phone_number: data.phone_number,


    }

    if (typeof data.id !== 'undefined') {
        result.id = data.id;
    }
    return result;
}

function exampleCustomers() {
    const data = {
			customer_name: 'Alice',
			email: 'alice@email.com',
			phone_number: '+1 (123) 456-7890'
    }
    return {...data}
}

function randomCustomers() {
    return {
		customer_name: random_person_name(),
		email: random_email(),
		phone_number: random_phone_number(),
    }
}

function verifyCustomers(data) {

    let result = {
        valid: true,
        errors: {}
    }

    if (typeof data.customer_name !== 'string') {
        result.error.customer_name = 'customer_name must be a string';
        result.valid = false;
    }


    if (typeof data.email !== 'string') {
        result.error.email = 'email must be a string';
        result.valid = false;
    }


    if (typeof data.phone_number !== 'string') {
        result.error.phone_number = 'phone_number must be a string';
        result.valid = false;
    }




    return result

}

function customersFromInputTBody(tbody) {   
    console.log('customersFromInputTBody', tbody);
    const data = {};

    // parse id if exists

    const idInput = tbody.querySelector('input[name="id"]');
    if (idInput) {
        data.id = idInput.value;
    }

    const customer_nameInput = tbody.querySelector('input[name="customer_name"]');
    data.customer_name = customer_nameInput.value;


    const emailInput = tbody.querySelector('input[name="email"]');
    data.email = emailInput.value;


    const phone_numberInput = tbody.querySelector('input[name="phone_number"]');
    data.phone_number = phone_numberInput.value;




    return data;
}

function customersToInputTBody(data, tbody) {
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
    // customer_name - str
    //

    const customer_nameTdKey = document.createElement('td');
    customer_nameTdKey.textContent = 'customer_name';

    const customer_nameTdInput = document.createElement('td');
    const customer_nameInput = document.createElement('input');
    customer_nameInput.name = 'customer_name';
    customer_nameInput.value = data.customer_name || '';
    customer_nameInput.size = 35;
    customer_nameTdInput.appendChild(customer_nameInput);

    const customer_nameTdOther = document.createElement('td');
    customer_nameTdOther.textContent = '-';

    const customer_nameTr = document.createElement('tr');
    customer_nameTr.appendChild(customer_nameTdKey);
    customer_nameTr.appendChild(customer_nameTdInput);
    customer_nameTr.appendChild(customer_nameTdOther);

    tbody.appendChild(customer_nameTr);


    //
    // email - str
    //

    const emailTdKey = document.createElement('td');
    emailTdKey.textContent = 'email';

    const emailTdInput = document.createElement('td');
    const emailInput = document.createElement('input');
    emailInput.name = 'email';
    emailInput.value = data.email || '';
    emailInput.size = 35;
    emailTdInput.appendChild(emailInput);

    const emailTdOther = document.createElement('td');
    emailTdOther.textContent = '-';

    const emailTr = document.createElement('tr');
    emailTr.appendChild(emailTdKey);
    emailTr.appendChild(emailTdInput);
    emailTr.appendChild(emailTdOther);

    tbody.appendChild(emailTr);


    //
    // phone_number - str
    //

    const phone_numberTdKey = document.createElement('td');
    phone_numberTdKey.textContent = 'phone_number';

    const phone_numberTdInput = document.createElement('td');
    const phone_numberInput = document.createElement('input');
    phone_numberInput.name = 'phone_number';
    phone_numberInput.value = data.phone_number || '';
    phone_numberInput.size = 35;
    phone_numberTdInput.appendChild(phone_numberInput);

    const phone_numberTdOther = document.createElement('td');
    phone_numberTdOther.textContent = '-';

    const phone_numberTr = document.createElement('tr');
    phone_numberTr.appendChild(phone_numberTdKey);
    phone_numberTr.appendChild(phone_numberTdInput);
    phone_numberTr.appendChild(phone_numberTdOther);

    tbody.appendChild(phone_numberTr);




    return tbody;

}

function customersToDisplayTBody(data, tbody) {
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
    // customer_name - str
    //

    const customer_nameTdKey = document.createElement('td');
    customer_nameTdKey.textContent = 'customer_name';

    const customer_nameTdValue = document.createElement('td');
    customer_nameTdValue.textContent = data.customer_name;

    const customer_nameTr = document.createElement('tr');
    customer_nameTr.appendChild(customer_nameTdKey);
    customer_nameTr.appendChild(customer_nameTdValue);

    tbody.appendChild(customer_nameTr);


    //
    // email - str
    //

    const emailTdKey = document.createElement('td');
    emailTdKey.textContent = 'email';

    const emailTdValue = document.createElement('td');
    emailTdValue.textContent = data.email;

    const emailTr = document.createElement('tr');
    emailTr.appendChild(emailTdKey);
    emailTr.appendChild(emailTdValue);

    tbody.appendChild(emailTr);


    //
    // phone_number - str
    //

    const phone_numberTdKey = document.createElement('td');
    phone_numberTdKey.textContent = 'phone_number';

    const phone_numberTdValue = document.createElement('td');
    phone_numberTdValue.textContent = data.phone_number;

    const phone_numberTr = document.createElement('tr');
    phone_numberTr.appendChild(phone_numberTdKey);
    phone_numberTr.appendChild(phone_numberTdValue);

    tbody.appendChild(phone_numberTr);




    return tbody;
}

function customersToTableRow(data) {

    const tr = document.createElement('tr');
    tr.style.cursor = 'pointer';
    tr.onclick = () => window.location.href = `/store/customers/${data.id}`

    // id - string

    const idTd = document.createElement('td');
    idTd.textContent = data.id;
    tr.appendChild(idTd);

    //
    // customer_name - str
    //

    const customer_nameTd = document.createElement('td');
    customer_nameTd.textContent = data.customer_name;
    tr.appendChild(customer_nameTd);


    //
    // email - str
    //

    const emailTd = document.createElement('td');
    emailTd.textContent = data.email;
    tr.appendChild(emailTd);


    //
    // phone_number - str
    //

    const phone_numberTd = document.createElement('td');
    phone_numberTd.textContent = data.phone_number;
    tr.appendChild(phone_numberTd);




    return tr;

}

function customersListToDisplayTBody(customersList, tbody) {

    tbody.innerHTML = '';

    for (const customers of customersList) {
        tbody.appendChild(customersToTableRow(customers));
    }

    return tbody;

}

//
// serialize functions
//

function customersForJSON(data) {
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

function clientCreateCustomers(data) {
    
    return fetchWithSession('/api/store/customers', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
}

function clientReadCustomers(id) {

    return fetchWithSession('/api/store/customers/' + id, {
        method: 'GET',
    })
}

function clientUpdateCustomers(id, data) {

    return fetchWithSession(`/api/store/customers/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })

}

function clientDeleteCustomers(id) {

    return fetchWithSession(`/api/store/customers/${id}`, {
        method: 'DELETE',
    })

}

function clientListCustomerss(offset, size) {

    return fetchWithSession(`/api/store/customers?offset=${offset}&size=${size}`, {
        method: 'GET',
    })
}