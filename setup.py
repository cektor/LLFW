from setuptools import setup, find_packages

setup(
    name="llfw",  # Paket adı
    version="1.0",  # Paket sürümü
    description="Low-Level Formatter Wizard",  # Paket açıklaması
    author="Fatih Önder",  # Paket sahibi adı
    author_email="fatih@algyazilim.com",  # Paket sahibi e-posta adresi
    url="https://github.com/cektor/LLFW",  # Paket deposu URL'si
    packages=find_packages(),  # Otomatik olarak tüm alt paketleri bulur
    install_requires=[
        'PyQt5',  # PyQt5 bağımlılığı (versiyon sınırı belirtilmiş)
    ],
    package_data={
        'llfw': ['*.png', '*.desktop'],  # 'llfw' paketine dahil dosyalar
    },
    data_files=[
        ('share/applications', ['llfw.desktop']),  # Uygulama menüsüne .desktop dosyasını ekler
        ('share/icons/hicolor/48x48/apps', ['llfwlo.png']),  # Simgeyi uygun yere ekler
    ],
    entry_points={
        'gui_scripts': [
            'llfw=llfw:main',  # `llfw` modülündeki `main` fonksiyonu çalıştırılır
        ]
    },
)

