from common.read_str import ReadStr

class PasswordEngine:
    def __init__(self, manage_folder:object, scan_file:object, manage_engines:object,rabbit:object) -> None:
        self.manage_folder = manage_folder
        self.scan_file = scan_file
        self.manage_engines = manage_engines
        self.rabbit = rabbit

    def run(self):
        self.manage_engines.consume_engine(self.rabbit, self.handle_data)
    
    def handle_data(self, data):
        pass
    def scan_file_run(self, dir_name, file_name):
        read_str = ReadStr()
        file = self.manage_folder.read_data(dir_name, file_name, read_str)
        file_errors = self.scan_file.scan_file(file)
        return file_errors
        