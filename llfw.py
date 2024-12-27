import sys
import os
import subprocess
import time
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QLabel, QComboBox, QProgressBar, 
                           QPushButton, QMessageBox, QTextEdit, QCheckBox, QDialog,
                           QTabWidget, QRadioButton, QSpinBox, QScrollArea)
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
        'language': "Language:",
        'settings_tab': "Settings",
        'language_settings': "Language Settings",
        'theme_settings': "Theme Settings",
        'dark_theme': "Dark Theme",
        'light_theme': "Light Theme",
        'theme_restart': "Theme changes will take effect after restart.",
        'llf_tab': "Low Level Format",
        'disk_format_tab': "Disk Format",
        'about_tab': "About",
        'format_type_label': "Format Type:",
        'format_button': "Format",
        'refresh_button': "Refresh Disk List",
        'format_success': "Format completed successfully!",
        'format_warning': "This will format {} with {}. All data will be lost!\n\nContinue?",
        'partition_title': "Partitioning",
        'partition_count': "Number of Partitions:",
        'partition_size': "Partition {} Size (GB):",
        'format_type': "Format Type:",
        'security_settings': "Security Settings",
        'confirm_operations': "Ask for confirmation before operations",
        'detailed_logging': "Keep detailed logs",
        'format_settings': "Format Settings",
        'default_format_type': "Default Format Type:",
        'performance_settings': "Performance Settings",
        'operation_speed': "Operation Speed:",
        'speed_normal': "Normal",
        'speed_fast': "Fast",
        'speed_very_fast': "Very Fast",
        'auto_refresh': "Auto refresh disk list",
        'advanced_settings': "Advanced Settings",
        'partition_alignment': "Partition Alignment (MiB):",
        'advanced_mode': "Advanced mode (show additional options)",
        'disk_not_found': "Disk not found: {}",
        'disk_in_use': "Disk is in use: {}",
        'disk_size_error': "Could not get disk size: {}",
        'invalid_partition_count': "Invalid partition count!",
        'partition_settings_missing': "Partition settings are missing!",
        'partition_create_error': "Could not create partition {}!",
        'partition_format_error': "Could not format partition {}! Command: {}",
        'total_size_error': "Total partition size ({} GB) cannot be larger than disk size ({} GB)!",
        'format_type_update_error': "Error updating format type: {}",
        'partition_not_ready': "Partition is not ready: {}",
        'command_timeout': "Command timed out: {}",
        'command_error': "Command error: {}",
        'unexpected_error': "Unexpected error: {}",
        'view_logs': "View Logs",
        'log_dir_error': "Could not open log directory: {}"
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
        'language': "Dil:",
        'settings_tab': "Seçenekler",
        'language_settings': "Dil Ayarları",
        'theme_settings': "Tema Ayarları",
        'dark_theme': "Koyu Tema",
        'light_theme': "Açık Tema",
        'theme_restart': "Tema değişiklikleri yeniden başlatma sonrası etkin olacak.",
        'llf_tab': "Düşük Seviye Format",
        'disk_format_tab': "Disk Biçimlendir",
        'about_tab': "Hakkında",
        'format_type_label': "Format Tipi:",
        'format_button': "Biçimlendir",
        'refresh_button': "Disk Listesini Yenile",
        'format_success': "Biçimlendirme başarıyla tamamlandı!",
        'format_warning': "{} diski {} olarak biçimlendirilecek. Tüm veriler silinecek!\n\nDevam edilsin mi?",
        'partition_title': "Bölümlendirme",
        'partition_count': "Bölüm Sayısı:",
        'partition_size': "Bölüm {} Boyutu (GB):",
        'format_type': "Format Tipi:",
        'security_settings': "Güvenlik Ayarları",
        'confirm_operations': "İşlemler için onay iste",
        'detailed_logging': "Detaylı log kayıtları tut",
        'format_settings': "Format Ayarları",
        'default_format_type': "Varsayılan Format Tipi:",
        'performance_settings': "Performans Ayarları",
        'operation_speed': "İşlem Hızı:",
        'speed_normal': "Normal",
        'speed_fast': "Hızlı",
        'speed_very_fast': "Çok Hızlı",
        'auto_refresh': "Disk listesini otomatik yenile",
        'advanced_settings': "Gelişmiş Ayarlar",
        'partition_alignment': "Bölüm Hizalama (MiB):",
        'advanced_mode': "Gelişmiş mod (ek seçenekleri göster)",
        'disk_not_found': "Disk bulunamadı: {}",
        'disk_in_use': "Disk kullanımda: {}",
        'disk_size_error': "Disk boyutu alınamadı: {}",
        'invalid_partition_count': "Geçersiz bölüm sayısı!",
        'partition_settings_missing': "Bölüm ayarları eksik!",
        'partition_create_error': "Bölüm {} oluşturulamadı!",
        'partition_format_error': "Bölüm {} formatlanamadı! Komut: {}",
        'total_size_error': "Toplam bölüm boyutu ({} GB) disk boyutundan ({} GB) büyük olamaz!",
        'format_type_update_error': "Format tipi güncellenirken hata: {}",
        'partition_not_ready': "Bölüm hazır değil: {}",
        'command_timeout': "Komut zaman aşımına uğradı: {}",
        'command_error': "Komut hatası: {}",
        'unexpected_error': "Beklenmeyen hata: {}",
        'view_logs': "Logları Görüntüle",
        'log_dir_error': "Log dizini açılamadı: {}"
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

            self.status.emit(self.tr['operation_complete'])
            self.finished.emit(True)

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
        self.current_theme = self.settings.value('theme', 'dark')
        self.tr = TRANSLATIONS[self.current_language]
        
        # Temayı uygula
        self.apply_theme()
        
        self.init_ui()

    def apply_theme(self):
        """Seçili temayı uygula"""
        if self.current_theme == 'dark':
            app.setPalette(DarkPalette())
        else:
            app.setPalette(app.style().standardPalette())

    def init_ui(self):
        self.setWindowTitle(self.tr['window_title'])
        self.setMinimumSize(600, 500)
        
        # Logo yolu
        self.logo_path = get_resource_path("llfwlo.png")
        self.setWindowIcon(QIcon(self.logo_path))

        # Ana widget ve layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Tab widget oluştur
        tab_widget = QTabWidget()
        
        # Tab 1: LLF İşlemi
        llf_tab = QWidget()
        llf_layout = QVBoxLayout(llf_tab)
        
        # Root kontrol
        if not os.geteuid() == 0:
            warning_label = QLabel(self.tr['warning_root'])
            warning_label.setStyleSheet("color: red")
            llf_layout.addWidget(warning_label)

        # Disk seçimi
        drive_layout = QHBoxLayout()
        drive_label = QLabel(self.tr['disk_label'])
        self.drive_combo = QComboBox()
        self.update_drives()
        drive_layout.addWidget(drive_label)
        drive_layout.addWidget(self.drive_combo)
        llf_layout.addLayout(drive_layout)

        # Format metodu seçimi
        method_layout = QHBoxLayout()
        method_label = QLabel(self.tr['format_method'])
        self.method_combo = QComboBox()
        self.method_combo.addItems(["Zero Fill", "Random Data", "Secure Erase"])
        method_layout.addWidget(method_label)
        method_layout.addWidget(self.method_combo)
        llf_layout.addLayout(method_layout)

        # İlerleme çubuğu
        self.progress_bar = QProgressBar()
        llf_layout.addWidget(self.progress_bar)

        # Durum metni
        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        self.status_text.setMinimumHeight(100)
        llf_layout.addWidget(self.status_text)

        # Butonlar
        button_layout = QHBoxLayout()
        self.start_button = QPushButton(self.tr['start_button'])
        self.start_button.clicked.connect(self.start_format)
        self.stop_button = QPushButton(self.tr['stop_button'])
        self.stop_button.clicked.connect(self.stop_format)
        self.stop_button.setEnabled(False)
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        llf_layout.addLayout(button_layout)

        # Yenile butonu
        refresh_button = QPushButton(self.tr['refresh_disk_list'])
        refresh_button.clicked.connect(self.update_drives)
        llf_layout.addWidget(refresh_button)

        # Tab 2: Disk Biçimlendirme
        format_tab = QWidget()
        format_layout = QVBoxLayout(format_tab)
        
        # Disk seçimi
        format_drive_layout = QHBoxLayout()
        format_drive_label = QLabel(self.tr['disk_label'])
        self.format_drive_combo = QComboBox()
        self.update_format_drives()
        format_drive_layout.addWidget(format_drive_label)
        format_drive_layout.addWidget(self.format_drive_combo)
        format_layout.addLayout(format_drive_layout)

        # Format tipi seçimi
        format_type_layout = QHBoxLayout()
        format_type_label = QLabel(self.tr['format_type_label'])
        self.format_type_combo = QComboBox()
        self.format_type_combo.addItems(["NTFS", "FAT32", "FAT", "exFAT", "ext4"])
        # Format tipi değiştiğinde bölümleri güncelle
        self.format_type_combo.currentTextChanged.connect(self.update_partition_formats)
        format_type_layout.addWidget(format_type_label)
        format_type_layout.addWidget(self.format_type_combo)
        format_layout.addLayout(format_type_layout)

        # Bölümlendirme seçenekleri
        partition_group = QWidget()
        partition_layout = QVBoxLayout(partition_group)

        # Bölümlendirme başlığı
        partition_title = QLabel(self.tr['partition_title'])
        partition_title.setStyleSheet("font-weight: bold; font-size: 14px;")
        partition_layout.addWidget(partition_title)

        # Bölüm sayısı seçimi
        partition_count_layout = QHBoxLayout()
        partition_count_label = QLabel(self.tr['partition_count'])
        self.partition_count_combo = QComboBox()
        self.partition_count_combo.addItems(["1", "2", "3", "4"])
        self.partition_count_combo.currentIndexChanged.connect(self.update_partition_inputs)
        partition_count_layout.addWidget(partition_count_label)
        partition_count_layout.addWidget(self.partition_count_combo)
        partition_layout.addLayout(partition_count_layout)

        # Bölüm boyutları için container
        self.partition_sizes_widget = QWidget()
        self.partition_sizes_layout = QVBoxLayout(self.partition_sizes_widget)
        partition_layout.addWidget(self.partition_sizes_widget)

        format_layout.addWidget(partition_group)
        
        # İlk bölüm giriş alanlarını oluştur
        self.update_partition_inputs()
        
        # Format ilerleme çubuğu
        self.format_progress_bar = QProgressBar()
        format_layout.addWidget(self.format_progress_bar)

        # Format butonları
        format_button_layout = QHBoxLayout()
        self.format_button = QPushButton(self.tr['format_button'])
        self.format_button.clicked.connect(self.start_disk_format)
        self.format_refresh_button = QPushButton(self.tr['refresh_button'])
        self.format_refresh_button.clicked.connect(self.update_format_drives)
        format_button_layout.addWidget(self.format_button)
        format_button_layout.addWidget(self.format_refresh_button)
        format_layout.addLayout(format_button_layout)

        format_layout.addStretch()

        # Tab 3: Seçenekler
        settings_tab = QWidget()
        settings_layout = QVBoxLayout(settings_tab)

        # Scroll Area ekle
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # İçerik widget'ı
        settings_content = QWidget()
        settings_content_layout = QVBoxLayout(settings_content)
        
        # Dil Ayarları Grubu
        lang_group = QWidget()
        lang_layout = QVBoxLayout(lang_group)
        
        lang_title = QLabel(self.tr['language_settings'])
        lang_title.setStyleSheet("font-weight: bold; font-size: 14px;")
        lang_layout.addWidget(lang_title)
        
        lang_select_layout = QHBoxLayout()
        lang_label = QLabel(self.tr['language'])
        self.lang_combo = QComboBox()
        self.lang_combo.addItem("Türkçe", "tr")
        self.lang_combo.addItem("English", "en")
        
        index = self.lang_combo.findData(self.current_language)
        if index >= 0:
            self.lang_combo.setCurrentIndex(index)
        
        self.lang_combo.currentIndexChanged.connect(self.change_language)
        lang_select_layout.addWidget(lang_label)
        lang_select_layout.addWidget(self.lang_combo)
        lang_layout.addLayout(lang_select_layout)
        
        settings_content_layout.addWidget(lang_group)
        
        # Tema Ayarları Grubu
        theme_group = QWidget()
        theme_layout = QVBoxLayout(theme_group)
        
        theme_title = QLabel(self.tr['theme_settings'])
        theme_title.setStyleSheet("font-weight: bold; font-size: 14px;")
        theme_layout.addWidget(theme_title)
        
        self.dark_theme_radio = QRadioButton(self.tr['dark_theme'])
        self.light_theme_radio = QRadioButton(self.tr['light_theme'])
        
        # Mevcut tema seçimini işaretle
        if self.current_theme == 'dark':
            self.dark_theme_radio.setChecked(True)
        else:
            self.light_theme_radio.setChecked(True)
        
        self.dark_theme_radio.toggled.connect(self.change_theme)
        theme_layout.addWidget(self.dark_theme_radio)
        theme_layout.addWidget(self.light_theme_radio)
        
        settings_content_layout.addWidget(theme_group)
        
        # Güvenlik Ayarları
        security_group = QWidget()
        security_layout = QVBoxLayout(security_group)
        
        security_title = QLabel(self.tr['security_settings'])
        security_title.setStyleSheet("font-weight: bold; font-size: 14px;")
        security_layout.addWidget(security_title)
        
        # İşlem onayı
        self.confirm_operations = QCheckBox(self.tr['confirm_operations'])
        self.confirm_operations.setChecked(self.settings.value('confirm_operations', True, bool))
        self.confirm_operations.stateChanged.connect(
            lambda state: self.settings.setValue('confirm_operations', bool(state))
        )
        security_layout.addWidget(self.confirm_operations)
        
        # Detaylı log tutma ve log görüntüleme için yatay düzen
        log_layout = QHBoxLayout()
        
        # Detaylı log tutma
        self.detailed_logging = QCheckBox(self.tr['detailed_logging'])
        self.detailed_logging.setChecked(self.settings.value('detailed_logging', False, bool))
        self.detailed_logging.stateChanged.connect(
            lambda state: self.settings.setValue('detailed_logging', bool(state))
        )
        log_layout.addWidget(self.detailed_logging)
        
        # Log görüntüleme butonu
        self.view_logs_button = QPushButton(self.tr['view_logs'])
        self.view_logs_button.clicked.connect(self.view_logs)
        log_layout.addWidget(self.view_logs_button)
        
        security_layout.addLayout(log_layout)
        
        settings_content_layout.addWidget(security_group)
        
        # Format Ayarları
        format_settings_group = QWidget()
        format_settings_layout = QVBoxLayout(format_settings_group)
        
        format_settings_title = QLabel(self.tr['format_settings'])
        format_settings_title.setStyleSheet("font-weight: bold; font-size: 14px;")
        format_settings_layout.addWidget(format_settings_title)
        
        # Varsayılan format tipi
        default_format_layout = QHBoxLayout()
        default_format_label = QLabel(self.tr['default_format_type'])
        self.default_format_combo = QComboBox()
        self.default_format_combo.addItems(["NTFS", "FAT32", "FAT", "exFAT", "ext4"])
        current_default = self.settings.value('default_format', "NTFS")
        index = self.default_format_combo.findText(current_default)
        if index >= 0:
            self.default_format_combo.setCurrentIndex(index)
        self.default_format_combo.currentTextChanged.connect(
            lambda text: self.settings.setValue('default_format', text)
        )
        default_format_layout.addWidget(default_format_label)
        default_format_layout.addWidget(self.default_format_combo)
        format_settings_layout.addLayout(default_format_layout)
        
        settings_content_layout.addWidget(format_settings_group)
        
        # Performans Ayarları
        performance_group = QWidget()
        performance_layout = QVBoxLayout(performance_group)
        
        performance_title = QLabel(self.tr['performance_settings'])
        performance_title.setStyleSheet("font-weight: bold; font-size: 14px;")
        performance_layout.addWidget(performance_title)
        
        # İşlem hızı
        speed_layout = QHBoxLayout()
        speed_label = QLabel(self.tr['operation_speed'])
        self.speed_combo = QComboBox()
        self.speed_combo.addItems([
            self.tr['speed_normal'],
            self.tr['speed_fast'],
            self.tr['speed_very_fast']
        ])
        current_speed = self.settings.value('operation_speed', "Normal")
        index = self.speed_combo.findText(current_speed)
        if index >= 0:
            self.speed_combo.setCurrentIndex(index)
        self.speed_combo.currentTextChanged.connect(
            lambda text: self.settings.setValue('operation_speed', text)
        )
        speed_layout.addWidget(speed_label)
        speed_layout.addWidget(self.speed_combo)
        performance_layout.addLayout(speed_layout)
        
        # Otomatik yenileme
        self.auto_refresh = QCheckBox(self.tr['auto_refresh'])
        self.auto_refresh.setChecked(self.settings.value('auto_refresh', True, bool))
        self.auto_refresh.stateChanged.connect(
            lambda state: self.settings.setValue('auto_refresh', bool(state))
        )
        performance_layout.addWidget(self.auto_refresh)
        
        settings_content_layout.addWidget(performance_group)
        
        # Gelişmiş Ayarlar
        advanced_group = QWidget()
        advanced_layout = QVBoxLayout(advanced_group)
        
        advanced_title = QLabel(self.tr['advanced_settings'])
        advanced_title.setStyleSheet("font-weight: bold; font-size: 14px;")
        advanced_layout.addWidget(advanced_title)
        
        # Bölüm hizalama
        alignment_layout = QHBoxLayout()
        alignment_label = QLabel(self.tr['partition_alignment'])
        self.alignment_spin = QSpinBox()
        self.alignment_spin.setRange(1, 4096)
        self.alignment_spin.setValue(self.settings.value('partition_alignment', 1, int))
        self.alignment_spin.valueChanged.connect(
            lambda value: self.settings.setValue('partition_alignment', value)
        )
        alignment_layout.addWidget(alignment_label)
        alignment_layout.addWidget(self.alignment_spin)
        advanced_layout.addLayout(alignment_layout)
        
        # Gelişmiş mod
        self.advanced_mode = QCheckBox(self.tr['advanced_mode'])
        self.advanced_mode.setChecked(self.settings.value('advanced_mode', False, bool))
        self.advanced_mode.stateChanged.connect(
            lambda state: self.settings.setValue('advanced_mode', bool(state))
        )
        advanced_layout.addWidget(self.advanced_mode)
        
        settings_content_layout.addWidget(advanced_group)
        
        # Boşluk ekle
        settings_content_layout.addStretch()
        
        # Scroll Area'ya içerik widget'ını ekle
        scroll.setWidget(settings_content)
        
        # Ana layout'a Scroll Area'yı ekle
        settings_layout.addWidget(scroll)

        # Tab 4: Hakkında
        about_tab = QWidget()
        about_layout = QVBoxLayout(about_tab)

        logo_label = QLabel()
        logo_path = get_resource_path("llfwlo.png")
        pixmap = QPixmap(logo_path)
        scaled_pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(scaled_pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        about_layout.addWidget(logo_label)

        about_label = QLabel(self.tr['about_content'])
        about_label.setWordWrap(True)
        about_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        about_layout.addWidget(about_label)

        # Tabları ekle
        tab_widget.addTab(llf_tab, self.tr['llf_tab'])
        tab_widget.addTab(format_tab, self.tr['disk_format_tab'])
        tab_widget.addTab(settings_tab, self.tr['settings_tab'])
        tab_widget.addTab(about_tab, self.tr['about_tab'])
        
        layout.addWidget(tab_widget)

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

    def safe_run_command(self, command, check=True, timeout=30):
        """Komutları güvenli bir şekilde çalıştır"""
        try:
            result = subprocess.run(
                command,
                check=check,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                encoding='utf-8',
                timeout=timeout
            )
            return result
        except subprocess.TimeoutExpired:
            QMessageBox.critical(self, self.tr['error'], f"Komut zaman aşımına uğradı: {' '.join(command)}")
            return None
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, self.tr['error'], f"Komut hatası: {str(e)}")
            return None
        except Exception as e:
            QMessageBox.critical(self, self.tr['error'], f"Beklenmeyen hata: {str(e)}")
            return None

    def get_disk_info(self, dev_name):
        """Disk bilgilerini güvenli bir şekilde al"""
        try:
            # Disk varlığını kontrol et
            if not os.path.exists(f"/dev/{dev_name}"):
                return None, None, None, None

            # Disk boyutunu al
            size_cmd = self.safe_run_command(['lsblk', '-dn', '-o', 'SIZE', f'/dev/{dev_name}'])
            size_output = size_cmd.stdout.strip() if size_cmd else None

            # Disk modelini al
            model_cmd = self.safe_run_command(['lsblk', '-dn', '-o', 'MODEL', f'/dev/{dev_name}'])
            model_output = model_cmd.stdout.strip() if model_cmd else None

            # Disk tipini al
            type_cmd = self.safe_run_command(['lsblk', '-dn', '-o', 'TYPE', f'/dev/{dev_name}'])
            type_output = type_cmd.stdout.strip() if type_cmd else None

            # Disk etiketini al
            try:
                blkid_cmd = self.safe_run_command(['blkid', f'/dev/{dev_name}'], check=False)
                label = None
                if blkid_cmd and 'LABEL=' in blkid_cmd.stdout:
                    label = blkid_cmd.stdout.split('LABEL="')[1].split('"')[0]
            except:
                label = None

            return size_output, model_output, type_output, label
        except Exception as e:
            print(f"Disk bilgisi alınırken hata: {str(e)}")
            return None, None, None, None

    def update_drives(self):
        """İlk sekmedeki disk listesini güncelle"""
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
                    size, model, type_, label = self.get_disk_info(dev_name)
                    
                    if size:
                        display_text = f"/dev/{dev_name}"
                        if model:
                            display_text += f" [{model}]"
                        display_text += f" {size}"
                        if label:
                            display_text += f" - {label}"
                        
                        # LLF durumunu kontrol et
                        try:
                            parted_output = subprocess.check_output(
                                ['parted', '-s', f'/dev/{dev_name}', 'print'],
                                stderr=subprocess.DEVNULL,
                                encoding='utf-8'
                            )
                            if "unrecognised disk label" in parted_output.lower():
                                display_text += " [LLF Yapılmış]"
                        except:
                            display_text += " [LLF Yapılmış]"
                        
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

    def update_format_drives(self):
        """İkinci sekmedeki disk listesini güncelle"""
        self.format_drive_combo.clear()
        try:
            # Tüm diskleri ve bölümleri listele
            output = subprocess.check_output(
                ['lsblk', '-n', '-o', 'NAME,TYPE'],
                encoding='utf-8'
            )
            
            for line in output.strip().split('\n'):
                parts = line.split()
                if len(parts) >= 2:
                    dev_name = parts[0]
                    dev_type = parts[1]
                    
                    # Sadece disk ve loop cihazlarını göster
                    if dev_type in ['disk', 'loop']:
                        size, model, type_, label = self.get_disk_info(dev_name)
                        
                        if size:
                            display_text = f"/dev/{dev_name}"
                            if model:
                                display_text += f" [{model}]"
                            display_text += f" {size}"
                            if label:
                                display_text += f" - {label}"
                            
                            # LLF yapılmış diskleri belirt
                            try:
                                # Disk bölüm tablosunu kontrol et
                                parted_output = subprocess.check_output(
                                    ['parted', '-s', f'/dev/{dev_name}', 'print'],
                                    stderr=subprocess.DEVNULL,
                                    encoding='utf-8'
                                )
                                if "unrecognised disk label" in parted_output.lower():
                                    display_text += " [LLF Yapılmış]"
                            except:
                                display_text += " [LLF Yapılmış]"
                            
                            self.format_drive_combo.addItem(display_text)
        except Exception as e:
            QMessageBox.critical(self, self.tr['error'], str(e))

    def start_disk_format(self):
        """Seçili diski bölümlendir ve formatla"""
        if not self.format_drive_combo.currentText():
            QMessageBox.warning(self, self.tr['warning'], self.tr['select_disk'])
            return

        device = self.format_drive_combo.currentText().split()[0]

        reply = QMessageBox.warning(
            self,
            self.tr['warning'],
            f"Disk {device} bölümlendirilecek ve formatlanacak. Tüm veriler silinecek!\n\nDevam edilsin mi?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            try:
                # Diski bağlı değilse ayır
                subprocess.run(['umount', device], check=False)
                
                self.format_progress_bar.setValue(10)
                
                # Bölümlendirme ve formatlama işlemini başlat
                if self.create_partitions(device):
                    self.format_progress_bar.setValue(100)
                    QMessageBox.information(self, self.tr['info'], self.tr['format_success'])
                
            except Exception as e:
                QMessageBox.critical(self, self.tr['error'], f"{self.tr['error']}: {str(e)}")
            finally:
                self.format_progress_bar.setValue(0)

    def change_theme(self):
        """Tema değişikliğini kaydet"""
        new_theme = 'dark' if self.dark_theme_radio.isChecked() else 'light'
        if new_theme != self.current_theme:
            self.current_theme = new_theme
            self.settings.setValue('theme', new_theme)
            QMessageBox.information(self, self.tr['info'], self.tr['theme_restart'])

    def update_partition_inputs(self):
        """Seçilen bölüm sayısına göre boyut giriş alanlarını güncelle"""
        # Mevcut giriş alanlarını temizle
        for i in reversed(range(self.partition_sizes_layout.count())): 
            self.partition_sizes_layout.itemAt(i).widget().setParent(None)
        
        count = int(self.partition_count_combo.currentText())
        # Seçili format tipini al
        selected_format = self.format_type_combo.currentText()
        
        for i in range(count):
            row_layout = QHBoxLayout()
            
            label = QLabel(f"Bölüm {i+1} Boyutu (GB):")
            size_input = QSpinBox()
            size_input.setMinimum(1)
            size_input.setMaximum(2000)
            size_input.setValue(20)
            
            format_label = QLabel("Format:")
            format_combo = QComboBox()
            format_combo.addItems(["NTFS", "FAT32", "FAT", "exFAT", "ext4"])
            # Seçili format tipini ayarla
            index = format_combo.findText(selected_format)
            if index >= 0:
                format_combo.setCurrentIndex(index)
            
            row_layout.addWidget(label)
            row_layout.addWidget(size_input)
            row_layout.addWidget(format_label)
            row_layout.addWidget(format_combo)
            
            container = QWidget()
            container.setLayout(row_layout)
            self.partition_sizes_layout.addWidget(container)

    def create_partitions(self, device):
        """Diski bölümlendir ve formatla"""
        try:
            if not os.path.exists(device):
                QMessageBox.critical(self, self.tr['error'], 
                    self.tr['disk_not_found'].format(device))
                return False

            # Diskin kullanımda olup olmadığını kontrol et
            mount_check = self.safe_run_command(['lsof', device], check=False)
            if mount_check and mount_check.returncode == 0:
                QMessageBox.critical(self, self.tr['error'], 
                    self.tr['disk_in_use'].format(device))
                return False

            self.safe_run_command(['umount', device], check=False)
            
            # GPT tablosu oluştur
            if not self.safe_run_command(['parted', '-s', device, 'mklabel', 'gpt']):
                return False
            # Disk boyutunu al
            try:
                disk_cmd = self.safe_run_command(['blockdev', '--getsize64', device])
                if not disk_cmd:
                    return False
                total_disk_size = int(disk_cmd.stdout.strip()) // (1024 * 1024 * 1024)
            except Exception as e:
                QMessageBox.critical(self, self.tr['error'], f"Disk boyutu alınamadı: {str(e)}")
                return False
            # Bölüm sayısını kontrol et
            count = int(self.partition_count_combo.currentText())
            if count < 1 or count > 4:
                QMessageBox.critical(self, self.tr['error'], "Geçersiz bölüm sayısı!")
                return False
            # Widget kontrolü
            if not self.partition_sizes_layout or self.partition_sizes_layout.count() < count:
                QMessageBox.critical(self, self.tr['error'], "Bölüm ayarları eksik!")
                return False
            start = 1
            total_size = 0
            created_partitions = []
            # Bölümleri oluştur
            for i in range(count):
                try:
                    # Widget kontrolü
                    container = self.partition_sizes_layout.itemAt(i)
                    if not container or not container.widget():
                        raise ValueError(f"Bölüm {i+1} ayarları bulunamadı!")
                    row_layout = container.widget().layout()
                    if not row_layout:
                        raise ValueError(f"Bölüm {i+1} düzeni bulunamadı!")
                    size_input = row_layout.itemAt(1).widget()
                    format_combo = row_layout.itemAt(3).widget()
                    if not size_input or not format_combo:
                        raise ValueError(f"Bölüm {i+1} için gerekli alanlar bulunamadı!")
                    size = int(size_input.value())
                    format_type = format_combo.currentText().lower()
                    # Boyut kontrolü
                    if size < 1:
                        raise ValueError(f"Bölüm {i+1} için geçersiz boyut!")
                    # Son bölüm için kalan alan
                    if i == count - 1:
                        end = -1
                    else:
                        end = start + (size * 1024)
                        total_size += size
                        if total_size > total_disk_size:
                            raise ValueError(
                                f"Toplam bölüm boyutu ({total_size}GB) "
                                f"disk boyutundan ({total_disk_size}GB) büyük!"
                            )
                    # Bölüm oluştur
                    parted_cmd = ['parted', '-s', device, 'mkpart', 'primary']
                    if end == -1:
                        parted_cmd.extend([f'{start}MiB', '100%'])
                    else:
                        parted_cmd.extend([f'{start}MiB', f'{end}MiB'])
                    if not self.safe_run_command(parted_cmd):
                        raise ValueError(f"Bölüm {i+1} oluşturulamadı!")
                    # Bölümün oluşmasını bekle
                    partition_name = f"{device}{i+1}"
                    created_partitions.append(partition_name)
                    max_retries = 20
                    for _ in range(max_retries):
                        if os.path.exists(partition_name):
                            break
                        time.sleep(0.5)
                    else:
                        raise ValueError(f"Bölüm oluşturulamadı: {partition_name}")
                    # Formatlama
                    format_cmd = None
                    max_format_retries = 3  # Maksimum deneme sayısı
                    
                    # Bölümün hazır olması için biraz bekle
                    time.sleep(2)
                    
                    # Bölümü formatlamadan önce tekrar unmount et
                    self.safe_run_command(['umount', partition_name], check=False)
                    
                    for retry in range(max_format_retries):
                        try:
                            if format_type == "ntfs":
                                format_cmd = ['mkfs.ntfs', '-f', '-Q', partition_name]
                            elif format_type == "fat32":
                                # FAT32 için özel kontroller
                                size_mb = size * 1024  # GB'dan MB'a çevir
                                if size_mb > 32 * 1024:  # 32GB'dan büyükse
                                    format_cmd = ['mkfs.vfat', '-F', '32', '-S', '4096', partition_name]
                                else:
                                    format_cmd = ['mkfs.vfat', '-F', '32', partition_name]
                            elif format_type == "fat":
                                format_cmd = ['mkfs.vfat', '-F', '16', partition_name]
                            elif format_type == "exfat":
                                format_cmd = ['mkfs.exfat', partition_name]
                            elif format_type == "ext4":
                                format_cmd = ['mkfs.ext4', '-F', partition_name]

                            if format_cmd:
                                # Formatlamadan önce partition'ın hazır olduğundan emin ol
                                if not os.path.exists(partition_name):
                                    time.sleep(1)
                                    continue
                                    
                                # Formatlama işlemini çalıştır
                                result = self.safe_run_command(format_cmd, timeout=120)  # Timeout süresini artır
                                if result and result.returncode == 0:
                                    break  # Başarılı ise döngüden çık
                                else:
                                    if retry < max_format_retries - 1:  # Son deneme değilse
                                        time.sleep(2)  # Bir sonraki denemeden önce bekle
                                        continue
                                    else:
                                        raise ValueError(f"Bölüm {i+1} formatlanamadı! Komut: {' '.join(format_cmd)}")
                        except Exception as e:
                            if retry < max_format_retries - 1:  # Son deneme değilse
                                time.sleep(2)  # Bir sonraki denemeden önce bekle
                                continue
                            else:
                                raise ValueError(f"Bölüm {i+1} formatlanırken hata: {str(e)}")
                    start = end if end != -1 else start
                    self.format_progress_bar.setValue(int((i + 1) * 100 / count))
                except Exception as e:
                    # Hata durumunda oluşturulan bölümleri temizle
                    self.clean_up_partitions(device, created_partitions)
                    QMessageBox.critical(self, self.tr['error'], str(e))
                    return False
            return True
        except Exception as e:
            QMessageBox.critical(self, self.tr['error'], f"Bölümlendirme hatası: {str(e)}")
            return False
    def clean_up_partitions(self, device, partitions):
        """Hata durumunda oluşturulan bölümleri temizle"""
        try:
            # Bölümleri ayır
            for partition in partitions:
                self.safe_run_command(['umount', partition], check=False)

            # Disk bölüm tablosunu temizle
            self.safe_run_command(['parted', '-s', device, 'mklabel', 'gpt'], check=False)
        except:
            pass
    def update_partition_formats(self, selected_format):
        """Tüm bölümlerin format tipini güncelle"""
        try:
            # Mevcut bölüm sayısını al
            count = self.partition_sizes_layout.count()
            
            # Her bölümün format combobox'ını güncelle
            for i in range(count):
                container = self.partition_sizes_layout.itemAt(i)
                if container and container.widget():
                    row_layout = container.widget().layout()
                    if row_layout:
                        format_combo = row_layout.itemAt(3).widget()
                        if format_combo and isinstance(format_combo, QComboBox):
                            # Seçili format tipini bul ve ayarla
                            index = format_combo.findText(selected_format)
                            if index >= 0:
                                format_combo.setCurrentIndex(index)
        except Exception as e:
            QMessageBox.critical(self, self.tr['error'], f"Format tipi güncellenirken hata: {str(e)}")
    def view_logs(self):
        """Log dosyalarını görüntüle"""
        try:
            # Log dizinini oluştur
            log_dir = os.path.expanduser("~/.local/share/llfw/logs")
            os.makedirs(log_dir, exist_ok=True)
            
            # Platformlar arası uyumluluk için
            if sys.platform.startswith('linux'):
                subprocess.Popen(['xdg-open', log_dir])
            else:
                os.startfile(log_dir)
        except Exception as e:
            QMessageBox.critical(self, self.tr['error'], 
                               self.tr['log_dir_error'].format(str(e)))
if __name__ == '__main__':
    app = QApplication(sys.argv)
    if ICON_PATH:
        app.setWindowIcon(QIcon(ICON_PATH))
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())