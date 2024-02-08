############ previous version
# position = self.view.mapToScene(event.pos())
# line_height = 10
# column_width = 20
#
# # Calculate y position if its on a line or a space
# on_line = round(position.y() / line_height) * line_height
# on_space = round((position.y() + line_height / 2) / line_height) * line_height - line_height / 2
#
# # Calculate x pos based on column width
# x_position = round(position.x() / column_width) * column_width
#
# # if the note is closer to the line center note on line
# if abs(position.y() - on_line) < abs(position.y() - on_space):
#     if self.last_note_color == 'black':
#         self.add_black_note(x_position, on_line, 14, 8)
#     if self.last_note_color == 'white':
#         self.add_white_note(x_position, on_line, 14, 8)
#
# # If note is closer to space, center it on the space
# else:
#     if self.last_note_color == 'black':
#         self.add_black_note(x_position, on_space, 14, 8)
#     if self.last_note_color == 'white':
#         self.add_white_note(x_position, on_space, 14, 8)
##########################

# def wheelEvent(self, event):
#     # zoom in and out based on the mouse wheel
#     zoom_factor = 1.2
#
#     if event.angleDelta().y() < 0:
#         self.view.scale(zoom_factor, zoom_factor)
#     else:
#         self.view.scale(1.0 / zoom_factor, 1.0 / zoom_factor)
