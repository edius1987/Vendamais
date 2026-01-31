import sqlite3
import os
from datetime import datetime
from pathlib import Path
import shutil

class Database:
    def __init__(self):
        # Cria diretório data se não existir
        data_dir = Path(__file__).parent.parent / "data"
        data_dir.mkdir(exist_ok=True)
        self.db_path = data_dir / "vendamais.db"
        self.init_db()
    
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_db(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tabela de Produtos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                codigo_barras TEXT UNIQUE,
                preco_compra REAL NOT NULL DEFAULT 0.0,
                preco_venda REAL NOT NULL,
                estoque INTEGER NOT NULL DEFAULT 0,
                ncm TEXT,
                tributacao REAL DEFAULT 0.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tabela de Clientes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                documento TEXT UNIQUE,
                telefone TEXT,
                email TEXT,
                endereco TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tabela de Vendas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vendas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER,
                data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                total REAL NOT NULL,
                forma_pagamento TEXT,
                tipo_fiscal TEXT,
                FOREIGN KEY (cliente_id) REFERENCES clientes(id)
            )
        """)
        
        # Tabela de Itens da Venda
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS itens_venda (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                venda_id INTEGER NOT NULL,
                produto_id INTEGER NOT NULL,
                quantidade INTEGER NOT NULL,
                preco_unitario REAL NOT NULL,
                total_item REAL NOT NULL,
                FOREIGN KEY (venda_id) REFERENCES vendas(id),
                FOREIGN KEY (produto_id) REFERENCES produtos(id)
            )
        """)
        
        # Tabela de Configurações da Empresa
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS configuracoes_empresa (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                nome_empresa TEXT NOT NULL DEFAULT 'Minha Empresa',
                cnpj TEXT,
                inscricao_estadual TEXT,
                endereco TEXT,
                telefone TEXT,
                email TEXT,
                cidade TEXT,
                estado TEXT,
                cep TEXT
            )
        """)
        
        # Inserir configuração padrão se não existir
        cursor.execute("SELECT COUNT(*) as count FROM configuracoes_empresa WHERE id = 1")
        if cursor.fetchone()['count'] == 0:
            cursor.execute("""
                INSERT INTO configuracoes_empresa (id, nome_empresa) 
                VALUES (1, 'Minha Empresa')
            """)
        
        # Índices para performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_produto_codigo ON produtos(codigo_barras)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_venda_data ON vendas(data_hora)")
        
        conn.commit()
        conn.close()
    
    def backup(self):
        """Cria backup do banco de dados"""
        backup_path = f"{self.db_path}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.copy2(self.db_path, backup_path)
        return backup_path

db = Database()
