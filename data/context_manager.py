import sys
sys.path.append("..")
# Just a contextManager
class ContextManager:
    def __init__(self,filename):
        self.file = open(filename)

    def __enter__(self):
        return self.file

    def __exit__(self, type, value, traceback):
        self.file.close()