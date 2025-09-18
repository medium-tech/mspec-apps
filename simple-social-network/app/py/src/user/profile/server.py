import json
import re
from urllib.parse import parse_qs
from core.exceptions import NotFoundError, RequestError, JSONResponse
from user.profile.model import Profile
from user.profile.db import *


__all__ = [
    'profile_routes'
]

#
# router
#

def profile_routes(ctx:dict, env:dict, raw_req_body:bytes):

    # profile - instance routes #

    if (instance := re.match(r'/api/user/profile/(.+)', env['PATH_INFO'])) is not None:
        instance_id = instance.group(1)
        if env['REQUEST_METHOD'] == 'GET':
            try:
                item = db_read_profile(ctx, instance_id)
                ctx['log'](f'GET user.profile/{instance_id}')
                raise JSONResponse('200 OK', item.to_dict())
            except NotFoundError:
                ctx['log'](f'GET user.profile/{instance_id} - Not Found')
                raise RequestError('404 Not Found', f'not found user.profile.{instance_id}')

        elif env['REQUEST_METHOD'] == 'PUT':
            incoming_item = Profile(**json.loads(raw_req_body.decode('utf-8'))).convert_types()

            try:
                if instance_id != incoming_item.id:
                    raise RequestError('400 Bad Request', 'profile id mismatch')
            except KeyError:
                raise RequestError('400 Bad Request', 'profile is missing id')

            try:
                updated_item = db_update_profile(ctx, incoming_item)
            except NotFoundError:
                ctx['log'](f'PUT user.profile/{instance_id} - Not Found')
                raise RequestError('404 Not Found', f'not found user.profile.{instance_id}')
            
            ctx['log'](f'PUT user.profile/{instance_id}')
            raise JSONResponse('200 OK', updated_item.to_dict())

        elif env['REQUEST_METHOD'] == 'DELETE':
            db_delete_profile(ctx, instance_id)
            ctx['log'](f'DELETE user.profile/{instance_id}')
            raise JSONResponse('204 No Content')
        
        else:
            ctx['log'](f'ERROR 405 user.profile/{instance_id}')
            raise RequestError('405 Method Not Allowed', 'invalid request method')

    # profile - model routes #

    elif re.match(r'/api/user/profile', env['PATH_INFO']):
        if env['REQUEST_METHOD'] == 'POST':
            incoming_item = Profile(**json.loads(raw_req_body.decode('utf-8'))).convert_types()
            item = db_create_profile(ctx, incoming_item)

            ctx['log'](f'POST user.profile - id: {item.id}')
            raise JSONResponse('200 OK', item.to_dict())
        
        elif env['REQUEST_METHOD'] == 'GET':
            query = parse_qs(env['QUERY_STRING'])
            offset = query.get('offset', [0])[0]
            limit = query.get('limit', [25])[0]

            db_result = db_list_profile(ctx, offset=int(offset), limit=int(limit))
            ctx['log'](f'GET user.profile')

            raise JSONResponse('200 OK', {
                'total': db_result['total'],
                'items': [Profile.to_dict(item) for item in db_result['items']]
            })
    
        else:
            ctx['log'](f'ERROR 405 user.profile')
            raise RequestError('405 Method Not Allowed', 'invalid request method')