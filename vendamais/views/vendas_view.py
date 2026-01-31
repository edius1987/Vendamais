import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, GLib
from datetime import datetime

class VendasView(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        
        # Container com padding
        main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=24)
        main_box.set_margin_top(24)
        main_box.set_margin_bottom(24)
        main_box.set_margin_start(24)
        main_box.set_margin_end(24)
        
        # Painel esquerdo - Busca e lista de produtos
        left_panel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        left_panel.set_hexpand(True)
        
        title = Gtk.Label(label="Frente de Caixa (PDV)")
        title.add_css_class("title-1")
        title.set_halign(Gtk.Align.START)
        left_panel.append(title)
        
        # Busca de produto com autocomplete
        search_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        
        entry_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.search_entry = Gtk.Entry()
        self.search_entry.set_placeholder_text("Código de barras ou nome do produto...")
        self.search_entry.set_hexpand(True)
        
        # Conectar evento de digitação para busca interativa
        self.search_entry.connect("changed", self.on_search_changed)
        self.search_entry.connect("activate", self.on_search_activate)
        
        # Timer para busca automática após parar de digitar
        self.search_timeout_id = None
        
        btn_limpar_busca = Gtk.Button(icon_name="edit-clear-symbolic")
        btn_limpar_busca.add_css_class("flat")
        btn_limpar_busca.connect("clicked", self.on_limpar_busca)
        
        entry_box.append(self.search_entry)
        entry_box.append(btn_limpar_busca)
        search_box.append(entry_box)
        
        # Label de status da busca
        self.search_status = Gtk.Label(label="Digite para buscar produtos...")
        self.search_status.add_css_class("dim-label")
        self.search_status.add_css_class("caption")
        self.search_status.set_halign(Gtk.Align.START)
        search_box.append(self.search_status)
        
        left_panel.append(search_box)
        
        # Lista de produtos encontrados
        scrolled_produtos = Gtk.ScrolledWindow()
        scrolled_produtos.set_vexpand(True)
        scrolled_produtos.set_min_content_height(200)
        
        self.produtos_list = Gtk.ListBox()
        self.produtos_list.add_css_class("boxed-list")
        self.produtos_list.connect("row-activated", self.on_produto_selected)
        
        scrolled_produtos.set_child(self.produtos_list)
        left_panel.append(scrolled_produtos)
        
        # Painel direito - Carrinho e finalização
        right_panel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        right_panel.set_size_request(400, -1)
        
        carrinho_label = Gtk.Label(label="Carrinho de Compras")
        carrinho_label.add_css_class("title-2")
        carrinho_label.set_halign(Gtk.Align.START)
        right_panel.append(carrinho_label)
        
        # Seleção de Cliente (Opcional)
        cliente_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        cliente_box.add_css_class("card")
        cliente_box.set_margin_top(6)
        cliente_box.set_margin_bottom(6)
        cliente_box.set_margin_start(6)
        cliente_box.set_margin_end(6)
        
        cliente_header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        cliente_header.set_margin_top(6)
        cliente_header.set_margin_bottom(6)
        cliente_header.set_margin_start(6)
        cliente_header.set_margin_end(6)
        
        cliente_icon = Gtk.Image.new_from_icon_name("avatar-default-symbolic")
        cliente_header.append(cliente_icon)
        
        self.cliente_label = Gtk.Label(label="Nenhum cliente selecionado")
        self.cliente_label.add_css_class("caption")
        self.cliente_label.set_hexpand(True)
        self.cliente_label.set_halign(Gtk.Align.START)
        cliente_header.append(self.cliente_label)
        
        btn_selecionar_cliente = Gtk.Button(label="Selecionar")
        btn_selecionar_cliente.add_css_class("flat")
        btn_selecionar_cliente.connect("clicked", self.on_selecionar_cliente)
        cliente_header.append(btn_selecionar_cliente)
        
        self.btn_remover_cliente = Gtk.Button(icon_name="edit-clear-symbolic")
        self.btn_remover_cliente.add_css_class("flat")
        self.btn_remover_cliente.set_sensitive(False)
        self.btn_remover_cliente.connect("clicked", self.on_remover_cliente)
        cliente_header.append(self.btn_remover_cliente)
        
        cliente_box.append(cliente_header)
        right_panel.append(cliente_box)
        
        # Lista de itens no carrinho
        scrolled_carrinho = Gtk.ScrolledWindow()
        scrolled_carrinho.set_vexpand(True)
        
        self.carrinho_list = Gtk.ListBox()
        self.carrinho_list.add_css_class("boxed-list")
        
        scrolled_carrinho.set_child(self.carrinho_list)
        right_panel.append(scrolled_carrinho)
        
        # Total
        total_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        total_box.set_halign(Gtk.Align.END)
        total_label = Gtk.Label(label="Total: ")
        total_label.add_css_class("title-3")
        
        self.total_value = Gtk.Label(label="R$ 0,00")
        self.total_value.add_css_class("title-1")
        self.total_value.add_css_class("success")
        
        total_box.append(total_label)
        total_box.append(self.total_value)
        right_panel.append(total_box)
        
        # Botões de ação
        actions_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        actions_box.set_homogeneous(True)
        
        btn_limpar = Gtk.Button(label="Limpar Carrinho")
        btn_limpar.add_css_class("destructive-action")
        btn_limpar.connect("clicked", self.on_limpar_carrinho)
        
        btn_finalizar = Gtk.Button(label="Finalizar Venda")
        btn_finalizar.add_css_class("suggested-action")
        btn_finalizar.connect("clicked", self.on_finalizar_venda)
        
        actions_box.append(btn_limpar)
        actions_box.append(btn_finalizar)
        right_panel.append(actions_box)
        
        main_box.append(left_panel)
        main_box.append(Gtk.Separator(orientation=Gtk.Orientation.VERTICAL))
        main_box.append(right_panel)
        
        self.append(main_box)
        
        # Estado do carrinho
        self.carrinho = []
        self.cliente_selecionado = None  # Armazena o cliente selecionado (opcional)
    
    def on_limpar_busca(self, btn):
        """Limpa o campo de busca"""
        self.search_entry.set_text("")
        self.search_entry.grab_focus()
    
    def on_search_changed(self, entry):
        """Chamado quando o texto da busca muda - implementa busca interativa"""
        # Cancelar timer anterior se existir
        if self.search_timeout_id:
            GLib.source_remove(self.search_timeout_id)
        
        # Criar novo timer para buscar após 300ms de inatividade
        self.search_timeout_id = GLib.timeout_add(300, self.executar_busca)
    
    def on_search_activate(self, entry):
        """Chamado quando pressiona Enter - busca imediata"""
        if self.search_timeout_id:
            GLib.source_remove(self.search_timeout_id)
        self.executar_busca()
    
    def executar_busca(self):
        """Executa a busca de produtos"""
        from ..database import db
        
        termo = self.search_entry.get_text().strip()
        
        # Limpar lista de resultados
        while child := self.produtos_list.get_first_child():
            self.produtos_list.remove(child)
        
        if not termo:
            self.search_status.set_text("Digite para buscar produtos...")
            self.search_timeout_id = None
            return False
        
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # Busca por código exato ou nome parcial
        cursor.execute("""
            SELECT * FROM produtos 
            WHERE codigo_barras = ? OR LOWER(nome) LIKE LOWER(?)
            ORDER BY nome
            LIMIT 50
        """, (termo, f"%{termo}%"))
        
        produtos = cursor.fetchall()
        conn.close()
        
        if not produtos:
            self.search_status.set_text("Nenhum produto encontrado")
            self.search_timeout_id = None
            return False
        
        self.search_status.set_text(f"{len(produtos)} produto(s) encontrado(s)")
        
        for produto in produtos:
            row = Adw.ActionRow(
                title=produto['nome'],
                subtitle=f"Código: {produto['codigo_barras']} | Estoque: {produto['estoque']}"
            )
            
            preco_label = Gtk.Label(label=f"R$ {produto['preco_venda']:.2f}")
            preco_label.add_css_class("title-3")
            row.add_suffix(preco_label)
            
            # Botão para adicionar ao carrinho
            btn_add = Gtk.Button(label="Adicionar")
            btn_add.add_css_class("suggested-action")
            btn_add.connect("clicked", lambda b, p=produto: self.adicionar_ao_carrinho(p))
            row.add_suffix(btn_add)
            
            # Guardar dados do produto na row
            row.produto_data = produto
            
            self.produtos_list.append(row)
        
        self.search_timeout_id = None
        return False
    
    def on_produto_selected(self, listbox, row):
        """Adiciona produto ao carrinho ao clicar na linha"""
        if hasattr(row, 'produto_data'):
            self.adicionar_ao_carrinho(row.produto_data)
    
    def adicionar_ao_carrinho(self, produto):
        """Adiciona produto ao carrinho"""
        # Verificar estoque
        if produto['estoque'] <= 0:
            dialog = Adw.MessageDialog.new(
                self.get_root(),
                "Estoque Insuficiente",
                f"O produto '{produto['nome']}' está sem estoque!"
            )
            dialog.add_response("ok", "OK")
            dialog.present()
            return
        
        # Verificar se já está no carrinho
        for item in self.carrinho:
            if item['id'] == produto['id']:
                # Verificar se tem estoque para mais uma unidade
                if item['quantidade'] >= produto['estoque']:
                    dialog = Adw.MessageDialog.new(
                        self.get_root(),
                        "Estoque Insuficiente",
                        f"Quantidade em estoque: {produto['estoque']}"
                    )
                    dialog.add_response("ok", "OK")
                    dialog.present()
                    return
                
                item['quantidade'] += 1
                self.atualizar_carrinho()
                return
        
        # Adicionar novo item
        self.carrinho.append({
            'id': produto['id'],
            'nome': produto['nome'],
            'codigo_barras': produto['codigo_barras'],
            'preco': produto['preco_venda'],
            'quantidade': 1,
            'estoque_disponivel': produto['estoque']
        })
        
        self.atualizar_carrinho()
    
    def atualizar_carrinho(self):
        """Atualiza a exibição do carrinho"""
        # Limpar lista
        while child := self.carrinho_list.get_first_child():
            self.carrinho_list.remove(child)
        
        total = 0.0
        
        for item in self.carrinho:
            subtotal = item['preco'] * item['quantidade']
            total += subtotal
            
            row = Adw.ActionRow(
                title=item['nome'],
                subtitle=f"R$ {item['preco']:.2f} x {item['quantidade']} un"
            )
            
            # Box para quantidade e subtotal
            info_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
            
            # Botões de quantidade
            btn_menos = Gtk.Button(icon_name="list-remove-symbolic")
            btn_menos.add_css_class("flat")
            btn_menos.connect("clicked", self.on_diminuir_quantidade, item)
            
            btn_mais = Gtk.Button(icon_name="list-add-symbolic")
            btn_mais.add_css_class("flat")
            btn_mais.connect("clicked", self.on_aumentar_quantidade, item)
            
            # Subtotal
            subtotal_label = Gtk.Label(label=f"R$ {subtotal:.2f}")
            subtotal_label.add_css_class("monospace")
            subtotal_label.add_css_class("title-4")
            
            # Botão remover
            btn_remove = Gtk.Button(icon_name="edit-delete-symbolic")
            btn_remove.add_css_class("flat")
            btn_remove.add_css_class("error")
            btn_remove.connect("clicked", self.on_remove_item, item)
            
            info_box.append(btn_menos)
            info_box.append(btn_mais)
            info_box.append(subtotal_label)
            info_box.append(btn_remove)
            
            row.add_suffix(info_box)
            self.carrinho_list.append(row)
        
        self.total_value.set_text(f"R$ {total:.2f}")
    
    def on_aumentar_quantidade(self, btn, item):
        """Aumenta quantidade do item no carrinho"""
        if item['quantidade'] >= item['estoque_disponivel']:
            dialog = Adw.MessageDialog.new(
                self.get_root(),
                "Estoque Insuficiente",
                f"Quantidade máxima disponível: {item['estoque_disponivel']}"
            )
            dialog.add_response("ok", "OK")
            dialog.present()
            return
        
        item['quantidade'] += 1
        self.atualizar_carrinho()
    
    def on_diminuir_quantidade(self, btn, item):
        """Diminui quantidade do item no carrinho"""
        if item['quantidade'] > 1:
            item['quantidade'] -= 1
            self.atualizar_carrinho()
        else:
            self.on_remove_item(btn, item)
    
    def on_remove_item(self, btn, item):
        """Remove item do carrinho"""
        self.carrinho.remove(item)
        self.atualizar_carrinho()
    
    def on_selecionar_cliente(self, btn):
        """Abre diálogo para selecionar cliente"""
        from ..database import db
        
        # Criar diálogo customizado
        dialog = Gtk.Dialog(transient_for=self.get_root(), modal=True)
        dialog.set_title("Selecionar Cliente")
        dialog.set_default_size(500, 400)
        
        # Header
        header = Adw.HeaderBar()
        dialog.get_content_area().append(header)
        
        # Box principal
        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        content.set_margin_top(12)
        content.set_margin_bottom(12)
        content.set_margin_start(12)
        content.set_margin_end(12)
        
        # Busca de cliente
        search_entry = Gtk.Entry()
        search_entry.set_placeholder_text("Buscar por nome ou CPF/CNPJ...")
        content.append(search_entry)
        
        # Lista de clientes
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        
        clientes_list = Gtk.ListBox()
        clientes_list.add_css_class("boxed-list")
        scrolled.set_child(clientes_list)
        content.append(scrolled)
        
        # Carregar clientes
        def carregar_clientes(termo=""):
            # Limpar lista
            while child := clientes_list.get_first_child():
                clientes_list.remove(child)
            
            conn = db.get_connection()
            cursor = conn.cursor()
            
            if termo:
                cursor.execute("""
                    SELECT * FROM clientes 
                    WHERE LOWER(nome) LIKE LOWER(?) OR documento LIKE ?
                    ORDER BY nome
                    LIMIT 50
                """, (f"%{termo}%", f"%{termo}%"))
            else:
                cursor.execute("SELECT * FROM clientes ORDER BY nome LIMIT 50")
            
            clientes = cursor.fetchall()
            conn.close()
            
            if not clientes:
                label = Gtk.Label(label="Nenhum cliente encontrado")
                label.add_css_class("dim-label")
                label.set_margin_top(24)
                label.set_margin_bottom(24)
                clientes_list.append(label)
                return
            
            for cliente in clientes:
                row = Adw.ActionRow(
                    title=cliente['nome'],
                    subtitle=f"CPF/CNPJ: {cliente['documento'] or 'Não informado'}"
                )
                row.cliente_data = cliente
                row.set_activatable(True)
                clientes_list.append(row)
        
        # Conectar busca
        def on_search_changed(entry):
            carregar_clientes(entry.get_text())
        
        search_entry.connect("changed", on_search_changed)
        
        # Carregar lista inicial
        carregar_clientes()
        
        # Botões
        btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        btn_box.set_halign(Gtk.Align.END)
        
        btn_novo = Gtk.Button(label="Cadastrar Novo")
        btn_novo.connect("clicked", lambda b: self.on_cadastro_rapido_cliente(dialog))
        btn_box.append(btn_novo)
        
        btn_cancelar = Gtk.Button(label="Cancelar")
        btn_cancelar.connect("clicked", lambda b: dialog.close())
        btn_box.append(btn_cancelar)
        
        btn_ok = Gtk.Button(label="Selecionar")
        btn_ok.add_css_class("suggested-action")
        
        def on_selecionar():
            selected = clientes_list.get_selected_row()
            if selected and hasattr(selected, 'cliente_data'):
                self.cliente_selecionado = selected.cliente_data
                self.atualizar_cliente_label()
                dialog.close()
        
        btn_ok.connect("clicked", lambda b: on_selecionar())
        btn_box.append(btn_ok)
        
        content.append(btn_box)
        dialog.get_content_area().append(content)
        
        # Permitir seleção ao dar duplo clique
        def on_row_activated(listbox, row):
            if hasattr(row, 'cliente_data'):
                self.cliente_selecionado = row.cliente_data
                self.atualizar_cliente_label()
                dialog.close()
        
        clientes_list.connect("row-activated", on_row_activated)
        
        dialog.present()
    
    def on_cadastro_rapido_cliente(self, parent_dialog):
        """Diálogo para cadastro rápido de cliente"""
        from ..database import db
        
        dialog = Gtk.Dialog(transient_for=self.get_root(), modal=True)
        dialog.set_title("Cadastro Rápido de Cliente")
        dialog.set_default_size(400, 300)
        
        header = Adw.HeaderBar()
        dialog.get_content_area().append(header)
        
        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        content.set_margin_top(12)
        content.set_margin_bottom(12)
        content.set_margin_start(12)
        content.set_margin_end(12)
        
        # Campos
        entry_nome = Adw.EntryRow(title="Nome Completo*")
        content.append(entry_nome)
        
        entry_cpf = Adw.EntryRow(title="CPF/CNPJ*")
        content.append(entry_cpf)
        
        entry_telefone = Adw.EntryRow(title="Telefone")
        content.append(entry_telefone)
        
        entry_email = Adw.EntryRow(title="Email")
        content.append(entry_email)
        
        # Botões
        btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        btn_box.set_halign(Gtk.Align.END)
        btn_box.set_margin_top(12)
        
        btn_cancelar = Gtk.Button(label="Cancelar")
        btn_cancelar.connect("clicked", lambda b: dialog.close())
        btn_box.append(btn_cancelar)
        
        btn_salvar = Gtk.Button(label="Salvar")
        btn_salvar.add_css_class("suggested-action")
        
        def on_salvar():
            nome = entry_nome.get_text().strip()
            cpf = entry_cpf.get_text().strip()
            
            if not nome or not cpf:
                error = Adw.MessageDialog.new(
                    dialog,
                    "Campos Obrigatórios",
                    "Nome e CPF/CNPJ são obrigatórios!"
                )
                error.add_response("ok", "OK")
                error.present()
                return
            
            try:
                conn = db.get_connection()
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO clientes (nome, documento, telefone, email, endereco)
                    VALUES (?, ?, ?, ?, ?)
                """, (nome, cpf, entry_telefone.get_text(), entry_email.get_text(), ""))
                
                cliente_id = cursor.lastrowid
                conn.commit()
                
                # Buscar cliente recém criado
                cursor.execute("SELECT * FROM clientes WHERE id = ?", (cliente_id,))
                self.cliente_selecionado = cursor.fetchone()
                conn.close()
                
                self.atualizar_cliente_label()
                dialog.close()
                if parent_dialog:
                    parent_dialog.close()
                
            except Exception as e:
                conn.rollback()
                error = Adw.MessageDialog.new(
                    dialog,
                    "Erro ao Salvar",
                    f"Erro: {str(e)}"
                )
                error.add_response("ok", "OK")
                error.present()
        
        btn_salvar.connect("clicked", lambda b: on_salvar())
        btn_box.append(btn_salvar)
        
        content.append(btn_box)
        dialog.get_content_area().append(content)
        dialog.present()
    
    def on_remover_cliente(self, btn):
        """Remove cliente selecionado"""
        self.cliente_selecionado = None
        self.atualizar_cliente_label()
    
    def atualizar_cliente_label(self):
        """Atualiza o label mostrando o cliente selecionado"""
        if self.cliente_selecionado:
            nome = self.cliente_selecionado['nome']
            doc = self.cliente_selecionado['documento']
            self.cliente_label.set_text(f"{nome} - CPF/CNPJ: {doc}")
            self.btn_remover_cliente.set_sensitive(True)
        else:
            self.cliente_label.set_text("Nenhum cliente selecionado")
            self.btn_remover_cliente.set_sensitive(False)
    
    
    def on_limpar_carrinho(self, btn):
        """Limpa o carrinho"""
        if not self.carrinho:
            return
        
        dialog = Adw.MessageDialog.new(
            self.get_root(),
            "Limpar Carrinho?",
            "Tem certeza que deseja remover todos os itens?"
        )
        dialog.add_response("cancel", "Cancelar")
        dialog.add_response("clear", "Limpar")
        dialog.set_response_appearance("clear", Adw.ResponseAppearance.DESTRUCTIVE)
        dialog.connect("response", self.on_confirm_limpar)
        dialog.present()
    
    def on_confirm_limpar(self, dialog, response):
        if response == "clear":
            self.carrinho.clear()
            self.atualizar_carrinho()
    
    def on_finalizar_venda(self, btn):
        """Finaliza a venda"""
        if not self.carrinho:
            dialog = Adw.MessageDialog.new(
                self.get_root(),
                "Carrinho Vazio",
                "Adicione produtos antes de finalizar a venda."
            )
            dialog.add_response("ok", "OK")
            dialog.present()
            return
        
        # Dialog para escolher forma de pagamento
        dialog = Adw.MessageDialog.new(
            self.get_root(),
            "Finalizar Venda",
            "Escolha a forma de pagamento:"
        )
        dialog.add_response("dinheiro", "Dinheiro")
        dialog.add_response("debito", "Débito")
        dialog.add_response("credito", "Crédito")
        dialog.add_response("pix", "PIX")
        dialog.add_response("cancel", "Cancelar")
        dialog.set_response_appearance("cancel", Adw.ResponseAppearance.DESTRUCTIVE)
        
        dialog.connect("response", self.on_payment_selected)
        dialog.present()
    
    def on_payment_selected(self, dialog, response):
        """Processa a venda após escolher pagamento"""
        if response == "cancel":
            return
        
        from ..database import db
        
        formas = {
            "dinheiro": "Dinheiro",
            "debito": "Débito",
            "credito": "Crédito",
            "pix": "PIX"
        }
        
        forma_pagamento = formas.get(response, "Dinheiro")
        total = sum(item['preco'] * item['quantidade'] for item in self.carrinho)
        
        # Cliente ID (se selecionado)
        cliente_id = self.cliente_selecionado['id'] if self.cliente_selecionado else None
        
        conn = db.get_connection()
        cursor = conn.cursor()
        
        try:
            # Inserir venda
            cursor.execute("""
                INSERT INTO vendas (cliente_id, total, forma_pagamento, tipo_fiscal)
                VALUES (?, ?, ?, 'Cupom Fiscal')
            """, (cliente_id, total, forma_pagamento))
            
            venda_id = cursor.lastrowid
            
            # Inserir itens
            for item in self.carrinho:
                subtotal = item['preco'] * item['quantidade']
                cursor.execute("""
                    INSERT INTO itens_venda (venda_id, produto_id, quantidade, preco_unitario, total_item)
                    VALUES (?, ?, ?, ?, ?)
                """, (venda_id, item['id'], item['quantidade'], item['preco'], subtotal))
                
                # Atualizar estoque
                cursor.execute("""
                    UPDATE produtos SET estoque = estoque - ? WHERE id = ?
                """, (item['quantidade'], item['id']))
            
            conn.commit()
            
            # Gerar cupom fiscal
            self.gerar_cupom_fiscal(venda_id, forma_pagamento, total, cursor)
            
            # Limpar carrinho e cliente
            self.carrinho.clear()
            self.cliente_selecionado = None
            self.atualizar_carrinho()
            self.atualizar_cliente_label()
            
        except Exception as e:
            conn.rollback()
            error_dialog = Adw.MessageDialog.new(
                self.get_root(),
                "Erro",
                f"Erro ao finalizar venda: {str(e)}"
            )
            error_dialog.add_response("ok", "OK")
            error_dialog.present()
        
        finally:
            conn.close()
    
    def gerar_cupom_fiscal(self, venda_id, forma_pagamento, total, cursor):
        """Gera e exibe o cupom fiscal"""
        # Obter dados da empresa
        cursor.execute("SELECT * FROM configuracoes_empresa WHERE id = 1")
        empresa = cursor.fetchone()
        
        # Obter dados da venda e cliente (se houver)
        cursor.execute("""
            SELECT v.*, c.nome as cliente_nome, c.documento as cliente_cpf
            FROM vendas v
            LEFT JOIN clientes c ON v.cliente_id = c.id
            WHERE v.id = ?
        """, (venda_id,))
        venda = cursor.fetchone()
        
        # Obter itens da venda
        cursor.execute("""
            SELECT iv.*, p.nome, p.codigo_barras
            FROM itens_venda iv
            JOIN produtos p ON iv.produto_id = p.id
            WHERE iv.venda_id = ?
        """, (venda_id,))
        itens = cursor.fetchall()
        
        # Construir cupom fiscal
        cupom = []
        cupom.append("=" * 50)
        cupom.append(empresa['nome_empresa'].center(50))
        
        if empresa['cnpj']:
            cupom.append(f"CNPJ: {empresa['cnpj']}".center(50))
        if empresa['inscricao_estadual']:
            cupom.append(f"IE: {empresa['inscricao_estadual']}".center(50))
        if empresa['endereco']:
            cupom.append(empresa['endereco'].center(50))
        if empresa['cidade'] and empresa['estado']:
            cupom.append(f"{empresa['cidade']} - {empresa['estado']}".center(50))
        if empresa['telefone']:
            cupom.append(f"Tel: {empresa['telefone']}".center(50))
        
        cupom.append("=" * 50)
        cupom.append("CUPOM FISCAL".center(50))
        cupom.append("=" * 50)
        cupom.append(f"Venda nº: {venda_id}")
        cupom.append(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        
        # Dados do cliente (se houver)
        if venda['cliente_nome'] and venda['cliente_cpf']:
            cupom.append("-" * 50)
            cupom.append("DADOS DO CLIENTE:")
            cupom.append(f"Nome: {venda['cliente_nome']}")
            cupom.append(f"CPF/CNPJ: {venda['cliente_cpf']}")
        
        cupom.append("-" * 50)
        cupom.append(f"{'Item':<4} {'Produto':<25} {'Qtd':<5} {'Unit.':<8} {'Total':>8}")
        cupom.append("-" * 50)
        
        for i, item in enumerate(itens, 1):
            nome = item['nome'][:25]
            qtd = item['quantidade']
            preco = item['preco_unitario']
            total_item = item['total_item']
            cupom.append(f"{i:<4} {nome:<25} {qtd:<5} {preco:>7.2f} {total_item:>8.2f}")
        
        cupom.append("-" * 50)
        cupom.append(f"{'TOTAL':>42} R$ {total:>6.2f}")
        cupom.append(f"Forma de Pagamento: {forma_pagamento}")
        cupom.append("=" * 50)
        cupom.append("OBRIGADO PELA PREFERÊNCIA!".center(50))
        cupom.append("=" * 50)
        
        cupom_texto = "\n".join(cupom)
        
        # Exibir cupom em diálogo
        dialog = Gtk.Dialog(transient_for=self.get_root(), modal=True)
        dialog.set_title("Cupom Fiscal")
        dialog.set_default_size(600, 500)
        
        header = Adw.HeaderBar()
        dialog.get_content_area().append(header)
        
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        scrolled.set_hexpand(True)
        scrolled.set_margin_top(12)
        scrolled.set_margin_bottom(12)
        scrolled.set_margin_start(12)
        scrolled.set_margin_end(12)
        
        text_view = Gtk.TextView()
        text_view.set_editable(False)
        text_view.set_monospace(True)
        text_view.get_buffer().set_text(cupom_texto)
        scrolled.set_child(text_view)
        
        dialog.get_content_area().append(scrolled)
        
        # Botões
        btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        btn_box.set_halign(Gtk.Align.CENTER)
        btn_box.set_margin_bottom(12)
        
        btn_imprimir = Gtk.Button(label="Salvar/Imprimir")
        btn_imprimir.add_css_class("suggested-action")
        btn_imprimir.connect("clicked", lambda b: self.salvar_cupom(cupom_texto, venda_id))
        
        btn_fechar = Gtk.Button(label="Fechar")
        btn_fechar.connect("clicked", lambda b: dialog.close())
        
        btn_box.append(btn_imprimir)
        btn_box.append(btn_fechar)
        dialog.get_content_area().append(btn_box)
        
        dialog.present()
    
    def salvar_cupom(self, cupom_texto, venda_id):
        """Salva o cupom fiscal em arquivo"""
        from pathlib import Path
        
        # Criar diretório de cupons
        cupons_dir = Path.home() / "Documentos" / "VendaMais" / "Cupons"
        cupons_dir.mkdir(parents=True, exist_ok=True)
        
        # Nome do arquivo
        filename = cupons_dir / f"cupom_venda_{venda_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        # Salvar arquivo
        filename.write_text(cupom_texto, encoding='utf-8')
        
        # Confirmação
        dialog = Adw.MessageDialog.new(
            self.get_root(),
            "Cupom Salvo",
            f"Cupom fiscal salvo em:\n{filename}"
        )
        dialog.add_response("ok", "OK")
        dialog.present()
