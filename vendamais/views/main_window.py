import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, Gio
from .vendas_view import VendasView
from .produtos_view import ProdutosView
from .clientes_view import ClientesView
from .relatorios_view import RelatoriosView
from .configuracoes_view import ConfiguracoesView

class VendaMaisWindow(Adw.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app)
        
        self.set_title("VendaMais - Sistema de Gestão")
        self.set_default_size(1200, 700)
        
        # Container principal
        toolbar_view = Adw.ToolbarView()
        
        # Header Bar
        header = Adw.HeaderBar()
        
        # Menu button
        menu_button = Gtk.MenuButton()
        menu = Gio.Menu()
        menu.append("Fazer Backup", "app.backup")
        menu.append("Sobre", "app.about")
        menu_button.set_menu_model(menu)
        header.pack_end(menu_button)
        
        toolbar_view.add_top_bar(header)
        
        # Stack para as diferentes views
        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.stack.set_transition_duration(200)
        
        # Criar as views
        self.vendas_view = VendasView()
        self.produtos_view = ProdutosView()
        self.clientes_view = ClientesView()
        self.relatorios_view = RelatoriosView()
        self.configuracoes_view = ConfiguracoesView()
        
        # Adicionar as views ao stack
        self.stack.add_titled(self.vendas_view, "vendas", "PDV / Vendas")
        self.stack.add_titled(self.produtos_view, "produtos", "Produtos")
        self.stack.add_titled(self.clientes_view, "clientes", "Clientes")
        self.stack.add_titled(self.relatorios_view, "relatorios", "Relatórios")
        self.stack.add_titled(self.configuracoes_view, "configuracoes", "Configurações")
        
        # Stack Switcher para navegação
        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(self.stack)
        header.set_title_widget(stack_switcher)
        
        toolbar_view.set_content(self.stack)
        self.set_content(toolbar_view)
        
        # Actions
        self.create_actions()
    
    def create_actions(self):
        backup_action = Gio.SimpleAction.new("backup", None)
        backup_action.connect("activate", self.on_backup)
        self.get_application().add_action(backup_action)
        
        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self.on_about)
        self.get_application().add_action(about_action)
    
    def on_backup(self, action, param):
        from ..database import db
        backup_path = db.backup()
        
        dialog = Adw.MessageDialog.new(
            self,
            "Backup Criado",
            f"Backup salvo em:\n{backup_path}"
        )
        dialog.add_response("ok", "OK")
        dialog.present()
    
    def on_about(self, action, param):
        about = Adw.AboutWindow.new()
        about.set_transient_for(self)
        about.set_application_name("VendaMais")
        about.set_version("1.1.0")
        about.set_developer_name("Edius Ferreira")
        about.set_comments("Sistema de Gestão de Vendas, Estoque e PDV")
        about.set_website("https://github.com/edius1987/VendaMais")
        about.set_issue_url("https://github.com/edius1987/VendaMais/issues")
        about.set_license_type(Gtk.License.MIT_X11)
        about.set_developers([
            "Edius Ferreira https://github.com/edius1987"
        ])
        about.set_copyright("© 2026 Edius Ferreira")
        about.add_credit_section(
            "Tecnologias",
            [
                "Python 3.12+",
                "GTK4 e Libadwaita",
                "SQLite",
                "Matplotlib"
            ]
        )
        about.present()
