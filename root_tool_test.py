import sys
import subprocess
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QTextBrowser, QDialog, QFileDialog
from PyQt5.QtGui import QColor, QPainter, QBrush
from PyQt5.QtCore import Qt, pyqtSignal

Height_of_gui = 250
Width_of_gui = 400
Color_of_background = 'rgba(255, 255, 255, 0.03)'
Color_of_button = 'rgba(120, 255, 9, 0.6)'

class HelpDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Help with Rooting Tool ")
        self.setGeometry(100, 100, 600, 400)
        help_layout = QVBoxLayout(self)

        help_text = QTextBrowser(self)
        help_text.setStyleSheet('color: white; font-size: 14px; background-color: black;')
        help_layout.addWidget(help_text)

        help_text.setPlainText(
            "HOW TO MAKE THIS WORK\n\n"
            "1. Select button, the button will run a command via subprocess"
            "------------------------------------------------------------------------ \n\n"
            "INFO - CONTACT INFO\n\n"
            "This was made by @c.r.u.n.c.h.y, this is a tool that allows you to root easier."
            " Please Know I am not liable for any type of bricking! \n\n"
            "------------------------------------------------------------------------ \n"
        )

        self.setLayout(help_layout)

class RoundedWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('ROOTING GUI BY CRUNCHY')
        self.setGeometry(100, 100, Width_of_gui, Height_of_gui)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)

        label = QLabel(" ROOT TOOL - Version: 1.3", self)
        label.setStyleSheet('color: white; font-size: 20px;')
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(label)

        self.log_text = QTextBrowser(self)
        self.log_text.setStyleSheet('color: white; font-size: 12px; background-color: black;')
        main_layout.addWidget(self.log_text)

        buttons_layout = QVBoxLayout()

        options = ["ADB KILL-SERVER", "ADB DEVICES", "ADB REBOOT BOOTLOADER", "FASTBOOT DEVICES",
                   "FASTBOOT BOOT", "OEM UNLOCK", "FLASHING UNLOCK", "HELP"]
        for option in options:
            button = QPushButton(option, self)
            button.setStyleSheet(
                f'background-color: {Color_of_button}; color: white; border: none; border-radius: 10px; font-size: 18px;')
            button.clicked.connect(self.handle_button_click)
            buttons_layout.addWidget(button)

        exit_button = QPushButton("EXIT", self)
        exit_button.setStyleSheet(
            f'background-color: {Color_of_button}; color: white; border: none; border-radius: 10px; font-size: 18px;')
        exit_button.clicked.connect(self.close_app)
        buttons_layout.addWidget(exit_button)

        main_layout.addLayout(buttons_layout)

        self.setLayout(main_layout)

    def close_app(self):
        self.close()

    def handle_button_click(self):
        sender = self.sender()

        if isinstance(sender, QPushButton):
            button_text = sender.text()

            if button_text == "ADB KILL-SERVER":
                self.adb_kill()
            elif button_text == "ADB DEVICES":
                self.adb_devices()
            elif button_text == "ADB REBOOT BOOTLOADER":
                self.adb_reboot()
            elif button_text == "FASTBOOT DEVICES":
                self.fastboot_devices()
            elif button_text == "FASTBOOT BOOT":
                self.fastboot_boot()
            elif button_text == "OEM UNLOCK":
                self.oem_unlock()
            elif button_text == "FLASHING UNLOCK":
                self.flashing_unlock()
            elif button_text == "HELP":
                self.show_help()

    def run_command(self, command):
        try:
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output = result.stdout.strip() if result.stdout else result.stderr.strip()
            self.log_text.append(output)
        except Exception as e:
            self.log_text.append(f"Error: {e}")

    def adb_kill(self):
        self.run_command(["adb", "kill-server"])

    def adb_devices(self):
        self.run_command(["adb", "devices"])

    def adb_reboot(self):
        self.run_command(["adb", "reboot", "bootloader"])

    def fastboot_devices(self):
        self.run_command(["fastboot", "devices"])

    def fastboot_boot(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Boot Image Files (*.img *.img.gz *.zip)")
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                boot_image_path = selected_files[0]
                self.run_command(["fastboot", "boot", boot_image_path])

    def oem_unlock(self):
        self.run_command(["fastboot", "oem", "unlock"])

    def flashing_unlock(self):
        self.run_command(["fastboot", "flashing", "unlock"])

    def show_help(self):
        help_dialog = HelpDialog()
        help_dialog.exec_()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(QColor(Color_of_background)))
        painter.drawRoundedRect(self.rect(), 10, 10)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_pos)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RoundedWindow()
    window.show()
    sys.exit(app.exec_())
