import unittest
import sqlite3

from core.db import create_db_context
from core.client import create_client_context
from core.exceptions import NotFoundError
from admin.employees.model import Employees
from admin.employees.client import *


test_ctx = create_db_context()
test_ctx.update(create_client_context())

class TestEmployees(unittest.TestCase):

    def test_employees_crud(self):
        """
        only need to test the client, which by also tests the server and other modules

        + create
        + read
        + update
        + delete
        """

        test_employees = Employees.example()
        test_employees.validate()

        # create #
        
        created_employees = client_create_employees(test_ctx, test_employees)
        self.assertTrue(isinstance(created_employees, Employees))
        created_employees.validate()
        test_employees.id = created_employees.id

        self.assertEqual(created_employees, test_employees)

        # read #

        employees_read = client_read_employees(test_ctx, created_employees.id)
        self.assertTrue(isinstance(employees_read, Employees))
        employees_read.validate()
        self.assertEqual(employees_read, test_employees)
            
        # update #

        updated_employees = client_update_employees(test_ctx, employees_read)
        self.assertTrue(isinstance(updated_employees, Employees))
        updated_employees.validate()
        self.assertEqual(employees_read, updated_employees)

        # delete #

        delete_return = client_delete_employees(test_ctx, created_employees.id)
        self.assertIsNone(delete_return)
        self.assertRaises(NotFoundError, client_read_employees, test_ctx, created_employees.id)

        cursor:sqlite3.Cursor = test_ctx['db']['cursor']
        fetched_item = cursor.execute(f"SELECT * FROM employees WHERE id=?", (created_employees.id,)).fetchone()
        self.assertIsNone(fetched_item)



    def test_employees_pagination(self):

        # seed data #

        items = client_list_employees(test_ctx, offset=0, limit=101)
        items_len = len(items)
        if items_len > 100:
            raise Exception('excpecting 100 items or less, delete db and restart test')
        
        if items_len < 50:
            difference = 50 - items_len
            for _ in range(difference):
                item = Employees.random()
                item = client_create_employees(test_ctx, item)
        elif items_len > 50:
            difference = items_len - 50
            items_to_delete = items[:difference]
            for item in items_to_delete:
                client_delete_employees(test_ctx, item.id)

        test_employees = Employees.example()
        test_employees.validate()

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
                items = client_list_employees(test_ctx, offset=offset, limit=page_size)
                items_len = 0
                for item in items:
                    items_len += 1
                    item.validate()

                    self.assertTrue(isinstance(item, Employees))
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