import argparse
import random
from pprint import pprint
from core.db import create_db_context
from core.client import create_client_context

from user.profile.client import *
from user.profile.db import *
from user.profile.model import *



#
# define arguments
#


parser = argparse.ArgumentParser(description='simple_social_network - user - cli')

parser.add_argument('command', type=str, choices=[
    'data-seed',

    'verify-profile',
    'random-profile',
    'example-profile',
    'db-create-profile',
    'db-read-profile',
    'db-update-profile',
    'db-delete-profile',
    'db-list-profile',
    'client-create-profile',
    'client-read-profile',
    'client-update-profile',
    'client-delete-profile',
    'client-list-profile',

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

        db_create_profile(cli_ctx, Profile.random())



elif args.command == 'verify-profile':
    result = Profile.from_json(args.json).validate()

elif args.command == 'random-profile':
    result = Profile.random().to_json()

elif args.command == 'example-profile':
    result = Profile.example().to_json()

elif args.command == 'db-create-profile':
    if args.json is None:
        raise Exception('must supply data via json argument')
    result = db_create_profile(cli_ctx, Profile.from_json(args.json))

elif args.command == 'db-read-profile':
    result = db_read_profile(cli_ctx, args.id)

elif args.command == 'db-update-profile':
    if args.json is None:
        raise Exception('must supply data via json argument')
    result = db_update_profile(cli_ctx, args.id, Profile.from_json(args.json))

elif args.command == 'db-delete-profile':
    result = db_delete_profile(cli_ctx, args.id)

elif args.command == 'db-list-profile':
    result = db_list_profile(cli_ctx, args.offset, args.limit)

elif args.command == 'client-create-profile':
    if args.json is None:
        raise Exception('must supply data via json argument')
    result = client_create_profile(cli_ctx, Profile.from_json(args.json))

elif args.command == 'client-read-profile':
    result = client_read_profile(cli_ctx, )

elif args.command == 'client-update-profile':
    result = client_update_profile(cli_ctx, )

elif args.command == 'client-delete-profile':
    result = client_delete_profile(cli_ctx, )

elif args.command == 'client-list-profile':
    result = client_list_profile(cli_ctx, args.offset, args.limit)


#
# output result
#

if isinstance(result, dict):
    pprint(result)
elif result is None:
    pass
else:
    print(result)