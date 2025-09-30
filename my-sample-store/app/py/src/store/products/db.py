import sqlite3
from datetime import datetime
from core.types import datetime_format_str
from core.exceptions import NotFoundError
from store.products.model import Products


__all__ = [
    'db_create_products', 
    'db_read_products',
    'db_update_products', 
    'db_delete_products', 
    'db_list_products',
]

def db_create_products(ctx:dict, obj:Products) -> Products:
    """
    create a single model in the database, verifying the data first.

    args ::
        ctx :: dict containing the database client
        obj :: the Products object to create.

    return :: and Products object with the new id.
    """
    if obj.id is not None:
        raise ValueError('id must be null to create a new item')
    
    obj.validate()
    cursor:sqlite3.Cursor = ctx['db']['cursor']
    

    

    result = cursor.execute(
        "INSERT INTO products('in_stock', 'price', 'product_name') VALUES(?, ?, ?)",
        (obj.in_stock, obj.price, obj.product_name,)
    )
    assert result.rowcount == 1
    assert result.lastrowid is not None
    obj.id = str(result.lastrowid)




    

    ctx['db']['commit']()
    return obj

def db_read_products(ctx:dict, id:str) -> Products:
    """
    read a single model from the database and verify it.

    args ::
        ctx :: dict containing the database client
        id :: the id of the item to read.
    
    return :: the Products object.
    raises :: NotFoundError if the item is not found.
    """

    cursor:sqlite3.Cursor = ctx['db']['cursor']
    result = cursor.execute(f"SELECT * FROM products WHERE id=?", (id,))
    entry = result.fetchone()
    if entry is None:
        raise NotFoundError(f'products {id} not found')


    
    
    return Products(
        id=str(entry[0]),
        
            
        in_stock=bool(entry[1]),

            
        
            
        price=entry[2],

            
        
            
        product_name=entry[3],

            
        
        
    ).validate()

def db_update_products(ctx:dict, obj:Products) -> Products:
    """
    update a single model in the database, and verify the data first.

    args ::
        ctx :: dict containing the database client
        obj :: the Products object to update.

    return :: the Products object.
    raises :: NotFoundError if the item is not found
    """
    if obj.id is None:
        raise ValueError('id must not be null to update an item')
    
    obj.validate()
    cursor:sqlite3.Cursor = ctx['db']['cursor']
    

    result = cursor.execute(
        "UPDATE products SET 'in_stock'=?, 'price'=?, 'product_name'=? WHERE id=?",
        (obj.in_stock, obj.price, obj.product_name, obj.id)
    )
    if result.rowcount == 0:
        raise NotFoundError(f'products {obj.id} not found')




    ctx['db']['commit']()
    return obj

def db_delete_products(ctx:dict, id:str) -> None:
    """
    delete a single model from the database.

    args ::
        ctx :: dict containing the database client
        id :: the id of the item to delete.
    
    return :: None
    """

    cursor:sqlite3.Cursor = ctx['db']['cursor']
    


    cursor.execute(f"DELETE FROM products WHERE id=?", (id,))


    

    ctx['db']['commit']()

def db_list_products(ctx:dict, offset:int=0, limit:int=25) -> dict:
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
    query = cursor.execute("SELECT * FROM products ORDER BY id LIMIT ? OFFSET ?", (limit, offset))

    for entry in query.fetchall():
        
        items.append(Products(
            id=str(entry[0]),
            
                
        in_stock=bool(entry[1]),

                
            
                
        price=entry[2],

                
            
                
        product_name=entry[3],

                
            
            
        ).validate())

    return {
        'total': cursor.execute("SELECT COUNT(*) FROM products").fetchone()[0],
        'items': items
    }