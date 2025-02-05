import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel, QListWidgetItem, QWidget, QGridLayout, QGraphicsScene, QGraphicsView, QVBoxLayout
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QPixmap, QFont

# Import pages
from main_ui import Ui_MainWindow
from home_page import HomePage
from draw_page import DrawPage
from settings_page import SettingsPage


class CustomScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.placing_joints = False
        self.joints = []

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.placing_joints:
            scene_pos = event.scenePos()
            self.add_joint(scene_pos.x(), scene_pos.y())

    def add_joint(self, x, y):
        joint = self.addEllipse(x - 5, y - 5, 10, 10)  # Adjust the position to center the ellipse
        joint.setBrush(Qt.blue)
        self.joints.append((x, y))  # Store the joint position


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize the UI from the generated 'main_ui' class
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Set window properties
        self.setWindowIcon(QIcon("img/Logo.png"))
        self.setWindowTitle("Planar Mechanism Simulator")

        # Initialize UI elements
        self.title_label = self.ui.title_label
        self.title_label.setText("Sidebar Menu")

        self.title_icon = self.ui.title_icon
        self.title_icon.setText("")
        self.title_icon.setPixmap(QPixmap("img/Logo.png"))
        self.title_icon.setScaledContents(True)

        self.side_menu = self.ui.listWidget
        self.side_menu.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.side_menu_icon_only = self.ui.listWidget_icon_only
        self.side_menu_icon_only.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.side_menu_icon_only.hide()

        self.menu_btn = self.ui.menu_btn
        self.menu_btn.setText("")
        self.menu_btn.setIcon(QIcon("img/sidebar-left.svg"))
        self.menu_btn.setIconSize(QSize(30, 30))
        self.menu_btn.setCheckable(True)
        self.menu_btn.setChecked(False)

        self.main_content = self.ui.stackedWidget

        # Create a drawing area
        self.drawing_area = QGraphicsView()
        self.drawing_scene = CustomScene(self)
        self.drawing_area.setScene(self.drawing_scene)
        self.drawing_area.setFixedSize(400, 400)  # Set a fixed size for the drawing area

        # Define a list of menu items with names and icons
        self.menu_list = [
            {
                "name": "Home",
                "icon": "img/home.svg"
            },
            {
                "name": "Draw Joints",
                "icon": "img/draw.svg"
            },
            {
                "name": "Settings",
                "icon": "img/settings.svg"
            }
        ]

        # Initialize the UI elements and slots
        self.init_list_widget()
        self.init_stackwidget()
        self.init_single_slot()

    def init_single_slot(self):
        # Connect signals and slots for menu button and side menu
        self.menu_btn.toggled['bool'].connect(self.side_menu.setHidden)
        self.menu_btn.toggled['bool'].connect(self.title_label.setHidden)
        self.menu_btn.toggled['bool'].connect(self.side_menu_icon_only.setVisible)
        self.menu_btn.toggled['bool'].connect(self.title_icon.setHidden)

        # Connect signals and slots for switching between menu items
        self.side_menu.currentRowChanged['int'].connect(self.main_content.setCurrentIndex)
        self.side_menu_icon_only.currentRowChanged['int'].connect(self.main_content.setCurrentIndex)
        self.side_menu.currentRowChanged['int'].connect(self.side_menu_icon_only.setCurrentRow)
        self.side_menu_icon_only.currentRowChanged['int'].connect(self.side_menu.setCurrentRow)
        self.menu_btn.toggled.connect(self.button_icon_change)

    def init_list_widget(self):
        # Initialize the side menu and side menu with icons only
        self.side_menu_icon_only.clear()
        self.side_menu.clear()

        for menu in self.menu_list:
            # Set items for the side menu with icons only
            item = QListWidgetItem()
            item.setIcon(QIcon(menu.get("icon")))
            item.setSizeHint(QSize(40, 40))
            self.side_menu_icon_only.addItem(item)
            self.side_menu_icon_only.setCurrentRow(0)

            # Set items for the side menu with icons and text
            item_new = QListWidgetItem()
            item_new.setIcon(QIcon(menu.get("icon")))
            item_new.setText(menu.get("name"))
            self.side_menu.addItem(item_new)
            self.side_menu.setCurrentRow(0)

    def init_stackwidget(self):
        # Clear existing widgets
        widget_list = self.main_content.findChildren(QWidget)
        for widget in widget_list:
            self.main_content.removeWidget(widget)

        # Create instances of each page
        home_page = HomePage()
        draw_page = DrawPage()
        settings_page = SettingsPage()

        # Add pages to the stacked widget
        self.main_content.addWidget(home_page)
        self.main_content.addWidget(draw_page)
        self.main_content.addWidget(settings_page)

    def button_icon_change(self, status):
        # Change the menu button icon based on its status
        if status:
            self.menu_btn.setIcon(QIcon("img/sidebar-right.svg"))
        else:
            self.menu_btn.setIcon(QIcon("img/sidebar-left.svg"))


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Load style file
    with open("style.qss") as f:
        style_str = f.read()

    app.setStyleSheet(style_str)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())