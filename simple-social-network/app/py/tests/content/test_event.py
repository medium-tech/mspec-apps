import math
import unittest
import sqlite3
import time

from core.db import create_db_context
from core.client import *
from core.models import *
from core.exceptions import *
from content.event.model import Event
from content.event.client import *


def test_ctx_init() -> dict:
    ctx = create_db_context()
    ctx.update(create_client_context())
    return ctx

# create user for auth testing
def new_user() -> tuple[dict, User]:
    new_ctx = test_ctx_init()
    user = CreateUser(
        name='Test Event Auth',
        email=f'test-event-auth-{time.time()}@email.com',
        password1='my-test-password',
        password2='my-test-password',
    )
    created_user = client_create_user(new_ctx, user)
    login_ctx = client_login(new_ctx, created_user.email, user.password1)
    return login_ctx, created_user


class TestEvent(unittest.TestCase):

    
    def test_event_auth(self):
        test_event = Event.example()
        test_event.validate()

        logged_out_ctx = test_ctx_init()

        # should not be able to create event if logged out #
        self.assertRaises(AuthenticationError, client_create_event, logged_out_ctx, test_event)

    

    

    def test_event_crud(self):
        """
        only need to test the client, which by also tests the server and other modules

        + create
        + read
        + update
        + delete
        """

        crud_ctx = test_ctx_init()
        
        new_user_ctx, _user = new_user()
        crud_ctx.update(new_user_ctx)

        

        test_event = Event.example()
        try:
            test_event.user_id = ''
        except AttributeError:
            """ignore if model does not have user_id"""
        test_event.validate()

        # create #

        created_event = client_create_event(crud_ctx, test_event)
        self.assertTrue(isinstance(created_event, Event))
        created_event.validate()
        test_event.id = created_event.id
        try:
            test_event.user_id = created_event.user_id
        except AttributeError:
            pass

        self.assertEqual(created_event, test_event)

        # read #

        event_read = client_read_event(crud_ctx, created_event.id)
        self.assertTrue(isinstance(event_read, Event))
        event_read.validate()
        self.assertEqual(event_read, test_event)
            
        # update #

        updated_event = client_update_event(crud_ctx, event_read)
        self.assertTrue(isinstance(updated_event, Event))
        updated_event.validate()
        self.assertEqual(event_read, updated_event)

        # delete #

        delete_return = client_delete_event(crud_ctx, created_event.id)
        self.assertIsNone(delete_return)
        self.assertRaises(NotFoundError, client_read_event, crud_ctx, created_event.id)

        cursor:sqlite3.Cursor = crud_ctx['db']['cursor']
        fetched_item = cursor.execute(f"SELECT * FROM event WHERE id=?", (created_event.id,)).fetchone()
        self.assertIsNone(fetched_item)

        

    def test_event_pagination(self):

        pagination_ctx = test_ctx_init()

        # seed data #

        init_response = client_list_event(pagination_ctx, offset=0, limit=101)
        total_items = init_response['total']
        
        if total_items < 15:
            seed_ctx = create_client_context()
            
            new_user_ctx, _user = new_user()
            seed_ctx.update(new_user_ctx)

            
            while total_items < 15:
                
                item = Event.random()
                client_create_event(seed_ctx, item)
                total_items += 1

        test_event = Event.example()
        test_event.validate()

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
                result = client_list_event(pagination_ctx, offset=offset, limit=page_size)
                items = result['items']
                items_len = 0
                for item in items:
                    items_len += 1
                    item.validate()

                    self.assertTrue(isinstance(item, Event))
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