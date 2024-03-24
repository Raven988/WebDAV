import os

from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon
from webdav3.client import Client
from webdav3 import exceptions

from conf import options


class WebDavModel(QStandardItemModel):
    def __init__(self, path, parent=None):
        super().__init__(parent)
        self.setHorizontalHeaderLabels(['Name', 'Type'])
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
                    child_item = QStandardItem(QIcon("icon3.png"), f"{item[:-1]}")
                    parent_item.appendRow(child_item)
                    parent_item.setChild(row, 1, QStandardItem('dir'))
                    if item.endswith('/') and remote_path.endswith('/'):
                        path = remote_path + item
                    else:
                        path = remote_path + '/' + item
                    self.get_data_from_web_dav(path, child_item)
                else:
                    child_item = QStandardItem(f"{item}")
                    parent_item.appendRow(child_item)
                    file_type = os.path.splitext(remote_path + item)[1][1:] + ' file'
                    parent_item.setChild(row, 1, QStandardItem(file_type))

        except exceptions.ResponseErrorCode as e:
            self.parent_item.appendRow(QStandardItem(f'{e.code} {e.message}'))

        except exceptions.ConnectionException as e:
            self.parent_item.appendRow(QStandardItem(f'{e.exception}'))

        except exceptions.NoConnection as e:
            self.parent_item.appendRow(QStandardItem(f'{e}'))

        except exceptions.RemoteResourceNotFound as e:
            self.parent_item.appendRow(QStandardItem(f'{e}'))
