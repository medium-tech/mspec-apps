import argparse
import random
from pprint import pprint
from core.db import create_db_context
from core.client import create_client_context

from admin.employees.client import *
from admin.employees.db import *
from admin.employees.model import *



#
# define arguments
#


parser = argparse.ArgumentParser(description='my_sample_store - admin - cli')

parser.add_argument('command', type=str, choices=[
    'data-seed',
    
    'verify-employees',
    'random-employees',
    'example-employees',
    'db-create-employees',
    'db-read-employees',
    'db-update-employees',
    'db-delete-employees',
    'db-list-employees',
    'client-create-employees',
    'client-read-employees',
    'client-update-employees',
    'client-delete-employees',
    'client-list-employees',
    
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
        
        db_create_employees(cli_ctx, Employees.random())
        


elif args.command == 'verify-employees':
    result = Employees.from_json(args.json).validate()

elif args.command == 'random-employees':
    result = Employees.random().to_json()

elif args.command == 'example-employees':
    result = Employees.example().to_json()

elif args.command == 'db-create-employees':
    if args.json is None:
        raise Exception('must supply data via json argument')
    result = db_create_employees(cli_ctx, Employees.from_json(args.json))

elif args.command == 'db-read-employees':
    result = db_read_employees(cli_ctx, args.id)

elif args.command == 'db-update-employees':
    if args.json is None:
        raise Exception('must supply data via json argument')
    result = db_update_employees(cli_ctx, args.id, Employees.from_json(args.json))

elif args.command == 'db-delete-employees':
    result = db_delete_employees(cli_ctx, args.id)

elif args.command == 'db-list-employees':
    result = db_list_employees(cli_ctx, args.offset, args.limit)

elif args.command == 'client-create-employees':
    if args.json is None:
        raise Exception('must supply data via json argument')
    result = client_create_employees(cli_ctx, Employees.from_json(args.json))

elif args.command == 'client-read-employees':
    result = client_read_employees(cli_ctx, )

elif args.command == 'client-update-employees':
    result = client_update_employees(cli_ctx, )

elif args.command == 'client-delete-employees':
    result = client_delete_employees(cli_ctx, )

elif args.command == 'client-list-employees':
    result = client_list_employees(cli_ctx, args.offset, args.limit)


#
# output result
#

if isinstance(result, dict):
    pprint(result)
elif result is None:
    pass
else:
    print(result)