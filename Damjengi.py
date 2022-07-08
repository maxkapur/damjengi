import random
import ApplicationOrder
import importlib
import sys
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Gdk, Adw, Gio, GLib


DEFAULT_NUM_COLLEGES = 3
ADJECTIVES = "Absolute Basic Cowardly Dusty Eternal First Gorgeous Helluva Insincere Just Kramer Last Multiplicative Northernmost Overrated Practical Qualitative Wicked XYZ Yesterday Zealous".split()
NOUNS = "College,University,Institute of Technology,Arts Institute,Conservatory,Academy".split(
    ",")


def random_college_name():
    "Generate a random college name to serve as a placeholder for user input."
    adj = random.choice(ADJECTIVES)
    noun = random.choice(NOUNS)
    return "{} {}".format(adj, noun)


# Spacing unit for the grid: The total size of the grid is 12 * GRID_WIDTH_CHARS, plus padding
GRID_WIDTH_CHARS = 8


class CollegeEntry:
    "Holds a Gtk.CenterBox containing input fields for the college."

    def __init__(self):
        t = random.randint(1, 25)

        self.name_input = Gtk.Entry()
        self.name_input.set_width_chars(4 * GRID_WIDTH_CHARS)
        self.name_input.set_buffer(
            Gtk.EntryBuffer.new(random_college_name(), 240)
        )

        self.f_input = Gtk.Scale()
        self.f_input.set_digits(0)
        self.f_input.set_range(1, 100)
        self.f_input.set_value(int(1 / t * 100))
        self.f_input.set_draw_value(True)

        self.t_input = Gtk.Scale()
        self.t_input.set_digits(0)
        self.t_input.set_range(1, 100)
        self.t_input.set_value(t)
        self.t_input.set_draw_value(True)

        self.inputbox = Gtk.CenterBox()
        self.inputbox.set_start_widget(self.name_input)
        self.inputbox.set_center_widget(self.f_input)
        self.inputbox.set_end_widget(self.t_input)
        inputboxcontext = self.inputbox.get_style_context()
        inputboxcontext.add_class("collegeinputbox")


def left_justified_label(s):
    label = Gtk.Label.new(s)
    label.set_justify(Gtk.Justification.LEFT)
    return label

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_default_size(600, 250)
        self.set_title("Damjengi")
        GLib.set_application_name("Damjengi College Application Strategist")

        self.init_css("style.css")



        # Width is 12
        self.window_body = Gtk.Grid()
        self.window_body.set_name("windowbody")
        self.set_child(self.window_body)

        self.init_add_remove_buttons()
        self.init_example_college()
        self.init_input_area()

        # (0, 20) cell is the results area
        self.window_body.attach(
            Gtk.Label.new("Results will appear here …"),
            0, 20, 12, 1
        )

        self.compute_button = Gtk.Button(label="Compute application order")
        self.compute_button.connect("clicked", self.compute_application_order)
        self.window_body.attach(self.compute_button, 2, 40, 8, 1)

        self.about_button = Gtk.Button(label="About Damjengi")
        self.about_button.connect("clicked", self.show_about)
        self.window_body.attach(self.about_button, 3, 50, 6, 1)


    def init_css(self, relative_path):
        "Activate the stylesheet given by `relative_path`."
        style_file = Gio.File.new_for_path(relative_path)
        self.style_provider = Gtk.CssProvider()
        self.style_provider.load_from_file(style_file)

        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            self.style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )


    def init_add_remove_buttons(self):
        pop_college_button = Gtk.Button(label="➖ Remove a school")
        pop_college_button.connect("clicked", self.pop_college)
        self.window_body.attach(pop_college_button, 0, 0, 6, 1)

        add_college_button = Gtk.Button(label="➕ Add a school")
        add_college_button.connect("clicked", self.add_college)
        self.window_body.attach(add_college_button, 6, 0, 6, 1)


    def init_example_college(self):
        "Create the sample input header and input area."
        self.window_body.attach(
            left_justified_label("Sample input: "),
            0, 4, 1, 1
        )

        college_example_box = CollegeEntry()
        college_example_box.inputbox.set_name("exampleinput")
        college_example_box.name_input.set_buffer(
            Gtk.EntryBuffer.new("College name", 240)
        )
        college_example_box.f_input.set_value(50)
        college_example_box.f_input.set_format_value_func(
            lambda _, __: "Chance of admission (%)"
        )
        college_example_box.t_input.set_value(50)
        college_example_box.t_input.set_format_value_func(
            lambda _, __: "Utility value"
        )
        self.window_body.attach(college_example_box.inputbox, 0, 5, 12, 1)

    def init_input_area(self):
        "Generate some random colleges to initially populate the input area."
        self.window_body.attach(
            left_justified_label("Your colleges: "),
            0, 9, 1, 1
        )

        self.college_entries_list = []
        self.college_entries_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL)
        self.window_body.attach(self.college_entries_box, 0, 10, 12, 1)

        for _ in range(DEFAULT_NUM_COLLEGES):
            self.add_college(None)

    def add_college(self, _):
        self.college_entries_list.append(CollegeEntry())
        self.college_entries_box.append(self.college_entries_list[-1].inputbox)

    def pop_college(self, _):
        ce = self.college_entries_list.pop()
        self.college_entries_box.remove(ce.inputbox)

    def compute_application_order(self, _):
        try:
            self.window_body.remove(self.window_body.get_child_at(1, 20))
            self.window_body.remove(self.window_body.get_child_at(7, 20))
        except:
            pass

        if self.college_entries_list:
            xs, vs = ApplicationOrder._application_order(
                [ApplicationOrder.College(
                    ce.name_input.get_text(),
                    ce.f_input.get_value() / 100,
                    ce.t_input.get_value()
                ) for ce in self.college_entries_list]
            )

            results_x = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            results_v = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

            x_label_header = Gtk.Label.new("College name")
            x_label_header.set_justify(Gtk.Justification.CENTER)
            x_label_header.set_name("xlabelheader")
            v_label_header = Gtk.Label.new("Cumulative utility")
            v_label_header.set_name("vlabelheader")
            v_label_header.set_justify(Gtk.Justification.CENTER)

            results_x.append(x_label_header)
            results_v.append(v_label_header)

            self.window_body.attach(results_x, 1, 20, 4, 1)
            self.window_body.attach(results_v, 7, 20, 4, 1)

            x_list = Gtk.Label.new("\n".join(xs))
            x_list.set_justify(Gtk.Justification.LEFT)
            x_list.set_selectable(True)
            results_x.append(x_list)

            v_list = Gtk.Label.new("\n".join(f'{v:.3f}' for v in vs))
            v_list.set_justify(Gtk.Justification.RIGHT)
            v_list.set_selectable(True)
            results_v.append(v_list)

        else:
            self.window_body.attach(
                Gtk.Label.new("No colleges entered!"),
                0, 20, 12, 1
            )

    def show_about(self, about_button):
        self.about = Gtk.AboutDialog()
        # Makes the dialog always appear in from of the parent window
        self.about.set_transient_for(self)
        # Makes the parent window unresponsive while dialog is showing
        self.about.set_modal(self)

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


app = Damjengi(application_id="com.maxkapur.damjengi")
app.run(sys.argv)
