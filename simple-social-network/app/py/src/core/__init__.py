"""

simple social network

    user
    
        profile
            
            auth: true
                
                max models: 1
                
            
            fields:
                
                user_id: str
                
                username: str
                
                bio: str
                

    

    content
    
        post
            
            auth: true
                
            
            fields:
                
                user_id: str
                
                content: str
                

    
        event
            
            auth: true
                
            
            fields:
                
                user_id: str
                
                event_name: str
                
                event_date: datetime
                
                location: str
                
                description: str
                

    


"""