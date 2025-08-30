from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Optional

from core.types import *
from core.util import *


__all__ = [
    'Customers'
]






field_list = [
	'customer_name',
	'email',
	'phone_number'
]

longest_field_name_length = max([len(name) for name in field_list])

@dataclass
class Customers:

    customer_name: str
    email: str
    phone_number: str

    id: Optional[str] = None

    def convert_types(self) -> 'Customers':

        return self

    def validate(self) -> 'Customers':
        
        if not isinstance(self.id, str) and self.id is not None:
            raise TypeError('invalid type for id')

        # customer_name - str

        if not isinstance(self.customer_name, str):
            raise TypeError('customer_name must be a string')
        

        # email - str

        if not isinstance(self.email, str):
            raise TypeError('email must be a string')
        

        # phone_number - str

        if not isinstance(self.phone_number, str):
            raise TypeError('phone_number must be a string')
        




        return self

    def to_dict(self) -> dict:
        data = asdict(self)
        if self.id is None:
            del data['id']
        return data
    
    def to_json(self) -> str:
        return to_json(self.to_dict())

    @classmethod
    def example(cls) -> 'Customers':
        return cls(
			customer_name='Alice',
			email='alice@email.com',
			phone_number='+1 (123) 456-7890'
        ) 

    @classmethod
    def random(cls) -> 'Customers':
        return cls(
			customer_name=random_person_name(),
			email=random_email(),
			phone_number=random_phone_number()
        )