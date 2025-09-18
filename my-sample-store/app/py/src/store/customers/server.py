import json
import re
from urllib.parse import parse_qs
from core.exceptions import NotFoundError, RequestError, JSONResponse
from store.customers.model import Customers
from store.customers.db import *


__all__ = [
    'customers_routes'
]

#
# router
#

def customers_routes(ctx:dict, env:dict, raw_req_body:bytes):

    # customers - instance routes #

    if (instance := re.match(r'/api/store/customers/(.+)', env['PATH_INFO'])) is not None:
        instance_id = instance.group(1)
        if env['REQUEST_METHOD'] == 'GET':
            try:
                item = db_read_customers(ctx, instance_id)
                ctx['log'](f'GET store.customers/{instance_id}')
                raise JSONResponse('200 OK', item.to_dict())
            except NotFoundError:
                ctx['log'](f'GET store.customers/{instance_id} - Not Found')
                raise RequestError('404 Not Found', f'not found store.customers.{instance_id}')

        elif env['REQUEST_METHOD'] == 'PUT':
            incoming_item = Customers(**json.loads(raw_req_body.decode('utf-8'))).convert_types()

            try:
                if instance_id != incoming_item.id:
                    raise RequestError('400 Bad Request', 'customers id mismatch')
            except KeyError:
                raise RequestError('400 Bad Request', 'customers is missing id')

            try:
                updated_item = db_update_customers(ctx, incoming_item)
            except NotFoundError:
                ctx['log'](f'PUT store.customers/{instance_id} - Not Found')
                raise RequestError('404 Not Found', f'not found store.customers.{instance_id}')
            
            ctx['log'](f'PUT store.customers/{instance_id}')
            raise JSONResponse('200 OK', updated_item.to_dict())

        elif env['REQUEST_METHOD'] == 'DELETE':
            db_delete_customers(ctx, instance_id)
            ctx['log'](f'DELETE store.customers/{instance_id}')
            raise JSONResponse('204 No Content')
        
        else:
            ctx['log'](f'ERROR 405 store.customers/{instance_id}')
            raise RequestError('405 Method Not Allowed', 'invalid request method')

    # customers - model routes #

    elif re.match(r'/api/store/customers', env['PATH_INFO']):
        if env['REQUEST_METHOD'] == 'POST':
            incoming_item = Customers(**json.loads(raw_req_body.decode('utf-8'))).convert_types()
            item = db_create_customers(ctx, incoming_item)

            ctx['log'](f'POST store.customers - id: {item.id}')
            raise JSONResponse('200 OK', item.to_dict())
        
        elif env['REQUEST_METHOD'] == 'GET':
            query = parse_qs(env['QUERY_STRING'])
            offset = query.get('offset', [0])[0]
            limit = query.get('limit', [25])[0]

            db_result = db_list_customers(ctx, offset=int(offset), limit=int(limit))
            ctx['log'](f'GET store.customers')

            raise JSONResponse('200 OK', {
                'total': db_result['total'],
                'items': [Customers.to_dict(item) for item in db_result['items']]
            })
    
        else:
            ctx['log'](f'ERROR 405 store.customers')
            raise RequestError('405 Method Not Allowed', 'invalid request method')