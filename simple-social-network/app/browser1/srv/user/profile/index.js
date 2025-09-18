
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

function initProfile(data) {
    let result = {
        user_id: data.user_id,

        username: data.username,

        bio: data.bio,


    }

    if (typeof data.id !== 'undefined') {
        result.id = data.id;
    }
    return result;
}

function exampleProfile() {
    const data = {
			user_id: '1',
			username: 'alice',
			bio: 'Loves hiking and outdoor adventures.'
    }
    return {...data}
}

function randomProfile() {
    return {
		'username': randomStr(),

		'bio': randomStr(),

    }
}

function verifyProfile(data) {

    let result = {
        valid: true,
        errors: {}
    }

    if (typeof data.user_id !== 'string') {
        result.error.user_id = 'user_id must be a string';
        result.valid = false;
    }


    if (typeof data.username !== 'string') {
        result.error.username = 'username must be a string';
        result.valid = false;
    }


    if (typeof data.bio !== 'string') {
        result.error.bio = 'bio must be a string';
        result.valid = false;
    }




    return result

}

function profileFromInputTBody(tbody) {   
    console.log('profileFromInputTBody', tbody);
    const data = {};

    // parse id if exists

    const idInput = tbody.querySelector('input[name="id"]');
    if (idInput) {
        data.id = idInput.value;
    }

    const user_idInput = tbody.querySelector('input[name="user_id"]');
    data.user_id = user_idInput ? user_idInput.value : '';


    const usernameInput = tbody.querySelector('input[name="username"]');
    data.username = usernameInput.value;


    const bioInput = tbody.querySelector('input[name="bio"]');
    data.bio = bioInput.value;




    return data;
}

function profileToInputTBody(data, tbody) {
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
    // username - str
    //

    const usernameTdKey = document.createElement('td');
    usernameTdKey.textContent = 'username';

    const usernameTdInput = document.createElement('td');
    const usernameInput = document.createElement('input');
    usernameInput.name = 'username';
    usernameInput.value = data.username || '';
    usernameInput.size = 35;
    usernameTdInput.appendChild(usernameInput);

    const usernameTdOther = document.createElement('td');
    usernameTdOther.textContent = '-';

    const usernameTr = document.createElement('tr');
    usernameTr.appendChild(usernameTdKey);
    usernameTr.appendChild(usernameTdInput);
    usernameTr.appendChild(usernameTdOther);

    tbody.appendChild(usernameTr);


    //
    // bio - str
    //

    const bioTdKey = document.createElement('td');
    bioTdKey.textContent = 'bio';

    const bioTdInput = document.createElement('td');
    const bioInput = document.createElement('input');
    bioInput.name = 'bio';
    bioInput.value = data.bio || '';
    bioInput.size = 35;
    bioTdInput.appendChild(bioInput);

    const bioTdOther = document.createElement('td');
    bioTdOther.textContent = '-';

    const bioTr = document.createElement('tr');
    bioTr.appendChild(bioTdKey);
    bioTr.appendChild(bioTdInput);
    bioTr.appendChild(bioTdOther);

    tbody.appendChild(bioTr);




    return tbody;

}

function profileToDisplayTBody(data, tbody) {
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
    // username - str
    //

    const usernameTdKey = document.createElement('td');
    usernameTdKey.textContent = 'username';

    const usernameTdValue = document.createElement('td');
    usernameTdValue.textContent = data.username;

    const usernameTr = document.createElement('tr');
    usernameTr.appendChild(usernameTdKey);
    usernameTr.appendChild(usernameTdValue);

    tbody.appendChild(usernameTr);


    //
    // bio - str
    //

    const bioTdKey = document.createElement('td');
    bioTdKey.textContent = 'bio';

    const bioTdValue = document.createElement('td');
    bioTdValue.textContent = data.bio;

    const bioTr = document.createElement('tr');
    bioTr.appendChild(bioTdKey);
    bioTr.appendChild(bioTdValue);

    tbody.appendChild(bioTr);




    return tbody;
}

function profileToTableRow(data) {

    const tr = document.createElement('tr');
    tr.style.cursor = 'pointer';
    tr.onclick = () => window.location.href = `/user/profile/${data.id}`

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
    // username - str
    //

    const usernameTd = document.createElement('td');
    usernameTd.textContent = data.username;
    tr.appendChild(usernameTd);


    //
    // bio - str
    //

    const bioTd = document.createElement('td');
    bioTd.textContent = data.bio;
    tr.appendChild(bioTd);




    return tr;

}

function profileListToDisplayTBody(profileList, tbody) {

    tbody.innerHTML = '';

    for (const profile of profileList) {
        tbody.appendChild(profileToTableRow(profile));
    }

    return tbody;

}

//
// serialize functions
//

function profileForJSON(data) {
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

function clientCreateProfile(data) {
    
    return fetchWithSession('/api/user/profile', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
}

function clientReadProfile(id) {

    return fetchWithSession('/api/user/profile/' + id, {
        method: 'GET',
    })
}

function clientUpdateProfile(id, data) {

    return fetchWithSession(`/api/user/profile/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })

}

function clientDeleteProfile(id) {

    return fetchWithSession(`/api/user/profile/${id}`, {
        method: 'DELETE',
    })

}

function clientListProfiles(offset, size) {

    return fetchWithSession(`/api/user/profile?offset=${offset}&size=${size}`, {
        method: 'GET',
    })
}