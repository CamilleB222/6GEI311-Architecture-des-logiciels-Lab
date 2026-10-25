import subprocess
import sys
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class ReloadHandler(FileSystemEventHandler):

    def __init__(self, command):
        self.command = command
        self.process = None
        self.start_process()

    def start_process(self):
        if self.process:
            self.process.kill()
            self.process.wait()
        print("⚡ Redémarrage de l'application...")
        self.process = subprocess.Popen(self.command)

    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            self.start_process()


if __name__ == "__main__":
    # Commande à exécuter via l'interprète Python courant de uv
    cmd = [sys.executable, "app.py"]

    event_handler = ReloadHandler(cmd)
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=True)
    observer.start()

    print("👀 Surveillance active (Fichiers .py). Appuyez sur Ctrl+C pour arrêter.")
    try:
        observer.join()
    except KeyboardInterrupt:
        observer.stop()
        if event_handler.process:
            event_handler.process.kill()
    observer.join()