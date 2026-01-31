import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, Gio
import csv
from pathlib import Path

class ConfiguracoesView(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        
        self.set_margin_top(24)
        self.set_margin_bottom(24)
        self.set_margin_start(24)
        self.set_margin_end(24)
        
        title = Gtk.Label(label="Configurações do Sistema")
        title.add_css_class("title-1")
        title.set_halign(Gtk.Align.START)
        self.append(title)
        
        # Notebook com abas
        notebook = Gtk.Notebook()
        notebook.set_vexpand(True)
        
        # Aba 1: Dados da Empresa
        empresa_page = self.criar_pagina_empresa()
        notebook.append_page(empresa_page, Gtk.Label(label="Dados da Empresa"))
        
        # Aba 2: Importação de Dados
        importacao_page = self.criar_pagina_importacao()
        notebook.append_page(importacao_page, Gtk.Label(label="Importar Dados"))
        
        self.append(notebook)
        
        # Carregar dados da empresa
        self.carregar_dados_empresa()
    
    def criar_pagina_empresa(self):
        """Cria a página de configuração dos dados da empresa"""
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        box.set_margin_top(24)
        box.set_margin_bottom(24)
        box.set_margin_start(24)
        box.set_margin_end(24)
        
        # Scrolled window
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        
        form_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        form_box.set_size_request(600, -1)
        form_box.set_halign(Gtk.Align.CENTER)
        
        # Campos do formulário
        subtitle = Gtk.Label(label="Dados que aparecerão no Cupom Fiscal")
        subtitle.add_css_class("title-3")
        subtitle.add_css_class("dim-label")
        subtitle.set_halign(Gtk.Align.START)
        form_box.append(subtitle)
        
        # Nome da Empresa
        self.entry_nome = Adw.EntryRow(title="Nome da Empresa")
        form_box.append(self.entry_nome)
        
        # CNPJ
        self.entry_cnpj = Adw.EntryRow(title="CNPJ")
        form_box.append(self.entry_cnpj)
        
        # Inscrição Estadual
        self.entry_ie = Adw.EntryRow(title="Inscrição Estadual")
        form_box.append(self.entry_ie)
        
        # Endereço
        self.entry_endereco = Adw.EntryRow(title="Endereço")
        form_box.append(self.entry_endereco)
        
        # Cidade
        self.entry_cidade = Adw.EntryRow(title="Cidade")
        form_box.append(self.entry_cidade)
        
        # Estado
        self.entry_estado = Adw.EntryRow(title="Estado (UF)")
        form_box.append(self.entry_estado)
        
        # CEP
        self.entry_cep = Adw.EntryRow(title="CEP")
        form_box.append(self.entry_cep)
        
        # Telefone
        self.entry_telefone = Adw.EntryRow(title="Telefone")
        form_box.append(self.entry_telefone)
        
        # Email
        self.entry_email = Adw.EntryRow(title="Email")
        form_box.append(self.entry_email)
        
        # Botão Salvar
        btn_salvar = Gtk.Button(label="Salvar Configurações")
        btn_salvar.add_css_class("suggested-action")
        btn_salvar.add_css_class("pill")
        btn_salvar.set_margin_top(24)
        btn_salvar.connect("clicked", self.on_salvar_empresa)
        form_box.append(btn_salvar)
        
        scrolled.set_child(form_box)
        box.append(scrolled)
        
        return box
    
    def criar_pagina_importacao(self):
        """Cria a página de importação de dados"""
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=24)
        box.set_margin_top(24)
        box.set_margin_bottom(24)
        box.set_margin_start(24)
        box.set_margin_end(24)
        
        intro = Gtk.Label(label="Importe dados de clientes e produtos em formato CSV")
        intro.add_css_class("title-3")
        box.append(intro)
        
        # Card de Importação de Produtos
        produtos_card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        produtos_card.add_css_class("card")
        produtos_card.set_margin_top(12)
        produtos_card.set_margin_bottom(12)
        produtos_card.set_margin_start(12)
        produtos_card.set_margin_end(12)
        
        produtos_title = Gtk.Label(label="Importar Produtos")
        produtos_title.add_css_class("title-2")
        produtos_title.set_halign(Gtk.Align.START)
        produtos_card.append(produtos_title)
        
        produtos_desc = Gtk.Label(
            label="Formato CSV: nome,codigo_barras,preco_compra,preco_venda,estoque,ncm,tributacao"
        )
        produtos_desc.add_css_class("caption")
        produtos_desc.add_css_class("dim-label")
        produtos_desc.set_halign(Gtk.Align.START)
        produtos_desc.set_wrap(True)
        produtos_card.append(produtos_desc)
        
        btn_produtos = Gtk.Button(label="Selecionar Arquivo CSV de Produtos")
        btn_produtos.connect("clicked", self.on_importar_produtos)
        produtos_card.append(btn_produtos)
        
        btn_modelo_produtos = Gtk.Button(label="Baixar Modelo CSV")
        btn_modelo_produtos.add_css_class("flat")
        btn_modelo_produtos.connect("clicked", self.on_baixar_modelo_produtos)
        produtos_card.append(btn_modelo_produtos)
        
        box.append(produtos_card)
        
        # Card de Importação de Clientes
        clientes_card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        clientes_card.add_css_class("card")
        clientes_card.set_margin_top(12)
        clientes_card.set_margin_bottom(12)
        clientes_card.set_margin_start(12)
        clientes_card.set_margin_end(12)
        
        clientes_title = Gtk.Label(label="Importar Clientes")
        clientes_title.add_css_class("title-2")
        clientes_title.set_halign(Gtk.Align.START)
        clientes_card.append(clientes_title)
        
        clientes_desc = Gtk.Label(
            label="Formato CSV: nome,documento,telefone,email,endereco"
        )
        clientes_desc.add_css_class("caption")
        clientes_desc.add_css_class("dim-label")
        clientes_desc.set_halign(Gtk.Align.START)
        clientes_desc.set_wrap(True)
        clientes_card.append(clientes_desc)
        
        btn_clientes = Gtk.Button(label="Selecionar Arquivo CSV de Clientes")
        btn_clientes.connect("clicked", self.on_importar_clientes)
        clientes_card.append(btn_clientes)
        
        btn_modelo_clientes = Gtk.Button(label="Baixar Modelo CSV")
        btn_modelo_clientes.add_css_class("flat")
        btn_modelo_clientes.connect("clicked", self.on_baixar_modelo_clientes)
        clientes_card.append(btn_modelo_clientes)
        
        box.append(clientes_card)
        
        return box
    
    def carregar_dados_empresa(self):
        """Carrega os dados da empresa do banco de dados"""
        from ..database import db
        
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM configuracoes_empresa WHERE id = 1")
        empresa = cursor.fetchone()
        conn.close()
        
        if empresa:
            self.entry_nome.set_text(empresa['nome_empresa'] or "")
            self.entry_cnpj.set_text(empresa['cnpj'] or "")
            self.entry_ie.set_text(empresa['inscricao_estadual'] or "")
            self.entry_endereco.set_text(empresa['endereco'] or "")
            self.entry_cidade.set_text(empresa['cidade'] or "")
            self.entry_estado.set_text(empresa['estado'] or "")
            self.entry_cep.set_text(empresa['cep'] or "")
            self.entry_telefone.set_text(empresa['telefone'] or "")
            self.entry_email.set_text(empresa['email'] or "")
    
    def on_salvar_empresa(self, btn):
        """Salva os dados da empresa"""
        from ..database import db
        
        conn = db.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                UPDATE configuracoes_empresa 
                SET nome_empresa = ?, cnpj = ?, inscricao_estadual = ?,
                    endereco = ?, cidade = ?, estado = ?, cep = ?,
                    telefone = ?, email = ?
                WHERE id = 1
            """, (
                self.entry_nome.get_text(),
                self.entry_cnpj.get_text(),
                self.entry_ie.get_text(),
                self.entry_endereco.get_text(),
                self.entry_cidade.get_text(),
                self.entry_estado.get_text(),
                self.entry_cep.get_text(),
                self.entry_telefone.get_text(),
                self.entry_email.get_text()
            ))
            
            conn.commit()
            
            dialog = Adw.MessageDialog.new(
                self.get_root(),
                "Dados Salvos",
                "Configurações da empresa salvas com sucesso!"
            )
            dialog.add_response("ok", "OK")
            dialog.present()
            
        except Exception as e:
            conn.rollback()
            dialog = Adw.MessageDialog.new(
                self.get_root(),
                "Erro",
                f"Erro ao salvar: {str(e)}"
            )
            dialog.add_response("ok", "OK")
            dialog.present()
        
        finally:
            conn.close()
    
    def on_importar_produtos(self, btn):
        """Abre diálogo para selecionar arquivo CSV de produtos"""
        file_dialog = Gtk.FileDialog()
        file_dialog.set_title("Selecionar arquivo CSV de produtos")
        
        # Filtro para CSV
        filter_csv = Gtk.FileFilter()
        filter_csv.set_name("Arquivos CSV")
        filter_csv.add_pattern("*.csv")
        
        filters = Gio.ListStore.new(Gtk.FileFilter)
        filters.append(filter_csv)
        file_dialog.set_filters(filters)
        
        file_dialog.open(self.get_root(), None, self.on_arquivo_produtos_selecionado)
    
    def on_arquivo_produtos_selecionado(self, dialog, result):
        """Processa o arquivo CSV de produtos selecionado"""
        try:
            file = dialog.open_finish(result)
            if file:
                caminho = file.get_path()
                self.importar_produtos_csv(caminho)
        except Exception as e:
            if "dismissed" not in str(e).lower():
                dialog = Adw.MessageDialog.new(
                    self.get_root(),
                    "Erro",
                    f"Erro ao abrir arquivo: {str(e)}"
                )
                dialog.add_response("ok", "OK")
                dialog.present()
    
    def importar_produtos_csv(self, caminho):
        """Importa produtos do arquivo CSV"""
        from ..database import db
        
        try:
            importados = 0
            erros = 0
            
            with open(caminho, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                conn = db.get_connection()
                cursor = conn.cursor()
                
                for row in reader:
                    try:
                        cursor.execute("""
                            INSERT INTO produtos (nome, codigo_barras, preco_compra, preco_venda, estoque, ncm, tributacao)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                        """, (
                            row.get('nome', ''),
                            row.get('codigo_barras', ''),
                            float(row.get('preco_compra', 0)),
                            float(row.get('preco_venda', 0)),
                            int(row.get('estoque', 0)),
                            row.get('ncm', ''),
                            float(row.get('tributacao', 0))
                        ))
                        importados += 1
                    except Exception as e:
                        erros += 1
                        print(f"Erro ao importar linha: {e}")
                
                conn.commit()
                conn.close()
            
            dialog = Adw.MessageDialog.new(
                self.get_root(),
                "Importação Concluída",
                f"Produtos importados: {importados}\nErros: {erros}"
            )
            dialog.add_response("ok", "OK")
            dialog.present()
            
        except Exception as e:
            dialog = Adw.MessageDialog.new(
                self.get_root(),
                "Erro na Importação",
                f"Erro: {str(e)}"
            )
            dialog.add_response("ok", "OK")
            dialog.present()
    
    def on_importar_clientes(self, btn):
        """Abre diálogo para selecionar arquivo CSV de clientes"""
        file_dialog = Gtk.FileDialog()
        file_dialog.set_title("Selecionar arquivo CSV de clientes")
        
        # Filtro para CSV
        filter_csv = Gtk.FileFilter()
        filter_csv.set_name("Arquivos CSV")
        filter_csv.add_pattern("*.csv")
        
        filters = Gio.ListStore.new(Gtk.FileFilter)
        filters.append(filter_csv)
        file_dialog.set_filters(filters)
        
        file_dialog.open(self.get_root(), None, self.on_arquivo_clientes_selecionado)
    
    def on_arquivo_clientes_selecionado(self, dialog, result):
        """Processa o arquivo CSV de clientes selecionado"""
        try:
            file = dialog.open_finish(result)
            if file:
                caminho = file.get_path()
                self.importar_clientes_csv(caminho)
        except Exception as e:
            if "dismissed" not in str(e).lower():
                dialog = Adw.MessageDialog.new(
                    self.get_root(),
                    "Erro",
                    f"Erro ao abrir arquivo: {str(e)}"
                )
                dialog.add_response("ok", "OK")
                dialog.present()
    
    def importar_clientes_csv(self, caminho):
        """Importa clientes do arquivo CSV"""
        from ..database import db
        
        try:
            importados = 0
            erros = 0
            
            with open(caminho, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                conn = db.get_connection()
                cursor = conn.cursor()
                
                for row in reader:
                    try:
                        cursor.execute("""
                            INSERT INTO clientes (nome, documento, telefone, email, endereco)
                            VALUES (?, ?, ?, ?, ?)
                        """, (
                            row.get('nome', ''),
                            row.get('documento', ''),
                            row.get('telefone', ''),
                            row.get('email', ''),
                            row.get('endereco', '')
                        ))
                        importados += 1
                    except Exception as e:
                        erros += 1
                        print(f"Erro ao importar linha: {e}")
                
                conn.commit()
                conn.close()
            
            dialog = Adw.MessageDialog.new(
                self.get_root(),
                "Importação Concluída",
                f"Clientes importados: {importados}\nErros: {erros}"
            )
            dialog.add_response("ok", "OK")
            dialog.present()
            
        except Exception as e:
            dialog = Adw.MessageDialog.new(
                self.get_root(),
                "Erro na Importação",
                f"Erro: {str(e)}"
            )
            dialog.add_response("ok", "OK")
            dialog.present()
    
    def on_baixar_modelo_produtos(self, btn):
        """Cria arquivo modelo CSV para produtos"""
        modelo_dir = Path.home() / "Documentos" / "VendaMais" / "Modelos"
        modelo_dir.mkdir(parents=True, exist_ok=True)
        
        arquivo = modelo_dir / "modelo_produtos.csv"
        
        with open(arquivo, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['nome', 'codigo_barras', 'preco_compra', 'preco_venda', 'estoque', 'ncm', 'tributacao'])
            writer.writerow(['Produto Exemplo', '7891234567890', '10.00', '15.00', '100', '12345678', '0.0'])
        
        dialog = Adw.MessageDialog.new(
            self.get_root(),
            "Modelo Criado",
            f"Modelo salvo em:\n{arquivo}"
        )
        dialog.add_response("ok", "OK")
        dialog.present()
    
    def on_baixar_modelo_clientes(self, btn):
        """Cria arquivo modelo CSV para clientes"""
        modelo_dir = Path.home() / "Documentos" / "VendaMais" / "Modelos"
        modelo_dir.mkdir(parents=True, exist_ok=True)
        
        arquivo = modelo_dir / "modelo_clientes.csv"
        
        with open(arquivo, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['nome', 'documento', 'telefone', 'email', 'endereco'])
            writer.writerow(['Cliente Exemplo', '12345678900', '(11) 98765-4321', 'cliente@email.com', 'Rua Exemplo, 123'])
        
        dialog = Adw.MessageDialog.new(
            self.get_root(),
            "Modelo Criado",
            f"Modelo salvo em:\n{arquivo}"
        )
        dialog.add_response("ok", "OK")
        dialog.present()
