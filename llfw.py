import sys
import os
import subprocess
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QLabel, QComboBox, QProgressBar, 
                           QPushButton, QMessageBox, QTextEdit, QCheckBox, QDialog)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSettings
from PyQt5.QtGui import QPalette, QColor, QIcon, QPixmap

# Çeviriler
TRANSLATIONS = {
    'en': {
        'window_title': "LLFW",
        'warning_root': "WARNING: This application must be run with root privileges!",
        'disk_label': "Disk:",
        'format_method': "Format Method:",
        'start_button': "Start",
        'stop_button': "Stop",
        'refresh_disk_list': "Refresh Disk List",
        'about_button': "About",
        'error': "Error",
        'warning': "Warning",
        'info': "Information",
        'select_disk': "Please select a disk!",
        'root_required': "This application must be run with root privileges!",
        'careful_warning': "Please be careful!",
        'disk_warning': "Make sure you selected the correct disk!\nBecause you cannot recover your data after this operation!\n\nSelected disk: {}",
        'final_warning': "WARNING: This operation will permanently delete ALL data on the selected disk!\n\nThe operation may take a long time, please do not interfere until the operations are completely finished and you receive a completion message!\n\nAre you sure you want to continue?",
        'operation_cancelled': "Operation cancelled by user.",
        'stopping': "Stopping operation...",
        'format_complete': "Format operation completed! Please remove the disk, reinsert it and format it in the appropriate format.",
        'format_failed': "Format operation failed!",
        'about_title': "About",
        'about_content': """<h2>LLFW</h2>
            <p><b>Low-Level Formatter Wizard</p>
            <p>LLFW</b> is a tool for Linux users that performs low-level format operations on disks. Thanks to its user-friendly interface and powerful features, you can easily perform operations such as zero filling, random data writing or secure deletion.</p>
            <p><b>WARNING!</b> This tool permanently deletes all data on the selected disk and makes it unrecoverable. Please use carefully and make sure you select the correct disk before starting the operation.</p>
            <p><b>Developer:</b> ALG Software Inc.© 2024</p>
            <p>www.algyazilim.com | info@algyazilim.com</p>
            </br>
            <p>Fatih ÖNDER (CekToR) | fatih@algyazilim.com</p>
            <p><b>GitHub:</b> https://github.com/cektor</p>
            </br>
            </br>
            <p><b>ALG Software</b> Supports Migration to Pardus.</p>
            </br>
            <p><b>Version:</b> 1.0</p>
        """,
        'unmounting': "Unmounting disk: {}",
        'zero_fill_start': "Starting zero fill...",
        'random_data_start': "Writing random data...",
        'secure_erase_start': "Starting secure erase...",
        'operation_progress': "Operation in progress: {}/{} MB",
        'operation_complete': "Format operation completed!",
        'language': "Language:"
    },
    'tr': {
        'window_title': "LLFW",
        'warning_root': "UYARI: Bu uygulama root yetkileri ile çalıştırılmalıdır!",
        'disk_label': "Disk:",
        'format_method': "Format Metodu:",
        'start_button': "Başlat",
        'stop_button': "Durdur",
        'refresh_disk_list': "Disk Listesini Tazele",
        'about_button': "Hakkında",
        'error': "Hata",
        'warning': "Uyarı",
        'info': "Bilgi",
        'select_disk': "Lütfen bir disk seçin!",
        'root_required': "Bu uygulama root yetkileri ile çalıştırılmalıdır!",
        'careful_warning': "Lütfen Dikkatli Olun!",
        'disk_warning': "Doğru diski seçtinize emin olun!\nÇünkü bu işlem sonucunda verilerinizi geri getiremezsiniz!\n\nSeçilen disk: {}",
        'final_warning': "DİKKAT: Bu işlem seçili diskteki TÜM verileri kalıcı olarak silecek!\n\nİşlem uzun sürebilir,lütfen işlemler tamamen bitene ve bittiğine dair bilgi mesajı alana kadar müdehale etmeyiniz!\n\nDevam etmek istediğinizden emin misiniz?",
        'operation_cancelled': "İşlem kullanıcı tarafından iptal edildi.",
        'stopping': "İşlem durduruluyor...",
        'format_complete': "Format işlemi tamamlandı! Lütfen Diski Çıkartın,Tekrar Takın ve Uygun Formatta Biçimlendirin.",
        'format_failed': "Format işlemi başarısız oldu!",
        'about_title': "Hakkında",
        'about_content': """<h2>LLFW</h2>
            <p><b>Low-Level Formatter Wizard</p>
            <p>LLFW,</b> Linux kullanıcıları için disklere düşük seviyeli format işlemleri gerçekleştiren bir araçtır. Kullanıcı dostu arayüzü ve güçlü özellikleri sayesinde, sıfırlarla doldurma, rastgele veri yazma veya güvenli silme gibi işlemleri kolayca yapabilirsiniz.</p>
            <p><b>DİKKAT!</b> Bu araç, seçili diskteki tüm verileri kalıcı olarak siler ve geri kurtarılamaz hale gelir. Lütfen dikkatli kullanın ve işlemi başlatmadan önce doğru diski seçtiğinizden emin olun.</p>
            <p><b>Geliştirici:</b> ALG Yazılım Inc.© 2024</p>
            <p>www.algyazilim.com | info@algyazilim.com</p>
            </br>
            <p>Fatih ÖNDER (CekToR) | fatih@algyazilim.com</p>
            <p><b>GitHub:</b> https://github.com/cektor</p>
            </br>
            </br>
            <p><b>ALG Yazılım</b> Pardus'a Göç'ü Destekler.</p>
            </br>
            <p><b>Sürüm:</b> 1.0</p>
        """,
        'unmounting': "Disk bağlantısı kesiliyor: {}",
        'zero_fill_start': "Sıfırlarla doldurma başlatılıyor...",
        'random_data_start': "Rastgele veri yazılıyor...",
        'secure_erase_start': "Güvenli silme başlatılıyor...",
        'operation_progress': "İşlem devam ediyor: {}/{} MB",
        'operation_complete': "Format işlemi tamamlandı!",
        'language': "Dil:"
    }
}

