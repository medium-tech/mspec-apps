from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Optional

from core.types import *
from core.util import *


__all__ = [
    'Post'
]




    

    



field_list = [
    
    'content',

    
    'user_id',

    
]

longest_field_name_length = max([len(name) for name in field_list])

@dataclass
class Post:

    
        
    content: str

        
    
    
    user_id: str = ''

    
    id: Optional[str] = None

    def convert_types(self) -> 'Post':

        

        

        return self

    def validate(self) -> 'Post':
        
        if not isinstance(self.id, str) and self.id is not None:
            raise TypeError('invalid type for id')


        
        # user_id - str

        if not isinstance(self.user_id, str):
            raise TypeError('user_id must be a string')
        

        
        # content - str

        if not isinstance(self.content, str):
            raise TypeError('content must be a string')
        

        

        return self

    def to_dict(self) -> dict:
        data = asdict(self)
        if self.id is None:
            del data['id']
        return data
    
    def to_json(self) -> str:
        return to_json(self.to_dict())

    @classmethod
    def example(cls) -> 'Post':
        return cls(
            
                
            user_id='',

                
            
                
			content='Just had an amazing day at the beach!',

                
            
        ) 

    @classmethod
    def random(cls) -> 'Post':
        return cls(

            
                
			content=random_str(),

                
            
        )