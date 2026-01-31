# Arquitetura do VendaMais

## Visão Geral

O VendaMais é um sistema de gestão de vendas desenvolvido com foco em simplicidade, performance e experiência do usuário. A arquitetura segue o padrão de separação de responsabilidades, com camadas bem definidas.

## Tecnologias Principais

### Frontend
- **GTK4**: Framework moderno para interfaces gráficas nativas Linux
- **Libadwaita**: Biblioteca de componentes do GNOME para design consistente
- **PyGObject**: Bindings Python para GTK

### Backend
- **Python 3.12+**: Linguagem principal
- **SQLite**: Banco de dados relacional leve e eficiente
- **Matplotlib 3.8+**: Geração de gráficos e visualizações
- **uv**: Gerenciador de pacotes moderno e rápido

## Estrutura de Camadas

```
┌─────────────────────────────────────────┐
│         Interface (GTK4)                │
│  - VendaMaisApp                         │
│  - MainWindow                           │
│  - Views (Vendas, Produtos, etc.)       │
└─────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────┐
│      Lógica de Negócio                  │
│  - Validações                           │
│  - Cálculos                             │
│  - Regras de negócio                    │
│  - Geração de cupons fiscais            │
│  - Geração de gráficos                  │
└─────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────┐
│     Camada de Dados (Database)          │
│  - CRUD de produtos                     │
│  - CRUD de clientes                     │
│  - Gestão de vendas                     │
│  - Configurações da empresa             │
│  - Importação/Exportação CSV            │
│  - Relatórios e gráficos                │
└─────────────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────┐
│        SQLite Database                  │
│  vendamais.db                           │
└─────────────────────────────────────────┘
```

## Componentes Principais

### 1. VendaMaisApp (Aplicação)
- Herda de `Adw.Application`
- Gerencia o ciclo de vida da aplicação
- Inicializa o banco de dados
- Cria a janela principal
- Define actions globais (backup, about)

### 2. MainWindow (Janela Principal)
- Herda de `Adw.ApplicationWindow`
- Contém o `Gtk.Stack` para navegação entre páginas
- Gerencia o header bar com `StackSwitcher`
- Menu de ações (Backup, Sobre)
- Coordena as diferentes views

### 3. Views (Páginas)

#### VendasView (PDV)
- **Busca interativa** de produtos com autocomplete
- **Timer de busca** (300ms) para otimização
- **Carrinho de compras** com controle de quantidade (+/-)
- **Seleção opcional de cliente** com busca
- **Cadastro rápido de cliente** inline
- **Validação de estoque** em tempo real
- **Finalização de vendas** com múltiplas formas de pagamento
- **Geração de cupom fiscal** com dados empresa e cliente
- **Baixa automática de estoque**
- Salva cupons em `~/Documentos/VendaMais/Cupons/`

#### ProdutosView
- Listagem de produtos
- Cadastro e edição completos
- Campos: nome, código de barras, preços, estoque, NCM, tributação
- Busca e filtragem
- Exportação para CSV
- Alertas de estoque baixo

#### ClientesView
- Cadastro de clientes com CPF/CNPJ
- Busca por nome ou documento
- Dados completos: telefone, email, endereço
- Importação via CSV

#### RelatoriosView
- Dashboard com métricas em tempo real
- Cards: Vendas do dia, Vendas do mês, Estoque baixo
- Lista de vendas recentes
- Exportação de vendas (CSV)
- Exportação de produtos (CSV)
- **Gráficos de estoque** com matplotlib:
  - Estoque atual (Top 20 produtos)
  - Produtos com estoque baixo (cores de alerta)
  - Produtos mais vendidos (Top 15)
- Gráficos salvos em `~/Documentos/VendaMais/Graficos/`

#### ConfiguracoesView
- **Aba 1: Dados da Empresa**
  - Nome, CNPJ, Inscrição Estadual
  - Endereço completo, telefone, email
  - Dados usados no cupom fiscal
- **Aba 2: Importação de Dados**
  - Importar produtos via CSV
  - Importar clientes via CSV
  - Download de modelos CSV com exemplos
  - Modelos salvos em `~/Documentos/VendaMais/Modelos/`

### 4. Database (Camada de Dados)
- Singleton que gerencia conexões SQLite
- Localização: `data/vendamais.db`
- Métodos CRUD para todas as entidades
- Queries otimizadas com índices
- Transações seguras com rollback
- Sistema de backup manual
- Foreign keys com integridade referencial

## Modelo de Dados

### Tabelas

#### produtos
```sql
CREATE TABLE produtos (
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
```

