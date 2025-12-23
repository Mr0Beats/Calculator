import logging
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QGridLayout,
                             QLineEdit, QPushButton, QLabel, QMessageBox)
from PyQt5.QtCore import Qt, QSize

from core.lexer import Lexer
from core.parser import Parser
from utils.history import HistoryManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calc")
        self.setGeometry(100, 100, 360, 600) 
        self.logger = logging.getLogger("MathApp")
        
        self.is_dark_theme = True
        
        self.init_ui()
        self.apply_theme()

    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)

        self.theme_btn = QPushButton("🌙 / ☀️")
        self.theme_btn.setFixedSize(60, 30)
        self.theme_btn.clicked.connect(self.toggle_theme)
        self.main_layout.addWidget(self.theme_btn, alignment=Qt.AlignRight)

        self.history_label = QLabel("")
        self.history_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        self.history_label.setFixedHeight(30)
        self.main_layout.addWidget(self.history_label)

        self.input_field = QLineEdit()
        self.input_field.setAlignment(Qt.AlignRight)
        self.input_field.setReadOnly(True)
        self.input_field.setPlaceholderText("0")
        self.main_layout.addWidget(self.input_field)

        self.buttons_layout = QGridLayout()
        self.buttons_layout.setSpacing(10)
        self.main_layout.addLayout(self.buttons_layout)

        buttons_config = [
            ('C', 0, 0, 'clear'), ('^', 0, 1, 'op'), ('/', 0, 2, 'op'), ('⌫', 0, 3, 'clear'),
            ('7', 1, 0, 'num'),   ('8', 1, 1, 'num'), ('9', 1, 2, 'num'), ('*', 1, 3, 'op'),
            ('4', 2, 0, 'num'),   ('5', 2, 1, 'num'), ('6', 2, 2, 'num'), ('-', 2, 3, 'op'),
            ('1', 3, 0, 'num'),   ('2', 3, 1, 'num'), ('3', 3, 2, 'num'), ('+', 3, 3, 'op'),
            ('(', 4, 0, 'num'),   ('0', 4, 1, 'num'), (')', 4, 2, 'num'), ('=', 4, 3, 'eq'),
        ]

        self.buttons = {}
        for text, row, col, type_ in buttons_config:
            btn = QPushButton(text)
            btn.setFixedSize(70, 70)
            btn.setProperty('class', type_)
            
            if text == '=':
                btn.clicked.connect(self.calculate)
            elif text == 'C':
                btn.clicked.connect(self.clear_input)
            elif text == '⌫':
                btn.clicked.connect(self.backspace)
            else:
                btn.clicked.connect(lambda checked, t=text: self.add_to_input(t))
            
            self.buttons_layout.addWidget(btn, row, col)
            self.buttons[text] = btn

    def add_to_input(self, text):
        current_text = self.input_field.text()
        if current_text == "ERROR":
            current_text = ""
        self.input_field.setText(current_text + text)

    def clear_input(self):
        self.input_field.clear()
        self.history_label.setText("")

    def backspace(self):
        text = self.input_field.text()
        self.input_field.setText(text[:-1])

    def calculate(self):
        text = self.input_field.text()
        if not text:
            return

        self.logger.info(f"Input: {text}")
        try:
            lexer = Lexer(text)
            parser = Parser(lexer)
            tree = parser.parse()
            result = tree.evaluate()

            self.history_label.setText(text + " =")
            self.input_field.setText(str(result))
            
            self.logger.info(f"Success: {result}")
            HistoryManager.save(text, result, "success")

        except Exception as e:
            error_msg = str(e)
            self.logger.error(f"Error: {error_msg}")
            
            self.input_field.setText("ERROR")
            
            msg = QMessageBox(self)
            msg.setWindowTitle("Помилка")
            msg.setText(f"Некоректний вираз:\n{error_msg}")
            msg.setIcon(QMessageBox.Warning)
            
            msg.setStyleSheet("background-color: #F0F0F0; color: #000000; font-size: 14px;")
            
            msg.exec_()

    def toggle_theme(self):
        self.is_dark_theme = not self.is_dark_theme
        self.apply_theme()

    def apply_theme(self):
        if self.is_dark_theme:
            bg_color = "#1C1C1C"
            text_color = "#FFFFFF"
            btn_num_bg = "#333333"
            btn_num_hover = "#4D4D4D"
            btn_op_bg = "#FF9F0A"
            btn_op_hover = "#FFB340"
            btn_eq_bg = "#FF9F0A"
            btn_clear_bg = "#A5A5A5"
            btn_clear_text = "#000000"
            input_bg = "#1C1C1C"
        else:
            bg_color = "#F2F2F7"
            text_color = "#000000"
            btn_num_bg = "#FFFFFF"
            btn_num_hover = "#E5E5EA"
            btn_op_bg = "#007AFF"
            btn_op_hover = "#3395FF"
            btn_eq_bg = "#007AFF"
            btn_clear_bg = "#D1D1D6"
            btn_clear_text = "#000000"
            input_bg = "#F2F2F7"

        style = f"""
            QMainWindow {{
                background-color: {bg_color};
            }}
            QLineEdit {{
                background-color: {input_bg};
                color: {text_color};
                border: none;
                font-size: 48px;
                font-family: 'Segoe UI', sans-serif;
                font-weight: 300;
            }}
            QMainWindow QLabel {{
                color: {text_color};
                font-size: 18px;
                opacity: 0.6;
            }}
            
            QMessageBox {{
                background-color: #F0F0F0;
            }}
            QMessageBox QLabel {{
                color: #000000;
                font-size: 14px;
            }}

            QPushButton {{
                border-radius: 35px;
                font-size: 24px;
                font-weight: bold;
            }}
            
            QPushButton[class="num"] {{
                background-color: {btn_num_bg};
                color: {text_color};
            }}
            QPushButton[class="num"]:hover {{
                background-color: {btn_num_hover};
            }}

            QPushButton[class="op"] {{
                background-color: {btn_op_bg};
                color: #FFFFFF;
            }}
            QPushButton[class="op"]:hover {{
                background-color: {btn_op_hover};
            }}

            QPushButton[class="eq"] {{
                background-color: {btn_eq_bg};
                color: #FFFFFF;
            }}

            QPushButton[class="clear"] {{
                background-color: {btn_clear_bg};
                color: {btn_clear_text};
            }}
        """
        self.setStyleSheet(style)

        style = f"""
            QMainWindow {{
                background-color: {bg_color};
            }}
            QLineEdit {{
                background-color: {input_bg};
                color: {text_color};
                border: none;
                font-size: 48px;
                font-family: 'Segoe UI', sans-serif;
                font-weight: 300;
            }}
            QLabel {{
                color: {text_color};
                font-size: 18px;
                opacity: 0.6;
            }}
            QPushButton {{
                border-radius: 35px;
                font-size: 24px;
                font-weight: bold;
            }}
            
            QPushButton[class="num"] {{
                background-color: {btn_num_bg};
                color: {text_color};
            }}
            QPushButton[class="num"]:hover {{
                background-color: {btn_num_hover};
            }}

            QPushButton[class="op"] {{
                background-color: {btn_op_bg};
                color: #FFFFFF;
            }}
            QPushButton[class="op"]:hover {{
                background-color: {btn_op_hover};
            }}

            QPushButton[class="eq"] {{
                background-color: {btn_eq_bg};
                color: #FFFFFF;
            }}

            QPushButton[class="clear"] {{
                background-color: {btn_clear_bg};
                color: {btn_clear_text};
            }}
        """
        self.setStyleSheet(style)