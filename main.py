import os

os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = os.path.join(
    os.path.dirname(__file__),
    "aoi_env/lib/python3.12/site-packages/PyQt5/Qt/plugins/platforms",
)
import sys
from PyQt5.QtWidgets import QApplication
from ui import AOIApp

app = QApplication(sys.argv)
window = AOIApp()
window.show()
sys.exit(app.exec_())
