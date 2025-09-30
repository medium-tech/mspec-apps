import math
import unittest
import sqlite3
import time

from core.db import create_db_context
from core.client import *
from core.models import *
from core.exceptions import *
from admin.employees.model import Employees
from admin.employees.client import *


def test_ctx_init() -> dict:
    ctx = create_db_context()
    ctx.update(create_client_context())
    return ctx

# create user for auth testing
def new_user() -> tuple[dict, User]:
    new_ctx = test_ctx_init()
    user = CreateUser(
        name='Test Employees Auth',
        email=f'test-employees-auth-{time.time()}@email.com',
        password1='my-test-password',
        password2='my-test-password',
    )
    created_user = client_create_user(new_ctx, user)
    login_ctx = client_login(new_ctx, created_user.email, user.password1)
    return login_ctx, created_user


class TestEmployees(unittest.TestCase):

    

    

    def test_employees_crud(self):
        """
        only need to test the client, which by also tests the server and other modules

        + create
        + read
        + update
        + delete
        """

        crud_ctx = test_ctx_init()
        

        test_employees = Employees.example()
        try:
            test_employees.user_id = ''
        except AttributeError:
            """ignore if model does not have user_id"""
        test_employees.validate()

        # create #

        created_employees = client_create_employees(crud_ctx, test_employees)
        self.assertTrue(isinstance(created_employees, Employees))
        created_employees.validate()
        test_employees.id = created_employees.id
        try:
            test_employees.user_id = created_employees.user_id
        except AttributeError:
            pass

        self.assertEqual(created_employees, test_employees)

        # read #

        employees_read = client_read_employees(crud_ctx, created_employees.id)
        self.assertTrue(isinstance(employees_read, Employees))
        employees_read.validate()
        self.assertEqual(employees_read, test_employees)
            
        # update #

        updated_employees = client_update_employees(crud_ctx, employees_read)
        self.assertTrue(isinstance(updated_employees, Employees))
        updated_employees.validate()
        self.assertEqual(employees_read, updated_employees)

        # delete #

        delete_return = client_delete_employees(crud_ctx, created_employees.id)
        self.assertIsNone(delete_return)
        self.assertRaises(NotFoundError, client_read_employees, crud_ctx, created_employees.id)

        cursor:sqlite3.Cursor = crud_ctx['db']['cursor']
        fetched_item = cursor.execute(f"SELECT * FROM employees WHERE id=?", (created_employees.id,)).fetchone()
        self.assertIsNone(fetched_item)

        

    def test_employees_pagination(self):

        pagination_ctx = test_ctx_init()

        # seed data #

        init_response = client_list_employees(pagination_ctx, offset=0, limit=101)
        total_items = init_response['total']
        
        if total_items < 15:
            seed_ctx = create_client_context()
            
            while total_items < 15:
                
                item = Employees.random()
                client_create_employees(seed_ctx, item)
                total_items += 1

        test_employees = Employees.example()
        test_employees.validate()

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
                result = client_list_employees(pagination_ctx, offset=offset, limit=page_size)
                items = result['items']
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
            self.assertEqual(len(item_ids), total_items)
            self.assertEqual(len(set(item_ids)), total_items)
            

if __name__ == '__main__':
    unittest.main()