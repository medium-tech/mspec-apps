import math
import unittest
import sqlite3
import time

from core.db import create_db_context
from core.client import *
from core.models import *
from core.exceptions import *
from user.profile.model import Profile
from user.profile.client import *


def test_ctx_init() -> dict:
    ctx = create_db_context()
    ctx.update(create_client_context())
    return ctx

# create user for auth testing
def new_user() -> tuple[dict, User]:
    new_ctx = test_ctx_init()
    user = CreateUser(
        name='Test Profile Auth',
        email=f'test-profile-auth-{time.time()}@email.com',
        password1='my-test-password',
        password2='my-test-password',
    )
    created_user = client_create_user(new_ctx, user)
    login_ctx = client_login(new_ctx, created_user.email, user.password1)
    return login_ctx, created_user


class TestProfile(unittest.TestCase):

    
    def test_profile_auth(self):
        test_profile = Profile.example()
        test_profile.validate()

        logged_out_ctx = test_ctx_init()

        # should not be able to create profile if logged out #
        self.assertRaises(AuthenticationError, client_create_profile, logged_out_ctx, test_profile)

    

    
    def test_profile_auth_max_models(self):

        max_models_ctx, _user = new_user()

        for _ in range(1):
            client_create_profile(max_models_ctx, Profile.example())

        self.assertRaises(Exception, client_create_profile, max_models_ctx, Profile.example())

    

    def test_profile_crud(self):
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

        

        test_profile = Profile.example()
        try:
            test_profile.user_id = ''
        except AttributeError:
            """ignore if model does not have user_id"""
        test_profile.validate()

        # create #

        created_profile = client_create_profile(crud_ctx, test_profile)
        self.assertTrue(isinstance(created_profile, Profile))
        created_profile.validate()
        test_profile.id = created_profile.id
        try:
            test_profile.user_id = created_profile.user_id
        except AttributeError:
            pass

        self.assertEqual(created_profile, test_profile)

        # read #

        profile_read = client_read_profile(crud_ctx, created_profile.id)
        self.assertTrue(isinstance(profile_read, Profile))
        profile_read.validate()
        self.assertEqual(profile_read, test_profile)
            
        # update #

        updated_profile = client_update_profile(crud_ctx, profile_read)
        self.assertTrue(isinstance(updated_profile, Profile))
        updated_profile.validate()
        self.assertEqual(profile_read, updated_profile)

        # delete #

        delete_return = client_delete_profile(crud_ctx, created_profile.id)
        self.assertIsNone(delete_return)
        self.assertRaises(NotFoundError, client_read_profile, crud_ctx, created_profile.id)

        cursor:sqlite3.Cursor = crud_ctx['db']['cursor']
        fetched_item = cursor.execute(f"SELECT * FROM profile WHERE id=?", (created_profile.id,)).fetchone()
        self.assertIsNone(fetched_item)

        

    def test_profile_pagination(self):

        pagination_ctx = test_ctx_init()

        # seed data #

        init_response = client_list_profile(pagination_ctx, offset=0, limit=101)
        total_items = init_response['total']
        
        if total_items < 15:
            seed_ctx = create_client_context()
            
            new_user_ctx, _user = new_user()
            seed_ctx.update(new_user_ctx)

            
            while total_items < 15:
                
                # create new user(s) to avoid max models per user limits
                if total_items % 1 == 0:
                    new_user_ctx, _user = new_user()
                    seed_ctx.update(new_user_ctx)

                
                item = Profile.random()
                client_create_profile(seed_ctx, item)
                total_items += 1

        test_profile = Profile.example()
        test_profile.validate()

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
                result = client_list_profile(pagination_ctx, offset=offset, limit=page_size)
                items = result['items']
                items_len = 0
                for item in items:
                    items_len += 1
                    item.validate()

                    self.assertTrue(isinstance(item, Profile))
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