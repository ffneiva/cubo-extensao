from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.clock import Clock
from components import ColorPalette, DrawCube, Solution

Window.size = (Window.width, Window.height)

GUI = Builder.load_file('window.kv')

class RubikCube(App):
    def build(self):
        return GUI

    def on_start(self):
        Clock.schedule_once(self.initial_state, 0.1)
        Window.bind(on_resize=self.on_window_resize)
        Window.bind(on_maximize=self.on_window_maximize)
        Window.bind(on_restore=self.on_window_restore)

    def initial_state(self, dt):
        self.set_button_sizes()
        self.set_font_size()
        self.draw_cube()

    def on_window_resize(self, instance, width, height):
        self.set_button_sizes()
        self.set_font_size()
        self.draw_cube()
    
    def on_window_maximize(self, instance):
        self.set_button_sizes()
        self.set_font_size()
        self.draw_cube()
    
    def on_window_restore(self, instance):
        self.set_button_sizes()
        self.set_font_size()
        self.draw_cube()

    def set_button_sizes(self):
        buttons = self.root.ids.color_palette.button_layout
        size = (App.get_running_app().root.width - 70) / 6 if App.get_running_app() else (360 - 70) / 6
        for button in buttons.children:
            button.size = (size, size)
        
    def set_font_size(self):
        font_size = max([self.root.ids.solution.calculate_font_size(), 16])
        self.root.ids.solution.label.font_size = font_size
        self.root.ids.solution.submit_button.font_size = 2/3 * font_size
        self.root.ids.solution.clear_button.font_size = 2/3 * font_size
        stickers = self.root.ids.draw_cube.stickers
        for sticker in stickers.values():
            if sticker.label:
                sticker.label.font_size = 3/5 * font_size
    
    def draw_cube(self):
        self.root.ids.draw_cube.draw_cube()

RubikCube().run()
