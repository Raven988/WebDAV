"""Окно открытия отчета."""

import os
import subprocess  # noqa: S404
import sys

from WebDavModel import WebDavModel

from PyQt5.QtCore import QProcess, QTimer, QUrl, QDir
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout, \
    QApplication, QTreeView, QBoxLayout, QWidget, QLayout, QLayoutItem, QLineEdit, QFileSystemModel, QAbstractItemView


def to_layout(layout_cls, widgets: list, spacing: int = 10, parent=None):
    """Размещение виджетов в лейаут."""
    layout = layout_cls(parent)
    if not isinstance(layout, QBoxLayout):
        raise ValueError('Неподдерживаемый лейаут')
    layout.setSpacing(spacing)
    layout.setContentsMargins(0, 0, 0, 0)
    for wgt in widgets:
        if isinstance(wgt, QWidget):
            layout.addWidget(wgt)
        elif isinstance(wgt, QLayout):
            layout.addLayout(wgt)
        elif isinstance(wgt, QLayoutItem):
            layout.addItem(wgt)
        else:
            raise ValueError
    return layout


class UiReportDialog:
    """Интерфейс."""

    def __init__(self, parent):
        """Инициализация."""
        self.title = QLabel(parent)
        self.title.setWordWrap(True)

        self.open_file_btn = QPushButton('Открыть', parent)
        self.open_dir_btn = QPushButton('Показать в папке', parent)
        self.line_edit = QLineEdit()
        self.tree_view = QTreeView()
        self.tree_view.setSortingEnabled(True)
        self.tree_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.type_file_browser()

        self.btn_layout = to_layout(
            layout_cls=QHBoxLayout,
            widgets=[
                QSpacerItem(120, 0, hPolicy=QSizePolicy.Expanding),
                self.open_file_btn,
                self.open_dir_btn,
            ],
        )

        self.main_layout = to_layout(
            layout_cls=QVBoxLayout,
            spacing=25,
            widgets=[
                self.line_edit,
                self.tree_view,
                self.btn_layout,
            ],
        )
        self.main_layout.setContentsMargins(16, 15, 16, 10)
        parent.setLayout(self.main_layout)

        self.line_edit.textChanged.connect(self.type_file_browser)

    def type_file_browser(self, path: str = ''):
        if path.lower().startswith('wd://'):
            model = WebDavModel(path[4:])
            self.tree_view.setModel(model)
        else:
            model = QFileSystemModel()
            model.setRootPath((QDir.rootPath()))
            self.tree_view.setModel(model)
            self.tree_view.setRootIndex(model.index(path))


class ReportDialog(QDialog):
    """Виджет."""

    def __init__(self, parent=None):
        """Инициализация."""
        super().__init__(parent)
        self.target_file = None

        self.setWindowTitle('Результат')
        self.ui = UiReportDialog(self)

        self.ui.open_file_btn.clicked.connect(self.open_file)
        self.ui.open_dir_btn.clicked.connect(self.open_dir)

        self.ui.open_file_btn.clicked.connect(self._on_button_clicked)
        self.ui.open_dir_btn.clicked.connect(self._on_button_clicked)

    def update_ui(self, title, target_file):
        """Установить описание."""
        self.ui.title.setText(title)
        self.target_file = target_file

    def open_file(self) -> bool:
        """Открыть файл в приложении по умолчанию."""
        return QDesktopServices.openUrl(QUrl.fromLocalFile(self.target_file))

    def open_dir(self):
        """Открыть файл в файловом менеджере с выделением."""
        self._select(self.target_file)

    def _on_button_clicked(self):
        """Временная блокировка кнопок."""
        self.setEnabled(False)
        self.timer = QTimer()
        self.timer.singleShot(1500, lambda: self.setEnabled(True))

    def _select(self, path):
        # https://stackoverflow.com/a/9138437
        if os.name == 'nt':
            explorer = 'explorer'
            script_args = []
            if not os.path.isdir(path):
                script_args.append('/select,')
            script_args.append(os.path.normpath(path))
            QProcess.startDetached(explorer, script_args)
        elif os.name == 'posix':
            subprocess.run(
                f'xdg-open $(dirname {path})',
                shell=True,  # noqa: S602
            )


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = ReportDialog()
    win.show()
    app.exec_()
