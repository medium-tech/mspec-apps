import sqlite3
from datetime import datetime
from core.types import datetime_format_str
from core.exceptions import NotFoundError
from admin.employees.model import Employees


__all__ = [
    'db_create_employees', 
    'db_read_employees',
    'db_update_employees', 
    'db_delete_employees', 
    'db_list_employees',
]

def db_create_employees(ctx:dict, obj:Employees) -> Employees:
    """
    create a single model in the database, verifying the data first.

    args ::
        ctx :: dict containing the database client
        obj :: the Employees object to create.

    return :: and Employees object with the new id.
    """
    if obj.id is not None:
        raise ValueError('id must be null to create a new item')
    
    obj.validate()
    cursor:sqlite3.Cursor = ctx['db']['cursor']

    result = cursor.execute(
        "INSERT INTO employees('email', 'employee_name', 'hire_date', 'phone_number', 'position', 'salary') VALUES(?, ?, ?, ?, ?, ?)",
        (obj.email, obj.employee_name, obj.hire_date, obj.phone_number, obj.position, obj.salary,)
    )
    assert result.rowcount == 1
    assert result.lastrowid is not None
    obj.id = str(result.lastrowid)



    ctx['db']['commit']()
    return obj

def db_read_employees(ctx:dict, id:str) -> Employees:
    """
    read a single model from the database and verify it.

    args ::
        ctx :: dict containing the database client
        id :: the id of the item to read.
    
    return :: the Employees object.
    raises :: NotFoundError if the item is not found.
    """

    cursor:sqlite3.Cursor = ctx['db']['cursor']
    result = cursor.execute(f"SELECT * FROM employees WHERE id=?", (id,))
    entry = result.fetchone()
    if entry is None:
        raise NotFoundError(f'employees {id} not found')


    
    return Employees(
        id=str(entry[0]),
        email=entry[1],

        employee_name=entry[2],

        hire_date=entry[3],

        phone_number=entry[4],

        position=entry[5],

        salary=entry[6],


    ).validate()

def db_update_employees(ctx:dict, obj:Employees) -> Employees:
    """
    update a single model in the database, and verify the data first.

    args ::
        ctx :: dict containing the database client
        obj :: the Employees object to update.

    return :: the Employees object.
    raises :: NotFoundError if the item is not found
    """
    if obj.id is None:
        raise ValueError('id must not be null to update an item')
    
    obj.validate()
    cursor:sqlite3.Cursor = ctx['db']['cursor']

    result = cursor.execute(
        "UPDATE employees SET 'email'=?, 'employee_name'=?, 'hire_date'=?, 'phone_number'=?, 'position'=?, 'salary'=? WHERE id=?",
        (obj.email, obj.employee_name, obj.hire_date, obj.phone_number, obj.position, obj.salary, obj.id)
    )
    if result.rowcount == 0:
        raise NotFoundError(f'employees {obj.id} not found')



    ctx['db']['commit']()
    return obj

def db_delete_employees(ctx:dict, id:str) -> None:
    """
    delete a single model from the database.

    args ::
        ctx :: dict containing the database client
        id :: the id of the item to delete.
    
    return :: None
    """

    cursor:sqlite3.Cursor = ctx['db']['cursor']
    cursor.execute(f"DELETE FROM employees WHERE id=?", (id,))



    ctx['db']['commit']()

def db_list_employees(ctx:dict, offset:int=0, limit:int=25) -> list[Employees]:
    """
    list single models from the database, and verify each

    args ::
        ctx :: dict containing the database client
        offset :: the offset to start listing from.
        limit :: the maximum number of items to list.
    
    return :: list of each item as a dict.
    """
    cursor:sqlite3.Cursor = ctx['db']['cursor']
    
    items = []
    query = cursor.execute("SELECT * FROM employees ORDER BY id LIMIT ? OFFSET ?", (limit, offset))

    for entry in query.fetchall():

        
        items.append(Employees(
            id=str(entry[0]),
        email=entry[1],

        employee_name=entry[2],

        hire_date=entry[3],

        phone_number=entry[4],

        position=entry[5],

        salary=entry[6],


        ).validate())

    return items