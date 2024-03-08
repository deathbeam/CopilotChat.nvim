import os
import pynvim
import chromadb
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

def get_current_git_repository_path():
    return os.popen('git rev-parse --show-toplevel').read().strip()

def get_current_git_repository_files():
    return [os.path.join(os.popen('git rev-parse --show-toplevel').read().strip(), file) for file in os.popen('git ls-files').read().split('\n')]

class FileChangeHandler(PatternMatchingEventHandler):
    def __init__(self, patterns, collection):
        super().__init__(patterns=patterns)
        self.collection = collection

    def on_modified(self, event):
        if event.is_directory:
            return

        self.collection.add(
            documents = [ ],
            ids = [ event.src_path ],
        )

@pynvim.plugin
class CopilotChat(object):
    def __init__(self, nvim):
        self.nvim = nvim
        self.client = chromadb.PersistentClient(path="~/.cache/chromadb")
        self.observer = Observer()

    @pynvim.function('CopilotChatAgent', sync=True)
    def agent(self, args):
        path = get_current_git_repository_path()
        files = get_current_git_repository_files()
        collection = self.client.get_or_create_collection(path)
        event_handler = FileChangeHandler(files, collection)
        self.observer.schedule(event_handler, path=path, recursive=True)
        self.observer.start()

    @pynvim.function('CopilotChatEmbed', sync=True)
    def embed(self, args):
        path = args[0]
        filename = args[1]
        content = args[2]
        return args

    @pynvim.function('CopilotChatQuery', sync=True)
    def query(self, args):
        path = args[0]
        query = args[1]
        return args
