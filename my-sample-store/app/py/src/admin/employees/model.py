from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Optional

from core.types import *
from core.util import *


__all__ = [
    'Employees'
]


position_options = [
    'Manager', 
    'Sales', 
    'Support', 
]





field_list = [
	'email',
	'employee_name',
	'hire_date',
	'phone_number',
	'position',
	'salary'
]

longest_field_name_length = max([len(name) for name in field_list])

@dataclass
class Employees:

    employee_name: str
    position: str
    hire_date: str
    email: str
    phone_number: str
    salary: float

    id: Optional[str] = None

    def convert_types(self) -> 'Employees':

        return self

    def validate(self) -> 'Employees':
        
        if not isinstance(self.id, str) and self.id is not None:
            raise TypeError('invalid type for id')

        # employee_name - str

        if not isinstance(self.employee_name, str):
            raise TypeError('employee_name must be a string')
        

        # position - str enum

        if self.position not in position_options:
            raise TypeError('invalid enum option for position')


        # hire_date - str

        if not isinstance(self.hire_date, str):
            raise TypeError('hire_date must be a string')
        

        # email - str

        if not isinstance(self.email, str):
            raise TypeError('email must be a string')
        

        # phone_number - str

        if not isinstance(self.phone_number, str):
            raise TypeError('phone_number must be a string')
        

        # salary - float

        if not isinstance(self.salary, float):
            raise TypeError('salary must be a float')





        return self

    def to_dict(self) -> dict:
        data = asdict(self)
        if self.id is None:
            del data['id']
        return data
    
    def to_json(self) -> str:
        return to_json(self.to_dict())

    @classmethod
    def example(cls) -> 'Employees':
        return cls(
			employee_name='David',
			position='Manager',
			hire_date='2000-01-11T12:34:56',
			email='my-name@email.com',
			phone_number='+1 (123) 456-7890',
			salary=60000.0
        ) 

    @classmethod
    def random(cls) -> 'Employees':
        return cls(
			employee_name=random_person_name(),
			position=random_str_enum(position_options),
			hire_date=random_str(),
			email=random_email(),
			phone_number=random_phone_number(),
			salary=random_float()
        )