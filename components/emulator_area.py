from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.clock import Clock

from kivystudio.behaviors import HoverBehavior
from kivystudio.screens import AndroidPhoneScreen

__all__ = ('EmulatorArea')

class EmulatorArea(BoxLayout):

    def __init__(self, **kwargs):
        super(EmulatorArea, self).__init__(**kwargs)
        self.screen_manager = EmulatorScreens()
        self.add_widget(self.screen_manager)
        self.add_widget(ScreenDisplay())
    
    def add_widget(self, widget):
        if len(self.children) > 1:
            self.screen_manager.add_widget(widget, widget.name)
            tab = EmulatorTab(text=widget.name)
            self.ids.tab_manager.add_widget(tab)

        else:
            super(EmulatorArea, self).add_widget(widget)


class ScreenScaler(BoxLayout):
    
    screen = ObjectProperty(None)


class EmulatorTab(HoverBehavior, ToggleButtonBehavior,Label):

    def on_hover(self, *args):
        if self.hover:
            self.color = 1,1,1,1
        else:
            if not self.bold:
                self.color = .5,.5,.5,1

    def on_state(self, *args):
        if self.state == 'down':
            self.bold=True
            if not self.text.startswith('[u]'):
                self.text = '[u]'+self.text+'[/u]'
        else:
            self.bold=False
            self.text = self.text.replace('[u]','').replace('[/u]','')

    


class EmulatorScreens(ScreenManager):
    
    def add_widget(self, widget, name):
        screen = Screen(name=name)
        screen.add_widget(widget)
        super(EmulatorScreens, self).add_widget(screen)



class ScreenDisplay(HoverBehavior, FloatLayout):
    
    screen = ObjectProperty(None)

    scaler = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(ScreenDisplay, self).__init__(**kwargs)
        self.scaler = ScreenScaler()
        self.screen = AndroidPhoneScreen()

    def on_hover(self, *args):
        if self.hover:
            if self.scaler not in self.children:
                self.add_widget(self.scaler)
        else:
            if self.scaler in self.children:
                    Clock.schedule_once(
                        lambda dt: self.remove_widget(self.scaler), 0.5)

    def on_screen(self, obj, screen):
        if self.screen not in self.children:
            self.add_widget(screen)
            self.screen.bind(scale=lambda *args: setattr(self.screen, 'center', self.center))
            self.bind(center=self.screen.setter('center'))
            self.scaler.screen = screen



Builder.load_string('''

<EmulatorArea>:
    orientation: 'vertical'
    ScrollView:
        size_hint_y: None
        height: '36dp'
        canvas.before:
            Color:
                rgba: (0.2, 0.2, 0.2, 1)
            Rectangle:
                size: self.size
                pos: self.pos

        GridLayout:
            rows: 1
            id: tab_manager
            size_hint_x: None
            width: self.minimum_width


<EmulatorTab>:
    size_hint_x: None
    width: '100dp'
    # allow_no_selection: False
    group: 'emulator_tab'
    font_size: '13.5dp'
    color: .5,.5,.5,1
    markup: True



<ScreenDisplay>:
    name: 'Emulator'
    canvas.before:
        Color:
            rgba: .5,.5,.5,1
        Rectangle:
            size: self.size
            pos: self.pos


<ScreenScaler>:
    pos_hint: {'y': .01, 'center_x': .5}
    size_hint: None,None
    size: '110dp', '46dp'
    Button:
        text: '-'
        bold: True
        on_release:
            if not root.screen.scale < -100.0: root.screen.scale -= 0.05
    Button:
        text: '+'
        bold: True
        on_release: root.screen.scale += 0.05

''')