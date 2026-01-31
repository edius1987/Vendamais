# VendaMais - Sistema de Gestão de Vendas, Estoque e PDV

**Desenvolvido por:** Edius Ferreira  
**GitHub:** https://github.com/edius1987  
**Projeto:** https://github.com/edius1987/VendaMais  
**Licença:** MIT  
**Versão:** 1.1.0

---

## 📋 Visão Geral

O **VendaMais** é uma aplicação desktop robusta para gestão de estoque e frente de caixa (PDV), desenvolvida com **Python 3.12+**, **GTK4** e **SQLite**. O sistema oferece uma interface moderna e nativa para Linux, utilizando **Libadwaita** para uma experiência visual profissional.

---

## 🎯 Objetivos do Sistema

- **Principal:** Desenvolver uma aplicação desktop robusta para gestão de estoque e frente de caixa (PDV).
- **Interface:** Criar uma experiência de usuário (UX) fluida utilizando Stack para separar PDV, Cadastros, Relatórios e Configurações.
- **Persistência:** Garantir a integridade dos dados via SQLite e permitir a portabilidade/intercâmbio de dados através de arquivos CSV.
- **Conformidade:** Implementar a lógica para geração de cupons fiscais com dados da empresa.

---

## ✨ Funcionalidades Implementadas

### **Módulo PDV / Frente de Caixa**

- ✅ **Busca interativa** de produtos por código de barras ou nome
- ✅ **Autocomplete** - produtos aparecem conforme você digita (debounce 300ms)
- ✅ **Adicionar produtos ao carrinho** com um clique
- ✅ **Controle de quantidade** direto no carrinho (+/-)
- ✅ **Validação de estoque** em tempo real
- ✅ **Seleção opcional de cliente** - vincule clientes às vendas
- ✅ **Cadastro rápido de cliente** direto do PDV sem sair da tela
- ✅ **CPF na nota fiscal** - dados do cliente no cupom quando informado
- ✅ **Cupom fiscal completo** com dados da empresa e cliente
- ✅ Múltiplas formas de pagamento (Dinheiro, Débito, Crédito, PIX)
- ✅ Salvamento de cupons em `~/Documentos/VendaMais/Cupons/`

### **Módulo de Cadastro de Produtos**

- ✅ Registro completo: Nome, Código de Barras, Preços (Compra/Venda), NCM, Tributação
- ✅ Controle de estoque automático
- ✅ Cálculo de margem de lucro
- ✅ Busca e filtragem rápida
- ✅ Validação de unicidade de código de barras
- ✅ **Importação em massa via CSV**

### **Módulo de Clientes**

- ✅ Cadastro completo: Nome, CPF/CNPJ, Endereço, Telefone, Email
- ✅ Vínculo opcional do cliente no momento da venda
- ✅ **Importação em massa via CSV**
- ✅ Busca por nome ou documento

### **Módulo de Vendas e Emissão de Cupom**

- ✅ Interface de PDV para seleção de produtos e cálculo automático de totais
- ✅ **Geração de Cupom Fiscal** com dados da empresa
- ✅ **Inclusão de dados do cliente** (nome e CPF/CNPJ) quando informado
- ✅ Baixa automática de estoque
- ✅ Histórico de vendas com cliente vinculado

### **Gerenciamento de Dados**

- ✅ **SQLite:** Banco de dados relacional para armazenamento permanente
- ✅ **Exportação CSV:** Produtos e vendas
- ✅ **Importação CSV:** Produtos e clientes com modelos de exemplo
- ✅ **Backup manual** do banco de dados
- ✅ Modelos CSV salvos em `~/Documentos/VendaMais/Modelos/`

### **Gerador de Relatórios e Gráficos**

- ✅ Dashboard com métricas em tempo real
- ✅ Vendas do dia e vendas do mês
- ✅ Produtos com estoque baixo (alertas)
- ✅ Produtos mais vendidos
- ✅ **Gráficos de estoque** (matplotlib):
  - Estoque atual (Top 20 produtos)
  - Produtos com estoque baixo (cores de alerta)
  - Produtos mais vendidos (Top 15)
- ✅ Gráficos salvos em `~/Documentos/VendaMais/Graficos/`
- ✅ Exportação de relatórios em CSV

### **Configurações do Sistema**

- ✅ **Dados da Empresa** para cupom fiscal:
  - Nome, CNPJ, Inscrição Estadual
  - Endereço completo, cidade, estado, CEP
  - Telefone e Email
- ✅ **Importação de Dados:**
  - Upload de produtos via CSV
  - Upload de clientes via CSV
  - Download de modelos CSV

---

## 🗄️ Estrutura de Banco de Dados (SQLite)

### Tabelas Implementadas

