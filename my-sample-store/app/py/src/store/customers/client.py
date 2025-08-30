from core.exceptions import MSpecError, ConfigError, NotFoundError, AuthenticationError, ForbiddenError
from store.customers.model import Customers

import json

from urllib.request import Request, urlopen
from urllib.error import HTTPError


__all__ = [
    'client_create_customers',
    'client_read_customers',
    'client_update_customers',
    'client_delete_customers',
    'client_list_customers'
]

def client_create_customers(ctx:dict, obj:Customers) -> Customers:
    """
    create a customers on the server, verifying the data first.
    
    args ::
        ctx :: dict containing the client context.
        obj :: the Customers object to create.
    
    return :: Customers object with the new id.

    raises :: ConfigError, MSpecError
    """

    try:
        url = f'{ctx["host"]}/api/store/customers'
    except KeyError:
        raise ConfigError('invalid context, missing host')

    request_body = obj.validate().to_json().encode()

    try:
        request = Request(url, headers=ctx['headers'], method='POST', data=request_body)

        with urlopen(request) as response:
            response_body = response.read().decode('utf-8')
            return Customers(**json.loads(response_body)).convert_types()

    except (json.JSONDecodeError, KeyError) as e:
        raise MSpecError(f'invalid response from server, {e.__class__.__name__}: {e}')
    except Exception as e:
        raise MSpecError(f'error creating customers: {e.__class__.__name__}: {e}')

def client_read_customers(ctx:dict, id:str) -> Customers:
    """
    read a customers from the server, verifying it first.

    args ::
        ctx :: dict containing the client context.
        id :: str of the id of the item to read.
    
    return :: profile object if it exists.

    raises :: ConfigError, MSpecError, NotFoundError
    """

    try:
        url = ctx['host'] + '/api/store/customers/' + id
    except KeyError:
        raise ConfigError('invalid context, missing host')

    try:

        request = Request(url, headers=ctx['headers'], method='GET')

        with urlopen(request) as response:
            response_body = response.read().decode('utf-8')

    except HTTPError as e:
        if e.code == 401:
            raise AuthenticationError('Error reading customers: invalid username or password')
        elif e.code == 403:
            raise ForbiddenError('Error reading customers: forbidden')
        elif e.code == 404:
            raise NotFoundError(f'customers {id} not found')
        raise MSpecError(f'error reading customers: {e.__class__.__name__}: {e}')
    except (json.JSONDecodeError, KeyError) as e:
        raise MSpecError('invalid response from server, {e.__class__.__name__}: {e}')
    except Exception as e:
        raise MSpecError(f'error reading customers: {e.__class__.__name__}: {e}')

    return Customers(**json.loads(response_body)).convert_types()

def client_update_customers(ctx:dict, obj:Customers) -> Customers:
    """
    update a customers on the server, verifying the data first.

    args ::
        ctx :: dict containing the client context.
        obj :: the Customers object to update.
    
    return :: Customers object.

    raises :: ConfigError, MSpecError, NotFoundError
    """
    try:
        _id = obj.id
    except KeyError:
        raise ValueError('invalid data, missing id')

    if _id is None:
        raise ValueError('invalid data, missing id')

    try:
        url = f'{ctx["host"]}/api/store/customers/{_id}'
    except KeyError:
        raise ConfigError('invalid context, missing host')

    request_body = obj.validate().to_json().encode()

    try:
        request = Request(url, headers=ctx['headers'], method='PUT', data=request_body)

        with urlopen(request) as response:
            response_body = response.read().decode('utf-8')
    
    except HTTPError as e:
        if e.code == 401:
            raise AuthenticationError('Error updating customers: authentication error')
        elif e.code == 403:
            raise ForbiddenError('Error updating customers: forbidden')
        elif e.code == 404:
            raise NotFoundError(f'customers {id} not found')
        raise MSpecError(f'error updating customers: {e.__class__.__name__}: {e}')
        
    except (json.JSONDecodeError, KeyError) as e:
        raise MSpecError('invalid response from server, {e.__class__.__name__}: {e}')
    
    except Exception as e:
        raise MSpecError(f'error updating customers: {e.__class__.__name__}: {e}')

    return Customers(**json.loads(response_body)).convert_types()

def client_delete_customers(ctx:dict, id:str) -> None:
    """
    delete a customers from the server.

    args ::
        ctx :: dict containing the client context.
        id :: str of the id of the item to delete.
    
    return :: None

    raises :: ConfigError, MSpecError
    """

    try:
        url = f'{ctx["host"]}/api/store/customers/{id}'
    except KeyError:
        raise ConfigError('invalid context, missing host')

    try:
        request = Request(url, headers=ctx['headers'], method='DELETE')

        with urlopen(request) as response:
            _ = response.read().decode('utf-8')

    except (json.JSONDecodeError, KeyError) as e:
        raise MSpecError('invalid response from server, {e.__class__.__name__}: {e}')
    
    except Exception as e:
        raise MSpecError(f'error deleting customers: {e.__class__.__name__}: {e}')

def client_list_customers(ctx:dict, offset:int=0, limit:int=50) -> list[Customers]:
    """
    list customerss from the server, verifying each.

    args ::
        ctx :: dict containing the client context.
        offset :: int of the offset to start listing from.
        limit :: int of the maximum number of items to list.
    
    return :: list of Customers objects.

    raises :: ConfigError, MSpecError
    """

    try:
        url = f'{ctx["host"]}/api/store/customers?offset={offset}&limit={limit}'
    except KeyError:
        raise ConfigError('invalid context, missing host')

    try:
        request = Request(url, headers=ctx['headers'], method='GET')
        
        with urlopen(request) as response:
            response_body = response.read().decode('utf-8')

        return [Customers(**item).convert_types() for item in json.loads(response_body)]

    except (json.JSONDecodeError, TypeError) as e:
        raise MSpecError(f'invalid response from server, {e.__class__.__name__}: {e}')

    except Exception as e:
        raise MSpecError(f'error listing customerss: {e.__class__.__name__}: {e}')