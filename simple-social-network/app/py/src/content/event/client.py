from core.exceptions import MSpecError, ConfigError, NotFoundError, AuthenticationError, ForbiddenError
from content.event.model import Event

import json

from urllib.request import Request, urlopen
from urllib.error import HTTPError


__all__ = [
    'client_create_event',
    'client_read_event',
    'client_update_event',
    'client_delete_event',
    'client_list_event'
]

def client_create_event(ctx:dict, obj:Event) -> Event:
    """
    create a event on the server, verifying the data first.
    
    args ::
        ctx :: dict containing the client context.
        obj :: the Event object to create.
    
    return :: Event object with the new id.

    raises :: ConfigError, MSpecError
    """

    try:
        url = f'{ctx["host"]}/api/content/event'
    except KeyError:
        raise ConfigError('invalid context, missing host')

    request_body = obj.validate().to_json().encode()

    try:
        request = Request(url, headers=ctx['headers'], method='POST', data=request_body)

        with urlopen(request) as response:
            response_body = response.read().decode('utf-8')
            return Event(**json.loads(response_body)).convert_types()
        
    except HTTPError as e:
        if e.code == 401:
            raise AuthenticationError('Error creating event: authentication error')
        elif e.code == 403:
            raise ForbiddenError('Error creating event: forbidden')

        raise MSpecError(f'error creating event: {e.__class__.__name__}: {e}')

    except (json.JSONDecodeError, KeyError) as e:
        raise MSpecError(f'invalid response from server, {e.__class__.__name__}: {e}')
    except Exception as e:
        raise MSpecError(f'error creating event: {e.__class__.__name__}: {e}')

def client_read_event(ctx:dict, id:str) -> Event:
    """
    read a event from the server, verifying it first.

    args ::
        ctx :: dict containing the client context.
        id :: str of the id of the item to read.
    
    return :: profile object if it exists.

    raises :: ConfigError, MSpecError, NotFoundError
    """

    try:
        url = ctx['host'] + '/api/content/event/' + id
    except KeyError:
        raise ConfigError('invalid context, missing host')

    try:

        request = Request(url, headers=ctx['headers'], method='GET')

        with urlopen(request) as response:
            response_body = response.read().decode('utf-8')

    except HTTPError as e:
        if e.code == 401:
            raise AuthenticationError('Error reading event: invalid username or password')
        elif e.code == 403:
            raise ForbiddenError('Error reading event: forbidden')
        elif e.code == 404:
            raise NotFoundError(f'event {id} not found')
        raise MSpecError(f'error reading event: {e.__class__.__name__}: {e}')
    except (json.JSONDecodeError, KeyError) as e:
        raise MSpecError('invalid response from server, {e.__class__.__name__}: {e}')
    except Exception as e:
        raise MSpecError(f'error reading event: {e.__class__.__name__}: {e}')

    return Event(**json.loads(response_body)).convert_types()

def client_update_event(ctx:dict, obj:Event) -> Event:
    """
    update a event on the server, verifying the data first.

    args ::
        ctx :: dict containing the client context.
        obj :: the Event object to update.
    
    return :: Event object.

    raises :: ConfigError, MSpecError, NotFoundError
    """
    try:
        _id = obj.id
    except KeyError:
        raise ValueError('invalid data, missing id')

    if _id is None:
        raise ValueError('invalid data, missing id')

    try:
        url = f'{ctx["host"]}/api/content/event/{_id}'
    except KeyError:
        raise ConfigError('invalid context, missing host')

    request_body = obj.validate().to_json().encode()

    try:
        request = Request(url, headers=ctx['headers'], method='PUT', data=request_body)

        with urlopen(request) as response:
            response_body = response.read().decode('utf-8')
    
    except HTTPError as e:
        if e.code == 401:
            raise AuthenticationError('Error updating event: authentication error')
        elif e.code == 403:
            raise ForbiddenError('Error updating event: forbidden')
        elif e.code == 404:
            raise NotFoundError(f'event {id} not found')
        raise MSpecError(f'error updating event: {e.__class__.__name__}: {e}')
        
    except (json.JSONDecodeError, KeyError) as e:
        raise MSpecError('invalid response from server, {e.__class__.__name__}: {e}')
    
    except Exception as e:
        raise MSpecError(f'error updating event: {e.__class__.__name__}: {e}')

    return Event(**json.loads(response_body)).convert_types()

def client_delete_event(ctx:dict, id:str) -> None:
    """
    delete a event from the server.

    args ::
        ctx :: dict containing the client context.
        id :: str of the id of the item to delete.
    
    return :: None

    raises :: ConfigError, MSpecError
    """

    try:
        url = f'{ctx["host"]}/api/content/event/{id}'
    except KeyError:
        raise ConfigError('invalid context, missing host')

    try:
        request = Request(url, headers=ctx['headers'], method='DELETE')

        with urlopen(request) as response:
            _ = response.read().decode('utf-8')

    except (json.JSONDecodeError, KeyError) as e:
        raise MSpecError('invalid response from server, {e.__class__.__name__}: {e}')
    
    except Exception as e:
        raise MSpecError(f'error deleting event: {e.__class__.__name__}: {e}')

def client_list_event(ctx:dict, offset:int=0, limit:int=50) -> list[Event]:
    """
    list events from the server, verifying each.

    args ::
        ctx :: dict containing the client context.
        offset :: int of the offset to start listing from.
        limit :: int of the maximum number of items to list.
    
    return :: list of Event objects.

    raises :: ConfigError, MSpecError
    """

    try:
        url = f'{ctx["host"]}/api/content/event?offset={offset}&limit={limit}'
    except KeyError:
        raise ConfigError('invalid context, missing host')

    try:
        request = Request(url, headers=ctx['headers'], method='GET')
        
        with urlopen(request) as response:
            response_body = response.read().decode('utf-8')

        response_data = json.loads(response_body)

        return {
            'total': response_data['total'],
            'items': [Event(**item).convert_types() for item in response_data['items']]
        }

    except (json.JSONDecodeError, TypeError) as e:
        raise MSpecError(f'invalid response from server, {e.__class__.__name__}: {e}')

    except Exception as e:
        raise MSpecError(f'error listing events: {e.__class__.__name__}: {e}')