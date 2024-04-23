import sys
import os
import requests
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal

class Worker(QThread):
    log_signal = pyqtSignal(str)

    def __init__(self, api_key, days):
        super().__init__()
        self.api_key = api_key
        self.days = days

    def run(self):
        self.log_signal.emit("Starting search for certificates...")
        file_urls = self.make_request()
        if not file_urls:
            self.log_signal.emit("No certificates found within the specified timeframe.")
            return

        dir_name = self.setup_directories(datetime.now().strftime("%Y%m%d%H%M%S"))
        for url in file_urls:
            filename = self.download_file(url, dir_name)
            if filename:
                self.process_file(filename, dir_name)
        self.log_signal.emit(f"Process completed. Files are saved in {dir_name}.")

    def make_request(self):
        try:
            # Construct the API URL with filters
            api_url = f"https://buckets.grayhatwarfare.com/api/v2/files?extensions=pfx&days={self.days}"
            response = requests.get(api_url, headers={"Authorization": f"Bearer {self.api_key}"})
            response.raise_for_status()  # Check for HTTP request errors
            return [file['url'] for file in response.json()['files']]
        except requests.RequestException as e:
            self.log_signal.emit(f"Failed to fetch data: {str(e)}")
            return []


    def download_file(self, url, dir_name):
        try:
            response = requests.get(url)
            response.raise_for_status()
            filename = url.split('/')[-1]
            path = os.path.join(dir_name, filename)
            with open(path, 'wb') as file:
                file.write(response.content)
            return filename
        except requests.RequestException:
            self.log_signal.emit(f"Failed to download file: {url}")
            return None

    def process_file(self, filename, dir_name):
        self.log_signal.emit(f"Processed {filename}")

    def setup_directories(self, timestamp):
        dir_name = f"certs_{timestamp}"
        os.makedirs(dir_name, exist_ok=True)
        return dir_name

class StupidCertsApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # API Key Input
        api_key_layout = QHBoxLayout()
        api_key_label = QLabel('API Key:')
        self.api_key_input = QLineEdit()
        api_key_layout.addWidget(api_key_label)
        api_key_layout.addWidget(self.api_key_input)
        layout.addLayout(api_key_layout)

        # Days Input
        days_layout = QHBoxLayout()
        days_label = QLabel('Days:')
        self.days_input = QLineEdit()
        days_layout.addWidget(days_label)
        days_layout.addWidget(self.days_input)
        layout.addLayout(days_layout)

        # Start Button
        self.start_button = QPushButton('Start Search')
        self.start_button.clicked.connect(self.start_search)
        layout.addWidget(self.start_button)

        # Log Output
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        layout.addWidget(self.log_output)

        self.setLayout(layout)
        self.setWindowTitle('StupidCerts - Certificate Scraper')
        self.setGeometry(300, 300, 350, 250)

    def start_search(self):
        api_key = self.api_key_input.text()
        days = self.days_input.text()
        if not api_key or not days.isdigit():
            QMessageBox.warning(self, 'Error', 'Please enter a valid API key and number of days.')
            return
        self.worker = Worker(api_key, int(days))
        self.worker.log_signal.connect(self.update_log)
        self.worker.start()

    def update_log(self, message):
        self.log_output.append(message)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = StupidCertsApp()
    ex.show()
    sys.exit(app.exec_())
