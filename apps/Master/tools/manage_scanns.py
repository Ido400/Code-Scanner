from concurrent.futures import ThreadPoolExecutor

class ManageScannes:
    def __init__(self, max_workers:int, manage_engines:object, dir_name:str, manage_folder:object) -> None:
        self.thread_pool = ThreadPoolExecutor(max_workers=max_workers)
        self.manage_engines = manage_engines
        self.manage_engines.load_engines(dir_name, manage_folder)
    
    def consume_engines(self):
        with self.thread_pool as exc:
            for engine in self.manage_engines.engines:
                exc.submit(self.manage_engines.engines_consume(engine))

                