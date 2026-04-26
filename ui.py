import cv2
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QImage
from core_stub import run_aoi

class AOIApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Smart AOI")
        self.setGeometry(100, 100, 1000, 600)

        self.golden_path = None
        self.test_path = None
        self.current_defect_index = 0
        self.mask = None
        self.drawing = False
        self.start_point = None
        main_layout = QVBoxLayout()

        # 🔥 Top: Image + Zoom side-by-side
        top_layout = QHBoxLayout()

        # Main image
        self.image_label = QLabel("Image View")
        self.image_label.setFixedSize(700, 400)
        self.image_label.setStyleSheet("border: 1px solid black;")
        self.image_label.mousePressEvent = lambda event: self.on_click(event)

        # Zoom panel
        self.zoom_label = QLabel("Zoom View")
        self.zoom_label.setFixedSize(300, 200)
        self.zoom_label.setStyleSheet("border: 2px solid red;")
        self.zoom_label.hide()

        top_layout.addWidget(self.image_label)
        top_layout.addWidget(self.zoom_label)

        main_layout.addLayout(top_layout)

        # 🔥 Buttons row
        btn_layout = QHBoxLayout()

        btn_golden = QPushButton("Load Golden")
        btn_test = QPushButton("Load Test")
        btn_wave = QPushButton("Wave AOI")
        btn_smart = QPushButton("Smart AOI")

        btn_golden.clicked.connect(self.load_golden)
        btn_test.clicked.connect(self.load_test)
        btn_wave.clicked.connect(self.run_wave)
        btn_smart.clicked.connect(self.run_smart)

        btn_layout.addWidget(btn_golden)
        btn_layout.addWidget(btn_test)
        btn_layout.addWidget(btn_wave)
        btn_layout.addWidget(btn_smart)

        main_layout.addLayout(btn_layout)
        btn_next = QPushButton("Next")
        btn_prev = QPushButton("Prev")

        btn_next.clicked.connect(self.next_defect)
        btn_prev.clicked.connect(self.prev_defect)

        btn_layout.addWidget(btn_prev)
        btn_layout.addWidget(btn_next)

        # 🔥 Status bar
        self.status = QLabel("Status: Load images to begin")
        main_layout.addWidget(self.status)

        self.setLayout(main_layout)

    def on_click(self, event):
        if self.mask is None:
            return

        x = event.pos().x()
        y = event.pos().y()

        display_w = 700
        display_h = 400

        h_img, w_img = self.mask.shape

        scale_x = w_img / display_w
        scale_y = h_img / display_h

        x_real = int(x * scale_x)
        y_real = int(y * scale_y)

        # Start drawing rectangle
        if event.button() == 1:  # left click
            self.start_point = (x_real, y_real)
            self.drawing = True

    def show_image(self, path):
        print("SHOW IMAGE CALLED:", path)

        pixmap = QPixmap(path)

        if pixmap.isNull():
            self.status.setText("Failed to load image")
            return

        pixmap = pixmap.scaled(800, 400, aspectRatioMode=1)

        self.image_label.setPixmap(pixmap)  # ✅ MUST be image_label
        self.image_label.setPixmap(pixmap)  # ✅ correct

    def load_golden(self):
        self.golden_path, _ = QFileDialog.getOpenFileName()

        if self.golden_path:
            self.show_image(self.golden_path)
            self.zoom_label.clear()
            self.zoom_label.hide()
            self.status.setText("Golden Loaded")
            img = cv2.imread(self.golden_path, 0)
            self.mask = np.zeros_like(img)  # black mask

    def load_test(self):
        self.test_path, _ = QFileDialog.getOpenFileName()

        if self.test_path:
            self.show_image(self.test_path)
            self.zoom_label.clear()
            self.zoom_label.hide()
            self.status.setText("Test Loaded")

    def center_window(self):
        screen = QApplication.primaryScreen().availableGeometry()
        size = self.geometry()
        self.move(
            int((screen.width() - size.width()) / 2),
            int((screen.height() - size.height()) / 2),
        )

    def run_wave(self):
        self.run_aoi(False)

    def run_smart(self):
        self.run_aoi(True)

    def next_defect(self):
        if not self.current_defects:
            return

        self.current_defect_index += 1
        self.current_defect_index %= len(self.current_defects)

        x, y, w, h = self.current_defects[self.current_defect_index]
        self.show_zoom(x, y, w, h)

    def prev_defect(self):
        if not self.current_defects:
            return

        self.current_defect_index -= 1
        self.current_defect_index %= len(self.current_defects)

        x, y, w, h = self.current_defects[self.current_defect_index]
        self.show_zoom(x, y, w, h)

    def run_aoi(self, smart):
        if not self.golden_path or not self.test_path:
            self.status.setText("⚠️ Load both Golden and Test images")
            return

        # 🔥 Run AOI (with mask)
        img, defects = run_aoi(self.golden_path, self.test_path, self.mask, smart)

        # Convert to color
        img_color = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

        # Resize FIRST
        display_w = 700
        display_h = 400

        img_display = cv2.resize(img_color, (display_w, display_h))

        h_img, w_img = img.shape[:2]

        scale_x = display_w / w_img
        scale_y = display_h / h_img

        # 🔴 DRAW ON RESIZED IMAGE (IMPORTANT)
        for x, y, w, h in defects:

            x_d = int(x * scale_x)
            y_d = int(y * scale_y)
            w_d = int(w * scale_x)
            h_d = int(h * scale_y)

            w_d = max(8, w_d)
            h_d = max(8, h_d)

            if smart:
                color = (0, 0, 255)  # RED
            else:
                color = (0, 255, 255)  # YELLOW

            cv2.rectangle(img_display, (x_d, y_d), (x_d + w_d, y_d + h_d), color, 2)
        # 🔥 Store for zoom (CRITICAL)
        self.current_img = img_color.copy()
        self.current_defects = defects
        # 🔥 Initialize defect index
        self.current_defect_index = 0

        # 🔥 Auto show first defect
        if defects:
            x, y, w, h = defects[0]
            self.show_zoom(x, y, w, h)
        else:
            self.zoom_label.hide()

        # 🔥 Encode and display
        success, buffer = cv2.imencode(".png", img_display)
        if not success:
            self.status.setText("Display error")
            return

        qt_img = QImage()
        qt_img.loadFromData(buffer.tobytes())

        pixmap = QPixmap.fromImage(qt_img)
        pixmap = pixmap.scaled(display_w, display_h, aspectRatioMode=1)

        self.image_label.setPixmap(pixmap)

        # 🔥 Update status
        self.status.setText(f"Defects: {len(defects)}")

    def show_zoom(self, x, y, w, h):
        if not hasattr(self, "current_img"):
            return

        margin = 30

        x1 = max(0, x - margin)
        y1 = max(0, y - margin)
        x2 = min(self.current_img.shape[1], x + w + margin)
        y2 = min(self.current_img.shape[0], y + h + margin)

        crop = self.current_img[y1:y2, x1:x2]

        # 🔥 zoom it
        zoom = cv2.resize(crop, None, fx=2, fy=2, interpolation=cv2.INTER_NEAREST)

        success, buffer = cv2.imencode(".png", zoom)
        if not success:
            return

        qt_img = QImage()
        qt_img.loadFromData(buffer.tobytes())

        pixmap = QPixmap.fromImage(qt_img)
        pixmap = pixmap.scaled(300, 200, aspectRatioMode=1)

        self.zoom_label.setPixmap(pixmap)
        self.zoom_label.show()

    def mouseReleaseEvent(self, event):
        if not self.drawing or self.mask is None:
            return

        x = event.pos().x()
        y = event.pos().y()

        display_w = 700
        display_h = 400

        h_img, w_img = self.mask.shape

        scale_x = w_img / display_w
        scale_y = h_img / display_h

        x2 = int(x * scale_x)
        y2 = int(y * scale_y)

        x1, y1 = self.start_point

        # 🔥 draw mask (white = ignore)
        cv2.rectangle(self.mask, (x1, y1), (x2, y2), 255, -1)

        self.drawing = False

        print("Mask added:", x1, y1, x2, y2)
