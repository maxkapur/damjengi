import sys
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio, GLib
import ApplicationOrder
import random

DEFAULT_NUM_COLLEGES = 3
ADJECTIVES = "Absolute Basic Cowardly Dusty Eternal First Gorgeous Helluva Insincere Just Kramer Last Multiplicative Northernmost Overrated Practical Qualitative Wicked XYZ Yesterday Zealous".split()
NOUNS = "College,University,Institute of Technology,Arts Institute,Conservatory,Academy".split(",")

def random_college_name():
    adj = random.choice(ADJECTIVES)
    noun = random.choice(NOUNS)
    return "{} {}".format(adj, noun)

class CollegeEntry:
    def __init__(self):
        t = random.randint(1, 101)
    
        self.c = ApplicationOrder.College(
            random_college_name(),
            1 / t,
            t
        )

        self.name_input = Gtk.Entry()
        self.name_input.set_buffer(
            Gtk.EntryBuffer.new(self.c.name, 240)
        )

        self.name_input.connect("changed", self.update_name)
        
        self.f_input = Gtk.Scale()
        self.f_input.set_digits(0)
        self.f_input.set_range(1, 100) 
        self.f_input.set_value(int(self.c.f * 100))
        self.f_input.set_draw_value(True)
        self.f_input.connect("value-changed", self.update_f)
        
        self.t_input = Gtk.Scale()
        self.t_input.set_digits(0)
        self.t_input.set_range(1, 100) 
        self.t_input.set_value(self.c.t)
        self.t_input.set_draw_value(True)
        self.t_input.connect("value-changed", self.update_t)

        self.inputbox = Gtk.CenterBox()
        self.inputbox.set_start_widget(self.name_input)
        self.inputbox.set_center_widget(self.f_input)
        self.inputbox.set_end_widget(self.t_input)

    def update_name(self, _):
        self.c.name = self.name_input.get_text()

    def update_f(self, _):
        self.c.f = self.f_input.get_value() / 100

    def update_t(self, _):
        self.c.t = self.t_input.get_value()



class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_default_size(600, 250)
        self.set_title("Damjengi")
        GLib.set_application_name("Damjengi College Application Strategist")

        self.window_body = Gtk.Grid()
        self.set_child(self.window_body)

        self.college_entries_list = []
        self.college_entries_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.window_body.attach(self.college_entries_box, 0, 0, 1, 1)

        for _ in range(DEFAULT_NUM_COLLEGES):
            self.add_college(None)

        self.add_college_button = Gtk.Button(label="Add a new school")
        self.add_college_button.connect("clicked", self.add_college)
        self.window_body.attach(self.add_college_button, 0, 1, 1, 1)

        # (0, 2) cell is the results area
        self.window_body.attach(
            Gtk.Label.new("Results will appear here …"),
            0, 2, 1, 1
        )

        self.compute_button = Gtk.Button(label="Compute application order")
        self.compute_button.connect("clicked", self.compute_application_order)
        self.window_body.attach(self.compute_button, 0, 3, 1, 1)

        self.about_button = Gtk.Button(label="About Damjengi")
        self.about_button.connect("clicked", self.show_about)
        self.window_body.attach(self.about_button, 0, 4, 1, 1)

    def add_college(self, _):
        self.college_entries_list.append(CollegeEntry())
        self.college_entries_box.append(self.college_entries_list[-1].inputbox)

    def compute_application_order(self, _):
        xs, vs = ApplicationOrder._application_order(
            [ce.c for ce in self.college_entries_list]
        )

        try:
            self.window_body.remove(self.window_body.get_child_at(0, 2))
        except:
            pass
        
        results_grid = Gtk.Grid()

        for i, (x, v) in enumerate(zip(xs, vs)):
            results_grid.attach(
                Gtk.Label.new(str(x)),
                0, i, 1, 1
            )
            results_grid.attach(
                Gtk.Label.new(str(round(v, 3))), 
                1, i, 1, 1, 
            )

        self.window_body.attach(results_grid, 0, 2, 1, 1)

    def show_about(self, about_button):
        self.about = Gtk.AboutDialog()
        self.about.set_transient_for(self)  # Makes the dialog always appear in from of the parent window
        self.about.set_modal(self)  # Makes the parent window unresponsive while dialog is showing

        self.about.set_authors(["Max Kapur"])
        self.about.set_copyright("ⓒ 2022 Max Kapur")
        self.about.set_license_type(Gtk.License.GPL_3_0)
        self.about.set_website("https://maxkapur.com")
        self.about.set_website_label("maxkapur.com")
        self.about.set_version("0.1.0")
        self.about.show()


class Damjengi(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.win = MainWindow(application=app)
        self.win.present()

app = Damjengi(application_id="com.maxkapur.Damjengi")
app.run(sys.argv)
