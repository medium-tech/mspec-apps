
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

function initPost(data) {
    let result = {
        user_id: data.user_id,

        content: data.content,


    }

    if (typeof data.id !== 'undefined') {
        result.id = data.id;
    }
    return result;
}

function examplePost() {
    const data = {
			user_id: '1',
			content: 'Just had an amazing day at the beach!'
    }
    return {...data}
}

function randomPost() {
    return {
		'content': randomStr(),

    }
}

function verifyPost(data) {

    let result = {
        valid: true,
        errors: {}
    }

    if (typeof data.user_id !== 'string') {
        result.error.user_id = 'user_id must be a string';
        result.valid = false;
    }


    if (typeof data.content !== 'string') {
        result.error.content = 'content must be a string';
        result.valid = false;
    }




    return result

}

function postFromInputTBody(tbody) {   
    console.log('postFromInputTBody', tbody);
    const data = {};

    // parse id if exists

    const idInput = tbody.querySelector('input[name="id"]');
    if (idInput) {
        data.id = idInput.value;
    }

    const user_idInput = tbody.querySelector('input[name="user_id"]');
    data.user_id = user_idInput ? user_idInput.value : '';


    const contentInput = tbody.querySelector('input[name="content"]');
    data.content = contentInput.value;




    return data;
}

function postToInputTBody(data, tbody) {
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
    // content - str
    //

    const contentTdKey = document.createElement('td');
    contentTdKey.textContent = 'content';

    const contentTdInput = document.createElement('td');
    const contentInput = document.createElement('input');
    contentInput.name = 'content';
    contentInput.value = data.content || '';
    contentInput.size = 35;
    contentTdInput.appendChild(contentInput);

    const contentTdOther = document.createElement('td');
    contentTdOther.textContent = '-';

    const contentTr = document.createElement('tr');
    contentTr.appendChild(contentTdKey);
    contentTr.appendChild(contentTdInput);
    contentTr.appendChild(contentTdOther);

    tbody.appendChild(contentTr);




    return tbody;

}

function postToDisplayTBody(data, tbody) {
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
    // content - str
    //

    const contentTdKey = document.createElement('td');
    contentTdKey.textContent = 'content';

    const contentTdValue = document.createElement('td');
    contentTdValue.textContent = data.content;

    const contentTr = document.createElement('tr');
    contentTr.appendChild(contentTdKey);
    contentTr.appendChild(contentTdValue);

    tbody.appendChild(contentTr);




    return tbody;
}

function postToTableRow(data) {

    const tr = document.createElement('tr');
    tr.style.cursor = 'pointer';
    tr.onclick = () => window.location.href = `/content/post/${data.id}`

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
    // content - str
    //

    const contentTd = document.createElement('td');
    contentTd.textContent = data.content;
    tr.appendChild(contentTd);




    return tr;

}

function postListToDisplayTBody(postList, tbody) {

    tbody.innerHTML = '';

    for (const post of postList) {
        tbody.appendChild(postToTableRow(post));
    }

    return tbody;

}

//
// serialize functions
//

function postForJSON(data) {
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

function clientCreatePost(data) {
    
    return fetchWithSession('/api/content/post', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
}

function clientReadPost(id) {

    return fetchWithSession('/api/content/post/' + id, {
        method: 'GET',
    })
}

function clientUpdatePost(id, data) {

    return fetchWithSession(`/api/content/post/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })

}

function clientDeletePost(id) {

    return fetchWithSession(`/api/content/post/${id}`, {
        method: 'DELETE',
    })

}

function clientListPosts(offset, size) {

    return fetchWithSession(`/api/content/post?offset=${offset}&size=${size}`, {
        method: 'GET',
    })
}