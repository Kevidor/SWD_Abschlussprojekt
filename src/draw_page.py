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
        
        self.table = Table()
        self.table.table_widget.itemChanged.connect(self.update_drawing)

        self.joint_button = joint_button
        self.link_button = link_button
        self.joint_items = []
        self.link_items = []

        self.layout.addWidget(self.table)
        self.layout.addWidget(self.view)

    def update_drawing(self):
        # Clear previous drawing
        self.clear_drawing()

        # Draw joints based on table data
        for row in range(self.table.rows):
            x = float(self.table.table_widget.item(row, 0).text())
            y = float(self.table.table_widget.item(row, 1).text())
            ellipse_item = QGraphicsEllipseItem(x - 10, y - 10, 16, 16)
            ellipse_item.setBrush(QBrush(Qt.GlobalColor.blue))
            ellipse_item.setPen(QPen(Qt.GlobalColor.black))
            self.scene.addItem(ellipse_item)
            self.joint_items.append(ellipse_item)

    def clear_drawing(self):
        # Remove all joint and link items from the scene
        for item in self.joint_items:
            self.scene.removeItem(item)
        for item in self.link_items:
            self.scene.removeItem(item)
        self.joint_items.clear()
        self.link_items.clear()

    def mousePressEvent(self, event):
        scene_pos = self.view.mapToScene(event.pos())
        x, y = round(scene_pos.x(), 2), round(scene_pos.y(), 2)
        self.table.add_row(str(x), str(y))

        self.update_drawing()

class Table(QWidget):
    def __init__(self):
        super().__init__()
        self.rows = 1
        self.columns = 2

        self.setGeometry(100, 100, 400, 300)
        self.setFixedWidth(200)

        self.layout = QVBoxLayout(self)

        self.label = QLabel("Joint Coordinates")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.table_widget = QTableWidget(self.rows, self.columns)
        self.table_widget.setHorizontalHeaderLabels(["X", "Y"])
        self.table_widget.setColumnWidth(1, 83)
        self.table_widget.setColumnWidth(0, 83)

        for row in range(self.rows):
            for column in range(self.columns):
                item = QTableWidgetItem(f"0")
                self.table_widget.setItem(row, column, item)

        # Button to add a new row
        self.add_row_button = QPushButton("Add Row")
        self.add_row_button.clicked.connect(self.add_row)

        # Button to delete a row
        self.delete_row_button = QPushButton("Delete Row")
        self.delete_row_button.clicked.connect(self.delete_row)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.table_widget)
        self.layout.addWidget(self.add_row_button)
        self.layout.addWidget(self.delete_row_button)

    def add_row(self, x_value="0", y_value="1"):
            self.rows += 1
            self.table_widget.setRowCount(self.rows)

            self.table_widget.blockSignals(True)
            self.table_widget.setItem(self.rows - 1, 0, QTableWidgetItem(x_value))
            self.table_widget.setItem(self.rows - 1, 1, QTableWidgetItem(y_value))
            self.table_widget.blockSignals(False)

    def delete_row(self):
        current_row = self.table_widget.currentRow()
        if current_row >= 0:
            self.table_widget.removeRow(current_row)
            self.rows -= 1
        else:
            QMessageBox.warning(self, "Warning", "No row selected to delete.")

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