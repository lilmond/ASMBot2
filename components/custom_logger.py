from datetime import datetime
import os


class CustomLogger(object):
    def __init__(self, source_file: str):
        self.source_file = source_file
        
        self.logs_dir = f"{os.path.dirname(__file__)}/../logs"
        self.security_logs = "security.log"
        self.error_logs = "error.log"

        if not os.path.exists(self.logs_dir):
            os.mkdir(self.logs_dir)


    def log_error(self, message: str):
        log_date = datetime.now().strftime('%m-%d-%Y %H:%M:%S')
        log_message = f"[{log_date}][{self.source_file}] {message}\n"
        
        with open(f"{self.logs_dir}/{self.error_logs}", "a") as file:
            file.write(log_message)
            file.close()

    
    def log_security(self, message: str):
        log_date = datetime.now().strftime('%m-%d-%Y %H:%M:%S')
        log_message = f"[{log_date}][{self.source_file}] {message}\n"
        
        with open(f"{self.logs_dir}/{self.security_logs}", "a") as file:
            file.write(log_message)
            file.close()
