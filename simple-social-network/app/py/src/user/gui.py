import tkinter
from tkinter import ttk
from core.types import Fonts

from user.profile.gui import ProfileIndexPage



__all__ = [
    'UserIndexPage'
]

class UserIndexPage(tkinter.Frame):

    index_pages = (

        (ProfileIndexPage, 'profile'),

    )

    def __init__(self, parent, controller): 
        super().__init__(parent)
        self.controller = controller
        #self.config(background='white')

        back_button = ttk.Button(self, text='<-', command=lambda: controller.show_index_frame())
        back_button.grid(row=0, column=0)

        label = ttk.Label(self, text='template module', font=Fonts.heading1)
        label.grid(row=0, column=1)

        for n, item in enumerate(self.index_pages, start=1):
            button = ttk.Button(self, text=item[1], command=lambda frame=item[0]: controller.show_frame(frame))
            button.grid(row=n, column=0)