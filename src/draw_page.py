from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QStackedLayout, QPushButton, QApplication, QGraphicsScene, QGraphicsView, QGraphicsEllipseItem, QGraphicsLineItem,  QTableWidget, QTableWidgetItem, QMessageBox
from PyQt6.QtGui import QPainter, QPen, QBrush
from PyQt6.QtCore import Qt 
import sys

class DrawingArea(QWidget):
    def __init__(self, joint_button, link_button):
        super().__init__()
        self.layout = QHBoxLayout(self)

        self.scene = QGraphicsScene(0, 0, 400, 300)
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.RenderHint.Antialiasing)

        self.table = TableExample()

        self.layout.addWidget(self.table)
        self.layout.addWidget(self.view)
        self.joint_button = joint_button
        self.link_button = link_button
        self.selected_joints = []

    def add_Joint(self, x, y):
        ellipse_item = QGraphicsEllipseItem(x - 10, y - 10, 16, 16)
        ellipse_item.setBrush(QBrush(Qt.GlobalColor.blue))
        ellipse_item.setPen(QPen(Qt.GlobalColor.black))
        self.scene.addItem(ellipse_item)

    def add_Link(self, joint1, joint2):
        print(joint1.pos().x(), joint1.pos().y(), joint2.pos().x(), joint2.pos().y())
        line_item = QGraphicsLineItem(joint1.pos().x(), joint1.pos().y(), joint2.pos().x(), joint2.pos().y())
        line_item.setPen(QPen(Qt.GlobalColor.black, 2))
        self.scene.addItem(line_item)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            mouse_pos = event.pos()
            scene_pos = self.view.mapToScene(mouse_pos)
            if self.joint_button.isChecked():
                self.add_Joint(scene_pos.x(), scene_pos.y())
            if self.link_button.isChecked():
                joint = self.find_joint_at_position(scene_pos)
                if joint and joint not in self.selected_joints:
                    print(joint.pos().x(), joint.pos().y())

                    self.selected_joints.append(joint)
                    if len(self.selected_joints) == 2:
                        self.add_Link(self.selected_joints[0], self.selected_joints[1])
                        self.selected_joints = []

class TableExample(QWidget):
    def __init__(self):
        super().__init__()
        self.rows = 1
        self.columns = 2

        self.setGeometry(100, 100, 400, 300)
        self.setFixedWidth(233)

        self.layout = QVBoxLayout(self)

        self.label = QLabel("Joint Coordinates")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.table_widget = QTableWidget(self.rows, self.columns)
        self.table_widget.setHorizontalHeaderLabels(["X", "Y"])

        for row in range(self.rows):
            for column in range(self.columns):
                item = QTableWidgetItem(f"0")
                self.table_widget.setItem(row, column, item)

        # Button to add a new row
        self.add_row_button = QPushButton("Add Row")
        self.add_row_button.clicked.connect(self.add_row)

        self.delete_row_button = QPushButton("Delete Row")
        self.delete_row_button.clicked.connect(self.delete_row)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.table_widget)
        self.layout.addWidget(self.add_row_button)
        self.layout.addWidget(self.delete_row_button)

    def add_row(self, x_value="0", y_value="0"):
            self.rows += 1
            self.table_widget.setRowCount(self.rows)
            self.table_widget.setItem(self.rows - 1, 0, QTableWidgetItem(x_value))
            self.table_widget.setItem(self.rows - 1, 1, QTableWidgetItem(y_value))

    def delete_row(self):
        current_row = self.table_widget.currentRow()
        if current_row >= 0:
            self.table_widget.removeRow(current_row)
            self.rows -= 1
        else:
            QMessageBox.warning(self, "Warning", "No row selected to delete.")

    def fill_row(self):
        current_row = self.table_widget.currentRow()
        if current_row >= 0:
            for column in range(self.columns):
                item = QTableWidgetItem(f"Filled {current_row},{column}")
                self.table_widget.setItem(current_row, column, item)
        else:
            QMessageBox.warning(self, "Warning", "No row selected to fill.")

class ToolBar(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout(self)

        self.buttons = []
        
        self.joint_button = QPushButton("Joint")
        self.joint_button.setCheckable(True)
        self.joint_button.clicked.connect(self.on_button_clicked)
        self.buttons.append(self.joint_button)

        self.link_button = QPushButton("Link")
        self.link_button.setCheckable(True)
        self.link_button.clicked.connect(self.on_button_clicked)
        self.buttons.append(self.link_button)

        self.erase_button = QPushButton("Erase")
        self.erase_button.setCheckable(True)
        self.erase_button.clicked.connect(self.on_button_clicked)
        self.buttons.append(self.erase_button)

        for button in self.buttons:
            self.layout.addWidget(button)

    def on_button_clicked(self):
        sender = self.sender()
        
        for button in self.buttons:
            if button != sender:
                button.setChecked(False)

        #print(f"Checked button: {sender.text()}")

class DrawPage(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)

        # Toolbar
        self.custom_toolbar = ToolBar()

        # Drawing Area
        self.drawing_area = DrawingArea(self.custom_toolbar.joint_button, self.custom_toolbar.link_button)

        self.layout.addWidget(self.custom_toolbar)
        self.layout.addWidget(self.drawing_area)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DrawPage()
    window.show()
    sys.exit(app.exec())