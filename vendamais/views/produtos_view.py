import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw

class ProdutosView(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        
        self.set_margin_top(24)
        self.set_margin_bottom(24)
        self.set_margin_start(24)
        self.set_margin_end(24)
        
        # Título e botão adicionar
        header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        
        title = Gtk.Label(label="Gerenciamento de Produtos")
        title.add_css_class("title-1")
        title.set_halign(Gtk.Align.START)
        title.set_hexpand(True)
        
        btn_add = Gtk.Button(label="Adicionar Produto")
        btn_add.add_css_class("suggested-action")
        btn_add.connect("clicked", self.on_add_produto)
        
        header_box.append(title)
        header_box.append(btn_add)
        self.append(header_box)
        
        # Busca
        search_entry = Gtk.SearchEntry()
        search_entry.set_placeholder_text("Buscar produtos...")
        search_entry.connect("search-changed", self.on_search_changed)
        self.append(search_entry)
        
        # Lista de produtos
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        
        self.produtos_list = Gtk.ListBox()
        self.produtos_list.add_css_class("boxed-list")
        
        scrolled.set_child(self.produtos_list)
        self.append(scrolled)
        
        self.carregar_produtos()
    
    def carregar_produtos(self, filtro=""):
        from ..database import db
        
        # Limpar lista
        while child := self.produtos_list.get_first_child():
            self.produtos_list.remove(child)
        
        conn = db.get_connection()
        cursor = conn.cursor()
        
        if filtro:
            cursor.execute("""
                SELECT * FROM produtos 
                WHERE nome LIKE ? OR codigo_barras LIKE ?
                ORDER BY nome
            """, (f"%{filtro}%", f"%{filtro}%"))
        else:
            cursor.execute("SELECT * FROM produtos ORDER BY nome")
        
        produtos = cursor.fetchall()
        conn.close()
        
        for produto in produtos:
            row = Adw.ActionRow(
                title=produto['nome'],
                subtitle=f"Código: {produto['codigo_barras']} | Estoque: {produto['estoque']} | NCM: {produto['ncm'] or 'N/A'}"
            )
            
            # Box com preços
            preco_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
            preco_box.set_valign(Gtk.Align.CENTER)
            
            compra_label = Gtk.Label(label=f"Custo: R$ {produto['preco_compra']:.2f}")
            compra_label.add_css_class("caption")
            
            venda_label = Gtk.Label(label=f"Venda: R$ {produto['preco_venda']:.2f}")
            venda_label.add_css_class("title-4")
            
            preco_box.append(compra_label)
            preco_box.append(venda_label)
            row.add_suffix(preco_box)
            
            # Botão editar
            btn_edit = Gtk.Button(icon_name="document-edit-symbolic")
            btn_edit.add_css_class("flat")
            btn_edit.connect("clicked", self.on_edit_produto, produto)
            row.add_suffix(btn_edit)
            
            self.produtos_list.append(row)
    
    def on_search_changed(self, entry):
        self.carregar_produtos(entry.get_text())
    
    def on_add_produto(self, btn):
        self.show_produto_dialog(None)
    
    def on_edit_produto(self, btn, produto):
        self.show_produto_dialog(produto)
    
    def show_produto_dialog(self, produto):
        """Mostra dialog para adicionar/editar produto"""
        dialog = Adw.Dialog()
        dialog.set_title("Adicionar Produto" if not produto else "Editar Produto")
        
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
        entry_nome = Adw.EntryRow(title="Nome do Produto")
        entry_codigo = Adw.EntryRow(title="Código de Barras")
        entry_preco_compra = Adw.EntryRow(title="Preço de Compra")
        entry_preco_venda = Adw.EntryRow(title="Preço de Venda")
        entry_estoque = Adw.EntryRow(title="Quantidade em Estoque")
        entry_ncm = Adw.EntryRow(title="NCM (Opcional)")
        entry_tributacao = Adw.EntryRow(title="Tributação % (Opcional)")
        
        if produto:
            entry_nome.set_text(produto['nome'])
            entry_codigo.set_text(produto['codigo_barras'] or "")
            entry_preco_compra.set_text(str(produto['preco_compra']))
            entry_preco_venda.set_text(str(produto['preco_venda']))
            entry_estoque.set_text(str(produto['estoque']))
            entry_ncm.set_text(produto['ncm'] or "")
            entry_tributacao.set_text(str(produto['tributacao']))
        
        content.append(entry_nome)
        content.append(entry_codigo)
        content.append(entry_preco_compra)
        content.append(entry_preco_venda)
        content.append(entry_estoque)
        content.append(entry_ncm)
        content.append(entry_tributacao)
        
        # Botões
        btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        btn_box.set_halign(Gtk.Align.END)
        btn_box.set_margin_top(12)
        
        btn_cancel = Gtk.Button(label="Cancelar")
        btn_cancel.connect("clicked", lambda b: dialog.close())
        
        btn_save = Gtk.Button(label="Salvar")
        btn_save.add_css_class("suggested-action")
        btn_save.connect("clicked", self.on_save_produto, dialog, {
            'id': produto['id'] if produto else None,
            'nome': entry_nome,
            'codigo_barras': entry_codigo,
            'preco_compra': entry_preco_compra,
            'preco_venda': entry_preco_venda,
            'estoque': entry_estoque,
            'ncm': entry_ncm,
            'tributacao': entry_tributacao
        })
        
        btn_box.append(btn_cancel)
        btn_box.append(btn_save)
        content.append(btn_box)
        
        toolbar.set_content(content)
        dialog.set_child(toolbar)
        dialog.present(self.get_root())
    
    def on_save_produto(self, btn, dialog, entries):
        from ..database import db
        
        try:
            dados = {
                'nome': entries['nome'].get_text(),
                'codigo_barras': entries['codigo_barras'].get_text(),
                'preco_compra': float(entries['preco_compra'].get_text() or 0),
                'preco_venda': float(entries['preco_venda'].get_text() or 0),
                'estoque': int(entries['estoque'].get_text() or 0),
                'ncm': entries['ncm'].get_text() or None,
                'tributacao': float(entries['tributacao'].get_text() or 0)
            }
            
            conn = db.get_connection()
            cursor = conn.cursor()
            
            if entries['id']:
                # Atualizar
                cursor.execute("""
                    UPDATE produtos 
                    SET nome=?, codigo_barras=?, preco_compra=?, preco_venda=?, 
                        estoque=?, ncm=?, tributacao=?
                    WHERE id=?
                """, (dados['nome'], dados['codigo_barras'], dados['preco_compra'],
                      dados['preco_venda'], dados['estoque'], dados['ncm'],
                      dados['tributacao'], entries['id']))
            else:
                # Inserir
                cursor.execute("""
                    INSERT INTO produtos (nome, codigo_barras, preco_compra, preco_venda, 
                                        estoque, ncm, tributacao)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (dados['nome'], dados['codigo_barras'], dados['preco_compra'],
                      dados['preco_venda'], dados['estoque'], dados['ncm'],
                      dados['tributacao']))
            
            conn.commit()
            conn.close()
            
            dialog.close()
            self.carregar_produtos()
            
        except Exception as e:
            error_dialog = Adw.MessageDialog.new(
                self.get_root(),
                "Erro",
                f"Erro ao salvar produto: {str(e)}"
            )
            error_dialog.add_response("ok", "OK")
            error_dialog.present()
