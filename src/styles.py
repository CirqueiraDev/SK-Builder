control_btn_style = """
    QPushButton {
        text-align: center;
        background-color: transparent;
        color: #999;
        border: none;
        font-size: 11px;
        font-weight: bold;
        padding: 0px;
        min-width: 45px;
        max-width: 45px;
        min-height: 35px;
        max-height: 35px;
    }
    QPushButton:hover {
        background-color: #1a1a1a;
        color: #fff;
    }
"""

close_btn_style = """
    QPushButton {
        text-align: center;
        background-color: transparent;
        color: #999;
        border: none;
        font-size: 11px;
        font-weight: bold;
        padding: 0px;
        min-width: 45px;
        max-width: 45px;
        min-height: 35px;
        max-height: 35px;
    }
    QPushButton:hover {
        background-color: #ff4444;
        color: #fff;
    }
"""

webhook_group_style = """
    QGroupBox {
        font-size: 14px;
        font-weight: bold;
        color: #ff4444;
        border: 1px solid #2a2a2a;
        border-radius: 6px;
        margin-top: 10px;
        padding-top: 15px;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 5px;
    }
"""

SCROLL_STYLE = """
    QScrollArea {
        border: none;
    }

    QScrollBar:vertical {
        background: #181818;
        width: 8px;
        margin: 0px;
        border-radius: 4px;
    }

    QScrollBar::handle:vertical {
        background: #ff4444;
        min-height: 25px;
        border-radius: 4px;
    }

    QScrollBar::handle:vertical:hover {
        background: #ff6666;
    }

    QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
        width: 0;
        height: 0;
        background: none;
        border: none;
    }
    
    QScrollBar::sub-line:vertical, QScrollBar::add-line:vertical {
        height: 0px;
        background: none;
        border: none;
    }

    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
        background: none;
    }
"""

TOPBAR_STYLE = """
    QFrame {
        background-color: #0a0a0a; 
        border-bottom: 1px solid #1a1a1a;
    }
"""

SIDEBAR_STYLE = """
    background-color: #0f0f0f; 
    border-right: 1px solid #1a1a1a;
"""

MAIN_STYLE = """
    QWidget {
        background-color: #0a0a0a;
        color: #e0e0e0;
        font-family: 'Segoe UI';
    }
    QPushButton {
        background-color: transparent;
        border: none;
        color: #bbb;
        font-size: 14px;
        padding: 12px 16px;
        text-align: left;
        border-radius: 4px;
    }
    QPushButton:hover {
        background-color: #1a1a1a;
        color: #ff4444;
    }
    QPushButton#active {
        background-color: #1a1a1a;
        color: #ff4444;
        border-left: 3px solid #ff4444;
    }
    QLabel {
        font-size: 14px;
    }
    QCheckBox {
        color: #e0e0e0;
        font-size: 13px;
        spacing: 8px;
    }
    QCheckBox::indicator {
        width: 18px;
        height: 18px;
        border: 2px solid #ff4444;
        border-radius: 3px;
        background-color: transparent;
    }
    QCheckBox::indicator:checked {
        background-color: #ff4444;
        border: 2px solid #ff4444;
    }
    QCheckBox::indicator:hover {
        border: 2px solid #ff6666;
    }
    QLineEdit {
        background-color: #1a1a1a;
        border: 1px solid #2a2a2a;
        border-radius: 4px;
        padding: 8px;
        color: #e0e0e0;
        font-size: 13px;
    }
    QLineEdit:focus {
        border: 1px solid #ff4444;
    }
    QComboBox {
        background-color: #1a1a1a;
        border: 1px solid #2a2a2a;
        border-radius: 4px;
        padding: 8px;
        color: #e0e0e0;
        font-size: 13px;
    }
    QComboBox:hover {
        border: 1px solid #ff4444;
    }
    QComboBox::drop-down {
        border: none;
        padding-right: 8px;
    }
    QComboBox::down-arrow {
        image: none;
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-top: 5px solid #ff4444;
    }
    QComboBox QAbstractItemView {
        background-color: #1a1a1a;
        border: 1px solid #2a2a2a;
        selection-background-color: #ff4444;
        color: #e0e0e0;
    }
    QPushButton#buildButton {
        text-align: center;
        background-color: #ff4444;
        color: white;
        font-size: 14px;
        font-weight: bold;
        padding: 12px 24px;
        border-radius: 6px;
    }
    QPushButton#buildButton:hover {
    
        background-color: #ff6666;
    }
    QPushButton#buildButton:pressed {
        background-color: #cc3333;
    }
    QPushButton#iconButton {
        background-color: #1a1a1a;
        border: 1px solid #2a2a2a;
        color: #bbb;
        padding: 8px;
        border-radius: 4px;
    }
    QPushButton#iconButton:hover {
        border: 1px solid #ff4444;
        color: #e0e0e0;
    }
    QPushButton#testButton {
        background-color: #00aa44;
        color: white;
        font-size: 13px;
        font-weight: bold;
        padding: 10px 20px;
        border-radius: 4px;
    }
    QPushButton#testButton:hover {
        background-color: #00cc55;
    }
    QScrollArea {
        border: none;
        background-color: transparent;
    }
"""