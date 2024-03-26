from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon
from PyQt5.QtWidgets import QStyle, QApplication
from webdav3.client import Client
from webdav3.exceptions import WebDavException

from conf import options


class WebDavModel(QStandardItemModel):
    def __init__(self, path, parent=None):
        super().__init__(parent)
        self.setHorizontalHeaderLabels(['Name'])
        self.parent_item = self.invisibleRootItem()

        self.client = Client(options)
        self.get_data_from_web_dav(path)

    def get_data_from_web_dav(self, remote_path=None, parent_item=None):
        if parent_item is None:
            parent_item = self.parent_item
        try:
            contents = self.client.list(remote_path)
            for row, item in enumerate(contents):
                if item.endswith('/'):
                    child_item = QStandardItem(QApplication.style().standardIcon(QStyle.SP_DirIcon), f"{item[:-1]}")
                    parent_item.appendRow(child_item)
                    new_path = remote_path + item
                    self.get_data_from_web_dav(new_path, child_item)
                elif item.endswith('.json'):
                    child_item = QStandardItem(QIcon('json.png'), f"{remote_path+item}")
                    parent_item.appendRow(child_item)

        except WebDavException as e:
            self.parent_item.appendRow(QStandardItem(f'{e}'))
