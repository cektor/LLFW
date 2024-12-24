import sys
import os
import subprocess
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QLabel, QComboBox, QProgressBar, 
                           QPushButton, QMessageBox, QTextEdit, QCheckBox, QDialog, QVBoxLayout)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QPalette, QColor, QIcon, QPixmap

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
        # PyInstaller ile paketlendiğinde
        return os.path.join(sys._MEIPASS, filename)
    
    # Farklı olası konumlar
    possible_paths = [
        os.path.join(os.path.dirname(__file__), filename),
        f"/usr/share/icons/hicolor/48x48/apps/{filename}",
        os.path.expanduser(f"~/.local/share/icons/{filename}"),
        filename
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    return filename  # Son çare olarak orijinal dosya adını döndür


class FormatWorker(QThread):
    progress = pyqtSignal(int)
    status = pyqtSignal(str)
    finished = pyqtSignal(bool)

    def __init__(self, device, method):
        super().__init__()
        self.device = device
        self.method = method
        self.is_running = True


    def run(self):
        try:
            if not os.geteuid() == 0:
                self.status.emit("Hata: Bu işlem için root yetkileri gerekli!")
                self.finished.emit(False)
                return

            # Diski unmount et
            self.status.emit(f"Disk bağlantısı kesiliyor: {self.device}")
            try:
                subprocess.run(['umount', self.device], check=False)
            except:
                pass

            # Disk boyutunu al
            disk_info = subprocess.check_output(['blockdev', '--getsize64', self.device])
            total_size = int(disk_info.decode().strip())
            block_size = 1024 * 1024  # 1MB bloklar
            total_blocks = total_size // block_size

            if self.method == "Zero Fill":
                self.status.emit("Sıfırlarla doldurma başlatılıyor...")
                with open(self.device, 'wb') as disk:
                    for i in range(total_blocks):
                        if not self.is_running:
                            break
                        disk.write(b'\x00' * block_size)
                        self.progress.emit(int((i / total_blocks) * 100))
                        if i % 100 == 0:
                            self.status.emit(f"İşlem devam ediyor: {i}/{total_blocks} MB")

            elif self.method == "Random Data":
                self.status.emit("Rastgele veri yazılıyor...")
                for i in range(total_blocks):
                    if not self.is_running:
                        break
                    subprocess.run(['dd', 'if=/dev/urandom', f'of={self.device}',
                                 'bs=1M', 'count=1', f'seek={i}'],
                                 stdout=subprocess.DEVNULL,
                                 stderr=subprocess.DEVNULL)
                    self.progress.emit(int((i / total_blocks) * 100))
                    if i % 100 == 0:
                        self.status.emit(f"İşlem devam ediyor: {i}/{total_blocks} MB")

            elif self.method == "Secure Erase":
                self.status.emit("Güvenli silme başlatılıyor...")
                subprocess.run(['hdparm', '--security-erase', 'NULL', self.device],
                             check=True)
                self.progress.emit(100)

            self.status.emit("Format işlemi tamamlandı!")
            self.finished.emit(True)

        except Exception as e:
            self.status.emit(f"Hata: {str(e)}")
            self.finished.emit(False)

    def stop(self):
        self.is_running = False

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

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LLFW")
        self.setMinimumSize(400, 500)
        
                        # Logo yolu
        self.logo_path = get_resource_path("llfwlo.png")

                                # Ana layout

        # Ana widget ve layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        self.setWindowIcon(QIcon(self.logo_path))
        
      

        # Root kontrol
        if not os.geteuid() == 0:
            warning_label = QLabel("UYARI: Bu uygulama root yetkileri ile çalıştırılmalıdır!")
            warning_label.setStyleSheet("color: red")
            layout.addWidget(warning_label)
        

        

        # Disk seçimi
        drive_layout = QHBoxLayout()
        drive_label = QLabel("Disk:")
        self.drive_combo = QComboBox()
        self.update_drives()
        drive_layout.addWidget(drive_label)
        drive_layout.addWidget(self.drive_combo)
        layout.addLayout(drive_layout)

        # Format metodu seçimi
        method_layout = QHBoxLayout()
        method_label = QLabel("Format Metodu:")
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
        self.start_button = QPushButton("Başlat")
        self.start_button.clicked.connect(self.start_format)
        self.stop_button = QPushButton("Durdur")
        self.stop_button.clicked.connect(self.stop_format)
        self.stop_button.setEnabled(False)
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        layout.addLayout(button_layout)

    
        # Yenile butonu
        refresh_button = QPushButton("Disk Listesini Tazele")
        refresh_button.clicked.connect(self.update_drives)
        layout.addWidget(refresh_button)
        
        
                # Hakkında butonu - Ana layouta ekle
        about_button = QPushButton("Hakkında")
        about_button.clicked.connect(self.show_about_dialog)
        layout.addWidget(about_button)

    def get_disk_info(self, dev_name):
        """Disk bilgilerini al"""
        try:
            # Disk boyutunu al
            size_output = subprocess.check_output(
                ['lsblk', '-dn', '-o', 'SIZE', f'/dev/{dev_name}'],
                encoding='utf-8'
            ).strip()

            # Disk etiketini al
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
            # Sadece fiziksel diskleri listele
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
                        # Disk gösterim metni
                        display_text = f"/dev/{dev_name} [{size}]"
                        if label:
                            display_text += f" - {label}"
                            
                        self.drive_combo.addItem(display_text)
                        
        except Exception as e:
            self.add_status(f"Disk listesi alınamadı: {str(e)}")

    def add_status(self, message):
        self.status_text.append(message)
        
        
    def show_about_dialog(self):
        dialog = AboutDialog()
        dialog.exec_()      

    def start_format(self):
                # Başlat butonuna basıldığında
        self.start_button.setEnabled(False)  # Başlat butonu pasif
        self.stop_button.setEnabled(True)   # Durdur butonu aktif
        self.drive_combo.setEnabled(False)
        self.method_combo.setEnabled(False)
        if not os.geteuid() == 0:
            QMessageBox.critical(self, "Hata", "Bu uygulama root yetkileri ile çalıştırılmalıdır!")
            return

        if not self.drive_combo.currentText():
            QMessageBox.warning(self, "Uyarı", "Lütfen bir disk seçin!")
            return

        selected_disk = self.drive_combo.currentText()
        
        # İlk onay mesajı
        reply1 = QMessageBox.warning(
            self,
            "Lütfen Dikkatli Olun!",
            f"Doğru diski seçtinize emin olun!\n"
            f"Çünkü bu işlem sonucunda verilerinizi geri getiremezsiniz!\n\n"
            f"Seçilen disk: {selected_disk}\n\n",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply1 == QMessageBox.No:
            self.add_status("İşlem kullanıcı tarafından iptal edildi.")
            return

        # İkinci onay mesajı
        reply2 = QMessageBox.warning(
            self,
            "Son Onay",
            "DİKKAT: Bu işlem seçili diskteki TÜM verileri kalıcı olarak silecek!\n\n"
            "İşlem uzun sürebilir,lütfen işlemler tamamen bitene ve bittiğine dair bilgi mesajı alana kadar müdehale etmeyiniz!\n\n"
            "Devam etmek istediğinizden emin misiniz?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply2 == QMessageBox.Yes:
            device = self.drive_combo.currentText().split()[0]
            method = self.method_combo.currentText()

            self.worker = FormatWorker(device, method)
            self.worker.progress.connect(self.progress_bar.setValue)
            self.worker.status.connect(self.add_status)
            self.worker.finished.connect(self.format_finished)

            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            self.drive_combo.setEnabled(False)
            self.method_combo.setEnabled(False)

            self.worker.start()
        else:
            self.add_status("İşlem kullanıcı tarafından iptal edildi.")

    def stop_format(self):
            # Durdur butonuna basıldığında
        self.start_button.setEnabled(True)  # Başlat butonu aktif
        self.stop_button.setEnabled(False)  # Durdur butonu pasif
        if self.worker:
            self.worker.stop()
            self.add_status("İşlem durduruluyor...")

    def format_finished(self, success):
        # Format işlemi tamamlandığında
        self.start_button.setEnabled(True)  # Başlat butonu aktif
        self.stop_button.setEnabled(False)  # Durdur butonu pasif
        self.drive_combo.setEnabled(True)
        self.method_combo.setEnabled(True)
            # İlerleme çubuğunu sıfırla
        self.progress_bar.setValue(0)
        if success:
            QMessageBox.information(self, "Bilgi", "Format işlemi tamamlandı! Lütfen Diski Çıkartın,Tekrar Takın ve Uygun Formatta Biçimlendirin.")
        else:
            QMessageBox.critical(self, "Hata", "Format işlemi başarısız oldu!")
            
 
         
class AboutDialog(QDialog):
    def __init__(self):
        super().__init__()
        
        # Dialog başlığı
        self.setWindowTitle("Hakkında")
        self.setFixedSize(400, 550)

        # Layout
        layout = QVBoxLayout()

        # Logo ekleme
        logo_label = QLabel(self)
        logo_path = get_resource_path("llfwlo.png")
        pixmap = QPixmap(logo_path)
        scaled_pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(scaled_pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)

        # Uygulama hakkında bilgi
        about_label = QLabel("""<h2>LLFW</h2>
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
        """)
        about_label.setWordWrap(True)  # WordWrap özelliği eklendi
        about_label.setTextInteractionFlags(Qt.TextSelectableByMouse) # yazılar seçilebilir olsun
        layout.addWidget(about_label)   

        # Layout'u dialog'a ayarla
        self.setLayout(layout)                  
            
            

if __name__ == '__main__':
    app = QApplication(sys.argv)
    if ICON_PATH:
        app.setWindowIcon(QIcon(ICON_PATH))
    # Koyu tema uygula
    app.setPalette(DarkPalette())
    app.setStyle("Fusion")
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
