from kivy.uix.popup import Popup


class SaveDialog(Popup):

    def __init__(self, parent_widget, **kwargs):  # my_widget is now the object where popup was called from.
        super(SaveDialog, self).__init__(**kwargs)

        self.parent_widget = parent_widget

    def save(self, *args):
        self.parent_widget.add_marker(lat=float(self.ids.lat_txt_in.text),
                                      lon=float(self.ids.lon_txt_in.text))
        self.dismiss()

    def cancel(self, *args):
        self.dismiss()