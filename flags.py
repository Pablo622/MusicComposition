from PyQt5.QtWidgets import QWidget


class Flags(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        # Flags to indicate what element is being added
        self.current_element = None
        self.add_black_notes = False
        self.add_white_notes = False
        self.add_stems = False
        self.add_bar_lines = False
        self.add_dots = False

        # beams
        self.draw_beams = False
        self.one_beam = False
        # Variables for stem drawing
        self.stem_start = None
        self.stem_end = None
        self.temporary_stem = None
        self.beam_start_point = None
        self.beam_end_point = None
        self.bar_line_start = None
        self.bar_line_end = None
        self.dot_position = None

    def reset_flags(self, current_element):
        # Flags to indicate what element is being added
        self.add_black_notes = False
        self.add_white_notes = False
        self.add_stems = False
        self.add_bar_lines = False
        self.add_dots = False

        # beams
        self.draw_beams = False
        self.one_beam = False
        # Variables for stem drawing
        self.stem_start = None
        self.stem_end = None
        self.temporary_stem = None
        self.beam_start_point = None
        self.beam_end_point = None
        self.bar_line_start = None
        self.bar_line_end = None
        self.dot_position = None
        self.current_element = not current_element
