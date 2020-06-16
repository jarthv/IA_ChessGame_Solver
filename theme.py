from pyglet_gui.theme import Theme
def getTheme():
    theme = Theme({"font": "Lucida Grande",
                   "font_size": 16,
                   "text_color": [255, 255, 255, 255],
                   "gui_color": [255, 255, 255, 255],
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
                    "frame": {
                       "image": {
                           "source": "panel.png",
                           "frame": [8, 8, 16, 16],
                           "padding": [8, 8, 0, 0]
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
                   },
                   "checkbox": {
                       "checked": {
                           "image": {
                               "source": "checkbox-checked.png"
                           }
                       },
                       "unchecked": {
                           "image": {
                               "source": "checkbox.png"
                           }
                       }
                   },
                  }, resources_path='theme')
    return theme
def getPopUpMenssageTheme():
    theme = Theme({
        "font": "Lucida Grande",
        "font_size": 12,
        "font_size_small": 10,
        "gui_color": [255, 255, 255, 255],
        "disabled_color": [160, 160, 160, 255],
        "text_color": [255, 255, 255, 255],
        "focus_color": [255, 255, 255, 64],
        "button": {
            "down": {
                "focus": {
                    "image": {
                        "source": "button-highlight.png",
                        "frame": [8, 6, 2, 2],
                        "padding": [18, 18, 8, 6]
                    }
                },
                "image": {
                    "source": "button-down.png",
                    "frame": [6, 6, 3, 3],
                    "padding": [12, 12, 4, 2]
                },
                "text_color": [0, 0, 0, 255]
            },
            "up": {
                "focus": {
                    "image": {
                        "source": "button-highlight.png",
                        "frame": [8, 6, 2, 2],
                        "padding": [18, 18, 8, 6]
                    }
                },
                "image": {
                    "source": "button.png",
                    "frame": [6, 6, 3, 3],
                    "padding": [12, 12, 4, 2]
                }
            },
        },
        "frame": {
            "image": {
                "source": "panel.png",
                "frame": [8, 8, 16, 16],
                "padding": [16, 16, 8, 8]
            }
        }
    }, resources_path='theme')
    return theme
