from core.exceptions import MSpecError, ConfigError, NotFoundError, AuthenticationError, ForbiddenError
from admin.employees.model import Employees

import json

from urllib.request import Request, urlopen
from urllib.error import HTTPError


__all__ = [
    'client_create_employees',
    'client_read_employees',
    'client_update_employees',
    'client_delete_employees',
    'client_list_employees'
]

def client_create_employees(ctx:dict, obj:Employees) -> Employees:
    """
    create a employees on the server, verifying the data first.
    
    args ::
        ctx :: dict containing the client context.
        obj :: the Employees object to create.
    
    return :: Employees object with the new id.

    raises :: ConfigError, MSpecError
    """

    try:
        url = f'{ctx["host"]}/api/admin/employees'
    except KeyError:
        raise ConfigError('invalid context, missing host')

    request_body = obj.validate().to_json().encode()

    try:
        request = Request(url, headers=ctx['headers'], method='POST', data=request_body)

        with urlopen(request) as response:
            response_body = response.read().decode('utf-8')
            return Employees(**json.loads(response_body)).convert_types()

    except (json.JSONDecodeError, KeyError) as e:
        raise MSpecError(f'invalid response from server, {e.__class__.__name__}: {e}')
    except Exception as e:
        raise MSpecError(f'error creating employees: {e.__class__.__name__}: {e}')

def client_read_employees(ctx:dict, id:str) -> Employees:
    """
    read a employees from the server, verifying it first.

    args ::
        ctx :: dict containing the client context.
        id :: str of the id of the item to read.
    
    return :: profile object if it exists.

    raises :: ConfigError, MSpecError, NotFoundError
    """

    try:
        url = ctx['host'] + '/api/admin/employees/' + id
    except KeyError:
        raise ConfigError('invalid context, missing host')

    try:

        request = Request(url, headers=ctx['headers'], method='GET')

        with urlopen(request) as response:
            response_body = response.read().decode('utf-8')

    except HTTPError as e:
        if e.code == 401:
            raise AuthenticationError('Error reading employees: invalid username or password')
        elif e.code == 403:
            raise ForbiddenError('Error reading employees: forbidden')
        elif e.code == 404:
            raise NotFoundError(f'employees {id} not found')
        raise MSpecError(f'error reading employees: {e.__class__.__name__}: {e}')
    except (json.JSONDecodeError, KeyError) as e:
        raise MSpecError('invalid response from server, {e.__class__.__name__}: {e}')
    except Exception as e:
        raise MSpecError(f'error reading employees: {e.__class__.__name__}: {e}')

    return Employees(**json.loads(response_body)).convert_types()

def client_update_employees(ctx:dict, obj:Employees) -> Employees:
    """
    update a employees on the server, verifying the data first.

    args ::
        ctx :: dict containing the client context.
        obj :: the Employees object to update.
    
    return :: Employees object.

    raises :: ConfigError, MSpecError, NotFoundError
    """
    try:
        _id = obj.id
    except KeyError:
        raise ValueError('invalid data, missing id')

    if _id is None:
        raise ValueError('invalid data, missing id')

    try:
        url = f'{ctx["host"]}/api/admin/employees/{_id}'
    except KeyError:
        raise ConfigError('invalid context, missing host')

    request_body = obj.validate().to_json().encode()

    try:
        request = Request(url, headers=ctx['headers'], method='PUT', data=request_body)

        with urlopen(request) as response:
            response_body = response.read().decode('utf-8')
    
    except HTTPError as e:
        if e.code == 401:
            raise AuthenticationError('Error updating employees: authentication error')
        elif e.code == 403:
            raise ForbiddenError('Error updating employees: forbidden')
        elif e.code == 404:
            raise NotFoundError(f'employees {id} not found')
        raise MSpecError(f'error updating employees: {e.__class__.__name__}: {e}')
        
    except (json.JSONDecodeError, KeyError) as e:
        raise MSpecError('invalid response from server, {e.__class__.__name__}: {e}')
    
    except Exception as e:
        raise MSpecError(f'error updating employees: {e.__class__.__name__}: {e}')

    return Employees(**json.loads(response_body)).convert_types()

def client_delete_employees(ctx:dict, id:str) -> None:
    """
    delete a employees from the server.

    args ::
        ctx :: dict containing the client context.
        id :: str of the id of the item to delete.
    
    return :: None

    raises :: ConfigError, MSpecError
    """

    try:
        url = f'{ctx["host"]}/api/admin/employees/{id}'
    except KeyError:
        raise ConfigError('invalid context, missing host')

    try:
        request = Request(url, headers=ctx['headers'], method='DELETE')

        with urlopen(request) as response:
            _ = response.read().decode('utf-8')

    except (json.JSONDecodeError, KeyError) as e:
        raise MSpecError('invalid response from server, {e.__class__.__name__}: {e}')
    
    except Exception as e:
        raise MSpecError(f'error deleting employees: {e.__class__.__name__}: {e}')

def client_list_employees(ctx:dict, offset:int=0, limit:int=50) -> list[Employees]:
    """
    list employeess from the server, verifying each.

    args ::
        ctx :: dict containing the client context.
        offset :: int of the offset to start listing from.
        limit :: int of the maximum number of items to list.
    
    return :: list of Employees objects.

    raises :: ConfigError, MSpecError
    """

    try:
        url = f'{ctx["host"]}/api/admin/employees?offset={offset}&limit={limit}'
    except KeyError:
        raise ConfigError('invalid context, missing host')

    try:
        request = Request(url, headers=ctx['headers'], method='GET')
        
        with urlopen(request) as response:
            response_body = response.read().decode('utf-8')

        return [Employees(**item).convert_types() for item in json.loads(response_body)]

    except (json.JSONDecodeError, TypeError) as e:
        raise MSpecError(f'invalid response from server, {e.__class__.__name__}: {e}')

    except Exception as e:
        raise MSpecError(f'error listing employeess: {e.__class__.__name__}: {e}')