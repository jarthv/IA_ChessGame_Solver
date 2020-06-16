from setup import *

from pyglet_gui.manager import Manager
from pyglet_gui.document import Document
from pyglet_gui.theme import Theme
from pyglet_gui.containers import VerticalContainer
from pyglet_gui.buttons import Button

theme = Theme({"font": "Lucida Grande",
               "font_size": 12,
               "text_color": [255, 255, 255, 255],
               "gui_color": [64, 64, 64, 255],
                "button": {
                   "down": {
                       "image": {
                           "source": "button-down.png",
                           "frame": [6, 6, 3, 3],
                           "padding": [12, 12, 4, 2]
                       },
                       "text_color": [0, 0, 0, 255]
                   },
                   "up": {
                       "image": {
                           "source": "button.png",
                           "frame": [6, 6, 3, 3],
                           "padding": [12, 12, 4, 2]
                       }
                   }
               },
               "vscrollbar": {
                   "knob": {
                       "image": {
                           "source": "vscrollbar.png",
                           "region": [0, 16, 16, 16],
                           "frame": [0, 6, 16, 4],
                           "padding": [0, 0, 0, 0]
                       },
                       "offset": [0, 0]
                   },
                   "bar": {
                       "image": {
                           "source": "vscrollbar.png",
                           "region": [0, 64, 16, 16]
                       },
                       "padding": [0, 0, 0, 0]
                   }
               }
               
              }, resources_path='../theme')

document = pyglet.text.decode_attributed('''
In {bold True}Pyglet-gui{bold False} you can use
{underline (255, 255, 255, 255)}pyglet{underline None}'s documents in a
scrollable window.

You can also {font_name "Courier New"}change fonts{font_name Lucia Grande},
{italic True}italicize your text{italic False} and use all features of Pyglet's document.
''')
so =  Document(document, width=300, height=50)
def f(y):
    document ="Hola mundo"
    so.set_text(document+ so.get_text())
   
    
# Set up a Manager
Manager(so,
        window=window, batch=batch,
        theme=theme)
Manager(VerticalContainer([Button(label="Persistent button",on_press=f)]),
        window=window,
        batch=batch,
        theme=theme)

pyglet.app.run()
