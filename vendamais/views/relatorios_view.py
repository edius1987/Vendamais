import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw
from datetime import datetime
import csv

class RelatoriosView(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        
        self.set_margin_top(24)
        self.set_margin_bottom(24)
        self.set_margin_start(24)
        self.set_margin_end(24)
        
        title = Gtk.Label(label="Relatórios e Análises")
        title.add_css_class("title-1")
        title.set_halign(Gtk.Align.START)
        self.append(title)
        
        # Cards de resumo
        cards_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        cards_box.set_homogeneous(True)
        
        self.card_vendas_dia = self.criar_card("Vendas Hoje", "R$ 0,00")
        self.card_vendas_mes = self.criar_card("Vendas Mês", "R$ 0,00")
        self.card_estoque_baixo = self.criar_card("Produtos com Estoque Baixo", "0")
        
        cards_box.append(self.card_vendas_dia)
        cards_box.append(self.card_vendas_mes)
        cards_box.append(self.card_estoque_baixo)
        self.append(cards_box)
        
        # Ações
        actions_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        actions_box.set_margin_top(24)
        actions_box.set_margin_bottom(12)
        
        btn_vendas_csv = Gtk.Button(label="Exportar Vendas (CSV)")
        btn_vendas_csv.connect("clicked", self.on_export_vendas)
        actions_box.append(btn_vendas_csv)
        
        btn_produtos_csv = Gtk.Button(label="Exportar Produtos (CSV)")
        btn_produtos_csv.connect("clicked", self.on_export_produtos)
        actions_box.append(btn_produtos_csv)
        
        btn_graficos = Gtk.Button(label="Gráficos de Estoque")
        btn_graficos.add_css_class("suggested-action")
        btn_graficos.connect("clicked", self.on_mostrar_graficos)
        actions_box.append(btn_graficos)
        
        btn_atualizar = Gtk.Button(label="Atualizar Dados")
        btn_atualizar.connect("clicked", self.atualizar_resumo)
        actions_box.append(btn_atualizar)
        
        self.append(actions_box)
        
        # Lista de vendas recentes
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        
        self.vendas_list = Gtk.ListBox()
        self.vendas_list.add_css_class("boxed-list")
        
        scrolled.set_child(self.vendas_list)
        self.append(scrolled)
        
        self.atualizar_resumo()
    
    def criar_card(self, titulo, valor):
        card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        card.add_css_class("card")
        card.set_margin_top(12)
        card.set_margin_bottom(12)
        card.set_margin_start(12)
        card.set_margin_end(12)
        card.set_size_request(200, 100)
        
        label_titulo = Gtk.Label(label=titulo)
        label_titulo.add_css_class("caption")
        label_titulo.add_css_class("dim-label")
        card.append(label_titulo)
        
        label_valor = Gtk.Label(label=valor)
        label_valor.add_css_class("title-1")
        card.append(label_valor)
        
        return card
    
    def atualizar_resumo(self, btn=None):
        from ..database import db
        
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # Vendas do dia
        hoje = datetime.now().strftime('%Y-%m-%d')
        cursor.execute("""
            SELECT COALESCE(SUM(total), 0) as total 
            FROM vendas 
            WHERE date(data_hora) = ?
        """, (hoje,))
        vendas_dia = cursor.fetchone()['total']
        
        # Vendas do mês
        primeiro_dia = datetime.now().replace(day=1).strftime('%Y-%m-%d')
        cursor.execute("""
            SELECT COALESCE(SUM(total), 0) as total 
            FROM vendas 
            WHERE date(data_hora) >= ?
        """, (primeiro_dia,))
        vendas_mes = cursor.fetchone()['total']
        
        # Estoque baixo
        cursor.execute("SELECT COUNT(*) as total FROM produtos WHERE estoque <= 5")
        estoque_baixo = cursor.fetchone()['total']
        
        # Atualizar cards
        card_valor = self.card_vendas_dia.get_last_child()
        card_valor.set_text(f"R$ {vendas_dia:.2f}")
        
        card_valor = self.card_vendas_mes.get_last_child()
        card_valor.set_text(f"R$ {vendas_mes:.2f}")
        
        card_valor = self.card_estoque_baixo.get_last_child()
        card_valor.set_text(str(estoque_baixo))
        if estoque_baixo > 0:
            self.card_estoque_baixo.add_css_class("error")
        
        # Lista de vendas recentes
        while child := self.vendas_list.get_first_child():
            self.vendas_list.remove(child)
        
        cursor.execute("""
            SELECT v.*, c.nome as cliente_nome 
            FROM vendas v 
            LEFT JOIN clientes c ON v.cliente_id = c.id 
            ORDER BY v.data_hora DESC 
            LIMIT 50
        """)
        vendas = cursor.fetchall()
        
        for venda in vendas:
            cliente = venda['cliente_nome'] or "Consumidor Final"
            row = Adw.ActionRow(
                title=f"Venda #{venda['id']} - {cliente}",
                subtitle=str(venda['data_hora'])
            )
            total = Gtk.Label(label=f"R$ {venda['total']:.2f}")
            total.add_css_class("monospace")
            total.add_css_class("title-4")
            row.add_suffix(total)
            self.vendas_list.append(row)
        
        conn.close()
    
    def on_export_vendas(self, btn):
        from ..database import db
        
        filename = f"vendas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT v.id, v.data_hora, c.nome as cliente, v.total, v.forma_pagamento 
            FROM vendas v 
            LEFT JOIN clientes c ON v.cliente_id = c.id
            ORDER BY v.data_hora DESC
        """)
        vendas = cursor.fetchall()
        conn.close()
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Data/Hora', 'Cliente', 'Total', 'Forma Pagamento'])
            for v in vendas:
                writer.writerow([v['id'], v['data_hora'], v['cliente'], 
                               v['total'], v['forma_pagamento']])
        
        dialog = Adw.MessageDialog.new(self.get_root(), "Exportação Concluída", 
                                       f"Vendas exportadas para: {filename}")
        dialog.add_response("ok", "OK")
        dialog.present()
    
    def on_export_produtos(self, btn):
        from ..database import db
        
        filename = f"produtos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM produtos ORDER BY nome")
        produtos = cursor.fetchall()
        conn.close()
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Nome', 'Código de Barras', 'Preço Compra', 
                           'Preço Venda', 'Estoque', 'NCM', 'Tributação'])
            for p in produtos:
                writer.writerow([p['id'], p['nome'], p['codigo_barras'], 
                               p['preco_compra'], p['preco_venda'], p['estoque'],
                               p['ncm'], p['tributacao']])
        
        dialog = Adw.MessageDialog.new(self.get_root(), "Exportação Concluída", 
                                       f"Produtos exportados para: {filename}")
        dialog.add_response("ok", "OK")
        dialog.present()
    
    def on_mostrar_graficos(self, btn):
        """Mostra diálogo com opções de gráficos"""
        dialog = Adw.MessageDialog.new(
            self.get_root(),
            "Gráficos de Estoque",
            "Escolha o tipo de gráfico que deseja visualizar:"
        )
        dialog.add_response("estoque_atual", "Estoque Atual (Top 20)")
        dialog.add_response("estoque_baixo", "Produtos com Estoque Baixo")
        dialog.add_response("mais_vendidos", "Produtos Mais Vendidos")
        dialog.add_response("cancel", "Cancelar")
        dialog.set_response_appearance("cancel", Adw.ResponseAppearance.DESTRUCTIVE)
        
        dialog.connect("response", self.on_tipo_grafico_selecionado)
        dialog.present()
    
    def on_tipo_grafico_selecionado(self, dialog, response):
        """Processa a escolha do tipo de gráfico"""
        if response == "cancel":
            return
        
        tipos = {
            "estoque_atual": self.gerar_grafico_estoque_atual,
            "estoque_baixo": self.gerar_grafico_estoque_baixo,
            "mais_vendidos": self.gerar_grafico_mais_vendidos
        }
        
        metodo = tipos.get(response)
        if metodo:
            metodo()
    
    def gerar_grafico_estoque_atual(self):
        """Gera gráfico de estoque atual dos top 20 produtos"""
        try:
            import matplotlib
            matplotlib.use('Agg')
            import matplotlib.pyplot as plt
            from ..database import db
            from pathlib import Path
            
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT nome, estoque FROM produtos 
                ORDER BY estoque DESC 
                LIMIT 20
            """)
            dados = cursor.fetchall()
            conn.close()
            
            if not dados:
                self.mostrar_erro("Nenhum produto encontrado")
                return
            
            nomes = [d['nome'][:20] for d in dados]
            estoques = [d['estoque'] for d in dados]
            
            # Criar gráfico
            plt.figure(figsize=(12, 6))
            plt.bar(range(len(nomes)), estoques, color='#3584e4')
            plt.xlabel('Produtos')
            plt.ylabel('Quantidade em Estoque')
            plt.title('Top 20 Produtos por Estoque')
            plt.xticks(range(len(nomes)), nomes, rotation=45, ha='right')
            plt.tight_layout()
            
            # Salvar e exibir
            graficos_dir = Path.home() / "Documentos" / "VendaMais" / "Graficos"
            graficos_dir.mkdir(parents=True, exist_ok=True)
            filename = graficos_dir / f"estoque_atual_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            plt.savefig(filename, dpi=150, bbox_inches='tight')
            plt.close()
            
            self.mostrar_grafico(filename, "Gráfico de Estoque Atual")
            
        except ImportError:
            self.mostrar_erro("Biblioteca matplotlib não instalada.\nInstale com: pip install matplotlib")
        except Exception as e:
            self.mostrar_erro(f"Erro ao gerar gráfico: {str(e)}")
    
    def gerar_grafico_estoque_baixo(self):
        """Gera gráfico de produtos com estoque baixo"""
        try:
            import matplotlib
            matplotlib.use('Agg')
            import matplotlib.pyplot as plt
            from ..database import db
            from pathlib import Path
            
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT nome, estoque FROM produtos 
                WHERE estoque <= 10
                ORDER BY estoque ASC
                LIMIT 20
            """)
            dados = cursor.fetchall()
            conn.close()
            
            if not dados:
                self.mostrar_erro("Nenhum produto com estoque baixo")
                return
            
            nomes = [d['nome'][:20] for d in dados]
            estoques = [d['estoque'] for d in dados]
            
            # Criar gráfico com cores baseadas no nível
            cores = ['#e01b24' if e <= 5 else '#f6d32d' for e in estoques]
            
            plt.figure(figsize=(12, 6))
            plt.barh(range(len(nomes)), estoques, color=cores)
            plt.ylabel('Produtos')
            plt.xlabel('Quantidade em Estoque')
            plt.title('Produtos com Estoque Baixo (≤ 10 unidades)')
            plt.yticks(range(len(nomes)), nomes)
            plt.tight_layout()
            
            # Salvar e exibir
            graficos_dir = Path.home() / "Documentos" / "VendaMais" / "Graficos"
            graficos_dir.mkdir(parents=True, exist_ok=True)
            filename = graficos_dir / f"estoque_baixo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            plt.savefig(filename, dpi=150, bbox_inches='tight')
            plt.close()
            
            self.mostrar_grafico(filename, "Produtos com Estoque Baixo")
            
        except ImportError:
            self.mostrar_erro("Biblioteca matplotlib não instalada.\nInstale com: pip install matplotlib")
        except Exception as e:
            self.mostrar_erro(f"Erro ao gerar gráfico: {str(e)}")
    
    def gerar_grafico_mais_vendidos(self):
        """Gera gráfico dos produtos mais vendidos"""
        try:
            import matplotlib
            matplotlib.use('Agg')
            import matplotlib.pyplot as plt
            from ..database import db
            from pathlib import Path
            
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT p.nome, SUM(iv.quantidade) as total_vendido
                FROM itens_venda iv
                JOIN produtos p ON iv.produto_id = p.id
                GROUP BY p.id
                ORDER BY total_vendido DESC
                LIMIT 15
            """)
            dados = cursor.fetchall()
            conn.close()
            
            if not dados:
                self.mostrar_erro("Nenhuma venda registrada")
                return
            
            nomes = [d['nome'][:20] for d in dados]
            vendidos = [d['total_vendido'] for d in dados]
            
            # Criar gráfico
            plt.figure(figsize=(12, 6))
            plt.bar(range(len(nomes)), vendidos, color='#26a269')
            plt.xlabel('Produtos')
            plt.ylabel('Quantidade Vendida')
            plt.title('Top 15 Produtos Mais Vendidos')
            plt.xticks(range(len(nomes)), nomes, rotation=45, ha='right')
            plt.tight_layout()
            
            # Salvar e exibir
            graficos_dir = Path.home() / "Documentos" / "VendaMais" / "Graficos"
            graficos_dir.mkdir(parents=True, exist_ok=True)
            filename = graficos_dir / f"mais_vendidos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            plt.savefig(filename, dpi=150, bbox_inches='tight')
            plt.close()
            
            self.mostrar_grafico(filename, "Produtos Mais Vendidos")
            
        except ImportError:
            self.mostrar_erro("Biblioteca matplotlib não instalada.\nInstale com: pip install matplotlib")
        except Exception as e:
            self.mostrar_erro(f"Erro ao gerar gráfico: {str(e)}")
    
    def mostrar_grafico(self, filename, titulo):
        """Exibe o gráfico em um diálogo"""
        dialog = Gtk.Dialog(transient_for=self.get_root(), modal=True)
        dialog.set_title(titulo)
        dialog.set_default_size(900, 600)
        
        header = Adw.HeaderBar()
        dialog.get_content_area().append(header)
        
        # Mostrar imagem
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        scrolled.set_hexpand(True)
        
        picture = Gtk.Picture.new_for_filename(str(filename))
        picture.set_can_shrink(True)
        scrolled.set_child(picture)
        
        dialog.get_content_area().append(scrolled)
        
        # Botões
        btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        btn_box.set_halign(Gtk.Align.CENTER)
        btn_box.set_margin_top(12)
        btn_box.set_margin_bottom(12)
        
        btn_info = Gtk.Label(label=f"Salvo em: {filename}")
        btn_info.add_css_class("caption")
        btn_info.add_css_class("dim-label")
        
        btn_fechar = Gtk.Button(label="Fechar")
        btn_fechar.add_css_class("suggested-action")
        btn_fechar.connect("clicked", lambda b: dialog.close())
        
        btn_box.append(btn_info)
        btn_box.append(btn_fechar)
        dialog.get_content_area().append(btn_box)
        
        dialog.present()
    
    def mostrar_erro(self, mensagem):
        """Mostra diálogo de erro"""
        dialog = Adw.MessageDialog.new(
            self.get_root(),
            "Erro",
            mensagem
        )
        dialog.add_response("ok", "OK")
        dialog.present()

