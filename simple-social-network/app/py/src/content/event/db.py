import sqlite3
from datetime import datetime
from core.types import datetime_format_str
from core.exceptions import NotFoundError
from content.event.model import Event


__all__ = [
    'db_create_event', 
    'db_read_event',
    'db_update_event', 
    'db_delete_event', 
    'db_list_event',
]

def db_create_event(ctx:dict, obj:Event) -> Event:
    """
    create a single model in the database, verifying the data first.

    args ::
        ctx :: dict containing the database client
        obj :: the Event object to create.

    return :: and Event object with the new id.
    """
    if obj.id is not None:
        raise ValueError('id must be null to create a new item')
    
    obj.validate()
    cursor:sqlite3.Cursor = ctx['db']['cursor']
    
    # must be logged in to make event
    user = ctx['auth']['get_user']()
    if obj.user_id != '' and obj.user_id != user.id:
        raise ValueError(f'Incorrect user_id ({obj.user_id} != {user.id}) supplied for event creation')
    
    obj.user_id = user.id
    assert obj.user_id is not None

    

    

    result = cursor.execute(
        "INSERT INTO event('description', 'event_date', 'event_name', 'location', 'user_id') VALUES(?, ?, ?, ?, ?)",
        (obj.description, obj.event_date.isoformat(), obj.event_name, obj.location, obj.user_id,)
    )
    assert result.rowcount == 1
    assert result.lastrowid is not None
    obj.id = str(result.lastrowid)




    

    ctx['db']['commit']()
    return obj

def db_read_event(ctx:dict, id:str) -> Event:
    """
    read a single model from the database and verify it.

    args ::
        ctx :: dict containing the database client
        id :: the id of the item to read.
    
    return :: the Event object.
    raises :: NotFoundError if the item is not found.
    """

    cursor:sqlite3.Cursor = ctx['db']['cursor']
    result = cursor.execute(f"SELECT * FROM event WHERE id=?", (id,))
    entry = result.fetchone()
    if entry is None:
        raise NotFoundError(f'event {id} not found')


    
    
    return Event(
        id=str(entry[0]),
        
            
        description=entry[1],

            
        
            
        event_date=datetime.strptime(entry[2], datetime_format_str).replace(microsecond=0),

            
        
            
        event_name=entry[3],

            
        
            
        location=entry[4],

            
        
            
        user_id=str(entry[5]),

            
        
        
    ).validate()

def db_update_event(ctx:dict, obj:Event) -> Event:
    """
    update a single model in the database, and verify the data first.

    args ::
        ctx :: dict containing the database client
        obj :: the Event object to update.

    return :: the Event object.
    raises :: NotFoundError if the item is not found
    """
    if obj.id is None:
        raise ValueError('id must not be null to update an item')
    
    obj.validate()
    cursor:sqlite3.Cursor = ctx['db']['cursor']
    
    user = ctx['auth']['get_user']()
    if obj.user_id != user.id:
        raise ForbiddenError('not allowed to update this event')

    

    result = cursor.execute(
        "UPDATE event SET 'description'=?, 'event_date'=?, 'event_name'=?, 'location'=?, 'user_id'=? WHERE id=?",
        (obj.description, obj.event_date.isoformat(), obj.event_name, obj.location, obj.user_id, obj.id)
    )
    if result.rowcount == 0:
        raise NotFoundError(f'event {obj.id} not found')




    ctx['db']['commit']()
    return obj

def db_delete_event(ctx:dict, id:str) -> None:
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
        obj = db_read_event(ctx, id)
    except NotFoundError:
        return

    if obj.user_id != user.id:
        raise ForbiddenError('not allowed to delete this event')

    


    cursor.execute(f"DELETE FROM event WHERE id=?", (id,))


    

    ctx['db']['commit']()

def db_list_event(ctx:dict, offset:int=0, limit:int=25) -> dict:
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
    query = cursor.execute("SELECT * FROM event ORDER BY id LIMIT ? OFFSET ?", (limit, offset))

    for entry in query.fetchall():
        
        items.append(Event(
            id=str(entry[0]),
            
                
        description=entry[1],

                
            
                
        event_date=datetime.strptime(entry[2], datetime_format_str).replace(microsecond=0),

                
            
                
        event_name=entry[3],

                
            
                
        location=entry[4],

                
            
                
        user_id=str(entry[5]),

                
            
            
        ).validate())

    return {
        'total': cursor.execute("SELECT COUNT(*) FROM event").fetchone()[0],
        'items': items
    }