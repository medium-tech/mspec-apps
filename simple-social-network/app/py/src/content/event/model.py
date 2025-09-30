from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Optional

from core.types import *
from core.util import *


__all__ = [
    'Event'
]




    

    

    

    

    



field_list = [
    
    'description',

    
    'event_date',

    
    'event_name',

    
    'location',

    
    'user_id',

    
]

longest_field_name_length = max([len(name) for name in field_list])

@dataclass
class Event:

    
        
    description: str

        
    
        
    event_date: datetime

        
    
        
    event_name: str

        
    
        
    location: str

        
    
    
    user_id: str = ''

    
    id: Optional[str] = None

    def convert_types(self) -> 'Event':

        
        # event_date - datetime
        if isinstance(self.event_date, str):
            self.event_date = datetime.strptime(self.event_date, datetime_format_str).replace(microsecond=0)

        

        

        return self

    def validate(self) -> 'Event':
        
        if not isinstance(self.id, str) and self.id is not None:
            raise TypeError('invalid type for id')


        
        # user_id - str

        if not isinstance(self.user_id, str):
            raise TypeError('user_id must be a string')
        

        
        # event_name - str

        if not isinstance(self.event_name, str):
            raise TypeError('event_name must be a string')
        

        
        # event_date - datetime

        if not isinstance(self.event_date, datetime):
            raise TypeError('event_date must be a datetime')

        
        # location - str

        if not isinstance(self.location, str):
            raise TypeError('location must be a string')
        

        
        # description - str

        if not isinstance(self.description, str):
            raise TypeError('description must be a string')
        

        

        return self

    def to_dict(self) -> dict:
        data = asdict(self)
        if self.id is None:
            del data['id']
        return data
    
    def to_json(self) -> str:
        return to_json(self.to_dict())

    @classmethod
    def example(cls) -> 'Event':
        return cls(
            
                
            user_id='',

                
            
                
			event_name='Birthday Party',

                
            
                
			event_date=datetime.strptime('2023-10-15T18:00:00', datetime_format_str),

                
            
                
			location='Central Park',

                
            
                
			description='Join us for a fun birthday celebration!',

                
            
        ) 

    @classmethod
    def random(cls) -> 'Event':
        return cls(

            
                
			event_name=random_str(),

                
            
                
			event_date=random_datetime(),

                
            
                
			location=random_str(),

                
            
                
			description=random_str(),

                
            
        )