#!/usr/bin/env python3
"""
Script para popular o banco de dados com produtos de exemplo
"""

import sqlite3
from pathlib import Path

# Caminho do banco de dados
db_path = Path(__file__).parent / "data" / "vendamais.db"

# Produtos de exemplo
produtos_exemplo = [
    ("Coca-Cola 2L", "7894900011517", 4.50, 7.99, 50, "22021000", 0.0),
    ("Arroz Tipo 1 5kg", "7896004711027", 15.00, 22.90, 30, "10063020", 0.0),
    ("Feijão Preto 1kg", "7896004711034", 5.50, 8.90, 40, "07133300", 0.0),
    ("Óleo de Soja 900ml", "7896004711041", 4.00, 6.50, 25, "15071000", 0.0),
    ("Açúcar Cristal 1kg", "7896004711058", 2.50, 4.20, 35, "17011100", 0.0),
    ("Café Torrado 500g", "7896004711065", 8.00, 14.90, 20, "09012100", 0.0),
    ("Leite Integral 1L", "7896004711072", 3.20, 5.50, 45, "04011000", 0.0),
    ("Macarrão Espaguete 500g", "7896004711089", 2.00, 3.80, 60, "19021100", 0.0),
    ("Farinha de Trigo 1kg", "7896004711096", 3.00, 5.20, 28, "11010000", 0.0),
    ("Sal Refinado 1kg", "7896004711102", 1.00, 1.99, 50, "25010010", 0.0),
    ("Sabão em Pó 1kg", "7896004711119", 6.50, 11.90, 15, "34022010", 0.0),
    ("Papel Higiênico 12 rolos", "7896004711126", 8.00, 14.50, 22, "48030010", 0.0),
    ("Detergente Líquido 500ml", "7896004711133", 1.50, 2.90, 38, "34022090", 0.0),
    ("Sabonete 90g", "7896004711140", 1.20, 2.50, 42, "34011190", 0.0),
    ("Água Sanitária 1L", "7896004711157", 2.00, 3.80, 30, "28289000", 0.0),
    ("Biscoito Cream Cracker", "7896004711164", 2.50, 4.50, 35, "19053100", 0.0),
    ("Achocolatado em Pó 400g", "7896004711171", 4.50, 7.90, 25, "18069000", 0.0),
    ("Extrato de Tomate 340g", "7896004711188", 2.20, 3.90, 33, "20029000", 0.0),
    ("Molho de Tomate 340g", "7896004711195", 1.80, 3.20, 40, "21032000", 0.0),
    ("Vinagre 750ml", "7896004711201", 1.50, 2.80, 28, "22090000", 0.0),
]

def popular_banco():
    """Popula o banco com produtos de exemplo"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar se já tem produtos
        cursor.execute("SELECT COUNT(*) FROM produtos")
        count = cursor.fetchone()[0]
        
        if count > 0:
            print(f"⚠️  Banco já possui {count} produtos.")
            resposta = input("Deseja adicionar mais produtos de exemplo? (s/n): ")
            if resposta.lower() != 's':
                print("Operação cancelada.")
                return
        
        # Inserir produtos
        inseridos = 0
        erros = 0
        
        for produto in produtos_exemplo:
            try:
                cursor.execute("""
                    INSERT INTO produtos (nome, codigo_barras, preco_compra, preco_venda, estoque, ncm, tributacao)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, produto)
                inseridos += 1
            except sqlite3.IntegrityError:
                erros += 1
                print(f"❌ Produto já existe: {produto[0]}")
            except Exception as e:
                erros += 1
                print(f"❌ Erro ao inserir {produto[0]}: {e}")
        
        conn.commit()
        conn.close()
        
        print(f"\n✅ Produtos inseridos: {inseridos}")
        print(f"⚠️  Erros/Duplicados: {erros}")
        print(f"📦 Total no banco: {count + inseridos}")
        
    except Exception as e:
        print(f"❌ Erro ao conectar ao banco: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("POPULAR BANCO DE DADOS - VENDAMAIS")
    print("=" * 60)
    print()
    
    if not db_path.exists():
        print(f"❌ Banco de dados não encontrado em: {db_path}")
        print("Execute o aplicativo primeiro para criar o banco.")
    else:
        popular_banco()
    
    print()
    print("=" * 60)
