import sqlite3
from datetime import datetime
from core.types import datetime_format_str
from core.exceptions import NotFoundError
from store.customers.model import Customers


__all__ = [
    'db_create_customers', 
    'db_read_customers',
    'db_update_customers', 
    'db_delete_customers', 
    'db_list_customers',
]

def db_create_customers(ctx:dict, obj:Customers) -> Customers:
    """
    create a single model in the database, verifying the data first.

    args ::
        ctx :: dict containing the database client
        obj :: the Customers object to create.

    return :: and Customers object with the new id.
    """
    if obj.id is not None:
        raise ValueError('id must be null to create a new item')
    
    obj.validate()
    cursor:sqlite3.Cursor = ctx['db']['cursor']


    result = cursor.execute(
        "INSERT INTO customers('customer_name', 'email', 'phone_number') VALUES(?, ?, ?)",
        (obj.customer_name, obj.email, obj.phone_number,)
    )
    assert result.rowcount == 1
    assert result.lastrowid is not None
    obj.id = str(result.lastrowid)



    ctx['db']['commit']()
    return obj

def db_read_customers(ctx:dict, id:str) -> Customers:
    """
    read a single model from the database and verify it.

    args ::
        ctx :: dict containing the database client
        id :: the id of the item to read.
    
    return :: the Customers object.
    raises :: NotFoundError if the item is not found.
    """

    cursor:sqlite3.Cursor = ctx['db']['cursor']
    result = cursor.execute(f"SELECT * FROM customers WHERE id=?", (id,))
    entry = result.fetchone()
    if entry is None:
        raise NotFoundError(f'customers {id} not found')


    
    return Customers(
        id=str(entry[0]),
        customer_name=entry[1],

        email=entry[2],

        phone_number=entry[3],


    ).validate()

def db_update_customers(ctx:dict, obj:Customers) -> Customers:
    """
    update a single model in the database, and verify the data first.

    args ::
        ctx :: dict containing the database client
        obj :: the Customers object to update.

    return :: the Customers object.
    raises :: NotFoundError if the item is not found
    """
    if obj.id is None:
        raise ValueError('id must not be null to update an item')
    
    obj.validate()
    cursor:sqlite3.Cursor = ctx['db']['cursor']

    result = cursor.execute(
        "UPDATE customers SET 'customer_name'=?, 'email'=?, 'phone_number'=? WHERE id=?",
        (obj.customer_name, obj.email, obj.phone_number, obj.id)
    )
    if result.rowcount == 0:
        raise NotFoundError(f'customers {obj.id} not found')



    ctx['db']['commit']()
    return obj

def db_delete_customers(ctx:dict, id:str) -> None:
    """
    delete a single model from the database.

    args ::
        ctx :: dict containing the database client
        id :: the id of the item to delete.
    
    return :: None
    """

    cursor:sqlite3.Cursor = ctx['db']['cursor']

    cursor.execute(f"DELETE FROM customers WHERE id=?", (id,))



    ctx['db']['commit']()

def db_list_customers(ctx:dict, offset:int=0, limit:int=25) -> dict:
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
    query = cursor.execute("SELECT * FROM customers ORDER BY id LIMIT ? OFFSET ?", (limit, offset))

    for entry in query.fetchall():

        
        items.append(Customers(
            id=str(entry[0]),
        customer_name=entry[1],

        email=entry[2],

        phone_number=entry[3],


        ).validate())

    return {
        'total': cursor.execute("SELECT COUNT(*) FROM customers").fetchone()[0],
        'items': items
    }