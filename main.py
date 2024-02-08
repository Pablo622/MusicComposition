import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from staff_paper_widget import StaffPaper


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Score")
        self.setGeometry(0, 0, 500, 1000)


        # Create a central widget and a layout
        central_widget = QWidget(self)
        central_widget.setStyleSheet("background-color: white;")
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)



        # create instances of staff paper

        staff_paper = StaffPaper()
        layout.addWidget(staff_paper)

        # Set the central widget of the main windowb
        self.setCentralWidget(central_widget)

        # Set main window background to white
        self.setStyleSheet("background-color: white;")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()

    sys.exit(app.exec_())
