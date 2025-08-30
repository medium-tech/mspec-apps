from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Optional

from core.types import *
from core.util import *


__all__ = [
    'Products'
]






field_list = [
	'in_stock',
	'price',
	'product_name'
]

longest_field_name_length = max([len(name) for name in field_list])

@dataclass
class Products:

    product_name: str
    price: float
    in_stock: bool

    id: Optional[str] = None

    def convert_types(self) -> 'Products':

        return self

    def validate(self) -> 'Products':
        
        if not isinstance(self.id, str) and self.id is not None:
            raise TypeError('invalid type for id')

        # product_name - str

        if not isinstance(self.product_name, str):
            raise TypeError('product_name must be a string')
        

        # price - float

        if not isinstance(self.price, float):
            raise TypeError('price must be a float')


        # in_stock - bool

        if not isinstance(self.in_stock, bool):
            raise TypeError('in_stock must be a bool')





        return self

    def to_dict(self) -> dict:
        data = asdict(self)
        if self.id is None:
            del data['id']
        return data
    
    def to_json(self) -> str:
        return to_json(self.to_dict())

    @classmethod
    def example(cls) -> 'Products':
        return cls(
			product_name='Laptop',
			price=999.99,
			in_stock=True
        ) 

    @classmethod
    def random(cls) -> 'Products':
        return cls(
			product_name=random_thing_name(),
			price=random_float(),
			in_stock=random_bool()
        )