def get_icon_path():
    """Simge dosyasının yolunu döndürür."""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, "llfwlo.png")
    elif os.path.exists("/usr/share/icons/hicolor/48x48/apps/llfwlo.png"):
        return "/usr/share/icons/hicolor/48x48/apps/llfwlo.png"
    return None

ICON_PATH = get_icon_path()

def get_resource_path(filename):
    """Uygun kaynak dosya yolunu döndürür."""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filename)
    
    possible_paths = [
        os.path.join(os.path.dirname(__file__), filename),
        f"/usr/share/icons/hicolor/48x48/apps/{filename}",
        os.path.expanduser(f"~/.local/share/icons/{filename}"),
        filename
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    return filename

class DarkPalette(QPalette):
    def __init__(self):
        super().__init__()
        self.setColor(QPalette.Window, QColor(53, 53, 53))
        self.setColor(QPalette.WindowText, Qt.white)
        self.setColor(QPalette.Base, QColor(35, 35, 35))
        self.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        self.setColor(QPalette.ToolTipBase, QColor(25, 25, 25))
        self.setColor(QPalette.ToolTipText, Qt.white)
        self.setColor(QPalette.Text, Qt.white)
        self.setColor(QPalette.Button, QColor(53, 53, 53))
        self.setColor(QPalette.ButtonText, Qt.white)
        self.setColor(QPalette.BrightText, Qt.red)
        self.setColor(QPalette.Link, QColor(42, 130, 218))
        self.setColor(QPalette.Highlight, QColor(42, 130, 218))
        self.setColor(QPalette.HighlightedText, QColor(35, 35, 35))

class FormatWorker(QThread):
    progress = pyqtSignal(int)
    status = pyqtSignal(str)
    finished = pyqtSignal(bool)

    def __init__(self, device, method, tr):
        super().__init__()
        self.device = device
        self.method = method
        self.is_running = True
        self.tr = tr

    def run(self):
        try:
            if not os.geteuid() == 0:
                self.status.emit(self.tr['root_required'])
                self.finished.emit(False)
                return

            self.status.emit(self.tr['unmounting'].format(self.device))
            try:
                subprocess.run(['umount', self.device], check=False)
                subprocess.run(['umount', f"{self.device}1"], check=False)
            except:
                pass

            disk_info = subprocess.check_output(['blockdev', '--getsize64', self.device])
            total_size = int(disk_info.decode().strip())
            block_size = 1024 * 1024
            total_blocks = total_size // block_size

            if self.method == "Zero Fill":
                self.status.emit(self.tr['zero_fill_start'])
                with open(self.device, 'wb') as disk:
                    for i in range(total_blocks):
                        if not self.is_running:
                            break
                        disk.write(b'\x00' * block_size)
                        self.progress.emit(int((i / total_blocks) * 100))
                        if i % 100 == 0:
                            self.status.emit(self.tr['operation_progress'].format(i, total_blocks))

            elif self.method == "Random Data":
                self.status.emit(self.tr['random_data_start'])
                for i in range(total_blocks):
                    if not self.is_running:
                        break
                    subprocess.run(['dd', 'if=/dev/urandom', f'of={self.device}',
                                 'bs=1M', 'count=1', f'seek={i}'],
                                 stdout=subprocess.DEVNULL,
                                 stderr=subprocess.DEVNULL)
                    self.progress.emit(int((i / total_blocks) * 100))
                    if i % 100 == 0:
                        self.status.emit(self.tr['operation_progress'].format(i, total_blocks))

            elif self.method == "Secure Erase":
                self.status.emit(self.tr['secure_erase_start'])
                subprocess.run(['hdparm', '--security-erase', 'NULL', self.device],
                             check=True)
                self.progress.emit(100)

            # MBR Formatlama ve FAT32 ile biçimlendirme
            self.status.emit("Formatting the disk to MBR...")
            subprocess.run(['parted', self.device, '--script', 'mklabel', 'msdos'], check=True)

            self.status.emit("Creating a FAT32 partition...")
            subprocess.run(['parted', self.device, '--script', 'mkpart', 'primary', 'fat32', '1MiB', '100%'], check=True)

            self.status.emit("Ensuring the partition is unmounted...")
            partition = self.device + "1"
            subprocess.run(['umount', partition], check=False)

            self.status.emit("Formatting partition to FAT32...")
            subprocess.run(['mkfs.fat', '-F', '32', partition], check=True)

            self.status.emit(self.tr['operation_complete'])
            self.finished.emit(True)

        except subprocess.CalledProcessError as e:
            self.status.emit(f"{self.tr['error']}: Command failed with code {e.returncode}. Command: {' '.join(e.cmd)}")
            self.finished.emit(False)

        except Exception as e:
            self.status.emit(f"{self.tr['error']}: {str(e)}")
            self.finished.emit(False)

    def stop(self):
        self.is_running = False

class AboutDialog(QDialog):
    def __init__(self, tr):
        super().__init__()
        self.tr = tr
        self.setWindowTitle(self.tr['about_title'])
        self.setFixedSize(400, 550)

        layout = QVBoxLayout()

        logo_label = QLabel(self)
        logo_path = get_resource_path("llfwlo.png")
        pixmap = QPixmap(logo_path)
        scaled_pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(scaled_pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)

        about_label = QLabel(self.tr['about_content'])
        about_label.setWordWrap(True)
        about_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        layout.addWidget(about_label)

        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # QSettings ayarlarını başlat
        self.settings = QSettings('ALG', 'LLFW')
        self.current_language = self.settings.value('language', 'tr')
        self.tr = TRANSLATIONS[self.current_language]
        
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.tr['window_title'])
        self.setMinimumSize(400, 500)
        
        # Logo yolu
        self.logo_path = get_resource_path("llfwlo.png")
        self.setWindowIcon(QIcon(self.logo_path))

        # Ana widget ve layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Dil seçimi
        lang_layout = QHBoxLayout()
        lang_label = QLabel(self.tr['language'])
        self.lang_combo = QComboBox()
        self.lang_combo = QComboBox()
        self.lang_combo.addItem("Türkçe", "tr")
        self.lang_combo.addItem("English", "en")
        
        # Mevcut dili seç
        index = self.lang_combo.findData(self.current_language)
        if index >= 0:
            self.lang_combo.setCurrentIndex(index)
            
        self.lang_combo.currentIndexChanged.connect(self.change_language)
        lang_layout.addWidget(lang_label)
        lang_layout.addWidget(self.lang_combo)
        layout.addLayout(lang_layout)

        # Root kontrol
        if not os.geteuid() == 0:
            warning_label = QLabel(self.tr['warning_root'])
            warning_label.setStyleSheet("color: red")
            layout.addWidget(warning_label)

        # Disk seçimi
        drive_layout = QHBoxLayout()
        drive_label = QLabel(self.tr['disk_label'])
        self.drive_combo = QComboBox()
        self.update_drives()
        drive_layout.addWidget(drive_label)
        drive_layout.addWidget(self.drive_combo)
        layout.addLayout(drive_layout)

        # Format metodu seçimi
        method_layout = QHBoxLayout()
        method_label = QLabel(self.tr['format_method'])
        self.method_combo = QComboBox()
        self.method_combo.addItems(["Zero Fill", "Random Data", "Secure Erase"])
        method_layout.addWidget(method_label)
        method_layout.addWidget(self.method_combo)
        layout.addLayout(method_layout)

        # İlerleme çubuğu
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        # Durum metni
        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        self.status_text.setMinimumHeight(100)
        layout.addWidget(self.status_text)

        # Butonlar
        button_layout = QHBoxLayout()
        self.start_button = QPushButton(self.tr['start_button'])
        self.start_button.clicked.connect(self.start_format)
        self.stop_button = QPushButton(self.tr['stop_button'])
        self.stop_button.clicked.connect(self.stop_format)
        self.stop_button.setEnabled(False)
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        layout.addLayout(button_layout)

        # Yenile butonu
        refresh_button = QPushButton(self.tr['refresh_disk_list'])
        refresh_button.clicked.connect(self.update_drives)
        layout.addWidget(refresh_button)

        # Hakkında butonu
        about_button = QPushButton(self.tr['about_button'])
        about_button.clicked.connect(self.show_about_dialog)
        layout.addWidget(about_button)

    def change_language(self):
        new_lang = self.lang_combo.currentData()
        if new_lang != self.current_language:
            self.current_language = new_lang
            self.settings.setValue('language', new_lang)
            
            # Kullanıcıya bilgi ver
            QMessageBox.information(self, self.tr['info'], "Dil değişikliğinin uygulanması için program yeniden başlatın.")
            
            # Programın yolunu al
            program_path = sys.argv[0]
            
            # Yönetici olarak yeniden başlat
            if sys.platform.startswith('linux'):
                subprocess.Popen(['pkexec', 'python3', program_path])
            
            # Mevcut uygulamayı kapat
            self.close()
            sys.exit(0)

    def update_ui_texts(self):
        """Tüm UI metinlerini güncelle"""
        self.setWindowTitle(self.tr['window_title'])
        self.start_button.setText(self.tr['start_button'])
        self.stop_button.setText(self.tr['stop_button'])
        self.drive_combo.setItemText(0, self.tr['disk_label'])
        self.method_combo.setItemText(0, self.tr['format_method'])
        # Diğer metinleri güncelle

    def get_disk_info(self, dev_name):
        """Disk bilgilerini al"""
        try:
            size_output = subprocess.check_output(
                ['lsblk', '-dn', '-o', 'SIZE', f'/dev/{dev_name}'],
                encoding='utf-8'
            ).strip()

            blkid_output = subprocess.check_output(
                ['blkid', f'/dev/{dev_name}'],
                encoding='utf-8',
                stderr=subprocess.DEVNULL
            ).strip()

            label = None
            if 'LABEL=' in blkid_output:
                label = blkid_output.split('LABEL="')[1].split('"')[0]

            return size_output, label
        except:
            return None, None

    def update_drives(self):
        self.drive_combo.clear()
        try:
            output = subprocess.check_output(
                ['lsblk', '-d', '-n', '-o', 'NAME,TYPE'],
                encoding='utf-8'
            )
            
            for line in output.strip().split('\n'):
                parts = line.split()
                if len(parts) >= 2 and parts[1] == "disk":
                    dev_name = parts[0]
                    size, label = self.get_disk_info(dev_name)
                    
                    if size:
                        display_text = f"/dev/{dev_name} [{size}]"
                        if label:
                            display_text += f" - {label}"
                        self.drive_combo.addItem(display_text)
        except Exception as e:
            self.add_status(f"{self.tr['error']}: {str(e)}")

    def add_status(self, message):
        self.status_text.append(message)

    def show_about_dialog(self):
        dialog = AboutDialog(self.tr)
        dialog.exec_()

    def start_format(self):
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.drive_combo.setEnabled(False)
        self.method_combo.setEnabled(False)
        
        if not os.geteuid() == 0:
            QMessageBox.critical(self, self.tr['error'], self.tr['root_required'])
            return

        if not self.drive_combo.currentText():
            QMessageBox.warning(self, self.tr['warning'], self.tr['select_disk'])
            return

        selected_disk = self.drive_combo.currentText()
        
        reply1 = QMessageBox.warning(
            self,
            self.tr['careful_warning'],
            self.tr['disk_warning'].format(selected_disk),
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply1 == QMessageBox.No:
            self.add_status(self.tr['operation_cancelled'])
            return

        reply2 = QMessageBox.warning(
            self,
            self.tr['warning'],
            self.tr['final_warning'],
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply2 == QMessageBox.Yes:
            device = self.drive_combo.currentText().split()[0]
            method = self.method_combo.currentText()

            self.worker = FormatWorker(device, method, self.tr)
            self.worker.progress.connect(self.progress_bar.setValue)
            self.worker.status.connect(self.add_status)
            self.worker.finished.connect(self.format_finished)

            self.worker.start()
        else:
            self.add_status(self.tr['operation_cancelled'])
            self.format_finished(False)

    def stop_format(self):
        if hasattr(self, 'worker'):
            self.worker.stop()
            self.add_status(self.tr['stopping'])

    def format_finished(self, success):
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.drive_combo.setEnabled(True)
        self.method_combo.setEnabled(True)
        self.progress_bar.setValue(0)
        
        if success:
            QMessageBox.information(self, self.tr['info'], self.tr['format_complete'])
        else:
            QMessageBox.critical(self, self.tr['error'], self.tr['format_failed'])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    if ICON_PATH:
        app.setWindowIcon(QIcon(ICON_PATH))
    app.setPalette(DarkPalette())
    app.setStyle("Fusion")
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())