#### clientes
```sql
CREATE TABLE clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    documento TEXT UNIQUE,
    telefone TEXT,
    email TEXT,
    endereco TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

#### vendas
```sql
CREATE TABLE vendas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER,
    data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total REAL NOT NULL,
    forma_pagamento TEXT,
    tipo_fiscal TEXT,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
)
```

#### itens_venda
```sql
CREATE TABLE itens_venda (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    venda_id INTEGER NOT NULL,
    produto_id INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    preco_unitario REAL NOT NULL,
    total_item REAL NOT NULL,
    FOREIGN KEY (venda_id) REFERENCES vendas(id),
    FOREIGN KEY (produto_id) REFERENCES produtos(id)
)
```

#### configuracoes_empresa
```sql
CREATE TABLE configuracoes_empresa (
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
```

### Relacionamentos
```
produtos (1) ──< (N) itens_venda
clientes (0..1) ──< (N) vendas
vendas (1) ──< (N) itens_venda
configuracoes_empresa (1) - Singleton
```

### Integridade Referencial
- Foreign keys garantem relacionamentos
- LEFT JOIN permite vendas sem cliente (consumidor final)
- Histórico de vendas preservado
- Índices em campos de busca: `codigo_barras`, `data_hora`

## Fluxo de Dados

### Cadastro de Produto
```
1. Usuário preenche formulário (ProdutoDialog)
2. Validação de campos obrigatórios
3. Database.get_connection()
4. INSERT no SQLite com prepared statement
5. Commit da transação
6. Retorna produto_id
7. Atualização da lista (ProdutosView)
```

### Busca Interativa no PDV
```
1. Usuário digita no campo de busca
2. Timer de 300ms é iniciado (on_search_changed)
3. Ao expirar, executar_busca() é chamado
4. Query: SELECT com LIKE case-insensitive
5. Resultados exibidos com botão "Adicionar"
6. Status atualizado (N produtos encontrados)
```

### Seleção de Cliente
```
1. Usuário clica "Selecionar Cliente"
2. Diálogo com lista de clientes
3. Busca interativa por nome/CPF
4. Opção "Cadastrar Novo" inline
5. Cliente selecionado armazenado em memória
6. Label atualizado: "Nome - CPF/CNPJ"
7. cliente_id vinculado à venda
```

### Realização de Venda
```
1. Usuário busca e adiciona produtos ao carrinho
2. (Opcional) Seleciona cliente
3. Clica "Finalizar Venda"
4. Escolhe forma de pagamento
5. BEGIN TRANSACTION
6. INSERT vendas (cliente_id pode ser NULL)
7. INSERT múltiplos em itens_venda
8. UPDATE estoque dos produtos (decrementar)
9. SELECT dados empresa e cliente
10. Gera cupom fiscal
11. COMMIT
12. Exibe cupom em diálogo
13. Limpa carrinho e cliente
```

### Geração de Gráficos
```
1. Usuário clica "Gráficos de Estoque"
2. Escolhe tipo de gráfico
3. Query específica no banco
4. matplotlib em modo 'Agg' (sem display)
5. Gera gráfico (plt.figure, plt.bar)
6. Salva PNG em ~/Documentos/VendaMais/Graficos/
7. Exibe em Gtk.Picture dentro de Dialog
8. Botão "Fechar" para voltar
```

## Padrões de Design Utilizados

### 1. MVC (Model-View-Controller)
- **Model**: Classes Database e estrutura SQLite
- **View**: Componentes GTK4 (Views, Dialogs)
- **Controller**: Lógica nos métodos `on_*` das Views

### 2. Singleton
- Database mantém instância única
- ConfiguracoesEmpresa sempre id=1

### 3. Observer
- GTK signals para comunicação entre componentes
- Callbacks para eventos de UI (`connect()`)

### 4. Factory
- Métodos `criar_*_row()` criam widgets dinamicamente
- Exemplo: `criar_card()` em RelatoriosView

### 5. Timer Pattern (Debounce)
- GLib.timeout_add() para busca interativa
- Evita queries excessivas durante digitação

## Performance

### Otimizações Implementadas

1. **Busca com Debounce**
   - Timer de 300ms para evitar queries excessivas
   - Cancela timer anterior ao digitar novamente

2. **Indexação**
   - Índice em `produtos.codigo_barras`
   - Índice em `vendas.data_hora`
   - Primary keys para joins rápidos

3. **Transações**
   - Vendas em transação única
   - Rollback automático em erro
   - Garante consistência ACID

4. **Lazy Rendering**
   - Gráficos gerados sob demanda
   - Matplotlib modo 'Agg' (sem overhead de display)

5. **Prepared Statements**
   - Todas queries usam placeholders `?`
   - Proteção contra SQL injection
   - Cache de query plans pelo SQLite

6. **Limitação de Resultados**
   - LIMIT 50 em listas de clientes
   - LIMIT 20 em produtos buscados
   - Top N em gráficos

## Segurança

### Implementado
- ✅ Validação de entrada em todos formulários
- ✅ Prepared statements (proteção SQL injection)
- ✅ Transações ACID
- ✅ Backup manual do banco
- ✅ Tratamento de exceções robusto
- ✅ Validação de unicidade (código barras, CPF/CNPJ)

### Planejado
- [ ] Criptografia de dados sensíveis
- [ ] Sistema de autenticação multi-usuário
- [ ] Logs de auditoria de vendas
- [ ] Permissões por usuário/papel
- [ ] Validação de CPF/CNPJ com algoritmo

## Escalabilidade

### Capacidade Atual
- **SQLite**: Até ~1 milhão de produtos (adequado para PME)
- **Vendas**: ~10 milhões de registros
- **Interface**: Single-thread GTK (adequado desktop)
- **Escopo**: Single-store

### Limitações
- Sem suporte multi-loja nativo
- Sem sincronização cloud
- Banco local apenas

### Evolução Futura
- Migração para PostgreSQL para grandes volumes
- API REST para integração
- Sistema multi-tenant
- Sincronização cloud (AWS S3, Google Drive)
- App mobile complementar

## Sistema de Arquivos

### Estrutura de Diretórios Gerados
```
~/Documentos/VendaMais/
├── Cupons/              # Cupons fiscais em .txt
├── Graficos/            # Gráficos em .png
└── Modelos/             # Modelos CSV
    ├── modelo_produtos.csv
    └── modelo_clientes.csv

./<projeto>/
└── data/
    └── vendamais.db     # Banco de dados SQLite
```

## Testes

### Estratégia Atual
```
Testes manuais via interface GTK
- Fluxo completo de venda
- Validações de formulário
- Importação CSV
- Geração de cupom
- Gráficos
```

### Planejado
```
1. Testes Unitários
   - database.py CRUD
   - Validações de campos
   - Cálculos de margem/total

2. Testes de Integração
   - Fluxo venda completo
   - Importação/Exportação CSV
   - Geração de cupom
   - Geração de gráficos

3. Testes de UI
   - Navegação entre views
   - Formulários e validações
   - Diálogos modais
```

## Deployment

### Desktop Application
```bash
# Empacotamento com PyInstaller
pip install pyinstaller
pyinstaller --windowed --onefile vendamais/main.py

# Flatpak (recomendado para Linux)
flatpak-builder build com.vendamais.app.yml

# AppImage
# Snap
# .deb / .rpm
```

### Distribuição Recomendada
1. **Flatpak** (preferencial) - isolado e seguro
2. **AppImage** - portável
3. **Snap** - Ubuntu/derivados
4. **.deb** - Debian/Ubuntu
5. **.rpm** - Fedora/RHEL

## Manutenção

### Backup Manual
```python
# Via menu da aplicação
Menu → Fazer Backup

# Cria arquivo:
# data/vendamais.db.backup.YYYYMMDD_HHMMSS
```

### Migrations
Atualmente não há sistema formal de migrations. Schema criado em `database.py::init_db()`.

**Planejado:**
```python
def get_schema_version():
    # Versão do schema em tabela metadata
    
def migrate_to_version(target_version):
    # Aplica migrações progressivas
```

## Tecnologias e Dependências

### Core
- Python 3.12+
- PyGObject >= 3.46.0
- GTK4
- Libadwaita

### Análise/Visualização
- matplotlib >= 3.8.0
- numpy (dependência do matplotlib)

### Desenvolvimento
- pytest >= 8.0.0 (dev)
- ruff >= 0.3.0 (dev)
- uv (package manager)

## Referências

- [GTK4 Documentation](https://docs.gtk.org/gtk4/)
- [Libadwaita](https://gnome.pages.gitlab.gnome.org/libadwaita/)
- [PyGObject](https://pygobject.readthedocs.io/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Matplotlib](https://matplotlib.org/stable/index.html)
- [uv Package Manager](https://github.com/astral-sh/uv)
- [Python Packaging](https://packaging.python.org/)

## Changelog de Arquitetura

### v1.1.0 (2026-01-30)
- ✅ Adicionada seleção de cliente no PDV
- ✅ Cupom fiscal com dados do cliente
- ✅ Cadastro rápido de cliente inline
- ✅ Tabela `configuracoes_empresa`
- ✅ Sistema de importação CSV
- ✅ Geração de gráficos com matplotlib
- ✅ ConfiguracoesView com abas
- ✅ Busca interativa com debounce

### v1.0.0 (2026-01-29)
- ✅ PDV com busca de produtos
- ✅ CRUD de produtos e clientes
- ✅ Gestão de vendas
- ✅ Relatórios básicos
- ✅ Exportação CSV
- ✅ Cupom fiscal básico
