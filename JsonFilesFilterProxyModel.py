from typing import Optional

from PyQt5.QtCore import QSortFilterProxyModel
from PyQt5.QtWidgets import QFileSystemModel


class JsonFilesFilterProxyModel(QSortFilterProxyModel):
    def filterAcceptsRow(self, source_row, source_parent):
        source_model: Optional[QFileSystemModel] = self.sourceModel()
        index = source_model.index(source_row, 0, source_parent)

        if index.isValid() and index.model().hasChildren(index):
            return True

        filename = source_model.fileName(index)
        if filename.endswith('.json'):
            return True

        return False
