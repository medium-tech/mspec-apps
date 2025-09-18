import sqlite3
from datetime import datetime
from core.types import datetime_format_str
from core.exceptions import NotFoundError
from content.post.model import Post


__all__ = [
    'db_create_post', 
    'db_read_post',
    'db_update_post', 
    'db_delete_post', 
    'db_list_post',
]

def db_create_post(ctx:dict, obj:Post) -> Post:
    """
    create a single model in the database, verifying the data first.

    args ::
        ctx :: dict containing the database client
        obj :: the Post object to create.

    return :: and Post object with the new id.
    """
    if obj.id is not None:
        raise ValueError('id must be null to create a new item')
    
    obj.validate()
    cursor:sqlite3.Cursor = ctx['db']['cursor']
    # must be logged in to make post
    user = ctx['auth']['get_user']()
    if obj.user_id != '' and obj.user_id != user.id:
        raise ValueError(f'Incorrect user_id ({obj.user_id} != {user.id}) supplied for post creation')
    
    obj.user_id = user.id
    assert obj.user_id is not None



    result = cursor.execute(
        "INSERT INTO post('content', 'user_id') VALUES(?, ?)",
        (obj.content, obj.user_id,)
    )
    assert result.rowcount == 1
    assert result.lastrowid is not None
    obj.id = str(result.lastrowid)



    ctx['db']['commit']()
    return obj

def db_read_post(ctx:dict, id:str) -> Post:
    """
    read a single model from the database and verify it.

    args ::
        ctx :: dict containing the database client
        id :: the id of the item to read.
    
    return :: the Post object.
    raises :: NotFoundError if the item is not found.
    """

    cursor:sqlite3.Cursor = ctx['db']['cursor']
    result = cursor.execute(f"SELECT * FROM post WHERE id=?", (id,))
    entry = result.fetchone()
    if entry is None:
        raise NotFoundError(f'post {id} not found')


    
    return Post(
        id=str(entry[0]),
        content=entry[1],

        user_id=entry[2],


    ).validate()

def db_update_post(ctx:dict, obj:Post) -> Post:
    """
    update a single model in the database, and verify the data first.

    args ::
        ctx :: dict containing the database client
        obj :: the Post object to update.

    return :: the Post object.
    raises :: NotFoundError if the item is not found
    """
    if obj.id is None:
        raise ValueError('id must not be null to update an item')
    
    obj.validate()
    cursor:sqlite3.Cursor = ctx['db']['cursor']


    result = cursor.execute(
        "UPDATE post SET 'content'=?, 'user_id'=? WHERE id=?",
        (obj.content, obj.user_id, obj.id)
    )
    if result.rowcount == 0:
        raise NotFoundError(f'post {obj.id} not found')



    ctx['db']['commit']()
    return obj

def db_delete_post(ctx:dict, id:str) -> None:
    """
    delete a single model from the database.

    args ::
        ctx :: dict containing the database client
        id :: the id of the item to delete.
    
    return :: None
    """

    cursor:sqlite3.Cursor = ctx['db']['cursor']


    cursor.execute(f"DELETE FROM post WHERE id=?", (id,))



    ctx['db']['commit']()

def db_list_post(ctx:dict, offset:int=0, limit:int=25) -> dict:
    """
    list single models from the database, and verify each

    args ::
        ctx :: dict containing the database client
        offset :: the offset to start listing from.
        limit :: the maximum number of items to list.
    
    return :: dict with two keys:
        total :: int of the total number of items.
        items :: list of each item as a dict.
    """
    cursor:sqlite3.Cursor = ctx['db']['cursor']
    
    items = []
    query = cursor.execute("SELECT * FROM post ORDER BY id LIMIT ? OFFSET ?", (limit, offset))

    for entry in query.fetchall():

        
        items.append(Post(
            id=str(entry[0]),
        content=entry[1],

        user_id=entry[2],


        ).validate())

    return {
        'total': cursor.execute("SELECT COUNT(*) FROM post").fetchone()[0],
        'items': items
    }