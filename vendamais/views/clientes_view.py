import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw

class ClientesView(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        
        self.set_margin_top(24)
        self.set_margin_bottom(24)
        self.set_margin_start(24)
        self.set_margin_end(24)
        
        # Título e botão adicionar
        header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        
        title = Gtk.Label(label="Gerenciamento de Clientes")
        title.add_css_class("title-1")
        title.set_halign(Gtk.Align.START)
        title.set_hexpand(True)
        
        btn_add = Gtk.Button(label="Adicionar Cliente")
        btn_add.add_css_class("suggested-action")
        btn_add.connect("clicked", self.on_add_cliente)
        
        header_box.append(title)
        header_box.append(btn_add)
        self.append(header_box)
        
        # Busca
        search_entry = Gtk.SearchEntry()
        search_entry.set_placeholder_text("Buscar clientes...")
        search_entry.connect("search-changed", self.on_search_changed)
        self.append(search_entry)
        
        # Lista de clientes
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        
        self.clientes_list = Gtk.ListBox()
        self.clientes_list.add_css_class("boxed-list")
        
        scrolled.set_child(self.clientes_list)
        self.append(scrolled)
        
        self.carregar_clientes()
    
    def carregar_clientes(self, filtro=""):
        from ..database import db
        
        # Limpar lista
        while child := self.clientes_list.get_first_child():
            self.clientes_list.remove(child)
        
        conn = db.get_connection()
        cursor = conn.cursor()
        
        if filtro:
            cursor.execute("""
                SELECT * FROM clientes 
                WHERE nome LIKE ? OR documento LIKE ?
                ORDER BY nome
            """, (f"%{filtro}%", f"%{filtro}%"))
        else:
            cursor.execute("SELECT * FROM clientes ORDER BY nome")
        
        clientes = cursor.fetchall()
        conn.close()
        
        for cliente in clientes:
            row = Adw.ActionRow(
                title=cliente['nome'],
                subtitle=f"Doc: {cliente['documento']} | Tel: {cliente['telefone'] or 'N/A'}"
            )
            
            # Botão editar
            btn_edit = Gtk.Button(icon_name="document-edit-symbolic")
            btn_edit.add_css_class("flat")
            btn_edit.connect("clicked", self.on_edit_cliente, cliente)
            row.add_suffix(btn_edit)
            
            self.clientes_list.append(row)
    
    def on_search_changed(self, entry):
        self.carregar_clientes(entry.get_text())
    
    def on_add_cliente(self, btn):
        self.show_cliente_dialog(None)
    
    def on_edit_cliente(self, btn, cliente):
        self.show_cliente_dialog(cliente)
    
    def show_cliente_dialog(self, cliente):
        """Mostra dialog para adicionar/editar cliente"""
        dialog = Adw.Dialog()
        dialog.set_title("Adicionar Cliente" if not cliente else "Editar Cliente")
        
        toolbar = Adw.ToolbarView()
        header = Adw.HeaderBar()
        toolbar.add_top_bar(header)
        
        # Formulário
        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        content.set_margin_top(24)
        content.set_margin_bottom(24)
        content.set_margin_start(24)
        content.set_margin_end(24)
        
        # Campos
        entry_nome = Adw.EntryRow(title="Nome Completo")
        entry_documento = Adw.EntryRow(title="CPF/CNPJ")
        entry_telefone = Adw.EntryRow(title="Telefone")
        entry_email = Adw.EntryRow(title="Email")
        entry_endereco = Adw.EntryRow(title="Endereço")
        
        if cliente:
            entry_nome.set_text(cliente['nome'])
            entry_documento.set_text(cliente['documento'] or "")
            entry_telefone.set_text(cliente['telefone'] or "")
            entry_email.set_text(cliente['email'] or "")
            entry_endereco.set_text(cliente['endereco'] or "")
        
        content.append(entry_nome)
        content.append(entry_documento)
        content.append(entry_telefone)
        content.append(entry_email)
        content.append(entry_endereco)
        
        # Botões
        btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        btn_box.set_halign(Gtk.Align.END)
        btn_box.set_margin_top(12)
        
        btn_cancel = Gtk.Button(label="Cancelar")
        btn_cancel.connect("clicked", lambda b: dialog.close())
        
        btn_save = Gtk.Button(label="Salvar")
        btn_save.add_css_class("suggested-action")
        btn_save.connect("clicked", self.on_save_cliente, dialog, {
            'id': cliente['id'] if cliente else None,
            'nome': entry_nome,
            'documento': entry_documento,
            'telefone': entry_telefone,
            'email': entry_email,
            'endereco': entry_endereco
        })
        
        btn_box.append(btn_cancel)
        btn_box.append(btn_save)
        content.append(btn_box)
        
        toolbar.set_content(content)
        dialog.set_child(toolbar)
        dialog.present(self.get_root())
    
    def on_save_cliente(self, btn, dialog, entries):
        from ..database import db
        
        try:
            dados = {
                'nome': entries['nome'].get_text(),
                'documento': entries['documento'].get_text(),
                'telefone': entries['telefone'].get_text(),
                'email': entries['email'].get_text(),
                'endereco': entries['endereco'].get_text()
            }
            
            conn = db.get_connection()
            cursor = conn.cursor()
            
            if entries['id']:
                # Atualizar
                cursor.execute("""
                    UPDATE clientes 
                    SET nome=?, documento=?, telefone=?, email=?, endereco=?
                    WHERE id=?
                """, (dados['nome'], dados['documento'], dados['telefone'],
                      dados['email'], dados['endereco'], entries['id']))
            else:
                # Inserir
                cursor.execute("""
                    INSERT INTO clientes (nome, documento, telefone, email, endereco)
                    VALUES (?, ?, ?, ?, ?)
                """, (dados['nome'], dados['documento'], dados['telefone'],
                      dados['email'], dados['endereco']))
            
            conn.commit()
            conn.close()
            
            dialog.close()
            self.carregar_clientes()
            
        except Exception as e:
            error_dialog = Adw.MessageDialog.new(
                self.get_root(),
                "Erro",
                f"Erro ao salvar cliente: {str(e)}"
            )
            error_dialog.add_response("ok", "OK")
            error_dialog.present()
