import sys
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, Gio
from .views.main_window import VendaMaisWindow
from .database import db

class VendaMaisApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id='com.example.vendamais',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)
        
        # Inicializar banco de dados
        db.init_db()
        
        self.connect('activate', self.on_activate)
    
    def on_activate(self, app):
        win = VendaMaisWindow(app)
        win.present()

def main():
    app = VendaMaisApp()
    return app.run(sys.argv)

if __name__ == '__main__':
    main()
