import kivy.weakmethod as wm
import kivy_garden.mapview as mv
from kivy.uix.widget import Widget
from kivy_garden.mapview.utils import clamp

"""source:
https://github.com/kivy-garden/mapview/issues/33
"""


class MyMapView(mv.MapView):
    def on_touch_down(self, touch):
        # if not self.collide_point(*touch.pos):
        if not self.collide_point(*touch.pos) or self.disabled:
            return
        if self.pause_on_action:
            self._pause = True
        if "button" in touch.profile and touch.button in ("scrolldown", "scrollup"):
            # d = 1 if touch.button == "scrollup" else -1
            d = 1 if touch.button == "scrolldown" else -1
            self.animated_diff_scale_at(d, *touch.pos)
            return True
        elif touch.is_double_tap and self.double_tap_zoom:
            self.animated_diff_scale_at(1, *touch.pos)
            return True
        touch.grab(self)
        self._touch_count += 1
        if self._touch_count == 1:
            self._touch_zoom = (self.zoom, self._scale)
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if touch.grab_current == self:
            touch.ungrab(self)
            self._touch_count -= 1
            if self._touch_count == 0:
                # animate to the closest zoom
                zoom, scale = self._touch_zoom
                cur_zoom = self.zoom
                cur_scale = self._scale
                # if cur_zoom < zoom or round(cur_scale, 2) < scale:
                #     pass
                #     # self.animated_diff_scale_at(1.0 - cur_scale, *touch.pos)
                # elif cur_zoom > zoom or round(cur_scale, 2) > scale:
                #     self.animated_diff_scale_at(2.0 - cur_scale, *touch.pos)
                self._pause = False
            return True
        return super(mv.MapView, self).on_touch_up(touch)

    def on_transform(self, *args):
        self._invalid_scale = True
        if self._transform_lock:
            return
        self._transform_lock = True
        # recalculate viewport
        map_source = self.map_source
        zoom = self._zoom
        scatter = self._scatter
        scale = scatter.scale
        if round(scale, 2) >= 2.0:
            zoom += 1
            scale /= 2.0
        elif round(scale, 2) < 1.0:
            zoom -= 1
            scale *= 2.0
        zoom = clamp(zoom, map_source.min_zoom, map_source.max_zoom)
        if zoom != self._zoom:
            self.set_zoom_at(zoom, scatter.x, scatter.y, scale=scale)
            self.trigger_update(True)
        else:
            if zoom == map_source.min_zoom and round(scatter.scale, 2) < 1.0:
                scatter.scale = 1.0
                self.trigger_update(True)
            else:
                self.trigger_update(False)

        if map_source.bounds:
            self._apply_bounds()
        self._transform_lock = False
        self._scale = self._scatter.scale

    @property
    def scale(self):
        if self._invalid_scale:
            self._invalid_scale = False
            self._scale = round(self._scatter.scale, 2)
        return self._scale
