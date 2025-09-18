
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

function initEvent(data) {
    let result = {
        user_id: data.user_id,

        event_name: data.event_name,

        event_date: new Date(data.event_date),

        location: data.location,

        description: data.description,


    }

    if (typeof data.id !== 'undefined') {
        result.id = data.id;
    }
    return result;
}

function exampleEvent() {
    const data = {
			user_id: '1',
			event_name: 'Birthday Party',
			event_date: new Date('2023-10-15T18:00:00'),
			location: 'Central Park',
			description: 'Join us for a fun birthday celebration!'
    }
    return {...data}
}

function randomEvent() {
    return {
		'event_name': randomStr(),

		'event_date': randomDatetime(),

		'location': randomStr(),

		'description': randomStr(),

    }
}

function verifyEvent(data) {

    let result = {
        valid: true,
        errors: {}
    }

    if (typeof data.user_id !== 'string') {
        result.error.user_id = 'user_id must be a string';
        result.valid = false;
    }


    if (typeof data.event_name !== 'string') {
        result.error.event_name = 'event_name must be a string';
        result.valid = false;
    }


    if (Object.prototype.toString.call(data.event_date) !== '[object Date]') {
        result.error.event_date = 'event_date must be a datetime';
        result.valid = false;
    }

    if (typeof data.location !== 'string') {
        result.error.location = 'location must be a string';
        result.valid = false;
    }


    if (typeof data.description !== 'string') {
        result.error.description = 'description must be a string';
        result.valid = false;
    }




    return result

}

function eventFromInputTBody(tbody) {   
    console.log('eventFromInputTBody', tbody);
    const data = {};

    // parse id if exists

    const idInput = tbody.querySelector('input[name="id"]');
    if (idInput) {
        data.id = idInput.value;
    }

    const user_idInput = tbody.querySelector('input[name="user_id"]');
    data.user_id = user_idInput ? user_idInput.value : '';


    const event_nameInput = tbody.querySelector('input[name="event_name"]');
    data.event_name = event_nameInput.value;


    const event_dateInput = tbody.querySelector('input[name="event_date"]');
    data.event_date = new Date(event_dateInput.value);

    const locationInput = tbody.querySelector('input[name="location"]');
    data.location = locationInput.value;


    const descriptionInput = tbody.querySelector('input[name="description"]');
    data.description = descriptionInput.value;




    return data;
}

function eventToInputTBody(data, tbody) {
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
    // user_id - str
    //

    const user_idTdKey = document.createElement('td');
    user_idTdKey.textContent = 'user_id';

    const user_idTdInput = document.createElement('td');
    const user_idInput = document.createElement('input');
    user_idInput.name = 'user_id';
    user_idInput.value = data.user_id || '';
    user_idInput.size = 35;
    user_idInput.readOnly = true;
    user_idInput.placeholder = 'automatic field';
    user_idTdInput.appendChild(user_idInput);

    const user_idTdOther = document.createElement('td');
    user_idTdOther.textContent = 'automatic field, not editable';

    const user_idTr = document.createElement('tr');
    user_idTr.appendChild(user_idTdKey);
    user_idTr.appendChild(user_idTdInput);
    user_idTr.appendChild(user_idTdOther);

    tbody.appendChild(user_idTr);


    //
    // event_name - str
    //

    const event_nameTdKey = document.createElement('td');
    event_nameTdKey.textContent = 'event_name';

    const event_nameTdInput = document.createElement('td');
    const event_nameInput = document.createElement('input');
    event_nameInput.name = 'event_name';
    event_nameInput.value = data.event_name || '';
    event_nameInput.size = 35;
    event_nameTdInput.appendChild(event_nameInput);

    const event_nameTdOther = document.createElement('td');
    event_nameTdOther.textContent = '-';

    const event_nameTr = document.createElement('tr');
    event_nameTr.appendChild(event_nameTdKey);
    event_nameTr.appendChild(event_nameTdInput);
    event_nameTr.appendChild(event_nameTdOther);

    tbody.appendChild(event_nameTr);


    //
    // event_date - datetime
    //

    const event_dateTdKey = document.createElement('td');
    event_dateTdKey.textContent = 'event_date';

    const event_dateTdInput = document.createElement('td');
    const event_dateInput = document.createElement('input');
    event_dateInput.name = 'event_date';
    event_dateInput.type = 'datetime-local';
    try {
        event_dateInput.value = data.event_date.toISOString().split('.')[0].slice(0, 16);
    }catch {
        event_dateInput.value = '';
    }
    event_dateTdInput.appendChild(event_dateInput);

    const event_dateTdOther = document.createElement('td');
    event_dateTdOther.textContent = '-';

    const event_dateTr = document.createElement('tr');
    event_dateTr.appendChild(event_dateTdKey);
    event_dateTr.appendChild(event_dateTdInput);
    event_dateTr.appendChild(event_dateTdOther);

    tbody.appendChild(event_dateTr);

    //
    // location - str
    //

    const locationTdKey = document.createElement('td');
    locationTdKey.textContent = 'location';

    const locationTdInput = document.createElement('td');
    const locationInput = document.createElement('input');
    locationInput.name = 'location';
    locationInput.value = data.location || '';
    locationInput.size = 35;
    locationTdInput.appendChild(locationInput);

    const locationTdOther = document.createElement('td');
    locationTdOther.textContent = '-';

    const locationTr = document.createElement('tr');
    locationTr.appendChild(locationTdKey);
    locationTr.appendChild(locationTdInput);
    locationTr.appendChild(locationTdOther);

    tbody.appendChild(locationTr);


    //
    // description - str
    //

    const descriptionTdKey = document.createElement('td');
    descriptionTdKey.textContent = 'description';

    const descriptionTdInput = document.createElement('td');
    const descriptionInput = document.createElement('input');
    descriptionInput.name = 'description';
    descriptionInput.value = data.description || '';
    descriptionInput.size = 35;
    descriptionTdInput.appendChild(descriptionInput);

    const descriptionTdOther = document.createElement('td');
    descriptionTdOther.textContent = '-';

    const descriptionTr = document.createElement('tr');
    descriptionTr.appendChild(descriptionTdKey);
    descriptionTr.appendChild(descriptionTdInput);
    descriptionTr.appendChild(descriptionTdOther);

    tbody.appendChild(descriptionTr);




    return tbody;

}

