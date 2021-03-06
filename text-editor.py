from tkinter import *
from tkinter.ttk import *
import tkinter.messagebox as msg
from tkinter import filedialog
import os


# TODO Move untilty function to its own file
def generic_msg(title='Alert', text='Not ready yet.\nSorry'):
    """
    Shows the user a msg
    :param title: str
    :param text: str
    :return: None
    """
    msg.showinfo(title, text)


def parse_filename(path):
    return path.split(os.sep)[-1]


# TODO Move constants to its own file
HEIGHT = 700
WIDTH = 500


class ScrollBarComponent(Scrollbar):
    def __init__(self, parent):
        super().__init__(parent)

    def set_options(self, side, fill):
        self.pack(side=side, fill=fill)


# TODO Move each class to its own file.
class TextSection(Text):
    """
    This widget controls the Text box
    """

    def __init__(self, master_frame, state=NORMAL,
                 yscrollcommand=None,
                 height=80, width=100):
        super().__init__(master_frame.root, state=state,
                         yscrollcommand=yscrollcommand.set,
                         height=height,
                         width=width)
        self.parent = master_frame.root
        self.master = master_frame
        self.y_scrollbar = yscrollcommand
        self.y_scrollbar.config(command=self.yview)

        # Writes Text to the screen
        #self.insert_text(SENTENCE1)

        # Render to Screen
        self.pack(fill=BOTH)
        self.clear_text()

    def insert_text(self, text):
        """
        Inserts text to the text box
        :param text: str
        :return: None
        """
        self.insert(INSERT, text)

    def clear_text(self):
        """
        Clears the text from the index '1.0' to the 'END' of
        the text box
        :return: None
        """
        self.delete("1.0", END)

    def get_all_text(self):
        return self.get("1.0", END)


class NavBar(Menu):
    """
    This Widget controls the nav bar options and selection
    """

    def __init__(self, master_frame):
        super().__init__(master_frame.root)
        self.parent = master_frame.root
        self.master = master_frame
        self.file_menu = None

        # Creates the File Tab
        self.create_tab("File", self.file_menu, self.get_file_menu_data())

        # displays the menus
        master_frame.root.config(menu=self)

    def create_tab(self, name, menu, options, tearoff=0):
        """
        Creates the tab for the Nav Bar and fills it with options
        :param name: str - name of the tab
        :param menu: property - A reference link between the class and the
                     menu within the tab
        :param options: iterable of two item tuples (label, command)
        :param tearoff: int - sets the value for the tearoff
        :return: None
        """
        menu = Menu(self, tearoff=tearoff)

        # Creates the list of options
        for label, command in options:
            menu.add_command(label=label, command=command)

        # Adds this menu to the main Nav bar
        self.add_cascade(label=name, menu=menu)

    def get_file_menu_data(self):
        return (
            ('Open', self.master.open_file),
            ('Save', self.master.save_existing_file),
            ('Save as', self.master.save_new_file),
            ('Exit', self.close),
        )

    def close(self):
        self.parent.quit()


class Gui(Frame):
    """
    This widget is the main frame of the program. The parent frame.
    """

    def __init__(self, root, width=WIDTH, height=HEIGHT):
        """
        Setting the defaults for the frame
        :param root: Tk() object
        :param width: int - set default width
        :param height: int - set default height
        :return: None
        """
        super().__init__(root, width=width, height=height)
        self.root = root
        self.nav_bar = None
        self.text_section = None

        # Properties
        self.current_file_name = None

        # Gives the Gui a Title
        self.set_title()

        # Create Gui Parts
        self.create_nav_bar()
        self.create_text_section()

        # packs the Gui
        self.pack()

        # Testing things out
        print("""height: {0},
        width: {1}""".format(self.winfo_height(), self.winfo_width()))

    def set_title(self, file_name=''):
        """
        Sets the title for the GUI
        :param title: str
        :return: None
        """
        title = "Text Editor" + file_name
        self.root.title(title)

    def create_nav_bar(self):
        """
        Creates an instance of the NavBar class and associates it with
        this class.
        :return: None
        """
        self.nav_bar = NavBar(self)

    def create_text_section(self):
        """
        Creates an instance of the TextSection class and associates it with
        this class.
        :return: None
        """
        y_scrollbar = ScrollBarComponent(self.root)
        y_scrollbar.set_options(RIGHT, Y)
        self.text_section = TextSection(self, yscrollcommand=y_scrollbar)

    def open_file(self):
        test = filedialog.askopenfile()
        generic_msg(text=test.name)
        print(test)
        self.text_section.clear_text()
        with open(test.name, "r") as f:
            text = f.read()
            self.text_section.insert_text(text)

        self.text_section.pack()

        # Save the name of the file
        self.current_file_name = test.name

        # Alter the GUI Title
        file_name = parse_filename(test.name)
        self.set_title(file_name=": " + file_name)

    def save_new_file(self):
        file_name = filedialog.asksaveasfilename()
        print("asksaveasfilename:", file_name)

        # Cancelling the process results in an empty string
        if file_name != "":
            with open(file_name, "w") as f:
                text = self.text_section.get_all_text()
                f.write(text)

        # Save the name of the file
        self.current_file_name = file_name

        # Alter the GUI Title
        self.set_title(file_name=": " + file_name)

    def save_existing_file(self):
        file_name = self.current_file_name

        with open(file_name, "w") as f:
            text = self.text_section.get_all_text()
            f.write(text)


if __name__ == '__main__':
    root = Tk()
    initiate = Gui(root)
    initiate.mainloop()
