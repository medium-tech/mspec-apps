import argparse
import random
from pprint import pprint
from core.db import create_db_context
from core.client import create_client_context

from store.products.client import *
from store.products.db import *
from store.products.model import *

from store.customers.client import *
from store.customers.db import *
from store.customers.model import *



#
# define arguments
#


parser = argparse.ArgumentParser(description='my_sample_store - store - cli')

parser.add_argument('command', type=str, choices=[
    'data-seed',

    'verify-products',
    'random-products',
    'example-products',
    'db-create-products',
    'db-read-products',
    'db-update-products',
    'db-delete-products',
    'db-list-products',
    'client-create-products',
    'client-read-products',
    'client-update-products',
    'client-delete-products',
    'client-list-products',

    'verify-customers',
    'random-customers',
    'example-customers',
    'db-create-customers',
    'db-read-customers',
    'db-update-customers',
    'db-delete-customers',
    'db-list-customers',
    'client-create-customers',
    'client-read-customers',
    'client-update-customers',
    'client-delete-customers',
    'client-list-customers',

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

        db_create_products(cli_ctx, Products.random())

        db_create_customers(cli_ctx, Customers.random())



elif args.command == 'verify-products':
    result = Products.from_json(args.json).validate()

elif args.command == 'random-products':
    result = Products.random().to_json()

elif args.command == 'example-products':
    result = Products.example().to_json()

elif args.command == 'db-create-products':
    if args.json is None:
        raise Exception('must supply data via json argument')
    result = db_create_products(cli_ctx, Products.from_json(args.json))

elif args.command == 'db-read-products':
    result = db_read_products(cli_ctx, args.id)

elif args.command == 'db-update-products':
    if args.json is None:
        raise Exception('must supply data via json argument')
    result = db_update_products(cli_ctx, args.id, Products.from_json(args.json))

elif args.command == 'db-delete-products':
    result = db_delete_products(cli_ctx, args.id)

elif args.command == 'db-list-products':
    result = db_list_products(cli_ctx, args.offset, args.limit)

elif args.command == 'client-create-products':
    if args.json is None:
        raise Exception('must supply data via json argument')
    result = client_create_products(cli_ctx, Products.from_json(args.json))

elif args.command == 'client-read-products':
    result = client_read_products(cli_ctx, )

elif args.command == 'client-update-products':
    result = client_update_products(cli_ctx, )

elif args.command == 'client-delete-products':
    result = client_delete_products(cli_ctx, )

elif args.command == 'client-list-products':
    result = client_list_products(cli_ctx, args.offset, args.limit)

elif args.command == 'verify-customers':
    result = Customers.from_json(args.json).validate()

elif args.command == 'random-customers':
    result = Customers.random().to_json()

elif args.command == 'example-customers':
    result = Customers.example().to_json()

elif args.command == 'db-create-customers':
    if args.json is None:
        raise Exception('must supply data via json argument')
    result = db_create_customers(cli_ctx, Customers.from_json(args.json))

elif args.command == 'db-read-customers':
    result = db_read_customers(cli_ctx, args.id)

elif args.command == 'db-update-customers':
    if args.json is None:
        raise Exception('must supply data via json argument')
    result = db_update_customers(cli_ctx, args.id, Customers.from_json(args.json))

elif args.command == 'db-delete-customers':
    result = db_delete_customers(cli_ctx, args.id)

elif args.command == 'db-list-customers':
    result = db_list_customers(cli_ctx, args.offset, args.limit)

elif args.command == 'client-create-customers':
    if args.json is None:
        raise Exception('must supply data via json argument')
    result = client_create_customers(cli_ctx, Customers.from_json(args.json))

elif args.command == 'client-read-customers':
    result = client_read_customers(cli_ctx, )

elif args.command == 'client-update-customers':
    result = client_update_customers(cli_ctx, )

elif args.command == 'client-delete-customers':
    result = client_delete_customers(cli_ctx, )

elif args.command == 'client-list-customers':
    result = client_list_customers(cli_ctx, args.offset, args.limit)


#
# output result
#

if isinstance(result, dict):
    pprint(result)
elif result is None:
    pass
else:
    print(result)