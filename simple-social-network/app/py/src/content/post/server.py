import json
import re
from urllib.parse import parse_qs
from core.exceptions import NotFoundError, RequestError, JSONResponse
from content.post.model import Post
from content.post.db import *


__all__ = [
    'post_routes'
]

#
# router
#

def post_routes(ctx:dict, env:dict, raw_req_body:bytes):

    # post - instance routes #

    if (instance := re.match(r'/api/content/post/(.+)', env['PATH_INFO'])) is not None:
        instance_id = instance.group(1)
        if env['REQUEST_METHOD'] == 'GET':
            try:
                item = db_read_post(ctx, instance_id)
                ctx['log'](f'GET content.post/{instance_id}')
                raise JSONResponse('200 OK', item.to_dict())
            except NotFoundError:
                ctx['log'](f'GET content.post/{instance_id} - Not Found')
                raise RequestError('404 Not Found', f'not found content.post.{instance_id}')

        elif env['REQUEST_METHOD'] == 'PUT':
            incoming_item = Post(**json.loads(raw_req_body.decode('utf-8'))).convert_types()

            try:
                if instance_id != incoming_item.id:
                    raise RequestError('400 Bad Request', 'post id mismatch')
            except KeyError:
                raise RequestError('400 Bad Request', 'post is missing id')

            try:
                updated_item = db_update_post(ctx, incoming_item)
            except NotFoundError:
                ctx['log'](f'PUT content.post/{instance_id} - Not Found')
                raise RequestError('404 Not Found', f'not found content.post.{instance_id}')
            
            ctx['log'](f'PUT content.post/{instance_id}')
            raise JSONResponse('200 OK', updated_item.to_dict())

        elif env['REQUEST_METHOD'] == 'DELETE':
            db_delete_post(ctx, instance_id)
            ctx['log'](f'DELETE content.post/{instance_id}')
            raise JSONResponse('204 No Content')
        
        else:
            ctx['log'](f'ERROR 405 content.post/{instance_id}')
            raise RequestError('405 Method Not Allowed', 'invalid request method')

    # post - model routes #

    elif re.match(r'/api/content/post', env['PATH_INFO']):
        if env['REQUEST_METHOD'] == 'POST':
            incoming_item = Post(**json.loads(raw_req_body.decode('utf-8'))).convert_types()
            item = db_create_post(ctx, incoming_item)

            ctx['log'](f'POST content.post - id: {item.id}')
            raise JSONResponse('200 OK', item.to_dict())
        
        elif env['REQUEST_METHOD'] == 'GET':
            query = parse_qs(env['QUERY_STRING'])
            offset = query.get('offset', [0])[0]
            limit = query.get('limit', [25])[0]

            db_result = db_list_post(ctx, offset=int(offset), limit=int(limit))
            ctx['log'](f'GET content.post')

            raise JSONResponse('200 OK', {
                'total': db_result['total'],
                'items': [Post.to_dict(item) for item in db_result['items']]
            })
    
        else:
            ctx['log'](f'ERROR 405 content.post')
            raise RequestError('405 Method Not Allowed', 'invalid request method')