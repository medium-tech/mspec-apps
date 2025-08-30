from core.exceptions import MSpecError, ConfigError, NotFoundError, AuthenticationError, ForbiddenError
from store.products.model import Products

import json

from urllib.request import Request, urlopen
from urllib.error import HTTPError


__all__ = [
    'client_create_products',
    'client_read_products',
    'client_update_products',
    'client_delete_products',
    'client_list_products'
]

def client_create_products(ctx:dict, obj:Products) -> Products:
    """
    create a products on the server, verifying the data first.
    
    args ::
        ctx :: dict containing the client context.
        obj :: the Products object to create.
    
    return :: Products object with the new id.

    raises :: ConfigError, MSpecError
    """

    try:
        url = f'{ctx["host"]}/api/store/products'
    except KeyError:
        raise ConfigError('invalid context, missing host')

    request_body = obj.validate().to_json().encode()

    try:
        request = Request(url, headers=ctx['headers'], method='POST', data=request_body)

        with urlopen(request) as response:
            response_body = response.read().decode('utf-8')
            return Products(**json.loads(response_body)).convert_types()

    except (json.JSONDecodeError, KeyError) as e:
        raise MSpecError(f'invalid response from server, {e.__class__.__name__}: {e}')
    except Exception as e:
        raise MSpecError(f'error creating products: {e.__class__.__name__}: {e}')

def client_read_products(ctx:dict, id:str) -> Products:
    """
    read a products from the server, verifying it first.

    args ::
        ctx :: dict containing the client context.
        id :: str of the id of the item to read.
    
    return :: profile object if it exists.

    raises :: ConfigError, MSpecError, NotFoundError
    """

    try:
        url = ctx['host'] + '/api/store/products/' + id
    except KeyError:
        raise ConfigError('invalid context, missing host')

    try:

        request = Request(url, headers=ctx['headers'], method='GET')

        with urlopen(request) as response:
            response_body = response.read().decode('utf-8')

    except HTTPError as e:
        if e.code == 401:
            raise AuthenticationError('Error reading products: invalid username or password')
        elif e.code == 403:
            raise ForbiddenError('Error reading products: forbidden')
        elif e.code == 404:
            raise NotFoundError(f'products {id} not found')
        raise MSpecError(f'error reading products: {e.__class__.__name__}: {e}')
    except (json.JSONDecodeError, KeyError) as e:
        raise MSpecError('invalid response from server, {e.__class__.__name__}: {e}')
    except Exception as e:
        raise MSpecError(f'error reading products: {e.__class__.__name__}: {e}')

    return Products(**json.loads(response_body)).convert_types()

def client_update_products(ctx:dict, obj:Products) -> Products:
    """
    update a products on the server, verifying the data first.

    args ::
        ctx :: dict containing the client context.
        obj :: the Products object to update.
    
    return :: Products object.

    raises :: ConfigError, MSpecError, NotFoundError
    """
    try:
        _id = obj.id
    except KeyError:
        raise ValueError('invalid data, missing id')

    if _id is None:
        raise ValueError('invalid data, missing id')

    try:
        url = f'{ctx["host"]}/api/store/products/{_id}'
    except KeyError:
        raise ConfigError('invalid context, missing host')

    request_body = obj.validate().to_json().encode()

    try:
        request = Request(url, headers=ctx['headers'], method='PUT', data=request_body)

        with urlopen(request) as response:
            response_body = response.read().decode('utf-8')
    
    except HTTPError as e:
        if e.code == 401:
            raise AuthenticationError('Error updating products: authentication error')
        elif e.code == 403:
            raise ForbiddenError('Error updating products: forbidden')
        elif e.code == 404:
            raise NotFoundError(f'products {id} not found')
        raise MSpecError(f'error updating products: {e.__class__.__name__}: {e}')
        
    except (json.JSONDecodeError, KeyError) as e:
        raise MSpecError('invalid response from server, {e.__class__.__name__}: {e}')
    
    except Exception as e:
        raise MSpecError(f'error updating products: {e.__class__.__name__}: {e}')

    return Products(**json.loads(response_body)).convert_types()

def client_delete_products(ctx:dict, id:str) -> None:
    """
    delete a products from the server.

    args ::
        ctx :: dict containing the client context.
        id :: str of the id of the item to delete.
    
    return :: None

    raises :: ConfigError, MSpecError
    """

    try:
        url = f'{ctx["host"]}/api/store/products/{id}'
    except KeyError:
        raise ConfigError('invalid context, missing host')

    try:
        request = Request(url, headers=ctx['headers'], method='DELETE')

        with urlopen(request) as response:
            _ = response.read().decode('utf-8')

    except (json.JSONDecodeError, KeyError) as e:
        raise MSpecError('invalid response from server, {e.__class__.__name__}: {e}')
    
    except Exception as e:
        raise MSpecError(f'error deleting products: {e.__class__.__name__}: {e}')

def client_list_products(ctx:dict, offset:int=0, limit:int=50) -> list[Products]:
    """
    list productss from the server, verifying each.

    args ::
        ctx :: dict containing the client context.
        offset :: int of the offset to start listing from.
        limit :: int of the maximum number of items to list.
    
    return :: list of Products objects.

    raises :: ConfigError, MSpecError
    """

    try:
        url = f'{ctx["host"]}/api/store/products?offset={offset}&limit={limit}'
    except KeyError:
        raise ConfigError('invalid context, missing host')

    try:
        request = Request(url, headers=ctx['headers'], method='GET')
        
        with urlopen(request) as response:
            response_body = response.read().decode('utf-8')

        return [Products(**item).convert_types() for item in json.loads(response_body)]

    except (json.JSONDecodeError, TypeError) as e:
        raise MSpecError(f'invalid response from server, {e.__class__.__name__}: {e}')

    except Exception as e:
        raise MSpecError(f'error listing productss: {e.__class__.__name__}: {e}')