| **Tabela**                | **Campos Principais**                                                                                     |
| ------------------------- | --------------------------------------------------------------------------------------------------------- |
| **produtos**              | `id, nome, codigo_barras, preco_compra, preco_venda, estoque, ncm, tributacao, created_at`               |
| **clientes**              | `id, nome, documento, telefone, email, endereco, created_at`                                              |
| **vendas**                | `id, cliente_id, data_hora, total, forma_pagamento, tipo_fiscal`                                          |
| **itens_venda**           | `id, venda_id, produto_id, quantidade, preco_unitario, total_item`                                        |
| **configuracoes_empresa** | `id, nome_empresa, cnpj, inscricao_estadual, endereco, telefone, email, cidade, estado, cep` (Singleton) |

### Relacionamentos

```
produtos (1) ──< (N) itens_venda
clientes (0..1) ──< (N) vendas    [LEFT JOIN - cliente opcional]
vendas (1) ──< (N) itens_venda
configuracoes_empresa (1)         [Sempre id=1, único registro]
```

---

## 🏗️ Arquitetura do Sistema

### Tecnologias

- **Linguagem:** Python 3.12+
- **Interface Gráfica:** GTK4 (via PyGObject)
- **Design System:** Libadwaita (GNOME moderno)
- **Banco de Dados:** SQLite
- **Gráficos:** Matplotlib 3.8+
- **Gerenciador de Pacotes:** uv

### Padrões de Design

- **MVC:** Model-View-Controller
- **Singleton:** Database e ConfiguracoesEmpresa
- **Observer:** GTK signals e callbacks
- **Factory:** Criação dinâmica de widgets
- **Timer/Debounce:** Busca interativa otimizada

### Estrutura de Arquivos

```
VendaMais/
├── vendamais/              # Código fonte principal
│   ├── __init__.py
│   ├── main.py            # Aplicação principal
│   ├── database.py        # Camada de dados
│   ├── models.py          # Modelos de dados
│   ├── styles.css         # Estilos customizados
│   └── views/             # Views da aplicação
│       ├── main_window.py      # Janela principal
│       ├── vendas_view.py      # PDV/Vendas
│       ├── produtos_view.py    # Gestão de produtos
│       ├── clientes_view.py    # Gestão de clientes
│       ├── relatorios_view.py  # Relatórios e gráficos
│       └── configuracoes_view.py  # Configurações
├── data/                  # Banco de dados
│   └── vendamais.db
├── popular_db.py          # Script para dados de exemplo
├── pyproject.toml         # Configuração do projeto
├── README.md              # Documentação principal
├── ARCHITECTURE.md        # Arquitetura técnica
├── CONTRIBUTING.md        # Guia de desenvolvimento
└── AGENT.md               # Este arquivo
```

---

## 🚀 Como Executar

### Instalação de Dependências do Sistema

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install libgirepository1.0-dev gcc libcairo2-dev pkg-config \
                 python3-dev gir1.2-gtk-4.0 gir1.2-adw-1

# Fedora
sudo dnf install gobject-introspection-devel cairo-gobject-devel \
                 gtk4-devel libadwaita-devel

# Arch Linux
sudo pacman -S gobject-introspection gtk4 libadwaita
```

### Instalação do Projeto

```bash
# Clone o repositório
git clone https://github.com/edius1987/VendaMais.git
cd VendaMais

# Configure ambiente Python com uv
uv venv
uv sync

# Execute o aplicativo
uv run vendamais

# (Opcional) Popular banco com dados de exemplo
uv run python popular_db.py
```

---

## 💡 Diferenciais Implementados

### ✅ **Dashboard de Indicadores**

Painel visual mostrando:

- Total de vendas do dia
- Total de vendas do mês
- Produtos com estoque baixo (alerta visual)
- Vendas recentes
- Gráficos interativos

### ✅ **Busca Inteligente**

- Busca interativa com debounce (300ms)
- Autocomplete em tempo real
- Busca por código de barras ou nome
- Limite LIMIT para performance

### ✅ **Modo Dark/Light Automático**

Integração com o esquema de cores do sistema operacional via **Libadwaita**, deixando o app com aparência moderna e profissional.

### ✅ **Gestão Completa de Clientes no PDV**

- Seleção de cliente existente
- Cadastro rápido inline
- CPF/CNPJ na nota fiscal
- Link cliente-venda para relatórios

### ✅ **Importação/Exportação Massiva**

- CSV para produtos e clientes
- Modelos pré-configurados
- Validação e feedback de erros
- Exportação de vendas para análise

### ✅ **Visualizações Gráficas**

- Gráficos de barras com matplotlib
- Salvamento automático em PNG
- Cores inteligentes (alertas em vermelho/amarelo)
- Interface integrada com GTK

---

## 📊 Exemplo de Cupom Fiscal

```
==================================================
           Loja Exemplo LTDA
              CNPJ: 12.345.678/0001-90
             IE: 123.456.789.012
         Rua Exemplo, 123 - Centro
            São Paulo - SP
             Tel: (11) 3456-7890
