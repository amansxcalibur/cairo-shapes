import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib
import cairo
import threading
from utils.morph import Morph


class ShapeMorph(Gtk.DrawingArea):
    def __init__(self):
        super().__init__()
        self.set_size_request(300, 300)

        # self.start_vertices = [(0.2, 0.1), (0.8, 0.7), (0.5, 0.5)]
        # self.end_vertices = [(0.1, 0.1), (0.9, 0.1), (0.9, 0.9), (0.1, 0.9)]
        self.start_vertices = [(0.5, 0.1), (0.9, 0.8), (0.1, 0.8)]
        # self.end_vertices = [
        #     (0.5, 0.05),  # top
        #     (0.95, 0.38),  # top-right
        #     (0.77, 0.90),  # bottom-right
        #     (0.23, 0.90),  # bottom-left
        #     (0.05, 0.38),  # top-left
        # ]
        self.end_vertices = [
            (0.50, 0.95),  # spike
            (0.58, 0.70),
            (0.78, 0.78),  # spike
            (0.65, 0.60),
            (0.95, 0.50),  # spike
            (0.65, 0.40),
            (0.78, 0.22),  # spike
            (0.58, 0.30),
            (0.50, 0.05),  # spike
            (0.42, 0.30),
            (0.22, 0.22),  # spike
            (0.35, 0.40),
            (0.05, 0.50),  # spike
            (0.35, 0.60),
            (0.22, 0.78),  # spike
            (0.42, 0.70),
        ]

        # self.start_vertices = [(1,1),(2,2),(4,4)]
        # self.end_vertices =  [(1.1,1.1),(2.2,2.2),(3.3,3.3),(4.4,4.4)]

        # self.v1, self.v2 = Morph.equalize_vertices(
        #     self.start_vertices, self.end_vertices
        # )

        self.v1, self.v2 = Morph.map_vertices(self.start_vertices, self.end_vertices)

        self.alpha = 0.0
        self.direction = 1
        self.step_once = False

        self.connect("draw", self.on_draw)

        GLib.timeout_add(16, self.update_animation)

        threading.Thread(target=self.wait_for_enter, daemon=True).start()
        self.show_all()

    def wait_for_enter(self):
        while True:
            input()
            GLib.idle_add(self._trigger_step)

    def _trigger_step(self):
        self.step_once = True
        return False  # run once

    def update_animation(self):
        if not self.step_once:
            return True

        self.step_once = False

        # step = 0.032 * self.direction
        step = 0.1 * self.direction
        self.alpha += step

        if self.alpha >= 1.0:
            self.alpha = 1.0
            self.direction = -1
        elif self.alpha <= 0.0:
            self.alpha = 0.0
            self.direction = 1

        self.queue_draw()
        return True

    def on_draw(self, widget, ctx: cairo.Context):
        width = self.get_allocated_width()
        height = self.get_allocated_height()

        side = min(width, height)
        ctx.translate((width - side) / 2, (height - side) / 2)
        ctx.scale(side, side)

        points = Morph.get_interpolated(self.v1, self.v2, self.alpha)

        ctx.set_source_rgb(0.4, 0.6, 0.9)
        ctx.move_to(*points[0])
        for p in points[1:]:
            ctx.line_to(*p)
        ctx.close_path()

        ctx.set_line_width(0.02)
        ctx.stroke_preserve()
        ctx.set_source_rgba(0.4, 0.6, 0.9, 0.4)
        ctx.fill()

        return False
