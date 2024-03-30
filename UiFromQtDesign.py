import sys

from PyQt5.QtCore import QModelIndex, QPropertyAnimation, QRect, QParallelAnimationGroup
from PyQt5.QtWidgets import QApplication, QDialog, QFileSystemModel
from PyQt5 import uic

from JsonFilesFilterProxyModel import JsonFilesFilterProxyModel
from WebDavModel import WebDavModel


class MainWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi('MainUI.ui', self)
        self.model = QFileSystemModel()
        self.model.setRootPath('.')
        self.proxy_model = JsonFilesFilterProxyModel()
        self.proxy_model.setSourceModel(self.model)
        self.web_dav_model: WebDavModel = WebDavModel()
        self.tree_view.setModel(self.proxy_model)
        self.tree_view.setRootIndex(self.proxy_model.mapFromSource(self.model.index('.')))
        self._anim_group = None
        self._anim_right = None
        self._anim_left = None

        self.line_edit.textChanged.connect(self.type_file_browser)
        self.tree_view.doubleClicked.connect(self.add_file_to_queue)
        self.close_button.clicked.connect(self.close_queue_ui)
        self.list_widget.doubleClicked.connect(self.delete_select_file)

        self.queue_is_open = False
        self.temp_list_files = []

    def add_file_to_queue(self, file_index: QModelIndex):
        """Добавление файла в очередь."""
        self.list_widget.clear()

        if not self.line_edit.text().startswith('wd://'):
            current_index = self.proxy_model.mapToSource(file_index)
            file_path = self.model.filePath(current_index)
            if file_path.endswith('.json') and file_path not in self.temp_list_files:
                self.temp_list_files.append(file_path)
                if not self.queue_is_open:
                    self.start_open_animation()
                self.queue_is_open = True
        else:
            if file_index.data().endswith('.json'):
                file_path = self.lineEdit.text() + self.web_dav_model.filePath(file_index)[:-1]
                if file_path not in self.temp_list_files:
                    self.temp_list_files.append(file_path)
                if not self.queue_is_open:
                    self.start_open_animation()
                self.queue_is_open = True

        for i in self.temp_list_files:
            self.list_widget.addItem(i)

    def delete_select_file(self, file_index):
        """Удаление выделенного файла из очереди."""
        self.temp_list_files.remove(file_index.data())
        self.list_widget.clear()
        if self.temp_list_files:
            for i in self.temp_list_files:
                self.list_widget.addItem(i)
        else:
            self.close_queue_ui()

    def close_queue_ui(self):
        """Закрытие очереди."""
        self.start_open_animation(450, 700, 250, 0)
        self.list_widget.clear()
        self.temp_list_files.clear()
        self.queue_is_open = False

    def start_open_animation(self, width_fb_start=700, width_fb_end=450, width_queue_start=0, width_queue_end=250):
        """Анимированное открытие фрейма."""
        animation_duration = 100

        self._anim_left = QPropertyAnimation(self.tree_view_frame, b'geometry')
        self._anim_left.setDuration(animation_duration)
        self._anim_left.setStartValue(QRect(0, 0, width_fb_start, 433))
        self._anim_left.setEndValue(QRect(0, 0, width_fb_end, 433))

        self._anim_right = QPropertyAnimation(self.list_frame, b'geometry')
        self._anim_right.setDuration(animation_duration)
        self._anim_right.setStartValue(QRect(width_fb_start, 0, width_queue_start, 433))
        self._anim_right.setEndValue(QRect(width_fb_end, 0, width_queue_end, 433))

        self._anim_group = QParallelAnimationGroup()
        self._anim_group.addAnimation(self._anim_left)
        self._anim_group.addAnimation(self._anim_right)
        self._anim_group.start()

    def type_file_browser(self, path: str = '.'):
        """Определение и установка модели для отображения в дереве."""
        path = '.' if path == '' else path

        if path.lower().startswith('wd://'):
            self.web_dav_model.clear()
            self.web_dav_model.get_data_from_web_dav(path[4:])
            self.treeView.setModel(self.web_dav_model)
        else:
            self.treeView.setModel(self.proxy_model)
            self.treeView.setRootIndex(self.proxy_model.mapFromSource(self.model.index(path)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
