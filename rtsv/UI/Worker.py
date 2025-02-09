import numpy as np
from PySide6.QtCore import QThread, Signal

from rtsv.Processing.ScoutProcessing import ScoutProcessing


class SignalReader(QThread):
    """
    Поток для чтения новых файлов из директории.
    """
    new_data = Signal(np.ndarray)

    def __init__(self, dir_path):
        self.c = None
        self.k = None
        self.old_filenames = None
        self.new_filenames = None
        self.dir_path = dir_path
        self.running = True
        super().__init__()

    def run(self):
        self.c = 1

        self.k = 0
        self.old_filenames = ScoutProcessing.get_filenames(self.dir_path, 3)

        while self.running:
            try:
                self.new_filenames = ScoutProcessing.get_filenames(self.dir_path, 3)
                if self.new_filenames != self.old_filenames:
                    self.old_filenames = self.new_filenames
                    self.k = 1
                    self.c += 1
                else:
                    self.k = 0
                if self.k == 1:
                    scout_list = ScoutProcessing.get_scout_list(self.old_filenames)
                    data = ScoutProcessing.get_data(scout_list)
                    self.new_data.emit(data)
                  # Отправляем данные в основной поток

            except Exception as e:
                print(f"Ошибка при чтении файлов: {e}")

    def stop(self):
        self.running = False
        self.wait()
