import math
import unittest
import sqlite3
import time

from core.db import create_db_context
from core.client import *
from core.models import *
from core.exceptions import *
from store.products.model import Products
from store.products.client import *


def test_ctx_init() -> dict:
    ctx = create_db_context()
    ctx.update(create_client_context())
    return ctx



class TestProducts(unittest.TestCase):



    def test_products_crud(self):
        """
        only need to test the client, which by also tests the server and other modules

        + create
        + read
        + update
        + delete
        """

        crud_ctx = test_ctx_init()


        test_products = Products.example()
        try:
            test_products.user_id = ''
        except AttributeError:
            """ignore if model does not have user_id"""
        test_products.validate()

        # create #

        created_products = client_create_products(crud_ctx, test_products)
        self.assertTrue(isinstance(created_products, Products))
        created_products.validate()
        test_products.id = created_products.id
        try:
            test_products.user_id = created_products.user_id
        except AttributeError:
            pass

        self.assertEqual(created_products, test_products)

        # read #

        products_read = client_read_products(crud_ctx, created_products.id)
        self.assertTrue(isinstance(products_read, Products))
        products_read.validate()
        self.assertEqual(products_read, test_products)
            
        # update #

        updated_products = client_update_products(crud_ctx, products_read)
        self.assertTrue(isinstance(updated_products, Products))
        updated_products.validate()
        self.assertEqual(products_read, updated_products)

        # delete #

        delete_return = client_delete_products(crud_ctx, created_products.id)
        self.assertIsNone(delete_return)
        self.assertRaises(NotFoundError, client_read_products, crud_ctx, created_products.id)

        cursor:sqlite3.Cursor = crud_ctx['db']['cursor']
        fetched_item = cursor.execute(f"SELECT * FROM products WHERE id=?", (created_products.id,)).fetchone()
        self.assertIsNone(fetched_item)



    def test_products_pagination(self):

        pagination_ctx = test_ctx_init()

        # seed data #

        init_response = client_list_products(pagination_ctx, offset=0, limit=101)
        total_items = init_response['total']
        
        if total_items < 15:
            seed_ctx = create_client_context()
            while total_items < 15:

                item = Products.random()
                client_create_products(seed_ctx, item)
                total_items += 1

        test_products = Products.example()
        test_products.validate()

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
                result = client_list_products(pagination_ctx, offset=offset, limit=page_size)
                items = result['items']
                items_len = 0
                for item in items:
                    items_len += 1
                    item.validate()

                    self.assertTrue(isinstance(item, Products))
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