==================================================
                 CUPOM FISCAL
==================================================
Venda nº: 15
Data: 30/01/2026 22:05:30
--------------------------------------------------
DADOS DO CLIENTE:
Nome: João da Silva
CPF/CNPJ: 123.456.789-00
--------------------------------------------------
Item Produto                   Qtd   Unit.   Total
--------------------------------------------------
1    Coca-Cola 2L              2      7.99   15.98
2    Arroz Tipo 1 5kg          1     22.90   22.90
--------------------------------------------------
                                  TOTAL R$  38.88
Forma de Pagamento: PIX
==================================================
         OBRIGADO PELA PREFERÊNCIA!
==================================================
```

---

## 🎯 Funcionalidades Planejadas (Roadmap)

### V1.2 (Q1 2026)

- [ ] Testes automatizados (pytest)
- [ ] Sistema de backup automático
- [ ] Validação de CPF/CNPJ com algoritmo
- [ ] Modo escuro forçado (toggle manual)

### V2.0 (Q2 2026)

- [ ] Multi-usuário com autenticação
- [ ] Logs de auditoria de vendas
- [ ] Relatórios em PDF
- [ ] Integração com impressora fiscal
- [ ] Leitor de código de barras USB

### Futuro

- [ ] API REST para integração
- [ ] App mobile complementar
- [ ] Sincronização em nuvem (AWS S3, Google Drive)
- [ ] Sistema de plugins/extensões
- [ ] Multi-loja/Multi-caixa
- [ ] Controle de usuários e níveis de acesso
- [ ] Impressão térmica direta (58mm/80mm)

---

## 🛠️ Tecnologias Utilizadas

### Core

- **Python 3.12+** - Linguagem principal
- **GTK4** - Framework de interface gráfica
- **Libadwaita** - Design system moderno do GNOME
- **PyGObject** - Bindings Python para GTK

### Dados e Persistência

- **SQLite** - Banco de dados relacional
- **CSV** - Importação/Exportação de dados

### Visualização

- **Matplotlib 3.8+** - Gráficos e visualizações
- **NumPy** - Dependência do Matplotlib

### Desenvolvimento

- **uv** - Gerenciador de pacotes moderno
- **pytest** - Framework de testes (dev)
- **ruff** - Linter e formatter (dev)

---

## 📝 Licença

Este projeto está licenciado sob a **MIT License**.

```
MIT License

Copyright (c) 2026 Edius Ferreira

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 👨‍💻 Autor

**Edius Ferreira**

- GitHub: [@edius1987](https://github.com/edius1987)
- Projeto: [VendaMais](https://github.com/edius1987/VendaMais)

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor, leia o [CONTRIBUTING.md](CONTRIBUTING.md) para detalhes sobre o processo de desenvolvimento.

### Como Contribuir

1. Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'feat: adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

---

## 📚 Documentação

- [README.md](README.md) - Visão geral e guia de uso
- [ARCHITECTURE.md](ARCHITECTURE.md) - Arquitetura técnica detalhada
- [CONTRIBUTING.md](CONTRIBUTING.md) - Guia de desenvolvimento
- [ALTERACOES.md](ALTERACOES.md) - Changelog completo
- [ATUALIZACAO_CLIENTE_PDV.md](ATUALIZACAO_CLIENTE_PDV.md) - Feature específica de cliente

---

## 🙏 Agradecimentos

- **GNOME Project** - Por GTK4 e Libadwaita
- **Python Software Foundation** - Pela linguagem Python
- **SQLite** - Pelo banco de dados leve e eficiente
- **Matplotlib** - Pelas visualizações gráficas
- **Comunidade Open Source** - Por todo o suporte e inspiração

---

## 📞 Suporte

Para reportar bugs ou solicitar features:

- **Issues:** https://github.com/edius1987/VendaMais/issues
- **Discussions:** https://github.com/edius1987/VendaMais/discussions

---

## 📈 Status do Projeto

- ✅ **Versão Atual:** 1.1.0
- ✅ **Status:** Ativo e em desenvolvimento
- ✅ **Última Atualização:** 30/01/2026
- ✅ **Python:** 3.12+
- ✅ **Plataforma:** Linux (Ubuntu, Fedora, Arch)

---

**VendaMais** - Sistema Completo de Gestão de Vendas e Estoque  
Desenvolvido com ❤️ por [Edius Ferreira](https://github.com/edius1987)
