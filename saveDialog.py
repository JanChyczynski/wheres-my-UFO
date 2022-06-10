from abc import abstractmethod

import geocoder
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
import pylab
import rtlsdr
from rtlsdr.rtlsdr import LibUSBError

'''
to use this you must put rtlsdr.dll in the same folder as python location 
(https://github.com/librtlsdr/librtlsdr/releases)
'''

from coords_receiver import CoordinatesReceiver

Builder.load_file('saveDialogs.kv')


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
        # TODO check for conversion errors
        self.parent_widget.add_coordinates(lat=float(self.ids.lat_txt_in.text),
                                           lon=float(self.ids.lon_txt_in.text),
                                           strength=float(self.ids.signal_txt_in.text))
        self.dismiss()

    def save_auto_radio(self):
        try:
            sdr = rtlsdr.RtlSdr()
            sdr.sample_rate = float(self.ids.sample_txt_in)
            sdr.center_freq = float(self.ids.freq_txt_in)
            sdr.gain = float(self.ids.gain_txt_in)
            samples = sdr.read_samples(500e3)
            self.parent_widget.add_coordinates(lat=float(self.ids.lat_txt_in.text),
                                               lon=float(self.ids.lon_txt_in.text),
                                               strength=float(10 * pylab.log10(pylab.var(samples))))
        except LibUSBError as err:
            self.dismiss()
            box = BoxLayout(orientation='vertical', padding=(10))
            box.add_widget(Label(text=str(err)))
            btn1 = Button(text="close")
            box.add_widget(btn1)

            popup = Popup(title='signal strength reading error', title_size=(30),
                          title_align='center', content=box,
                          size_hint=(None, None), size=(600, 200),
                          auto_dismiss=True)

            btn1.bind(on_press=popup.dismiss)
            popup.open()
            print(err)


class SaveUserDialog(SaveDialog):

    def __init__(self, parent_widget, **kwargs):
        super(SaveUserDialog, self).__init__(parent_widget, title='Insert your coordinates', **kwargs)

    def save(self, *args):
        self.parent_widget.add_user_coordinates(lat=float(self.ids.lat_txt_in.text),
                                                lon=float(self.ids.lon_txt_in.text))
        self.dismiss()

    def auto_loc(self, *args):
        Clock.schedule_interval(self.send_loc, 2)
        self.dismiss()

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

    def socket_receive(self, *args):
        self.parent_widget.start_receiving(self.ids.ip_txt_in.text, int(self.ids.port_txt_in.text))
        self.dismiss()
