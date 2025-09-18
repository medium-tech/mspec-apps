import math
import unittest
import sqlite3
import time

from core.db import create_db_context
from core.client import *
from core.models import *
from core.exceptions import *
from store.customers.model import Customers
from store.customers.client import *


def test_ctx_init() -> dict:
    ctx = create_db_context()
    ctx.update(create_client_context())
    return ctx



class TestCustomers(unittest.TestCase):



    def test_customers_crud(self):
        """
        only need to test the client, which by also tests the server and other modules

        + create
        + read
        + update
        + delete
        """

        crud_ctx = test_ctx_init()


        test_customers = Customers.example()
        try:
            test_customers.user_id = ''
        except AttributeError:
            """ignore if model does not have user_id"""
        test_customers.validate()

        # create #

        created_customers = client_create_customers(crud_ctx, test_customers)
        self.assertTrue(isinstance(created_customers, Customers))
        created_customers.validate()
        test_customers.id = created_customers.id
        try:
            test_customers.user_id = created_customers.user_id
        except AttributeError:
            pass

        self.assertEqual(created_customers, test_customers)

        # read #

        customers_read = client_read_customers(crud_ctx, created_customers.id)
        self.assertTrue(isinstance(customers_read, Customers))
        customers_read.validate()
        self.assertEqual(customers_read, test_customers)
            
        # update #

        updated_customers = client_update_customers(crud_ctx, customers_read)
        self.assertTrue(isinstance(updated_customers, Customers))
        updated_customers.validate()
        self.assertEqual(customers_read, updated_customers)

        # delete #

        delete_return = client_delete_customers(crud_ctx, created_customers.id)
        self.assertIsNone(delete_return)
        self.assertRaises(NotFoundError, client_read_customers, crud_ctx, created_customers.id)

        cursor:sqlite3.Cursor = crud_ctx['db']['cursor']
        fetched_item = cursor.execute(f"SELECT * FROM customers WHERE id=?", (created_customers.id,)).fetchone()
        self.assertIsNone(fetched_item)



    def test_customers_pagination(self):

        pagination_ctx = test_ctx_init()

        # seed data #

        init_response = client_list_customers(pagination_ctx, offset=0, limit=101)
        total_items = init_response['total']
        
        if total_items < 15:
            seed_ctx = create_client_context()
            while total_items < 15:

                item = Customers.random()
                client_create_customers(seed_ctx, item)
                total_items += 1

        test_customers = Customers.example()
        test_customers.validate()

        # paginate #

        pg_configs = [
            {'page_size': 5, 'expected_pages': math.ceil(total_items / 5)},
            {'page_size': 8, 'expected_pages': math.ceil(total_items / 8)},
            {'page_size': 15, 'expected_pages': math.ceil(total_items / 15)}
        ]

        for pg_config in pg_configs:
            page_size = pg_config['page_size']
            expected_pages = pg_config['expected_pages']

            offset = 0
            item_ids = []
            num_pages = 0
            while True:
                result = client_list_customers(pagination_ctx, offset=offset, limit=page_size)
                items = result['items']
                items_len = 0
                for item in items:
                    items_len += 1
                    item.validate()

                    self.assertTrue(isinstance(item, Customers))
                    item_ids.append(item.id)

                if items_len > 0:
                    num_pages += 1

                if items_len < page_size:
                    break

                self.assertTrue(items_len <= page_size)

                offset += page_size
                
            self.assertEqual(num_pages, expected_pages)
            self.assertEqual(len(item_ids), total_items)
            self.assertEqual(len(set(item_ids)), total_items)
            

if __name__ == '__main__':
    unittest.main()