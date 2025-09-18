import argparse
import random
from pprint import pprint
from core.db import create_db_context
from core.client import create_client_context

from content.post.client import *
from content.post.db import *
from content.post.model import *

from content.event.client import *
from content.event.db import *
from content.event.model import *



#
# define arguments
#


parser = argparse.ArgumentParser(description='simple_social_network - content - cli')

parser.add_argument('command', type=str, choices=[
    'data-seed',

    'verify-post',
    'random-post',
    'example-post',
    'db-create-post',
    'db-read-post',
    'db-update-post',
    'db-delete-post',
    'db-list-post',
    'client-create-post',
    'client-read-post',
    'client-update-post',
    'client-delete-post',
    'client-list-post',

    'verify-event',
    'random-event',
    'example-event',
    'db-create-event',
    'db-read-event',
    'db-update-event',
    'db-delete-event',
    'db-list-event',
    'client-create-event',
    'client-read-event',
    'client-update-event',
    'client-delete-event',
    'client-list-event',

])

parser.add_argument('--id', type=str, default=None)
parser.add_argument('--json', type=str, default=None, help='pass in data as a json string')

parser.add_argument('--offset', type=int, default=0, help='used with pagination')
parser.add_argument('--limit', type=int, default=25, help='used with pagination')
parser.add_argument('--seed', type=int, default=None, help='seed for random data generation')
parser.add_argument('--count', type=int, default=101, help='number of items to seed')

#
# parse input
#

args = parser.parse_args()
    
if args.seed is not None:
    random.seed(args.seed)

cli_ctx = {}
cli_ctx.update(create_db_context())
cli_ctx.update(create_client_context())

#
# run program
#

if args.command == 'data-seed':
    for _ in range(args.count):

        db_create_post(cli_ctx, Post.random())

        db_create_event(cli_ctx, Event.random())



elif args.command == 'verify-post':
    result = Post.from_json(args.json).validate()

elif args.command == 'random-post':
    result = Post.random().to_json()

elif args.command == 'example-post':
    result = Post.example().to_json()

elif args.command == 'db-create-post':
    if args.json is None:
        raise Exception('must supply data via json argument')
    result = db_create_post(cli_ctx, Post.from_json(args.json))

elif args.command == 'db-read-post':
    result = db_read_post(cli_ctx, args.id)

elif args.command == 'db-update-post':
    if args.json is None:
        raise Exception('must supply data via json argument')
    result = db_update_post(cli_ctx, args.id, Post.from_json(args.json))

elif args.command == 'db-delete-post':
    result = db_delete_post(cli_ctx, args.id)

elif args.command == 'db-list-post':
    result = db_list_post(cli_ctx, args.offset, args.limit)

elif args.command == 'client-create-post':
    if args.json is None:
        raise Exception('must supply data via json argument')
    result = client_create_post(cli_ctx, Post.from_json(args.json))

elif args.command == 'client-read-post':
    result = client_read_post(cli_ctx, )

elif args.command == 'client-update-post':
    result = client_update_post(cli_ctx, )

elif args.command == 'client-delete-post':
    result = client_delete_post(cli_ctx, )

elif args.command == 'client-list-post':
    result = client_list_post(cli_ctx, args.offset, args.limit)

elif args.command == 'verify-event':
    result = Event.from_json(args.json).validate()

elif args.command == 'random-event':
    result = Event.random().to_json()

elif args.command == 'example-event':
    result = Event.example().to_json()

elif args.command == 'db-create-event':
    if args.json is None:
        raise Exception('must supply data via json argument')
    result = db_create_event(cli_ctx, Event.from_json(args.json))

elif args.command == 'db-read-event':
    result = db_read_event(cli_ctx, args.id)

elif args.command == 'db-update-event':
    if args.json is None:
        raise Exception('must supply data via json argument')
    result = db_update_event(cli_ctx, args.id, Event.from_json(args.json))

elif args.command == 'db-delete-event':
    result = db_delete_event(cli_ctx, args.id)

elif args.command == 'db-list-event':
    result = db_list_event(cli_ctx, args.offset, args.limit)

elif args.command == 'client-create-event':
    if args.json is None:
        raise Exception('must supply data via json argument')
    result = client_create_event(cli_ctx, Event.from_json(args.json))

elif args.command == 'client-read-event':
    result = client_read_event(cli_ctx, )

elif args.command == 'client-update-event':
    result = client_update_event(cli_ctx, )

elif args.command == 'client-delete-event':
    result = client_delete_event(cli_ctx, )

elif args.command == 'client-list-event':
    result = client_list_event(cli_ctx, args.offset, args.limit)


#
# output result
#

if isinstance(result, dict):
    pprint(result)
elif result is None:
    pass
else:
    print(result)