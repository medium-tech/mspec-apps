import json
import re
from urllib.parse import parse_qs
from core.exceptions import NotFoundError, RequestError, JSONResponse
from admin.employees.model import Employees
from admin.employees.db import *


__all__ = [
    'employees_routes'
]

#
# router
#

def employees_routes(ctx:dict, env:dict, raw_req_body:bytes):

    # employees - instance routes #

    if (instance := re.match(r'/api/admin/employees/(.+)', env['PATH_INFO'])) is not None:
        instance_id = instance.group(1)
        if env['REQUEST_METHOD'] == 'GET':
            try:
                item = db_read_employees(ctx, instance_id)
                ctx['log'](f'GET admin.employees/{instance_id}')
                raise JSONResponse('200 OK', item.to_dict())
            except NotFoundError:
                ctx['log'](f'GET admin.employees/{instance_id} - Not Found')
                raise RequestError('404 Not Found', f'not found admin.employees.{instance_id}')

        elif env['REQUEST_METHOD'] == 'PUT':
            incoming_item = Employees(**json.loads(raw_req_body.decode('utf-8'))).convert_types()

            try:
                if instance_id != incoming_item.id:
                    raise RequestError('400 Bad Request', 'employees id mismatch')
            except KeyError:
                raise RequestError('400 Bad Request', 'employees is missing id')

            try:
                updated_item = db_update_employees(ctx, incoming_item)
            except NotFoundError:
                ctx['log'](f'PUT admin.employees/{instance_id} - Not Found')
                raise RequestError('404 Not Found', f'not found admin.employees.{instance_id}')
            
            ctx['log'](f'PUT admin.employees/{instance_id}')
            raise JSONResponse('200 OK', updated_item.to_dict())

        elif env['REQUEST_METHOD'] == 'DELETE':
            db_delete_employees(ctx, instance_id)
            ctx['log'](f'DELETE admin.employees/{instance_id}')
            raise JSONResponse('204 No Content')
        
        else:
            ctx['log'](f'ERROR 405 admin.employees/{instance_id}')
            raise RequestError('405 Method Not Allowed', 'invalid request method')

    # employees - model routes #

    elif re.match(r'/api/admin/employees', env['PATH_INFO']):
        if env['REQUEST_METHOD'] == 'POST':
            incoming_item = Employees(**json.loads(raw_req_body.decode('utf-8'))).convert_types()
            item = db_create_employees(ctx, incoming_item)

            ctx['log'](f'POST admin.employees - id: {item.id}')
            raise JSONResponse('200 OK', item.to_dict())
        
        elif env['REQUEST_METHOD'] == 'GET':
            query = parse_qs(env['QUERY_STRING'])
            offset = query.get('offset', [0])[0]
            limit = query.get('limit', [25])[0]

            items = db_list_employees(ctx, offset=int(offset), limit=int(limit))
            ctx['log'](f'GET admin.employees')

            raise JSONResponse('200 OK', [Employees.to_dict(item) for item in items])
    
        else:
            ctx['log'](f'ERROR 405 admin.employees')
            raise RequestError('405 Method Not Allowed', 'invalid request method')