function eventToDisplayTBody(data, tbody) {
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
    // user_id - str
    //

    const user_idTdKey = document.createElement('td');
    user_idTdKey.textContent = 'user_id';

    const user_idTdValue = document.createElement('td');
    user_idTdValue.textContent = data.user_id;

    const user_idTr = document.createElement('tr');
    user_idTr.appendChild(user_idTdKey);
    user_idTr.appendChild(user_idTdValue);

    tbody.appendChild(user_idTr);

    //
    // event_name - str
    //

    const event_nameTdKey = document.createElement('td');
    event_nameTdKey.textContent = 'event_name';

    const event_nameTdValue = document.createElement('td');
    event_nameTdValue.textContent = data.event_name;

    const event_nameTr = document.createElement('tr');
    event_nameTr.appendChild(event_nameTdKey);
    event_nameTr.appendChild(event_nameTdValue);

    tbody.appendChild(event_nameTr);


    //
    // event_date - datetime
    //

    const event_dateTdKey = document.createElement('td');
    event_dateTdKey.textContent = 'event_date';

    const event_dateTdValue = document.createElement('td');
    event_dateTdValue.textContent = data.event_date.toISOString().split('.')[0];

    const event_dateTr = document.createElement('tr');
    event_dateTr.appendChild(event_dateTdKey);
    event_dateTr.appendChild(event_dateTdValue);

    tbody.appendChild(event_dateTr);

    //
    // location - str
    //

    const locationTdKey = document.createElement('td');
    locationTdKey.textContent = 'location';

    const locationTdValue = document.createElement('td');
    locationTdValue.textContent = data.location;

    const locationTr = document.createElement('tr');
    locationTr.appendChild(locationTdKey);
    locationTr.appendChild(locationTdValue);

    tbody.appendChild(locationTr);


    //
    // description - str
    //

    const descriptionTdKey = document.createElement('td');
    descriptionTdKey.textContent = 'description';

    const descriptionTdValue = document.createElement('td');
    descriptionTdValue.textContent = data.description;

    const descriptionTr = document.createElement('tr');
    descriptionTr.appendChild(descriptionTdKey);
    descriptionTr.appendChild(descriptionTdValue);

    tbody.appendChild(descriptionTr);




    return tbody;
}

function eventToTableRow(data) {

    const tr = document.createElement('tr');
    tr.style.cursor = 'pointer';
    tr.onclick = () => window.location.href = `/content/event/${data.id}`

    // id - string

    const idTd = document.createElement('td');
    idTd.textContent = data.id;
    tr.appendChild(idTd);

    //
    // user_id - str
    //
    
    const user_idTd = document.createElement('td');
    user_idTd.textContent = data.user_id;
    tr.appendChild(user_idTd);

    //
    // event_name - str
    //

    const event_nameTd = document.createElement('td');
    event_nameTd.textContent = data.event_name;
    tr.appendChild(event_nameTd);


    //
    // event_date - datetime
    //
    
    const event_dateTd = document.createElement('td');
    event_dateTd.textContent = data.event_date.toISOString().split('.')[0];
    tr.appendChild(event_dateTd);

    //
    // location - str
    //

    const locationTd = document.createElement('td');
    locationTd.textContent = data.location;
    tr.appendChild(locationTd);


    //
    // description - str
    //

    const descriptionTd = document.createElement('td');
    descriptionTd.textContent = data.description;
    tr.appendChild(descriptionTd);




    return tr;

}

function eventListToDisplayTBody(eventList, tbody) {

    tbody.innerHTML = '';

    for (const event of eventList) {
        tbody.appendChild(eventToTableRow(event));
    }

    return tbody;

}

//
// serialize functions
//

function eventForJSON(data) {
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

function clientCreateEvent(data) {
    
    return fetchWithSession('/api/content/event', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
}

function clientReadEvent(id) {

    return fetchWithSession('/api/content/event/' + id, {
        method: 'GET',
    })
}

function clientUpdateEvent(id, data) {

    return fetchWithSession(`/api/content/event/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })

}

function clientDeleteEvent(id) {

    return fetchWithSession(`/api/content/event/${id}`, {
        method: 'DELETE',
    })

}

function clientListEvents(offset, size) {

    return fetchWithSession(`/api/content/event?offset=${offset}&size=${size}`, {
        method: 'GET',
    })
}