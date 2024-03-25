import socket
import kociemba
import math
from constants import SIDES, FACES, NOTATION
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock


class Solution(BoxLayout):
    def __init__(self, **kwargs):
        super(Solution, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.height = 50

        self.label = Label(
            text='Preencha o cubo para mostrar a solução',
            font_size=25,
            bold=True,
            size_hint=(0.8, 1),
        )

        self.submit_button = Button(
            text='Solução',
            size_hint=(0.1, 1),
            valign='center',
            on_release=self.submit,
        )
        
        self.clear_button = Button(
            text='Limpar',
            size_hint=(0.1, 1),
            valign='center',
            on_release=self.clear,
        )

        self.add_widget(self.label)
        self.add_widget(self.submit_button)
        self.add_widget(self.clear_button)

    def submit(self, instance):
        scramble = ''
        sequence = ''
        colors = self.parent.ids.draw_cube.sticker_colors
        if None in colors:
            self.label.text = 'Preencha todas as cores primeiro!'
            Clock.schedule_once(self.restore_label_text, 2)
            return
        for color in colors:
            scramble += FACES[color]
            sequence += NOTATION[color]
        try:
            solve = kociemba.solve(self.organize_scramble(scramble))
            self.label.text = solve
            # self.wifi_send_solve(solve, sequence)
            self.bluetooth_send_solve(solve, sequence)
        except ValueError as e:
            print(e)
            self.label.text = 'Erro ao encontrar solução!'
            Clock.schedule_once(self.restore_label_text, 2)
    
    def clear(self, instance):
        draw_cube = self.parent.ids.draw_cube
        self.parent.ids.color_palette.input.text = ''
        stickers = draw_cube.sticker_colors
        centers = [(math.ceil(SIDES**2 / 2) - 1) + SIDES**2 * i for i in range(6)]
        for i in range(len(stickers)):
            if SIDES % 2 and i in centers:
                pass
            else:
                stickers[i] = None
        draw_cube.draw_cube()
        Clock.schedule_once(self.restore_label_text, 0.01)

    def wifi_send_solve(self, solve, sequence):
        wifi = socket.socket()
        host = '172.16.61.53'
        port = 5001

        try:
            organized_solve = self.reorganize_scramble(solve).encode('utf-8')
            organized_sequence = self.organize_sequence(sequence).lower().encode('utf-8')
            print(organized_solve, organized_sequence)
            wifi.connect((host, port))
            wifi.send(organized_solve, organized_sequence)
            wifi.close()
        except Exception as e:
            self.label.text = 'Erro ao enviar dados via bluetooth'
            Clock.schedule_once(lambda dt: self.restore_label_text(dt, text=solve), 2)
            print(e)
    
    def bluetooth_send_solve(self, solve, sequence):
        bluetooth = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        address = '24:d7:eb:11:83:a7'
        # address = '24:d7:eb:11:83:a7'
        channel = 4

        try:
            organized_solve = self.reorganize_scramble(solve).encode('utf-8')
            organized_sequence = self.organize_sequence(sequence).lower().encode('utf-8')
            print(organized_solve, organized_sequence)
            bluetooth.connect((address, channel))
            bluetooth.send(organized_solve, organized_sequence)
            bluetooth.close()
        except Exception as e:
            self.label.text = 'Erro ao enviar dados via bluetooth'
            Clock.schedule_once(lambda dt: self.restore_label_text(dt, text=solve), 2)
            print(e)
    
    def restore_label_text(self, df, text='Preencha o cubo para mostrar a solução'):
        self.label.text = text
    
    def calculate_font_size(self):
        window_width = App.get_running_app().root.width
        return window_width * 0.03
    
    def organize_scramble(self, scramble):
        organized_scramble = ''
        
        # White
        organized_scramble += scramble[SIDES*2:SIDES*3]
        organized_scramble += scramble[SIDES*1:SIDES*2]
        organized_scramble += scramble[SIDES*0:SIDES*1]
        
        # Right
        organized_scramble += scramble[SIDES*11:SIDES*12]
        organized_scramble += scramble[SIDES*10:SIDES*11]
        organized_scramble += scramble[SIDES*9:SIDES*10]

        # Front
        organized_scramble += scramble[SIDES*8:SIDES*9]
        organized_scramble += scramble[SIDES*7:SIDES*8]
        organized_scramble += scramble[SIDES*6:SIDES*7]

        # Down
        organized_scramble += scramble[SIDES*17:SIDES*18]
        organized_scramble += scramble[SIDES*16:SIDES*17]
        organized_scramble += scramble[SIDES*15:SIDES*16]

        # Left
        organized_scramble += scramble[SIDES*5:SIDES*6]
        organized_scramble += scramble[SIDES*4:SIDES*5]
        organized_scramble += scramble[SIDES*3:SIDES*4]

        # Back
        organized_scramble += scramble[SIDES*14:SIDES*15]
        organized_scramble += scramble[SIDES*13:SIDES*14]
        organized_scramble += scramble[SIDES*12:SIDES*13]
        
        return organized_scramble
    
    def reorganize_scramble(self, scramble):
        return '$' + scramble + ' +'

    def organize_sequence(self, sequence):
        organized_sequence = ''
        
        s = sequence
        sequence_list = [
            s[ 6], s[ 7], s[ 8], s[ 5], s[ 2], s[ 1], s[ 0], s[ 3], s[ 4],
            s[15], s[16], s[17], s[14], s[11], s[10], s[ 9], s[12], s[13],
            s[24], s[25], s[26], s[23], s[20], s[19], s[18], s[21], s[22],
            s[33], s[34], s[35], s[32], s[29], s[28], s[27], s[30], s[31],
            s[42], s[43], s[44], s[41], s[38], s[37], s[36], s[39], s[40],
            s[51], s[52], s[53], s[50], s[47], s[46], s[45], s[48], s[49],
        ]

        for item in sequence_list:
            organized_sequence += item
        
        return organized_sequence
