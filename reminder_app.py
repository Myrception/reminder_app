import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import QTimer
import notify2
import os
import threading

# Initialize the notification system
notify2.init("Reminder App")

# Define the time interval in milliseconds (1 hour = 3600 seconds)
TIME_INTERVAL_MS = 3600 * 1000

class ReminderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Task Reminder')
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.label = QLabel("Please acknowledge your task.")
        layout.addWidget(self.label)

        self.ack_button = QPushButton('Acknowledge')
        self.ack_button.clicked.connect(self.acknowledge_task)
        layout.addWidget(self.ack_button)

        self.setLayout(layout)

    def show_notification(self):
        n = notify2.Notification("Task Reminder", "It's time to do your task!")
        n.show()
        threading.Thread(target=self.play_sound).start()

    def play_sound(self):
        try:
            os.system('paplay /usr/share/sounds/freedesktop/stereo/alarm-clock-elapsed.oga')  # Play a system sound
        except Exception as e:
            print(f"Error playing sound: {e}")

    def acknowledge_task(self):
        self.label.setText("Task acknowledged.")
        self.ack_button.setEnabled(False)
        QTimer.singleShot(TIME_INTERVAL_MS, self.reset_acknowledge)  # Reset after the defined interval

    def reset_acknowledge(self):
        self.label.setText("Please acknowledge your task.")
        self.ack_button.setEnabled(True)

def main():
    app = QApplication(sys.argv)
    reminder_app = ReminderApp()
    reminder_app.show()

    timer = QTimer()
    timer.timeout.connect(reminder_app.show_notification)
    timer.start(TIME_INTERVAL_MS)  # Start the timer with the defined interval

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
