from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QComboBox, QPushButton, QFileDialog
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QThread
from PyQt5.QtGui import QFont
from src.pages.build_box import BuildLogBox
from src.functions.build_manager import BuildManager
import threading


class BuildThread(QThread):
    """Thread separada para não travar a GUI durante o build"""
    log_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(bool, str)
    
    def __init__(self, compress, webhook_url, selected_payloads, file_name, file_type, file_icon_path):
        super().__init__()
        self.compress = compress
        self.webhook_url = webhook_url
        self.selected_payloads = selected_payloads
        self.file_name = file_name
        self.file_type = file_type
        self.file_icon_path = file_icon_path
    
    def log(self, msg):
        """Envia log para a GUI de forma segura"""
        self.log_signal.emit(msg)
    
    def run(self):
        """Executa o build em background"""
        try:
            success = BuildManager.buildFinal(
                compress=self.compress,
                webhook_url=self.webhook_url,
                selected_payloads=self.selected_payloads,
                file_name=self.file_name,
                file_type=self.file_type,
                file_icon_path=self.file_icon_path,
                log=self.log
            )
            
            if success:
                self.finished_signal.emit(True, "Build completed successfully!")
            else:
                self.finished_signal.emit(False, "Build failed!")
                
        except Exception as e:
            self.log(f"\n✗ ERROR:\n{str(e)}")
            self.finished_signal.emit(False, f"Build error: {str(e)}")


class BuilderPage(QWidget):
    def __init__(self, options_page):
        super().__init__()
        self.options_page = options_page
        self.selected_icon = None
        self.build_thread = None
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(30)
        
        title = QLabel("Build Configuration")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setStyleSheet("color: #ff4444;")
        
        form_layout = QVBoxLayout()
        form_layout.setSpacing(25)
        
        filename_layout = QVBoxLayout()
        filename_layout.setSpacing(8)
        filename_label = QLabel("File Name:")
        filename_label.setStyleSheet("font-weight: bold; font-size: 13px;")
        self.filename_input = QLineEdit()
        self.filename_input.setPlaceholderText("Enter file name...")
        self.filename_input.setMinimumHeight(40)
        filename_layout.addWidget(filename_label)
        filename_layout.addWidget(self.filename_input)
        
        filetype_layout = QVBoxLayout()
        filetype_layout.setSpacing(8)
        filetype_label = QLabel("File Type:")
        filetype_label.setStyleSheet("font-weight: bold; font-size: 13px;")
        self.filetype_combo = QComboBox()
        self.filetype_combo.addItems([".exe", ".py", ".pyw"])
        self.filetype_combo.setMinimumHeight(40)
        self.filetype_combo.currentTextChanged.connect(self.on_filetype_changed)
        filetype_layout.addWidget(filetype_label)
        filetype_layout.addWidget(self.filetype_combo)
        
        icon_layout = QVBoxLayout()
        icon_layout.setSpacing(8)
        self.icon_label = QLabel("Exe Icon (Optional):")
        self.icon_label.setStyleSheet("font-weight: bold; font-size: 13px;")
        self.icon_button = QPushButton("Select Icon")
        self.icon_button.setObjectName("iconButton")
        self.icon_button.setMinimumHeight(40)
        self.icon_button.clicked.connect(self.select_icon)
        self.icon_path_label = QLabel("No icon selected")
        self.icon_path_label.setStyleSheet("color: #888; font-size: 12px; font-style: italic;")
        icon_layout.addWidget(self.icon_label)
        icon_layout.addWidget(self.icon_button)
        icon_layout.addWidget(self.icon_path_label)
        
        form_layout.addLayout(filename_layout)
        form_layout.addLayout(filetype_layout)
        form_layout.addLayout(icon_layout)
        form_layout.addStretch()
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        self.build_button = QPushButton("Start Build")
        
        self.build_button.setObjectName("buildButton")
        self.build_button.setMinimumSize(200, 50)
        self.build_button.clicked.connect(self.start_build)
        button_layout.addWidget(self.build_button)
        button_layout.addStretch()
        
        main_layout.addWidget(title)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)
        
        self.on_filetype_changed(self.filetype_combo.currentText())

    def on_filetype_changed(self, file_type):
        is_exe = file_type == ".exe"
        self.icon_label.setEnabled(is_exe)
        self.icon_button.setEnabled(is_exe)
        self.icon_path_label.setEnabled(is_exe)
        
        if not is_exe:
            self.selected_icon = None
            self.icon_path_label.setText("Icon only available for .exe files")
            self.icon_path_label.setStyleSheet("color: #666; font-size: 12px; font-style: italic;")
        else:
            if not self.selected_icon:
                self.icon_path_label.setText("No icon selected")
                self.icon_path_label.setStyleSheet("color: #888; font-size: 12px; font-style: italic;")

    def select_icon(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Select Icon", 
            "icons", 
            "Icon Files (*.ico);;All Files (*)"
        )
        
        if file_path:
            self.selected_icon = file_path
            self.icon_path_label.setText(f"Selected: {file_path}")
            self.icon_path_label.setStyleSheet("color: #00aa44; font-size: 12px;")

    def start_build(self):
        # Validações
        filename = self.filename_input.text().strip()
        if not filename:
            return
            
        filetype = self.filetype_combo.currentText()
        icon = self.selected_icon
        selected = self.options_page.get_selected_options()
        webhook = self.options_page.webhook_input.text().strip()

        # Cria janela de log
        self.build_window = BuildLogBox(self)
        self.build_window.show()

        # Log inicial
        self.build_window.add_log("Starting build...")
        self.build_window.add_log(f"Webhook: {webhook}")
        self.build_window.add_log(f"File: {filename}{filetype}")
        self.build_window.add_log(f"Payloads: {selected}")
        self.build_window.add_log("")

        full_path = f"output/{filename}"

        # Cria e configura thread de build
        self.build_thread = BuildThread(
            compress=True,
            webhook_url=webhook,
            selected_payloads=selected.copy(),
            file_name=full_path,
            file_type=filetype.replace(".", ""),
            file_icon_path=icon
        )

        # Conecta sinais
        self.build_thread.log_signal.connect(self.build_window.add_log)
        self.build_thread.finished_signal.connect(self.on_build_finished)

        # Desabilita botão durante build
        self.build_button.setEnabled(False)
        self.build_button.setText("Building...")

        # Inicia thread
        self.build_thread.start()

    def on_build_finished(self, success, message):
        """Chamado quando o build termina"""
        self.build_window.add_log("")
        self.build_window.add_log(message)
        self.build_window.finish()
        
        # Reabilita botão
        self.build_button.setEnabled(True)
        self.build_button.setText("Start Build")
        
        # Limpa thread
        self.build_thread = None