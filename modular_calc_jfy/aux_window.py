from PyQt6 import QtWidgets, QtCore

class AuxCalcWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(AuxCalcWindow, self).__init__(parent)
        self.setWindowTitle("Auxiliary Calculator")
        self.setMinimumSize(200, 100)
        
        # Create a simple layout
        layout = QtWidgets.QVBoxLayout()
        
        # Add a temporary label
        label = QtWidgets.QLabel("Auxiliary Calculator\n(Temporary Window)")
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        
        # Add a close button
        close_button = QtWidgets.QPushButton("Close")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)
        
        self.setLayout(layout)
