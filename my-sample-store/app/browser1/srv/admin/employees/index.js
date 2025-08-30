
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

const position_options = [

    'Manager', 

    'Sales', 

    'Support', 

]



//
// data functions
//

function initEmployees(data) {
    let result = {
        employee_name: data.employee_name,

        position: data.position,

        hire_date: data.hire_date,

        email: data.email,

        phone_number: data.phone_number,

        salary: data.salary,


    }

    if (typeof data.id !== 'undefined') {
        result.id = data.id;
    }
    return result;
}

function exampleEmployees() {
    const data = {
			employee_name: 'David',
			position: 'Manager',
			hire_date: '2000-01-11T12:34:56',
			email: 'my-name@email.com',
			phone_number: '+1 (123) 456-7890',
			salary: 60000.0
    }
    return {...data}
}

function randomEmployees() {
    return {
		employee_name: random_person_name(),
		'position': randomStrEnum(position_options),

		'hire_date': randomStr(),

		email: random_email(),
		phone_number: random_phone_number(),
		'salary': randomFloat(),

    }
}

function verifyEmployees(data) {

    let result = {
        valid: true,
        errors: {}
    }

    if (typeof data.employee_name !== 'string') {
        result.error.employee_name = 'employee_name must be a string';
        result.valid = false;
    }


    if (typeof data.position !== 'string') {
        result.error.position = 'position must be a string';
        result.valid = false;
    }else if (!position_options.includes(data.position)) {
        result.error.position = 'invalid position';
        result.valid = false;
    }


    if (typeof data.hire_date !== 'string') {
        result.error.hire_date = 'hire_date must be a string';
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


    if (typeof data.salary !== 'number') {
        result.error.salary = 'salary must be a float';
        result.valid = false;
    }




    return result

}

function employeesFromInputTBody(tbody) {   
    console.log('employeesFromInputTBody', tbody);
    const data = {};

    // parse id if exists

    const idInput = tbody.querySelector('input[name="id"]');
    if (idInput) {
        data.id = idInput.value;
    }

    const employee_nameInput = tbody.querySelector('input[name="employee_name"]');
    data.employee_name = employee_nameInput.value;


    const positionInput = tbody.querySelector('select[name="position"]');
    data.position = positionInput.value;


    const hire_dateInput = tbody.querySelector('input[name="hire_date"]');
    data.hire_date = hire_dateInput.value;


    const emailInput = tbody.querySelector('input[name="email"]');
    data.email = emailInput.value;


    const phone_numberInput = tbody.querySelector('input[name="phone_number"]');
    data.phone_number = phone_numberInput.value;


    const salaryInput = tbody.querySelector('input[name="salary"]');
    data.salary = parseFloat(salaryInput.value);




    return data;
}

function employeesToInputTBody(data, tbody) {
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
    // employee_name - str
    //

    const employee_nameTdKey = document.createElement('td');
    employee_nameTdKey.textContent = 'employee_name';

    const employee_nameTdInput = document.createElement('td');
    const employee_nameInput = document.createElement('input');
    employee_nameInput.name = 'employee_name';
    employee_nameInput.value = data.employee_name || '';
    employee_nameInput.size = 35;
    employee_nameTdInput.appendChild(employee_nameInput);

    const employee_nameTdOther = document.createElement('td');
    employee_nameTdOther.textContent = '-';

    const employee_nameTr = document.createElement('tr');
    employee_nameTr.appendChild(employee_nameTdKey);
    employee_nameTr.appendChild(employee_nameTdInput);
    employee_nameTr.appendChild(employee_nameTdOther);

    tbody.appendChild(employee_nameTr);


    //
    // position - enum
    //

    const positionTdKey = document.createElement('td');
    positionTdKey.textContent = 'position';

    const positionTdInput = document.createElement('td');
    const positionInput = document.createElement('select');
    positionInput.name = 'position';
    for (const option of position_options) {
        const positionOption = document.createElement('option');
        positionOption.value = option;
        positionOption.textContent = option;
        if (option === data.position) {
            positionOption.selected = true;
        }
        positionInput.appendChild(positionOption);
    }
    positionTdInput.appendChild(positionInput);

    const positionTdOther = document.createElement('td');
    positionTdOther.textContent = '-';

    const positionTr = document.createElement('tr');
    positionTr.appendChild(positionTdKey);
    positionTr.appendChild(positionTdInput);
    positionTr.appendChild(positionTdOther);

    tbody.appendChild(positionTr);


    //
    // hire_date - str
    //

    const hire_dateTdKey = document.createElement('td');
    hire_dateTdKey.textContent = 'hire_date';

    const hire_dateTdInput = document.createElement('td');
    const hire_dateInput = document.createElement('input');
    hire_dateInput.name = 'hire_date';
    hire_dateInput.value = data.hire_date || '';
    hire_dateInput.size = 35;
    hire_dateTdInput.appendChild(hire_dateInput);

    const hire_dateTdOther = document.createElement('td');
    hire_dateTdOther.textContent = '-';

    const hire_dateTr = document.createElement('tr');
    hire_dateTr.appendChild(hire_dateTdKey);
    hire_dateTr.appendChild(hire_dateTdInput);
    hire_dateTr.appendChild(hire_dateTdOther);

    tbody.appendChild(hire_dateTr);


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


    //
    // salary - float
    //

    const salaryTdKey = document.createElement('td');
    salaryTdKey.textContent = 'salary';

    const salaryTdInput = document.createElement('td');
    const salaryInput = document.createElement('input');
    salaryInput.name = 'salary';
    salaryInput.type = 'number';
    salaryInput.size = 5;
    salaryInput.value = parseFloat(data.salary).toFixed(2);
    salaryInput.step = '.01';
    salaryTdInput.appendChild(salaryInput);

    const salaryTdOther = document.createElement('td');
    salaryTdOther.textContent = '-';

    const salaryTr = document.createElement('tr');
    salaryTr.appendChild(salaryTdKey);
    salaryTr.appendChild(salaryTdInput);
    salaryTr.appendChild(salaryTdOther);

    tbody.appendChild(salaryTr);




    return tbody;

}

function employeesToDisplayTBody(data, tbody) {
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
    // employee_name - str
    //

    const employee_nameTdKey = document.createElement('td');
    employee_nameTdKey.textContent = 'employee_name';

    const employee_nameTdValue = document.createElement('td');
    employee_nameTdValue.textContent = data.employee_name;

    const employee_nameTr = document.createElement('tr');
    employee_nameTr.appendChild(employee_nameTdKey);
    employee_nameTr.appendChild(employee_nameTdValue);

    tbody.appendChild(employee_nameTr);


    //
    // position - enum
    //

    const positionTdKey = document.createElement('td');
    positionTdKey.textContent = 'position';

    const positionTdValue = document.createElement('td');
    positionTdValue.textContent = data.position;

    const positionTr = document.createElement('tr');
    positionTr.appendChild(positionTdKey);
    positionTr.appendChild(positionTdValue);

    tbody.appendChild(positionTr);


    //
    // hire_date - str
    //

    const hire_dateTdKey = document.createElement('td');
    hire_dateTdKey.textContent = 'hire_date';

    const hire_dateTdValue = document.createElement('td');
    hire_dateTdValue.textContent = data.hire_date;

    const hire_dateTr = document.createElement('tr');
    hire_dateTr.appendChild(hire_dateTdKey);
    hire_dateTr.appendChild(hire_dateTdValue);

    tbody.appendChild(hire_dateTr);


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


    //
    // salary - float
    //

    const salaryTdKey = document.createElement('td');
    salaryTdKey.textContent = 'salary';

    const salaryTdValue = document.createElement('td');
    salaryTdValue.textContent = data.salary;
    
    const salaryTr = document.createElement('tr');
    salaryTr.appendChild(salaryTdKey);
    salaryTr.appendChild(salaryTdValue);

    tbody.appendChild(salaryTr);




    return tbody;
}

function employeesToTableRow(data) {

    const tr = document.createElement('tr');
    tr.style.cursor = 'pointer';
    tr.onclick = () => window.location.href = `/admin/employees/${data.id}`

    // id - string

    const idTd = document.createElement('td');
    idTd.textContent = data.id;
    tr.appendChild(idTd);

    //
    // employee_name - str
    //

    const employee_nameTd = document.createElement('td');
    employee_nameTd.textContent = data.employee_name;
    tr.appendChild(employee_nameTd);


    //
    // position - enum
    //

    const positionTd = document.createElement('td');
    positionTd.textContent = data.position;
    tr.appendChild(positionTd);


    //
    // hire_date - str
    //

    const hire_dateTd = document.createElement('td');
    hire_dateTd.textContent = data.hire_date;
    tr.appendChild(hire_dateTd);


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


    //
    // salary - float
    //

    const salaryTd = document.createElement('td');
    salaryTd.textContent = data.salary;
    tr.appendChild(salaryTd);




    return tr;

}

function employeesListToDisplayTBody(employeesList, tbody) {

    tbody.innerHTML = '';

    for (const employees of employeesList) {
        tbody.appendChild(employeesToTableRow(employees));
    }

    return tbody;

}

//
// serialize functions
//

function employeesForJSON(data) {
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

function clientCreateEmployees(data) {
    
    return fetch('/api/admin/employees', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
}

function clientReadEmployees(id) {

    return fetch(`/api/admin/employees/${id}`, {
        method: 'GET',
    })
}

function clientUpdateEmployees(id, data) {

    return fetch(`/api/admin/employees/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })

}

function clientDeleteEmployees(id) {

    return fetch(`/api/admin/employees/${id}`, {
        method: 'DELETE',
    })

}

function clientListEmployeess(offset, size) {

    return fetch(`/api/admin/employees?offset=${offset}&size=${size}`, {
        method: 'GET',
    })
}