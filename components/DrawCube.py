from constants import SIDES, COLORS
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.graphics import Rectangle, Color
import math


class Sticker(Widget):
    def __init__(self, pos, size, color=(0.5, 0.5, 0.5), index=None, **kwargs):
        super(Sticker, self).__init__(**kwargs)
        self.size = size
        self.pos = pos
        self.color = color
        self.original_color = color
        self.index = index
    
        with self.canvas:
            self.color_instruction = Color(*color)
            self.rect = Rectangle(pos=self.pos, size=self.size)
            self.label = Label(
                text=str(index + 1),
                pos=(self.pos[0] + 5, self.pos[1] + 5),
                size=(self.size[0] - 10, self.size[1] - 10),
                font_size=12,
                color=(0, 0, 0),
            )
            self.add_widget(self.label)

    def clear_canvas(self):
        self.canvas.clear()
    
    def on_touch_down(self, touch):
        if SIDES % 2:
            centers = [(math.ceil(SIDES**2 / 2) - 1) + SIDES**2 * i for i in range(6)]
            if self.index in centers:
                return
        if self.is_point_inside_shape(touch.x, touch.y):
            button = self.parent.parent.ids.color_palette.selected_button
            if button:
                new_color = button.original_color
                self.color_instruction.r, self.color_instruction.g, self.color_instruction.b, self.color_instruction.a = new_color
                text_colors = [key for key, value in COLORS.items() if value == new_color]
                text_color = text_colors[0] if len(text_colors) else None
                self.parent.sticker_colors[self.index] = text_color
    
    def is_point_inside_shape(self, x, y):
        return (self.rect.pos[0] <= x <= self.rect.pos[0] + self.rect.size[0]
                and self.rect.pos[1] <= y <= self.rect.pos[1] + self.rect.size[1])
        
class DrawCube(BoxLayout):
    def __init__(self, **kwargs):
        super(DrawCube, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.spacing = 10
        self.stickers = {}
        self.sticker_colors = []
        
    def draw_cube(self):
        grid = {
            'white' : [1, 2],
            'orange': [0, 1],
            'green' : [1, 1],
            'red'   : [2, 1],
            'blue'  : [3, 1],
            'yellow': [1, 0],
        }

        STICKER_AREA_TILE_GAP = 3
        STICKER_AREA_OFFSET = 5

        use_width = min([self.width, 4/3 * self.height])
        aditive = use_width * 0.1

        sticker_area_tile_size = (self.width - (SIDES * (SIDES + 1) * ((SIDES - 1) * STICKER_AREA_TILE_GAP + STICKER_AREA_OFFSET))) / (SIDES * (SIDES + 1))
        
        side_offset = STICKER_AREA_TILE_GAP * SIDES
        side_size = sticker_area_tile_size * SIDES + STICKER_AREA_TILE_GAP * (SIDES - 1)
        
        offset_x = self.width - (side_size * (SIDES + 1)) - (side_offset * (SIDES + 1)) - (4 * STICKER_AREA_OFFSET)
        offset_y = self.height - (side_size * SIDES) - (side_offset * SIDES) - (3 * STICKER_AREA_OFFSET) + 100

        for sticker in self.stickers.values():
            sticker.clear_canvas()
        self.canvas.clear()
        self.clear_widgets()
        self.stickers.clear()

        with self.canvas:
            i = -1
            for side, (grid_x, grid_y) in grid.items():
                index = -1
                for row in range(SIDES):
                    for col in range(SIDES):
                        i += 1
                        index += 1
                        x1 = offset_x + sticker_area_tile_size * col + STICKER_AREA_TILE_GAP * col + ((side_size + side_offset) * grid_x)
                        y1 = offset_y + sticker_area_tile_size * row + STICKER_AREA_TILE_GAP * row + ((side_size + side_offset) * grid_y)
                        x2 = x1 + sticker_area_tile_size
                        y2 = y1 + sticker_area_tile_size

                        Color(1, 1, 1)
                        Rectangle(pos=(x1, y1), size=(x2 - x1, y2 - y1))

                        if len(self.sticker_colors) > i:
                            try:
                                color = COLORS[self.sticker_colors[i]]
                            except:
                                color = (0.5, 0.5, 0.5)
                        elif SIDES % 2 and index == math.ceil(SIDES**2 / 2) - 1:
                            color = COLORS[side]
                        else:
                            color = (0.5, 0.5, 0.5)

                        sticker = Sticker(
                            pos=(x1 + 1, y1 + 1),
                            size=(x2 - x1 - 2, y2 - y1 - 2),
                            color=color,
                            index=i,
                        )
                        self.add_widget(sticker)
                        self.stickers[(side, index)] = sticker

                        text_colors = [key for key, value in COLORS.items() if value == color]
                        text_color = text_colors[0] if len(text_colors) else None
                        if len(self.sticker_colors) > i:
                            self.sticker_colors[i] = text_color
                        else:
                            self.sticker_colors.append(text_color)
