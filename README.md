# VendaMais

Sistema de Gestão de Vendas, Estoque e Frente de Caixa (PDV) desenvolvido com Python, GTK4 e SQLite.

## 🚀 Características

### Frente de Caixa (PDV)
- ✅ **Busca interativa** de produtos por código de barras ou nome
- ✅ **Autocomplete** - produtos aparecem conforme você digita
- ✅ **Adicionar produtos ao carrinho** com um clique
- ✅ **Controle de quantidade** direto no carrinho
- ✅ **Validação de estoque** em tempo real
- ✅ **Seleção de cliente (opcional)** - vincule clientes às vendas
- ✅ **CPF na nota fiscal** - dados do cliente no cupom quando informado
- ✅ **Cadastro rápido de cliente** direto do PDV
- ✅ **Cupom fiscal** completo com dados da empresa e cliente
- ✅ Múltiplas formas de pagamento (Dinheiro, Débito, Crédito, PIX)

### Gestão de Produtos e Clientes
- Cadastro completo de produtos com código de barras, NCM e tributação
- Gestão de clientes com CPF/CNPJ
- Controle de estoque automático
- **Importação em massa** via CSV

### Configurações
- ✅ **Configuração de dados da empresa** para cupom fiscal
  - Nome da empresa, CNPJ, Inscrição Estadual
  - Endereço completo, telefone, email
- ✅ **Importação de dados** via CSV
  - Importar produtos em lote
  - Importar clientes em lote
  - Modelos CSV para download

### Relatórios e Análises
- Dashboard com indicadores de vendas
- Vendas do dia e do mês
- Produtos com estoque baixo
- Exportação CSV de vendas e produtos
- ✅ **Gráficos de estoque** com matplotlib
  - Gráfico de estoque atual (Top 20 produtos)
  - Produtos com estoque baixo (com cores de alerta)
  - Produtos mais vendidos

## 📋 Requisitos do Sistema

- Python 3.12+
- GTK4
- Libadwaita
- PyGObject
- Matplotlib (para gráficos)

## 🔧 Instalação

### Dependências do Sistema

**Ubuntu/Debian:**
```bash
sudo apt install libgirepository1.0-dev gcc libcairo2-dev pkg-config python3-dev gir1.2-gtk-4.0 gir1.2-adw-1
```

**Fedora:**
```bash
sudo dnf install gobject-introspection-devel cairo-gobject-devel gtk4-devel libadwaita-devel
```

**Arch Linux:**
```bash
sudo pacman -S gobject-introspection gtk4 libadwaita
```

### Instalação do Projeto

Usando UV (recomendado):
```bash
uv venv
uv sync
uv run vendamais
```

Ou usando pip:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
python -m vendamais
```

## 📁 Estrutura do Projeto

```
vendamais/
├── pyproject.toml
├── README.md
├── vendamais/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   └── views/
│       ├── main_window.py
│       ├── vendas_view.py
│       ├── produtos_view.py
│       ├── clientes_view.py
│       ├── relatorios_view.py
│       └── configuracoes_view.py
└── data/
    └── vendamais.db
```

## 🎯 Uso

### 1️⃣ Configurar Empresa
- Vá em **Configurações** → **Dados da Empresa**
- Preencha os dados que aparecerão no cupom fiscal
- Clique em **Salvar Configurações**

### 2️⃣ Importar Dados (Opcional)
- Em **Configurações** → **Importar Dados**
- Baixe os modelos CSV de produtos ou clientes
- Preencha os dados e importe os arquivos

### 3️⃣ Cadastrar Produtos
- Use a aba **Produtos** para cadastrar mercadorias
- Informe código de barras, preços, estoque

### 4️⃣ Realizar Vendas
- Use a aba **PDV / Vendas**
- Digite o código de barras ou nome do produto
- Produtos aparecerão automaticamente conforme você digita
- Clique no botão **Adicionar** ou na linha do produto
- Ajuste quantidades no carrinho
- Clique em **Finalizar Venda**
- Escolha a forma de pagamento
- O cupom fiscal será gerado automaticamente

### 5️⃣ Visualizar Relatórios
- Use a aba **Relatórios** para ver estatísticas
- Clique em **Gráficos de Estoque** para visualizar:
  - Estoque atual dos produtos
  - Produtos com estoque baixo (alertas em vermelho/amarelo)
  - Produtos mais vendidos
- Exporte dados em CSV

## 📊 Arquivos Gerados

O sistema cria os seguintes diretórios em `~/Documentos/VendaMais/`:
- `Cupons/` - Cupons fiscais das vendas
- `Graficos/` - Gráficos de estoque gerados
- `Modelos/` - Modelos CSV para importação

## 🔐 Backup

Use o menu → **Fazer Backup** para criar cópias de segurança do banco de dados.

## 📝 Licença

MIT

