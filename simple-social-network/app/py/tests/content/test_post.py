import math
import unittest
import sqlite3
import time

from core.db import create_db_context
from core.client import *
from core.models import *
from core.exceptions import *
from content.post.model import Post
from content.post.client import *


def test_ctx_init() -> dict:
    ctx = create_db_context()
    ctx.update(create_client_context())
    return ctx

# create user for auth testing
def new_user() -> tuple[dict, User]:
    new_ctx = test_ctx_init()
    user = CreateUser(
        name='Test Post Auth',
        email=f'test-post-auth-{time.time()}@email.com',
        password1='my-test-password',
        password2='my-test-password',
    )
    created_user = client_create_user(new_ctx, user)
    login_ctx = client_login(new_ctx, created_user.email, user.password1)
    return login_ctx, created_user


class TestPost(unittest.TestCase):

    
    def test_post_auth(self):
        test_post = Post.example()
        test_post.validate()

        logged_out_ctx = test_ctx_init()

        # should not be able to create post if logged out #
        self.assertRaises(AuthenticationError, client_create_post, logged_out_ctx, test_post)

    

    

    def test_post_crud(self):
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

        

        test_post = Post.example()
        try:
            test_post.user_id = ''
        except AttributeError:
            """ignore if model does not have user_id"""
        test_post.validate()

        # create #

        created_post = client_create_post(crud_ctx, test_post)
        self.assertTrue(isinstance(created_post, Post))
        created_post.validate()
        test_post.id = created_post.id
        try:
            test_post.user_id = created_post.user_id
        except AttributeError:
            pass

        self.assertEqual(created_post, test_post)

        # read #

        post_read = client_read_post(crud_ctx, created_post.id)
        self.assertTrue(isinstance(post_read, Post))
        post_read.validate()
        self.assertEqual(post_read, test_post)
            
        # update #

        updated_post = client_update_post(crud_ctx, post_read)
        self.assertTrue(isinstance(updated_post, Post))
        updated_post.validate()
        self.assertEqual(post_read, updated_post)

        # delete #

        delete_return = client_delete_post(crud_ctx, created_post.id)
        self.assertIsNone(delete_return)
        self.assertRaises(NotFoundError, client_read_post, crud_ctx, created_post.id)

        cursor:sqlite3.Cursor = crud_ctx['db']['cursor']
        fetched_item = cursor.execute(f"SELECT * FROM post WHERE id=?", (created_post.id,)).fetchone()
        self.assertIsNone(fetched_item)

        

    def test_post_pagination(self):

        pagination_ctx = test_ctx_init()

        # seed data #

        init_response = client_list_post(pagination_ctx, offset=0, limit=101)
        total_items = init_response['total']
        
        if total_items < 15:
            seed_ctx = create_client_context()
            
            new_user_ctx, _user = new_user()
            seed_ctx.update(new_user_ctx)

            
            while total_items < 15:
                
                item = Post.random()
                client_create_post(seed_ctx, item)
                total_items += 1

        test_post = Post.example()
        test_post.validate()

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
                result = client_list_post(pagination_ctx, offset=offset, limit=page_size)
                items = result['items']
                items_len = 0
                for item in items:
                    items_len += 1
                    item.validate()

                    self.assertTrue(isinstance(item, Post))
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