from core.exceptions import MSpecError, ConfigError, NotFoundError, AuthenticationError, ForbiddenError
from user.profile.model import Profile

import json

from urllib.request import Request, urlopen
from urllib.error import HTTPError


__all__ = [
    'client_create_profile',
    'client_read_profile',
    'client_update_profile',
    'client_delete_profile',
    'client_list_profile'
]

def client_create_profile(ctx:dict, obj:Profile) -> Profile:
    """
    create a profile on the server, verifying the data first.
    
    args ::
        ctx :: dict containing the client context.
        obj :: the Profile object to create.
    
    return :: Profile object with the new id.

    raises :: ConfigError, MSpecError
    """

    try:
        url = f'{ctx["host"]}/api/user/profile'
    except KeyError:
        raise ConfigError('invalid context, missing host')

    request_body = obj.validate().to_json().encode()

    try:
        request = Request(url, headers=ctx['headers'], method='POST', data=request_body)

        with urlopen(request) as response:
            response_body = response.read().decode('utf-8')
            return Profile(**json.loads(response_body)).convert_types()
        
    except HTTPError as e:
        if e.code == 401:
            raise AuthenticationError('Error creating profile: authentication error')
        elif e.code == 403:
            raise ForbiddenError('Error creating profile: forbidden')

        raise MSpecError(f'error creating profile: {e.__class__.__name__}: {e}')

    except (json.JSONDecodeError, KeyError) as e:
        raise MSpecError(f'invalid response from server, {e.__class__.__name__}: {e}')
    except Exception as e:
        raise MSpecError(f'error creating profile: {e.__class__.__name__}: {e}')

def client_read_profile(ctx:dict, id:str) -> Profile:
    """
    read a profile from the server, verifying it first.

    args ::
        ctx :: dict containing the client context.
        id :: str of the id of the item to read.
    
    return :: profile object if it exists.

    raises :: ConfigError, MSpecError, NotFoundError
    """

    try:
        url = ctx['host'] + '/api/user/profile/' + id
    except KeyError:
        raise ConfigError('invalid context, missing host')

    try:

        request = Request(url, headers=ctx['headers'], method='GET')

        with urlopen(request) as response:
            response_body = response.read().decode('utf-8')

    except HTTPError as e:
        if e.code == 401:
            raise AuthenticationError('Error reading profile: invalid username or password')
        elif e.code == 403:
            raise ForbiddenError('Error reading profile: forbidden')
        elif e.code == 404:
            raise NotFoundError(f'profile {id} not found')
        raise MSpecError(f'error reading profile: {e.__class__.__name__}: {e}')
    except (json.JSONDecodeError, KeyError) as e:
        raise MSpecError('invalid response from server, {e.__class__.__name__}: {e}')
    except Exception as e:
        raise MSpecError(f'error reading profile: {e.__class__.__name__}: {e}')

    return Profile(**json.loads(response_body)).convert_types()

def client_update_profile(ctx:dict, obj:Profile) -> Profile:
    """
    update a profile on the server, verifying the data first.

    args ::
        ctx :: dict containing the client context.
        obj :: the Profile object to update.
    
    return :: Profile object.

    raises :: ConfigError, MSpecError, NotFoundError
    """
    try:
        _id = obj.id
    except KeyError:
        raise ValueError('invalid data, missing id')

    if _id is None:
        raise ValueError('invalid data, missing id')

    try:
        url = f'{ctx["host"]}/api/user/profile/{_id}'
    except KeyError:
        raise ConfigError('invalid context, missing host')

    request_body = obj.validate().to_json().encode()

    try:
        request = Request(url, headers=ctx['headers'], method='PUT', data=request_body)

        with urlopen(request) as response:
            response_body = response.read().decode('utf-8')
    
    except HTTPError as e:
        if e.code == 401:
            raise AuthenticationError('Error updating profile: authentication error')
        elif e.code == 403:
            raise ForbiddenError('Error updating profile: forbidden')
        elif e.code == 404:
            raise NotFoundError(f'profile {id} not found')
        raise MSpecError(f'error updating profile: {e.__class__.__name__}: {e}')
        
    except (json.JSONDecodeError, KeyError) as e:
        raise MSpecError('invalid response from server, {e.__class__.__name__}: {e}')
    
    except Exception as e:
        raise MSpecError(f'error updating profile: {e.__class__.__name__}: {e}')

    return Profile(**json.loads(response_body)).convert_types()

def client_delete_profile(ctx:dict, id:str) -> None:
    """
    delete a profile from the server.

    args ::
        ctx :: dict containing the client context.
        id :: str of the id of the item to delete.
    
    return :: None

    raises :: ConfigError, MSpecError
    """

    try:
        url = f'{ctx["host"]}/api/user/profile/{id}'
    except KeyError:
        raise ConfigError('invalid context, missing host')

    try:
        request = Request(url, headers=ctx['headers'], method='DELETE')

        with urlopen(request) as response:
            _ = response.read().decode('utf-8')

    except (json.JSONDecodeError, KeyError) as e:
        raise MSpecError('invalid response from server, {e.__class__.__name__}: {e}')
    
    except Exception as e:
        raise MSpecError(f'error deleting profile: {e.__class__.__name__}: {e}')

def client_list_profile(ctx:dict, offset:int=0, limit:int=50) -> list[Profile]:
    """
    list profiles from the server, verifying each.

    args ::
        ctx :: dict containing the client context.
        offset :: int of the offset to start listing from.
        limit :: int of the maximum number of items to list.
    
    return :: list of Profile objects.

    raises :: ConfigError, MSpecError
    """

    try:
        url = f'{ctx["host"]}/api/user/profile?offset={offset}&limit={limit}'
    except KeyError:
        raise ConfigError('invalid context, missing host')

    try:
        request = Request(url, headers=ctx['headers'], method='GET')
        
        with urlopen(request) as response:
            response_body = response.read().decode('utf-8')

        response_data = json.loads(response_body)

        return {
            'total': response_data['total'],
            'items': [Profile(**item).convert_types() for item in response_data['items']]
        }

    except (json.JSONDecodeError, TypeError) as e:
        raise MSpecError(f'invalid response from server, {e.__class__.__name__}: {e}')

    except Exception as e:
        raise MSpecError(f'error listing profiles: {e.__class__.__name__}: {e}')