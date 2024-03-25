import math
from constants import SIDES, COLORS, NOTATION
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput


class SquareButton(Button):
    def __init__(self, color, text, **kwargs):
        super(SquareButton, self).__init__(**kwargs)
        self.original_color = color
        self.background_color = color
        self.text = text
        self.bold = True
        self.size_hint = (None, None)
        self.selected = False

class Input(TextInput):
    def __init__(self, **kwargs):
        super(Input, self).__init__(**kwargs)
        self.bind(text=self.on_text_update)
        self.previous_text = ''
        self.size_hint = (1, 0.5)
    
    def on_text_update(self, instance, value):
        updated_text = ''
        draw_cube = self.parent.parent.ids.draw_cube
        colors = draw_cube.sticker_colors
        centers = [(math.ceil(SIDES**2 / 2) - 1) + SIDES**2 * i for i in range(6)]
        
        for i, letter in enumerate(value):
            if i >= len(colors):
                break
            elif SIDES % 2 and i in centers:
                updated_text += NOTATION[colors[i]]
            elif letter.upper() in NOTATION.values():
                updated_text += letter.upper()
            else:
                continue
            text_colors = [key for key, value in NOTATION.items() if value == updated_text[-1]]
            text_color = text_colors[0] if len(text_colors) else None
            colors[i] = text_color
        
        if len(value) < len(self.previous_text):
            for i in range(len(colors)):
                if i >= len(value) and not (SIDES % 2 and i in centers):
                    colors[i] = None
        
        self.text = updated_text
        self.previous_text = value
        draw_cube.draw_cube()
        
class ColorPalette(BoxLayout):
    def __init__(self, **kwargs):
        super(ColorPalette, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 10
        self.selected_button = None
        self.input = Input()
        self.add_widget(self.input)
        self.button_layout = GridLayout(cols=6, spacing=10)

        for key, color in COLORS.items():
            button = SquareButton(color=color, text=NOTATION[key], on_release=self.color_selected)
            self.button_layout.add_widget(button)
        self.add_widget(self.button_layout)

    def color_selected(self, instance):
        if instance != self.selected_button:
            if self.selected_button:
                self.selected_button.selected = False
                self.selected_button.background_color = self.selected_button.original_color
            self.selected_button = instance

        instance.selected = not instance.selected
        if instance.selected:
            instance.background_color = (instance.original_color[0], instance.original_color[1], instance.original_color[2], 0.5)
        else:
            instance.background_color = instance.original_color
