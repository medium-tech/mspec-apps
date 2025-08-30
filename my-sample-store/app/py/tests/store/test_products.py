import unittest
import sqlite3

from core.db import create_db_context
from core.client import create_client_context
from core.exceptions import NotFoundError
from store.products.model import Products
from store.products.client import *


test_ctx = create_db_context()
test_ctx.update(create_client_context())

class TestProducts(unittest.TestCase):

    def test_products_crud(self):
        """
        only need to test the client, which by also tests the server and other modules

        + create
        + read
        + update
        + delete
        """

        test_products = Products.example()
        test_products.validate()

        # create #
        
        created_products = client_create_products(test_ctx, test_products)
        self.assertTrue(isinstance(created_products, Products))
        created_products.validate()
        test_products.id = created_products.id

        self.assertEqual(created_products, test_products)

        # read #

        products_read = client_read_products(test_ctx, created_products.id)
        self.assertTrue(isinstance(products_read, Products))
        products_read.validate()
        self.assertEqual(products_read, test_products)
            
        # update #

        updated_products = client_update_products(test_ctx, products_read)
        self.assertTrue(isinstance(updated_products, Products))
        updated_products.validate()
        self.assertEqual(products_read, updated_products)

        # delete #

        delete_return = client_delete_products(test_ctx, created_products.id)
        self.assertIsNone(delete_return)
        self.assertRaises(NotFoundError, client_read_products, test_ctx, created_products.id)

        cursor:sqlite3.Cursor = test_ctx['db']['cursor']
        fetched_item = cursor.execute(f"SELECT * FROM products WHERE id=?", (created_products.id,)).fetchone()
        self.assertIsNone(fetched_item)



    def test_products_pagination(self):

        # seed data #

        items = client_list_products(test_ctx, offset=0, limit=101)
        items_len = len(items)
        if items_len > 100:
            raise Exception('excpecting 100 items or less, delete db and restart test')
        
        if items_len < 50:
            difference = 50 - items_len
            for _ in range(difference):
                item = Products.random()
                item = client_create_products(test_ctx, item)
        elif items_len > 50:
            difference = items_len - 50
            items_to_delete = items[:difference]
            for item in items_to_delete:
                client_delete_products(test_ctx, item.id)

        test_products = Products.example()
        test_products.validate()

        # paginate #

        pg_configs = [
            {'page_size': 10, 'expected_pages': 5},
            {'page_size': 20, 'expected_pages': 3},
            {'page_size': 25, 'expected_pages': 2},
            {'page_size': 50, 'expected_pages': 1}
        ]

        for pg_config in pg_configs:
            page_size = pg_config['page_size']
            expected_pages = pg_config['expected_pages']

            offset = 0
            item_ids = []
            num_pages = 0
            while True:
                items = client_list_products(test_ctx, offset=offset, limit=page_size)
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
            self.assertEqual(len(item_ids), 50)
            self.assertEqual(len(set(item_ids)), 50)
            

if __name__ == '__main__':
    unittest.main()