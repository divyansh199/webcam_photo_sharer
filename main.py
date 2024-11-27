from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.clipboard import Clipboard

import time
import webbrowser

from fileshare import FileShare

Builder.load_file("webcam.kv")

class CameraScreen(Screen):

    def start(self):
        """
        starts the camera screen
        """
        self.ids.camera.opacity = 1
        self.ids.camera.play = True
        self.ids.camera_button.text = 'Stop Camera'
        self.ids.camera.texture = self.ids.camera._camera.texture

    def stop(self):
        """
        stops the camera screen
        """
        self.ids.camera.opacity = 0
        self.ids.camera.play = False
        self.ids.camera_button.text = 'Start Camera'
        self.ids.camera.texture = None

    def capture(self):
        """
        captures the image
        """
        current_time = time.strftime("%Y%m%d-%H%M%S")
        self.filepath = f'images/{current_time}.png'
        self.ids.camera.export_to_png(self.filepath)
        self.manager.current = 'image_screen'
        self.manager.current_screen.ids.img.source = self.filepath


class ImageScreen(Screen):
    """
    create a link in label box
    """
    def create_link(self):
        file_path = App.get_running_app().root.ids.camera_screen.filepath
        file_share = FileShare(file_path)
        self.url = file_share.share()
        self.ids.link.text = self.url

    def copy_link(self):
        """
        for copy the link present in label widget
        """
        try:
            Clipboard.copy(self.url)
        except:
            self.ids.link.text = 'please press the create link button'

    def open_link(self):
        """
        open the link in label widget
        """
        try:
            webbrowser.open(self.url)
        except:
            self.ids.link.text = 'please press the create link button'



class RootWidget(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()

MainApp().run()
