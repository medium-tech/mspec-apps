import sqlite3
from datetime import datetime
from core.types import datetime_format_str
from core.exceptions import NotFoundError
from user.profile.model import Profile


__all__ = [
    'db_create_profile', 
    'db_read_profile',
    'db_update_profile', 
    'db_delete_profile', 
    'db_list_profile',
]

def db_create_profile(ctx:dict, obj:Profile) -> Profile:
    """
    create a single model in the database, verifying the data first.

    args ::
        ctx :: dict containing the database client
        obj :: the Profile object to create.

    return :: and Profile object with the new id.
    """
    if obj.id is not None:
        raise ValueError('id must be null to create a new item')
    
    obj.validate()
    cursor:sqlite3.Cursor = ctx['db']['cursor']
    
    # must be logged in to make profile
    user = ctx['auth']['get_user']()
    if obj.user_id != '' and obj.user_id != user.id:
        raise ValueError(f'Incorrect user_id ({obj.user_id} != {user.id}) supplied for profile creation')
    
    obj.user_id = user.id
    assert obj.user_id is not None

    

    
    # each user can only create a maximum of 1 profile(s)
    cursor.execute("SELECT COUNT(*) FROM profile WHERE user_id=?", (user.id,))
    count = cursor.fetchone()[0]
    if count >= 1:
        raise ValueError('user has reached the maximum number of profile(s)')

    

    result = cursor.execute(
        "INSERT INTO profile('bio', 'user_id', 'username') VALUES(?, ?, ?)",
        (obj.bio, obj.user_id, obj.username,)
    )
    assert result.rowcount == 1
    assert result.lastrowid is not None
    obj.id = str(result.lastrowid)




    

    ctx['db']['commit']()
    return obj

def db_read_profile(ctx:dict, id:str) -> Profile:
    """
    read a single model from the database and verify it.

    args ::
        ctx :: dict containing the database client
        id :: the id of the item to read.
    
    return :: the Profile object.
    raises :: NotFoundError if the item is not found.
    """

    cursor:sqlite3.Cursor = ctx['db']['cursor']
    result = cursor.execute(f"SELECT * FROM profile WHERE id=?", (id,))
    entry = result.fetchone()
    if entry is None:
        raise NotFoundError(f'profile {id} not found')


    
    
    return Profile(
        id=str(entry[0]),
        
            
        bio=entry[1],

            
        
            
        user_id=str(entry[2]),

            
        
            
        username=entry[3],

            
        
        
    ).validate()

def db_update_profile(ctx:dict, obj:Profile) -> Profile:
    """
    update a single model in the database, and verify the data first.

    args ::
        ctx :: dict containing the database client
        obj :: the Profile object to update.

    return :: the Profile object.
    raises :: NotFoundError if the item is not found
    """
    if obj.id is None:
        raise ValueError('id must not be null to update an item')
    
    obj.validate()
    cursor:sqlite3.Cursor = ctx['db']['cursor']
    
    user = ctx['auth']['get_user']()
    if obj.user_id != user.id:
        raise ForbiddenError('not allowed to update this profile')

    

    result = cursor.execute(
        "UPDATE profile SET 'bio'=?, 'user_id'=?, 'username'=? WHERE id=?",
        (obj.bio, obj.user_id, obj.username, obj.id)
    )
    if result.rowcount == 0:
        raise NotFoundError(f'profile {obj.id} not found')




    ctx['db']['commit']()
    return obj

def db_delete_profile(ctx:dict, id:str) -> None:
    """
    delete a single model from the database.

    args ::
        ctx :: dict containing the database client
        id :: the id of the item to delete.
    
    return :: None
    """

    cursor:sqlite3.Cursor = ctx['db']['cursor']
    
    user = ctx['auth']['get_user']()
    try:
        obj = db_read_profile(ctx, id)
    except NotFoundError:
        return

    if obj.user_id != user.id:
        raise ForbiddenError('not allowed to delete this profile')

    


    cursor.execute(f"DELETE FROM profile WHERE id=?", (id,))


    

    ctx['db']['commit']()

def db_list_profile(ctx:dict, offset:int=0, limit:int=25) -> dict:
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
    query = cursor.execute("SELECT * FROM profile ORDER BY id LIMIT ? OFFSET ?", (limit, offset))

    for entry in query.fetchall():
        
        items.append(Profile(
            id=str(entry[0]),
            
                
        bio=entry[1],

                
            
                
        user_id=str(entry[2]),

                
            
                
        username=entry[3],

                
            
            
        ).validate())

    return {
        'total': cursor.execute("SELECT COUNT(*) FROM profile").fetchone()[0],
        'items': items
    }