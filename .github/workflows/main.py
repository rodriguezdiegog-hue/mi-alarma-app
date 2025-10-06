from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
import time
import threading
from datetime import datetime, timedelta

class ConfigScreen(Screen):
    def __init__(self, **kwargs):
        super(ConfigScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Título
        title = Label(text='Configurar Alarma', font_size='30sp', size_hint_y=0.15)
        self.layout.add_widget(title)
        
        # Configuración de hora
        time_layout = BoxLayout(orientation='horizontal', size_hint_y=0.12)
        time_layout.add_widget(Label(text='Hora (HH:MM):', font_size='20sp'))
        
        self.hour_input = TextInput(text='12', multiline=False, size_hint=(0.2, 1), font_size='20sp')
        time_layout.add_widget(self.hour_input)
        time_layout.add_widget(Label(text=':', font_size='20sp', size_hint=(0.05, 1)))
        self.minute_input = TextInput(text='00', multiline=False, size_hint=(0.2, 1), font_size='20sp')
        time_layout.add_widget(self.minute_input)
        self.layout.add_widget(time_layout)
        
        # Botón de prueba rápida
        self.test_btn = Button(text='Prueba Rápida (5 seg)', font_size='20sp', 
                              background_color=(0, 0.7, 0, 1), size_hint_y=0.15)
        self.test_btn.bind(on_press=self.activate_test)
        self.layout.add_widget(self.test_btn)
        
        # Estado
        self.status_label = Label(text='Alarma desactivada', font_size='18sp', size_hint_y=0.1)
        self.layout.add_widget(self.status_label)
        
        # Botón cerrar
        close_btn = Button(text='CERRAR', font_size='20sp', 
                          background_color=(0.7, 0.2, 0.2, 1), size_hint_y=0.1)
        close_btn.bind(on_press=self.close_app)
        self.layout.add_widget(close_btn)
        
        self.add_widget(self.layout)
        self.alarm_active = False

    def activate_test(self, instance):
        if not self.alarm_active:
            self.alarm_active = True
            self.status_label.text = 'Alarma activada - Sonará en 5 segundos'
            self.test_btn.disabled = True
            
            def alarm_countdown():
                time.sleep(5)
                if self.alarm_active:
                    Clock.schedule_once(lambda dt: self.trigger_alarm())
            
            threading.Thread(target=alarm_countdown, daemon=True).start()

    def trigger_alarm(self):
        if self.alarm_active:
            self.manager.current = 'alarm'

    def close_app(self, instance):
        App.get_running_app().stop()

class AlarmScreen(Screen):
    def __init__(self, **kwargs):
        super(AlarmScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # Mensaje de alarma
        alarm_label = Label(text='¡ALARMA ACTIVADA!', font_size='40sp', 
                           size_hint_y=0.3, color=(1, 0, 0, 1))
        self.layout.add_widget(alarm_label)
        
        # Botones
        buttons_layout = BoxLayout(orientation='horizontal', spacing=20, size_hint_y=0.5)
        
        # Botón posponer (azul)
        snooze_btn = Button(text='POSPONER', font_size='35sp', 
                           background_color=(0, 0.4, 1, 1))
        snooze_btn.bind(on_press=self.snooze_alarm)
        buttons_layout.add_widget(snooze_btn)
        
        # Botón apagar (rojo)
        stop_btn = Button(text='APAGAR', font_size='35sp', 
                         background_color=(1, 0, 0, 1))
        stop_btn.bind(on_press=self.stop_alarm)
        buttons_layout.add_widget(stop_btn)
        
        self.layout.add_widget(buttons_layout)
        
        # Botón cerrar aplicación
        close_btn = Button(text='CERRAR APLICACIÓN', font_size='20sp', 
                          background_color=(0.5, 0.5, 0.5, 1), size_hint_y=0.1)
        close_btn.bind(on_press=self.close_app)
        self.layout.add_widget(close_btn)
        
        self.add_widget(self.layout)

    def snooze_alarm(self, instance):
        config_screen = self.manager.get_screen('config')
        config_screen.status_label.text = 'Alarma pospuesta - Sonará en 5 minutos'
        config_screen.test_btn.disabled = False
        self.manager.current = 'config'

    def stop_alarm(self, instance):
        config_screen = self.manager.get_screen('config')
        config_screen.alarm_active = False
        config_screen.status_label.text = 'Alarma desactivada'
        config_screen.test_btn.disabled = False
        self.manager.current = 'config'

    def close_app(self, instance):
        App.get_running_app().stop()

class AlarmApp(App):
    def build(self):
        self.title = 'Mi Alarma'
        Window.size = (400, 600)
        
        sm = ScreenManager()
        sm.add_widget(ConfigScreen(name='config'))
        sm.add_widget(AlarmScreen(name='alarm'))
        return sm

if __name__ == '__main__':
    AlarmApp().run()
