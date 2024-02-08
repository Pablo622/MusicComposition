import PyQt5
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGraphicsPixmapItem, QGraphicsView, QGraphicsScene, QSizePolicy, \
    QApplication, \
    QGraphicsLineItem, QLineEdit, QGraphicsTextItem, QGraphicsProxyWidget, QTextEdit, QGraphicsPathItem
from PyQt5.QtGui import QPainter, QPen, QBrush, QCursor, QPixmap, QTextCharFormat, QTextCursor, QColor, QPainterPath
from PyQt5.QtCore import Qt, QEvent, QPoint, QPointF, QSize, QRectF
from PyQt5.QtWidgets import QGraphicsEllipseItem
import math


class StaffPaper(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        # set up staff paper widget
        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene)
        self.view.setSceneRect(0, 0, 500, 1000)
        self.staff_height = 160

        # List to keep track of added elements for undo
        self.added_elements_list = []

        # List to keep track of x positions (for vertical alignment)
        self.x_positions_list = []

        # List of notes
        self.notes_list = []

        # Selected elments
        self.selected_elements_list = []

        # Disable scroll bars
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # # Ensure that staff paper does not resize with the layout
        # self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.view)
        self.setStyleSheet("background-color: white;")
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        # # Make the border invisible
        # self.setStyleSheet("border: none;")

        # Draw the inital staff lines
        self.draw_staff_lines()

        # constants
        self.WIDTH_OF_NOTE = 14
        self.HEIGHT_OF_NOTE = 9
        self.BEAM_SPACING = 4

        # alignment
        self.vertical_align = False
        self.align_from_clicked_note = False
        self.alignment_point = None
        self.horizontal_spacing = False
        self.horizontal_spacing_amount = None

        # Flags to indicate what element is being added
        self.add_black_notes = False
        self.add_white_notes = False
        self.add_stems = False
        self.add_bar_lines = False
        self.add_dots = False
        self.add_text_boxes = False
        # beams
        self.draw_beams = False
        self.add_double_beams = False
        self.draw_triple_beams = False

        # Ledger Lines
        self.add_ledger_lines = False

        # Clefs
        self.add_treble_clefs = False
        self.add_bass_clefs = False

        # erase
        self.is_erase_on = False

        # select elements
        self.select_elements = False

        # Positional Variables for lines
        self.stem_start = None
        self.stem_end = None
        self.temporary_stem = None
        self.beam_start_point = None
        self.beam_end_point = None
        self.bar_line_start = None
        self.bar_line_end = None
        self.dot_position = None

    def reset_flags(self):

        # Alignment

        self.vertical_align = False

        # Flags to indicate what element is being added
        self.add_black_notes = False
        self.add_white_notes = False
        self.add_stems = False
        self.add_bar_lines = False
        self.add_dots = False
        self.add_text_boxes = False

        # beams
        self.draw_beams = False
        self.add_double_beams = False
        self.draw_triple_beams = False

        # ledger lines
        self.add_ledger_lines = False

        # Clefs
        self.add_treble_clefs = False
        self.add_bass_clefs = False

        # erase
        self.is_erase_on = False

        # select elements
        self.select_elements = False

        # Positional variables
        self.stem_start = None
        self.stem_end = None
        self.temporary_stem = None
        self.beam_start_point = None
        self.beam_end_point = None
        self.bar_line_start = None
        self.bar_line_end = None
        self.dot_position = None



    def add_notes_to_list(self, position):
        square_size = 5
        half_size = square_size / 2.0

        # Create a square area centered around the specified position
        square_area = QRectF(
            position.x() - half_size,
            position.y() - half_size,
            square_size,
            square_size
        )
        items_in_area = self.scene.items(square_area)
        for item in items_in_area:
            if isinstance(item, QGraphicsEllipseItem):
                self.selected_elements_list.append(item)
        print(self.selected_elements_list)


    def erase(self, position):
        threshold = 3  # Adjust this threshold as needed

        for item in self.added_elements_list:
            # Check if the item is a note
            if isinstance(item, QGraphicsEllipseItem):
                if abs(item.x() - position.x()) < threshold and abs(item.y() - position.y()) < threshold:
                    self.scene.removeItem(item)
                    self.notes_list.remove(item)
            # Check if the item is a stem
            elif isinstance(item, QGraphicsLineItem):
                # Calculate the distance from the point to the line formed by the stem
                distance = self.point_to_line_distance(position, item.line())
                if distance < threshold:
                    self.scene.removeItem(item)
            elif isinstance(QGraphicsPathItem):
                distance = self.point_to_line_distance(position, item.line())
                if distance < threshold:
                    self.scene.removeItem(item)

    def point_to_line_distance(self, point, line):
        x1, y1, x2, y2 = line.x1(), line.y1(), line.x2(), line.y2()
        return abs((y2 - y1) * point.x() - (x2 - x1) * point.y() + x2 * y1 - y2 * x1) / (
                (y2 - y1) ** 2 + (x2 - x1) ** 2) ** 0.5

    def draw_staff_lines(self):
        # Draw five lines for the staff
        pen = QPen(Qt.black)

        # Draw horizontal lines

        next_pair = 0
        shift_down = 50
        while next_pair <= 600:

            for i in range(5):
                y = (i * 10) + 50 + next_pair + shift_down
                self.scene.addLine(0, y, 1000, y, pen)
            # botton staff
            for i in range(5):
                y = 160 - (i * 10) + 50 + next_pair + shift_down
                self.scene.addLine(0, y, 1000, y, pen)

            # draw vertical lines
            x_start = 0
            x_end = 1000
            y_start = 0
            y_end = self.staff_height

            self.scene.addLine(x_start, y_start, x_start, y_end)
            self.scene.addLine(x_end, y_start, x_end, y_end)
            next_pair += 300

    def add_ledger_line(self, x, y):

        if self.alignment_point:
            line = self.scene.addLine(self.alignment_point, y, self.alignment_point + (self.WIDTH_OF_NOTE + 4), y)
            self.x_positions_list.append(self.alignment_point)
            self.added_elements_list.append(line)

            line.x = self.alignment_point
            print(line.x)
        else:
            line = self.scene.addLine(x, y, x + (self.WIDTH_OF_NOTE + 4), y)
            self.x_positions_list.append(x)
            self.added_elements_list.append(line)

            line.x = x
            print(line.x)

    def add_text_box(self, position):
        pass

    def add_grace_note(self):
        pass

    def add_treble_clef(self, position):
        original_pixmap = QPixmap("trebleCleff.png")

        # Resize the pixmap with high-quality antialiasing
        desired_size = QSize(36, 96)
        resized_pixmap = original_pixmap.scaled(desired_size, aspectRatioMode=Qt.KeepAspectRatio,
                                                transformMode=Qt.SmoothTransformation)

        # Create QGraphicsPixmapItem to display the treble clef
        treble_clef_item = QGraphicsPixmapItem(resized_pixmap)
        treble_clef_item.setPos(position)

        # Set in the background
        treble_clef_item.setZValue(-1)

        # Add to scene
        self.scene.addItem(treble_clef_item)
        self.added_elements_list.append(treble_clef_item)

    def add_bass_clef(self, position):
        original_pixmap = QPixmap("clef-music-bass-key-9399d8c158c0d7c71f13f6d20e9ce2ed.png")

        # Resize the pixmap with high-quality antialiasing
        desired_size = QSize(36, 96)
        resized_pixmap = original_pixmap.scaled(desired_size, aspectRatioMode=Qt.KeepAspectRatio,
                                                transformMode=Qt.SmoothTransformation)

        # Create QGraphicsPixmapItem to display the treble clef
        bass_clef_item = QGraphicsPixmapItem(resized_pixmap)
        bass_clef_item.setPos(position)

        # Set in the background
        bass_clef_item.setZValue(-1)

        # Add to scene
        self.scene.addItem(bass_clef_item)
        self.added_elements_list.append(bass_clef_item)

    def add_black_note(self, position):

        # Draw an ellipse to represent the note
        black_note = QGraphicsEllipseItem(0, 0, self.WIDTH_OF_NOTE, self.HEIGHT_OF_NOTE)
        # Set position
        if self.alignment_point:
            black_note.setPos(self.alignment_point, position.y() - 2)
        elif self.horizontal_spacing and self.horizontal_spacing_amount is not None:
            last_element = self.notes_list[-1]
            print(last_element)
            black_note.setPos(last_element.x() + self.horizontal_spacing_amount, position.y() - 2)

        else:
            black_note.setPos(position.x() - self.WIDTH_OF_NOTE / 2, position.y() - 2)

        # Rotate the note to give slanted look
        rotation_angle = 340
        black_note.setRotation(rotation_angle)
        black_note.setBrush(Qt.black)
        self.scene.addItem(black_note)

        # Add note to list of elements
        self.added_elements_list.append(black_note)
        self.x_positions_list.append(black_note.x())

        # append to notes list
        self.notes_list.append(black_note)

    def add_white_note(self, position):

        white_note = QGraphicsEllipseItem(0, 0, self.WIDTH_OF_NOTE, self.HEIGHT_OF_NOTE)

        # if self.vertical_align:
        #     white_note.setPos(position.x(), position.y() - 2)
        if self.alignment_point:
            white_note.setPos(self.alignment_point, position.y() - 2)
        elif self.horizontal_spacing and self.horizontal_spacing_amount is not None:
            last_element = self.notes_list[-1]
            white_note.setPos(last_element.x() + self.horizontal_spacing_amount, position.y() - 2)
        else:
            white_note.setPos(position.x() - self.WIDTH_OF_NOTE / 2, position.y() - 2)

        # Rotate the note to give slanted look
        rotation_angle = 340
        white_note.setRotation(rotation_angle)
        white_note.setPen(QPen(Qt.black))
        white_note.setBrush(QBrush(Qt.NoBrush))
        self.scene.addItem(white_note)

        # append to added elemnts list
        self.added_elements_list.append(white_note)
        self.x_positions_list.append(white_note.x())

        # append to notes list
        self.notes_list.append(white_note)

    def add_stem(self, start_point, end_point):
        # Draw a line to represent the stem

        stem = QGraphicsLineItem(start_point.x(), start_point.y(), start_point.x(), end_point.y())
        self.scene.addItem(stem)
        self.added_elements_list.append(stem)
        for item in self.added_elements_list:

            # stem align on left side of note
            if abs(item.x() - start_point.x()) < 2 and abs(item.y() - start_point.y()) < 5 \
                    and start_point.x() <= item.x() + (self.WIDTH_OF_NOTE / 2 + 1.4):
                print("item in range")
                print(f"old point {start_point}")
                new_x = item.x() + 1.4
                new_y = item.y() + 3
                print(f"new new x{new_x}")
                print(f"new y{new_y}")
                adjusted_stem = QGraphicsLineItem(new_x, new_y, new_x, end_point.y())
                lenght_of_stem = abs(new_y - end_point.y())
                self.scene.addItem(adjusted_stem)
                self.added_elements_list.append(adjusted_stem)
                self.scene.removeItem(stem)
                if self.selected_elements_list:
                    for note in self.selected_elements_list:

                        y_offset = abs(self.selected_elements_list[0].y() - note.y())
                        new_stem = QGraphicsLineItem(note.x() + 1.4, note.y() + 3, note.x() + 1.4,
                                                     end_point.y() - y_offset)
                        self.scene.addItem(new_stem)
                        self.added_elements_list.append(new_stem)

            # stem align on right of note
            elif abs(item.x() - start_point.x()) < 2 + self.WIDTH_OF_NOTE and abs(item.y() - start_point.y()) < 5 \
                    and start_point.x() > item.x() + (self.WIDTH_OF_NOTE / 2 + 1.4):
                print("item in range")
                print(f"old point {start_point}")
                new_x = item.x() + self.WIDTH_OF_NOTE + 0.7
                new_y = item.y() - 0.4
                print(f"new new x{new_x}")
                print(f"new y{new_y}")
                adjusted_stem = QGraphicsLineItem(new_x, new_y, new_x, end_point.y())
                self.scene.addItem(adjusted_stem)
                self.added_elements_list.append(adjusted_stem)
                self.scene.removeItem(stem)
                if self.added_elements_list:
                    for note in self.selected_elements_list:
                        y_offset = abs(self.selected_elements_list[0].y() - note.y())
                        new_stem = QGraphicsLineItem(note.x() + self.WIDTH_OF_NOTE + 0.7, note.y() - 0.4, note.x() + self.WIDTH_OF_NOTE + 0.7,
                                                     end_point.y() - y_offset)
                        self.scene.addItem(new_stem)
                        self.added_elements_list.append(new_stem)


    def add_bar_line(self, start_point, end_point=None):
        stem = QGraphicsLineItem
        bar_line = QGraphicsLineItem(start_point.x(), start_point.y(), start_point.x(), end_point.y())
        self.scene.addItem(bar_line)
        self.added_elements_list.append(bar_line)

    def adjust_stem_end(self, stem, new_endpoint):

        start_x = stem.line().x1()
        start_y = stem.line().y1()
        end_x = stem.line().x1()
        end_y = new_endpoint.y() + .5
        print(f"start x:{start_x}\n start y:{start_y}")
        print(f"end x:{end_x}\n end_y:{end_y}")

        stem.setLine(start_x, start_y, end_x, end_y)

    def draw_beam(self, beam_start_point, beam_end_point):

        beam_path = QPainterPath()
        num_segments = 24
        spacing = .25  # Adjust as needed

        for n in range(num_segments):
            segment_start = QPointF(beam_start_point.x(), beam_start_point.y() + ((n + 1) * spacing))
            segment_end = QPointF(beam_end_point.x(), beam_end_point.y() + ((n + 1) * spacing))
            beam_path.moveTo(segment_start)
            beam_path.lineTo(segment_end)

        # Create a QGraphicsPathItem representing the beam
        beam_item = QGraphicsPathItem(beam_path)
        self.scene.addItem(beam_item)
        self.added_elements_list.append(beam_item)
        stems_to_adjust = []

        for stem in self.added_elements_list:
            if isinstance(stem, QGraphicsLineItem) and stem != beam_item:
                if beam_item.collidesWithItem(stem):
                    print("Collision detected")
                    # Get collision points
                    intersection = beam_item.shape().intersected(stem.shape())
                    intersection_polygon = intersection.toFillPolygon()

                    # Check if the intersection_polygon is not empty
                    if not intersection_polygon.isEmpty():
                        # Use the at method to get the last point
                        adjusted_stem_endpoint = intersection_polygon.at(intersection_polygon.size() - 1)
                        print(f"Collision detected. Adjusted Stem Endpoint:{adjusted_stem_endpoint}")
                        stems_to_adjust.append((stem, adjusted_stem_endpoint))
                    else:
                        print("Collision detected, but intersection_polygon is empty.")

        print(stems_to_adjust)

        for pair in stems_to_adjust:
            self.adjust_stem_end(pair[0], pair[1])

            # for i in range(intersection_polygon.size()):
            #     collision_point = intersection_polygon[i]
            #     print(f"Collision Point {i + 1}: {collision_point}")
            #
            #     adjusted_stem_endpoint = intersection_polygon[intersection_polygon.size() - 1]
            #
            #     print(f"Collision detected. Adjusted Stem Endpoint:{adjusted_stem_endpoint}")

    def draw_double_beam(self, beam_start_point, beam_end_point):

        beam_path = QPainterPath()
        num_segments = 24
        spacing = .25  # Adjust as needed

        for n in range(num_segments):
            segment_start = QPointF(beam_start_point.x(), beam_start_point.y() + ((n + 1) * spacing))
            segment_end = QPointF(beam_end_point.x(), beam_end_point.y() + ((n + 1) * spacing))
            beam_path.moveTo(segment_start)
            beam_path.lineTo(segment_end)

        for n in range(num_segments):
            segment_start = QPointF(beam_start_point.x(),
                                    beam_start_point.y() + ((n + 1) * spacing) + self.BEAM_SPACING + 5)
            segment_end = QPointF(beam_end_point.x(), beam_end_point.y() + ((n + 1) * spacing) + self.BEAM_SPACING + 5)
            beam_path.moveTo(segment_start)
            beam_path.lineTo(segment_end)
        # Create a QGraphicsPathItem representing the beam
        beam_item = QGraphicsPathItem(beam_path)
        self.scene.addItem(beam_item)
        self.added_elements_list.append(beam_item)
        stems_to_adjust = []

        for stem in self.added_elements_list:
            if isinstance(stem, QGraphicsLineItem) and stem != beam_item:
                if beam_item.collidesWithItem(stem):
                    print("Collision detected")
                    # Get collision points
                    intersection = beam_item.shape().intersected(stem.shape())
                    intersection_polygon = intersection.toFillPolygon()

                    # Check if the intersection_polygon is not empty
                    if not intersection_polygon.isEmpty():
                        # Use the at method to get the last point
                        adjusted_stem_endpoint = intersection_polygon.at(intersection_polygon.size() - 1)
                        print(f"Collision detected. Adjusted Stem Endpoint:{adjusted_stem_endpoint}")
                        stems_to_adjust.append((stem, adjusted_stem_endpoint))
                    else:
                        print("Collision detected, but intersection_polygon is empty.")

        print(stems_to_adjust)

        for pair in stems_to_adjust:
            self.adjust_stem_end(pair[0], pair[1])

    def draw_triple_beam(self, beam_start_point, beam_end_point):

        beam_path = QPainterPath()
        num_segments = 24
        spacing = .25  # Adjust as needed

        for n in range(num_segments):
            segment_start = QPointF(beam_start_point.x(), beam_start_point.y() + ((n + 1) * spacing))
            segment_end = QPointF(beam_end_point.x(), beam_end_point.y() + ((n + 1) * spacing))
            beam_path.moveTo(segment_start)
            beam_path.lineTo(segment_end)

        for n in range(num_segments):
            segment_start = QPointF(beam_start_point.x(),
                                    beam_start_point.y() + ((n + 1) * spacing) + self.BEAM_SPACING + 5)
            segment_end = QPointF(beam_end_point.x(),
                                  beam_end_point.y() + ((n + 1) * spacing) + self.BEAM_SPACING + 5)
            beam_path.moveTo(segment_start)
            beam_path.lineTo(segment_end)

        for n in range(num_segments):
            segment_start = QPointF(beam_start_point.x(),
                                    beam_start_point.y() + ((n + 1) * spacing) + self.BEAM_SPACING + 14)
            segment_end = QPointF(beam_end_point.x(),
                                  beam_end_point.y() + ((n + 1) * spacing) + self.BEAM_SPACING + 14)
            beam_path.moveTo(segment_start)
            beam_path.lineTo(segment_end)
        # Create a QGraphicsPathItem representing the beam
        beam_item = QGraphicsPathItem(beam_path)
        self.scene.addItem(beam_item)
        self.added_elements_list.append(beam_item)
        stems_to_adjust = []

        for stem in self.added_elements_list:
            if isinstance(stem, QGraphicsLineItem) and stem != beam_item:
                if beam_item.collidesWithItem(stem):
                    print("Collision detected")
                    # Get collision points
                    intersection = beam_item.shape().intersected(stem.shape())
                    intersection_polygon = intersection.toFillPolygon()

                    # Check if the intersection_polygon is not empty
                    if not intersection_polygon.isEmpty():
                        # Use the at method to get the last point
                        adjusted_stem_endpoint = intersection_polygon.at(intersection_polygon.size() - 1)
                        print(f"Collision detected. Adjusted Stem Endpoint:{adjusted_stem_endpoint}")
                        stems_to_adjust.append((stem, adjusted_stem_endpoint))
                    else:
                        print("Collision detected, but intersection_polygon is empty.")

        print(stems_to_adjust)

        for pair in stems_to_adjust:
            self.adjust_stem_end(pair[0], pair[1])

    def add_dot(self, x, y):
        # Draw a dot at the specified location
        dot_radius = 2
        dot = QGraphicsEllipseItem(0, 0, dot_radius * 2, dot_radius * 2)

        if self.align_from_clicked_note:
            dot.setPos(self.alignment_point, y - dot_radius)
            dot.setBrush(Qt.black)
            self.scene.addItem(dot)
            # Add dot to the list of elements
            self.added_elements_list.append(dot)
        else:
            dot.setPos(x - dot_radius, y - dot_radius)
            dot.setBrush(Qt.black)
            self.scene.addItem(dot)
            # Add dot to the list of elements
            self.added_elements_list.append(dot)

    def undo_last_element(self):
        if self.added_elements_list:
            last_element = self.added_elements_list[-1]
            if isinstance(last_element, QGraphicsEllipseItem):
                self.notes_list.pop()

            self.added_elements_list.pop()
            self.scene.removeItem(last_element)
            print(self.notes_list)



    def set_horizontal_spacing(self):
        self.horizontal_spacing_amount = int(input("set spacing amount"))
        print(f"Horizontal spacing set at: {self.horizontal_spacing_amount}")

    def set_alignment_point(self, position):

        square_size = 4.0
        half_size = square_size / 2.0

        # Create a square area centered around the specified position
        square_area = QRectF(
            position.x() - half_size,
            position.y() - half_size,
            square_size,
            square_size
        )

        # Find the item within the square area
        items_in_area = self.scene.items(square_area)

        # Check if any items match the criteria
        for item in items_in_area:
            if isinstance(item, QGraphicsLineItem):
                self.alignment_point = item.line().x1()
                print(f"Alignment point set at {self.alignment_point}")
                break
            elif isinstance(item, QGraphicsEllipseItem):
                self.alignment_point = item.x()
                print(f"Alignment point set at {self.alignment_point}")
                break

    def set_beam_start(self, position):

        square_size = 4.0
        half_size = square_size / 2.0

        # Create a square area centered around the specified position
        square_area = QRectF(
            position.x() - half_size,
            position.y() - half_size,
            square_size,
            square_size
        )

        # Find the item within the square area
        items_in_area = self.scene.items(square_area)
        for item in items_in_area:
            if isinstance(item, QGraphicsLineItem):
                x_coordinate_of_stem = item.line().x1()
                print(f"Clicked stem's x-coordinate: {x_coordinate_of_stem}")
                self.beam_start_point = QPointF(x_coordinate_of_stem, position.y())

                print(f"beam start point: {self.beam_start_point}")

    def set_beam_end(self, position):

        square_size = 4.0
        half_size = square_size / 2.0

        # Create a square area centered around the specified position
        square_area = QRectF(
            position.x() - half_size,
            position.y() - half_size,
            square_size,
            square_size
        )
        items_in_area = self.scene.items(square_area)
        for item in items_in_area:
            if isinstance(item, QGraphicsLineItem):
                x_coordinate_of_stem = item.line().x1()
                print(f"Clicked stem's x-coordinate: {x_coordinate_of_stem}")
                self.beam_end_point = QPointF(x_coordinate_of_stem, position.y())
                print(f"beam end point: {self.beam_end_point}")

    def keyPressEvent(self, event):

        # Zoom in with the 'W' key
        if event.key() == Qt.Key_W:
            self.view.scale(1.2, 1.2)
            # Zoom out with the 'S' key
        elif event.key() == Qt.Key_S:
            current_scale = self.view.transform().m11()
            if current_scale / 1.2 >= 1.0:
                self.view.scale(1.0 / 1.2, 1.0 / 1.2)
        # undo function
        elif event.key() == Qt.Key_Z and event.modifiers() == Qt.ControlModifier:
            self.undo_last_element()

        elif event.key() == Qt.Key_M:
            self.selected_elements_list = []
            self.reset_flags()
            self.select_elements = not self.select_elements
            print(f"select notes{self.select_elements}")
        # add white notes
        elif event.key() == Qt.Key_Space:
            self.reset_flags()
            self.add_white_notes = not self.add_white_notes

        # Toggle adding black notes
        elif event.key() == Qt.Key_B:
            self.reset_flags()
            self.add_black_notes = not self.add_black_notes

        # Toggle Treble clefs
        elif event.key() == Qt.Key_T:
            self.reset_flags()
            self.add_treble_clefs = not self.add_treble_clefs

        # Toggle ledger lines
        elif event.key() == Qt.Key_X:
            self.reset_flags()
            self.add_ledger_lines = not self.add_ledger_lines

        # Toggle Text boxes
        elif event.key() == Qt.Key_P:
            self.reset_flags()
            self.add_text_boxes = not self.add_text_boxes

        # Toggle Bass cleffs
        elif event.key() == Qt.Key_Y:
            self.reset_flags()
            self.add_bass_clefs = not self.add_bass_clefs

        # toggle stems
        elif event.key() == Qt.Key_I:
            self.reset_flags()
            self.add_stems = not self.add_stems

        # reset flags
        elif event.key() == Qt.Key_1:
            self.reset_flags()
            self.add_double_beams = not self.add_double_beams

        # toggle bar_lines
        elif event.key() == Qt.Key_L:
            self.reset_flags()
            self.add_bar_lines = not self.add_bar_lines

        # toggle dots
        elif event.key() == Qt.Key_Period:
            self.reset_flags()
            self.add_dots = not self.add_dots

        # erase
        elif event.key() == Qt.Key_E:
            self.reset_flags()
            self.is_erase_on = not self.is_erase_on
            print("e pressed")
            print(f"erase is {self.is_erase_on}")

        # toggle beams
        elif event.key() == Qt.Key_Minus:
            self.reset_flags()
            self.draw_beams = not self.draw_beams

        # toggle double beams
        elif event.key() == Qt.Key_1:
            self.reset_flags()
            self.add_double_beams = not self.add_double_beams
        # toggle triple beams
        elif event.key() == Qt.Key_2:
            self.reset_flags()
            self.draw_triple_beams = not self.draw_triple_beams

        # toggle vertical align
        elif event.key() == Qt.Key_Shift:
            self.vertical_align = not self.vertical_align

        # toggle horizontal spacing
        elif event.key() == Qt.Key_H:
            self.horizontal_spacing = not self.horizontal_spacing
            print(f"horizontal spacing {self.horizontal_spacing}")
            if self.horizontal_spacing:
                self.set_horizontal_spacing()

        # reset flags
        elif event.key() == Qt.Key_Escape:
            self.reset_flags()

        # align from clicked note
        elif event.key() == Qt.Key_A:
            self.reset_flags()
            self.alignment_point = None
            self.align_from_clicked_note = not self.align_from_clicked_note
            print("A pressed")
            print(f"align from clicked note is {self.align_from_clicked_note}")
            print(f'alignment point at {self.alignment_point}')

    def mousePressEvent(self, event):
        position = self.view.mapToScene(event.pos())

        # align form clicked note
        if self.align_from_clicked_note and self.alignment_point is None:
            self.set_alignment_point(position)
            print(f"alignemnt point at {self.alignment_point}")

        # erase
        if self.is_erase_on:
            self.erase(position)

        # select elemnts
        if self.select_elements:
            self.add_notes_to_list(position)

        # Add text box
        if self.add_text_boxes:
            self.add_text_box(position)

        # Add the note based on the current color
        if self.add_black_notes:
            if self.add_black_notes and self.vertical_align:
                self.black_note_position = QPointF(self.x_positions_list[-1], round(position.y() / 5) * 5)
                self.add_black_note(self.black_note_position)
            else:
                self.black_note_position = QPointF(position.x(), round(position.y() / 5) * 5)
                self.add_black_note(self.black_note_position)
        if self.add_white_notes:
            if self.add_white_notes and self.vertical_align:
                self.white_note_position = QPointF(self.x_positions_list[-1], round(position.y() / 5) * 5)
                self.add_white_note(self.white_note_position)
            else:
                self.white_note_position = QPointF(position.x(), round(position.y() / 5) * 5)
                self.add_white_note(self.white_note_position)

        # set stem start and end point
        if self.add_stems:
            if self.stem_start is None:
                self.stem_start = QPointF(position.x(), position.y())

            # if stem_start exists, set stem_end and draw stem
            else:
                self.stem_end = QPointF(position.x(), position.y())
                self.add_stem(self.stem_start, self.stem_end)
                # Reset stem_start to None
                self.stem_start = None
                # Remove the temporary stem
        # bar lines
        if self.add_bar_lines:
            # set bar line start pont
            if self.bar_line_start is None:
                self.bar_line_start = QPointF(position.x(), round(position.y() / 10) * 10)
            # set bar line end point
            else:
                self.bar_line_end = QPointF(position.x(), round(position.y() / 10) * 10)
                self.add_bar_line(self.bar_line_start, self.bar_line_end)
                self.bar_line_start = None
        # ledger lines
        if self.add_ledger_lines:
            if self.add_ledger_lines and self.vertical_align:
                x = self.x_positions_list[-1]
                self.add_ledger_line(x, round(position.y() / 10) * 10)
            else:
                self.ledger_position = QPointF(position.x(), round(position.y() / 10) * 10)
                self.add_ledger_line(self.ledger_position.x(), self.ledger_position.y())
        # dots
        if self.add_dots:
            self.add_dot(position.x(), position.y())

        # set beam start and endpoint and call function
        if self.draw_beams:
            if not self.beam_start_point:
                self.set_beam_start(position)
            elif not self.beam_end_point:
                self.set_beam_end(position)
            if self.beam_start_point and self.beam_end_point:
                self.draw_beam(self.beam_start_point, self.beam_end_point)
                # Reset points for the next beam
                self.beam_start_point = None
                self.beam_end_point = None
        if self.add_double_beams:
            if not self.beam_start_point:
                self.set_beam_start(position)
            elif not self.beam_end_point:
                self.set_beam_end(position)
            if self.beam_start_point and self.beam_end_point:
                self.draw_double_beam(self.beam_start_point, self.beam_end_point)
                # Reset points for the next bea
                self.beam_start_point = None
                self.beam_end_point = None
        if self.draw_triple_beams:
            if not self.beam_start_point:
                self.set_beam_start(position)
            elif not self.beam_end_point:
                self.set_beam_end(position)
            if self.beam_start_point and self.beam_end_point:
                self.draw_triple_beam(self.beam_start_point, self.beam_end_point)
                # Reset points for the next bea
                self.beam_start_point = None
                self.beam_end_point = None
        # add treble clefs
        if self.add_treble_clefs:
            self.treble_clef_position = QPointF(position.x(), position.y())
            self.add_treble_clef(self.treble_clef_position)
        # Bass clefs
        if self.add_bass_clefs:
            self.bass_clef_position = QPointF(position.x(), position.y())
            self.add_bass_clef(self.bass_clef_position)
