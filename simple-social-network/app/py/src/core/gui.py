import tkinter
from tkinter import ttk
from core.client import create_client_context
from core.types import Fonts

from user.gui import UserIndexPage

from content.gui import ContentIndexPage

    
from user.profile.gui import ProfileIndexPage, ProfileInstancePage
    

    
from content.post.gui import PostIndexPage, PostInstancePage
    
from content.event.gui import EventIndexPage, EventInstancePage
    


def gui_main(start_frame='SimpleSocialNetworkIndexPage'):
    app = SimpleSocialNetworkGUI(start_frame)
    app.mainloop()
    
class SimpleSocialNetworkIndexPage(tkinter.Frame):
     
    def __init__(self, parent, controller:'SimpleSocialNetworkGUI'): 
        super().__init__(parent)

        label = ttk.Label(self, text='simple social network', font=Fonts.heading1, style='Custom.TButton')
        label.grid(row=0, column=0)

        
        button1 = ttk.Button(self, text='user', command=lambda: controller.show_frame(UserIndexPage), style='Custom.TButton')
        button1.grid(row=1, column=0)
        
        button2 = ttk.Button(self, text='content', command=lambda: controller.show_frame(ContentIndexPage), style='Custom.TButton')
        button2.grid(row=2, column=0)
        

class SimpleSocialNetworkGUI(tkinter.Tk):

    frame_classes = (
        SimpleSocialNetworkIndexPage, 
        
        UserIndexPage,
        
        ContentIndexPage,
        
        
            
        ProfileIndexPage,
        ProfileInstancePage,
            
        
            
        PostIndexPage,
        PostInstancePage,
            
        EventIndexPage,
        EventInstancePage,
            
        
    )

    def __init__(self, start_frame='SimpleSocialNetworkIndexPage'):
        super().__init__()
        self.title('simple social network')
        self.geometry('1000x800')

        self.ctx = create_client_context()

        style = ttk.Style()
        style.theme_use('classic')
        style.configure('Custom.TButton')

        container = ttk.Frame(self)
        container.config(style='Custom.TButton')
        container.grid(column=0, row=0, sticky='nsew')
  
        self.frames = {}
        self.current_frame = None
  
        for frame_class in self.frame_classes:
            self.frames[frame_class] = frame_class(container, self)
            self.frames[frame_class].grid(row=0, column=0, sticky='nsew')
            self.frames[frame_class].forget()
  
        self.show_frame_str(start_frame)
  
    def show_frame(self, frame_class, **kwargs):
        frame = self.frames[frame_class]
        frame.grid(row=0, column=0, sticky='nsew')
        frame.tkraise()

        try:
            self.current_frame.forget()
        except AttributeError:
            """self.current_frame is None"""

        on_show_frame = getattr(frame, 'on_show_frame', None)
        if on_show_frame:
            on_show_frame(**kwargs)
        else:
            print(f"Frame {frame_class} has no on_show_frame method")

        self.current_frame = frame

    def show_frame_str(self, frame_class_str, **kwargs):
        frame_class = globals()[frame_class_str]
        self.show_frame(frame_class, **kwargs)

    def show_index_frame(self, **kwargs):
        self.show_frame(SimpleSocialNetworkIndexPage, **kwargs)

if __name__ == '__main__':

    import argparse

    _default_start_frame = 'SimpleSocialNetworkIndexPage'
    parser = argparse.ArgumentParser(description='Run the gui')
    parser.add_argument('--start-frame', help=f'start frame for gui, default: {_default_start_frame}', default=_default_start_frame)
    args = parser.parse_args()

    gui_main(args.start_frame)