from core.exceptions import MSpecError, ConfigError, NotFoundError, AuthenticationError, ForbiddenError
from content.post.model import Post

import json

from urllib.request import Request, urlopen
from urllib.error import HTTPError


__all__ = [
    'client_create_post',
    'client_read_post',
    'client_update_post',
    'client_delete_post',
    'client_list_post'
]

def client_create_post(ctx:dict, obj:Post) -> Post:
    """
    create a post on the server, verifying the data first.
    
    args ::
        ctx :: dict containing the client context.
        obj :: the Post object to create.
    
    return :: Post object with the new id.

    raises :: ConfigError, MSpecError
    """

    try:
        url = f'{ctx["host"]}/api/content/post'
    except KeyError:
        raise ConfigError('invalid context, missing host')

    request_body = obj.validate().to_json().encode()

    try:
        request = Request(url, headers=ctx['headers'], method='POST', data=request_body)

        with urlopen(request) as response:
            response_body = response.read().decode('utf-8')
            return Post(**json.loads(response_body)).convert_types()
        
    except HTTPError as e:
        if e.code == 401:
            raise AuthenticationError('Error creating post: authentication error')
        elif e.code == 403:
            raise ForbiddenError('Error creating post: forbidden')

        raise MSpecError(f'error creating post: {e.__class__.__name__}: {e}')

    except (json.JSONDecodeError, KeyError) as e:
        raise MSpecError(f'invalid response from server, {e.__class__.__name__}: {e}')
    except Exception as e:
        raise MSpecError(f'error creating post: {e.__class__.__name__}: {e}')

def client_read_post(ctx:dict, id:str) -> Post:
    """
    read a post from the server, verifying it first.

    args ::
        ctx :: dict containing the client context.
        id :: str of the id of the item to read.
    
    return :: profile object if it exists.

    raises :: ConfigError, MSpecError, NotFoundError
    """

    try:
        url = ctx['host'] + '/api/content/post/' + id
    except KeyError:
        raise ConfigError('invalid context, missing host')

    try:

        request = Request(url, headers=ctx['headers'], method='GET')

        with urlopen(request) as response:
            response_body = response.read().decode('utf-8')

    except HTTPError as e:
        if e.code == 401:
            raise AuthenticationError('Error reading post: invalid username or password')
        elif e.code == 403:
            raise ForbiddenError('Error reading post: forbidden')
        elif e.code == 404:
            raise NotFoundError(f'post {id} not found')
        raise MSpecError(f'error reading post: {e.__class__.__name__}: {e}')
    except (json.JSONDecodeError, KeyError) as e:
        raise MSpecError('invalid response from server, {e.__class__.__name__}: {e}')
    except Exception as e:
        raise MSpecError(f'error reading post: {e.__class__.__name__}: {e}')

    return Post(**json.loads(response_body)).convert_types()

def client_update_post(ctx:dict, obj:Post) -> Post:
    """
    update a post on the server, verifying the data first.

    args ::
        ctx :: dict containing the client context.
        obj :: the Post object to update.
    
    return :: Post object.

    raises :: ConfigError, MSpecError, NotFoundError
    """
    try:
        _id = obj.id
    except KeyError:
        raise ValueError('invalid data, missing id')

    if _id is None:
        raise ValueError('invalid data, missing id')

    try:
        url = f'{ctx["host"]}/api/content/post/{_id}'
    except KeyError:
        raise ConfigError('invalid context, missing host')

    request_body = obj.validate().to_json().encode()

    try:
        request = Request(url, headers=ctx['headers'], method='PUT', data=request_body)

        with urlopen(request) as response:
            response_body = response.read().decode('utf-8')
    
    except HTTPError as e:
        if e.code == 401:
            raise AuthenticationError('Error updating post: authentication error')
        elif e.code == 403:
            raise ForbiddenError('Error updating post: forbidden')
        elif e.code == 404:
            raise NotFoundError(f'post {id} not found')
        raise MSpecError(f'error updating post: {e.__class__.__name__}: {e}')
        
    except (json.JSONDecodeError, KeyError) as e:
        raise MSpecError('invalid response from server, {e.__class__.__name__}: {e}')
    
    except Exception as e:
        raise MSpecError(f'error updating post: {e.__class__.__name__}: {e}')

    return Post(**json.loads(response_body)).convert_types()

def client_delete_post(ctx:dict, id:str) -> None:
    """
    delete a post from the server.

    args ::
        ctx :: dict containing the client context.
        id :: str of the id of the item to delete.
    
    return :: None

    raises :: ConfigError, MSpecError
    """

    try:
        url = f'{ctx["host"]}/api/content/post/{id}'
    except KeyError:
        raise ConfigError('invalid context, missing host')

    try:
        request = Request(url, headers=ctx['headers'], method='DELETE')

        with urlopen(request) as response:
            _ = response.read().decode('utf-8')

    except (json.JSONDecodeError, KeyError) as e:
        raise MSpecError('invalid response from server, {e.__class__.__name__}: {e}')
    
    except Exception as e:
        raise MSpecError(f'error deleting post: {e.__class__.__name__}: {e}')

def client_list_post(ctx:dict, offset:int=0, limit:int=50) -> list[Post]:
    """
    list posts from the server, verifying each.

    args ::
        ctx :: dict containing the client context.
        offset :: int of the offset to start listing from.
        limit :: int of the maximum number of items to list.
    
    return :: list of Post objects.

    raises :: ConfigError, MSpecError
    """

    try:
        url = f'{ctx["host"]}/api/content/post?offset={offset}&limit={limit}'
    except KeyError:
        raise ConfigError('invalid context, missing host')

    try:
        request = Request(url, headers=ctx['headers'], method='GET')
        
        with urlopen(request) as response:
            response_body = response.read().decode('utf-8')

        response_data = json.loads(response_body)

        return {
            'total': response_data['total'],
            'items': [Post(**item).convert_types() for item in response_data['items']]
        }

    except (json.JSONDecodeError, TypeError) as e:
        raise MSpecError(f'invalid response from server, {e.__class__.__name__}: {e}')

    except Exception as e:
        raise MSpecError(f'error listing posts: {e.__class__.__name__}: {e}')