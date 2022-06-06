from abc import abstractmethod

import geocoder
from kivy.clock import Clock
from kivy.uix.popup import Popup


class SaveDialog(Popup):

    def __init__(self, parent_widget, title='Insert coordinates',
                 **kwargs):  # my_widget is now the object where popup was called from.
        super(SaveDialog, self).__init__(title=title, **kwargs)
        self.parent_widget = parent_widget

    @abstractmethod
    def save(self, *args):
        pass

    def cancel(self, *args):
        self.dismiss()


class SaveSignalDialog(SaveDialog):

    def __init__(self, parent_widget, **kwargs):
        super(SaveSignalDialog, self).__init__(parent_widget, title='Insert signal coordinates', **kwargs)

    def save(self, *args):
        self.parent_widget.add_coordinates(lat=float(self.ids.lat_txt_in.text),
                                           lon=float(self.ids.lon_txt_in.text))
        self.dismiss()


class SaveUserDialog(SaveDialog):

    def __init__(self, parent_widget, **kwargs):
        super(SaveUserDialog, self).__init__(parent_widget, title='Insert your coordinates', **kwargs)

    def save(self, *args):
        self.parent_widget.add_user_coordinates(lat=float(self.ids.lat_txt_in.text),
                                                lon=float(self.ids.lon_txt_in.text))
        self.dismiss()

    def auto_loc(self, *args):
        Clock.schedule_interval(self.send_loc, 2)

    def send_loc(self, *args):
        g = geocoder.ip('me')
        self.parent_widget.add_user_coordinates(g.latlng[0], g.latlng[1])


class SaveUFODialog(SaveDialog):

    def __init__(self, parent_widget, **kwargs):
        super(SaveUFODialog, self).__init__(parent_widget, title='Insert UFO coordinates', **kwargs)

    def save(self, *args):
        self.parent_widget.add_UFO_coordinates(lat=float(self.ids.lat_txt_in.text),
                                               lon=float(self.ids.lon_txt_in.text))
        self.dismiss()
