# Guia de Desenvolvimento - VendaMais

## Começando

### Configuração do Ambiente

```bash
# Clone o repositório
git clone <url-do-repo>
cd VendaMais

# Instale dependências do sistema
# Ubuntu/Debian:
sudo apt install libgirepository1.0-dev gcc libcairo2-dev pkg-config \
                 python3-dev gir1.2-gtk-4.0 gir1.2-adw-1

# Fedora:
sudo dnf install gobject-introspection-devel cairo-gobject-devel \
                 gtk4-devel libadwaita-devel

# Arch Linux:
sudo pacman -S gobject-introspection gtk4 libadwaita

# Configure ambiente Python com uv
uv venv
uv sync
```

### Estrutura de Diretórios

```
VendaMais/
├── vendamais/              # Código fonte principal
│   ├── __init__.py        # Inicialização do pacote
│   ├── main.py            # Aplicação principal
│   ├── database.py        # Camada de dados
│   ├── models.py          # Modelos de dados
│   ├── styles.css         # Estilos customizados
│   └── views/             # Views da aplicação
│       ├── __init__.py
│       ├── main_window.py      # Janela principal
│       ├── vendas_view.py      # PDV/Vendas
│       ├── produtos_view.py    # Gestão de produtos
│       ├── clientes_view.py    # Gestão de clientes
│       ├── relatorios_view.py  # Relatórios e gráficos
│       └── configuracoes_view.py  # Configurações
├── data/                  # Banco de dados
│   └── vendamais.db      # SQLite database
├── popular_db.py         # Script para dados de exemplo
├── pyproject.toml        # Configuração do projeto
├── uv.lock               # Lock de dependências
├── README.md             # Documentação principal
├── ARCHITECTURE.md       # Arquitetura do sistema
├── CONTRIBUTING.md       # Este arquivo
├── ALTERACOES.md         # Changelog detalhado
├── ATUALIZACAO_CLIENTE_PDV.md  # Doc feature cliente
└── .gitignore           # Arquivos ignorados
```

## Rodando o Projeto

### Modo Desenvolvimento

```bash
# Ativar ambiente virtual e executar
uv run vendamais

# Ou manualmente:
source .venv/bin/activate
python -m vendamais

# Com dados de exemplo
uv run python popular_db.py
uv run vendamais
```

### Debug

```bash
# Com GTK Inspector (pressione Ctrl+Shift+I durante execução)
GTK_DEBUG=interactive uv run vendamais

# Com logs detalhados
G_MESSAGES_DEBUG=all uv run vendamais

# Python debug
python -m pdb -m vendamais
```

## Adicionando Funcionalidades

### 1. Nova View no Sistema

```python
# Em vendamais/views/minha_view.py

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw

class MinhaView(Gtk.Box):
    """Nova view do sistema"""
    
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        
        # Margens
        self.set_margin_top(24)
        self.set_margin_bottom(24)
        self.set_margin_start(24)
        self.set_margin_end(24)
        
        # Título
        title = Gtk.Label(label="Minha Nova View")
        title.add_css_class("title-1")
        title.set_halign(Gtk.Align.START)
        self.append(title)
        
        # Seus componentes aqui...

# Em vendamais/views/main_window.py:
from .minha_view import MinhaView

# No __init__ de MainWindow:
self.minha_view = MinhaView()
self.stack.add_titled(self.minha_view, "minha", "Minha View")
```

### 2. Nova Tabela no Banco

```python
# Em vendamais/database.py, no método init_db():

cursor.execute("""
    CREATE TABLE IF NOT EXISTS minha_tabela (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        campo1 TEXT NOT NULL,
        campo2 REAL,
        campo3 INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

# Criar índice se necessário
cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_campo1 
    ON minha_tabela(campo1)
""")
```

### 3. Diálogo de Seleção com Busca

Padrão usado em VendasView para seleção de cliente:

```python
def on_abrir_dialogo(self, btn):
    """Abre diálogo de seleção"""
    from ..database import db
    
    dialog = Gtk.Dialog(transient_for=self.get_root(), modal=True)
    dialog.set_title("Selecionar Item")
    dialog.set_default_size(500, 400)
    
    # Header
    header = Adw.HeaderBar()
    dialog.get_content_area().append(header)
    
    # Content
    content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
    content.set_margin_top(12)
    content.set_margin_bottom(12)
    content.set_margin_start(12)
    content.set_margin_end(12)
    
    # Campo de busca
    search_entry = Gtk.Entry()
    search_entry.set_placeholder_text("Buscar...")
    content.append(search_entry)
    
    # Lista
    scrolled = Gtk.ScrolledWindow()
    scrolled.set_vexpand(True)
    
    list_box = Gtk.ListBox()
    list_box.add_css_class("boxed-list")
    scrolled.set_child(list_box)
    content.append(scrolled)
    
    # Função para carregar dados
    def carregar_dados(termo=""):
        while child := list_box.get_first_child():
            list_box.remove(child)
        
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM tabela 
            WHERE nome LIKE ? 
            LIMIT 50
        """, (f"%{termo}%",))
        
        for row in cursor.fetchall():
            item_row = Adw.ActionRow(title=row['nome'])
            item_row.data = row
            list_box.append(item_row)
        
        conn.close()
    
    # Conectar busca
    search_entry.connect("changed", lambda e: carregar_dados(e.get_text()))
    
    # Carregar inicial
    carregar_dados()
    
    # Botões
    btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    btn_box.set_halign(Gtk.Align.END)
    
    btn_ok = Gtk.Button(label="Selecionar")
    btn_ok.add_css_class("suggested-action")
    btn_ok.connect("clicked", lambda b: self.processar_selecao(list_box, dialog))
    
    btn_box.append(btn_ok)
    content.append(btn_box)
    
    dialog.get_content_area().append(content)
    dialog.present()
```

### 4. Gerar Gráfico com Matplotlib

```python
def gerar_grafico(self):
    """Gera gráfico de exemplo"""
    try:
        import matplotlib
        matplotlib.use('Agg')  # Modo sem display
        import matplotlib.pyplot as plt
        from ..database import db
        from pathlib import Path
        
        # Buscar dados
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT nome, valor FROM tabela LIMIT 10")
        dados = cursor.fetchall()
        conn.close()
        
        if not dados:
            self.mostrar_erro("Nenhum dado encontrado")
            return
        
        # Preparar dados
        labels = [d['nome'][:20] for d in dados]
        values = [d['valor'] for d in dados]
        
        # Criar gráfico
        plt.figure(figsize=(10, 6))
        plt.bar(range(len(labels)), values, color='#3584e4')
        plt.xlabel('Itens')
        plt.ylabel('Valores')
        plt.title('Meu Gráfico')
        plt.xticks(range(len(labels)), labels, rotation=45, ha='right')
        plt.tight_layout()
        
        # Salvar
        graficos_dir = Path.home() / "Documentos" / "VendaMais" / "Graficos"
        graficos_dir.mkdir(parents=True, exist_ok=True)
        
        filename = graficos_dir / f"grafico_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        plt.close()
        
        # Exibir
        self.mostrar_grafico(filename, "Meu Gráfico")
        
    except ImportError:
        self.mostrar_erro("matplotlib não instalado")
    except Exception as e:
        self.mostrar_erro(f"Erro: {str(e)}")

def mostrar_grafico(self, filename, titulo):
    """Exibe gráfico em diálogo"""
    dialog = Gtk.Dialog(transient_for=self.get_root(), modal=True)
    dialog.set_title(titulo)
    dialog.set_default_size(900, 600)
    
    header = Adw.HeaderBar()
    dialog.get_content_area().append(header)
    
    scrolled = Gtk.ScrolledWindow()
    scrolled.set_vexpand(True)
    scrolled.set_hexpand(True)
    
    picture = Gtk.Picture.new_for_filename(str(filename))
    picture.set_can_shrink(True)
    scrolled.set_child(picture)
    
    dialog.get_content_area().append(scrolled)
    
    btn_fechar = Gtk.Button(label="Fechar")
    btn_fechar.add_css_class("suggested-action")
    btn_fechar.connect("clicked", lambda b: dialog.close())
    
    btn_box = Gtk.Box()
    btn_box.set_halign(Gtk.Align.CENTER)
    btn_box.set_margin_bottom(12)
    btn_box.append(btn_fechar)
    
    dialog.get_content_area().append(btn_box)
    dialog.present()
```

### 5. Importação CSV

```python
def importar_csv(self, caminho):
    """Importa dados de arquivo CSV"""
    from ..database import db
    import csv
    
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
                        INSERT INTO tabela (campo1, campo2)
                        VALUES (?, ?)
                    """, (row['campo1'], row['campo2']))
                    importados += 1
                except Exception as e:
                    erros += 1
                    print(f"Erro na linha: {e}")
            
            conn.commit()
            conn.close()
        
        dialog = Adw.MessageDialog.new(
            self.get_root(),
            "Importação Concluída",
            f"Importados: {importados}\nErros: {erros}"
        )
        dialog.add_response("ok", "OK")
        dialog.present()
        
    except Exception as e:
        self.mostrar_erro(f"Erro: {str(e)}")
```

## Estilização com GTK/Libadwaita

### Classes CSS Disponíveis

```python
# Títulos e texto
widget.add_css_class("title-1")      # Título muito grande
widget.add_css_class("title-2")      # Título grande
widget.add_css_class("title-3")      # Título médio
widget.add_css_class("title-4")      # Título pequeno
widget.add_css_class("heading")      # Cabeçalho
widget.add_css_class("caption")      # Legenda pequena
widget.add_css_class("dim-label")    # Texto secundário/desbotado
widget.add_css_class("monospace")    # Fonte monoespaçada
widget.add_css_class("numeric")      # Números

# Botões
widget.add_css_class("suggested-action")   # Ação principal (azul)
widget.add_css_class("destructive-action")  # Ação destrutiva (vermelho)
widget.add_css_class("flat")               # Botão sem borda
widget.add_css_class("pill")               # Botão arredondado

# Containers
widget.add_css_class("card")         # Card com sombra
widget.add_css_class("toolbar")      # Barra de ferramentas
widget.add_css_class("boxed-list")   # Lista com bordas arredondadas

# Estados
widget.add_css_class("success")      # Verde
widget.add_css_class("warning")      # Amarelo
widget.add_css_class("error")        # Vermelho
```

### Widgets Adwaita Comuns

```python
# ActionRow - linha de ação
row = Adw.ActionRow(
    title="Título",
    subtitle="Subtítulo"
)
row.add_suffix(widget)  # Adicionar widget à direita

# EntryRow - campo de entrada
entry = Adw.EntryRow(title="Nome")
texto = entry.get_text()

# PreferencesGroup - grupo de preferências
group = Adw.PreferencesGroup(title="Grupo")
group.add(row)

# MessageDialog - diálogo de mensagem
dialog = Adw.MessageDialog.new(parent, "Título", "Mensagem")
dialog.add_response("ok", "OK")
dialog.add_response("cancel", "Cancelar")
dialog.set_response_appearance("cancel", Adw.ResponseAppearance.DESTRUCTIVE)
dialog.connect("response", callback)
dialog.present()

# HeaderBar - barra de cabeçalho
header = Adw.HeaderBar()
header.pack_start(widget_esquerda)
header.pack_end(widget_direita)
```

## Padrões de Código

### Nomenclatura

```python
# Classes: PascalCase
class VendasView(Gtk.Box):
    pass

# Métodos e funções: snake_case
def criar_produto_row(self, produto):
    pass

# Callbacks: on_evento
def on_produto_selecionado(self, listbox, row):
    pass

# Variáveis privadas: _prefixo
def __init__(self):
    self._cliente_selecionado = None

# Constantes: UPPER_CASE
MAX_PRODUTOS = 1000
TIMEOUT_BUSCA_MS = 300
```

### Docstrings

```python
def minha_funcao(param1: str, param2: int) -> dict:
    """
    Breve descrição da função em uma linha.
    
    Descrição mais detalhada se necessário, explicando o propósito
    completo da função e casos de uso.
    
    Args:
        param1: Descrição do primeiro parâmetro
        param2: Descrição do segundo parâmetro
    
    Returns:
        Dicionário com as chaves:
        - 'sucesso': bool indicando sucesso
        - 'dados': dados retornados
    
    Raises:
        ValueError: Quando param1 está vazio
        DatabaseError: Quando falha ao acessar banco
    
    Example:
        >>> resultado = minha_funcao("teste", 42)
        >>> print(resultado['sucesso'])
        True
    """
    pass
```

### Type Hints

```python
from typing import List, Dict, Optional, Tuple

def buscar_produtos(
    self, 
    termo: Optional[str] = None,
    limite: int = 50
) -> List[Dict[str, any]]:
    """Busca produtos com type hints"""
    pass

# Para callbacks GTK
def on_button_clicked(self, button: Gtk.Button) -> None:
    pass

# Tipos customizados
from typing import TypedDict

class ProdutoDict(TypedDict):
    id: int
    nome: str
    preco: float

def get_produto(self, id: int) -> ProdutoDict:
    pass
```

## Boas Práticas

### 1. Gestão de Conexões

```python
# ✅ Correto - sempre feche conexões
def buscar_dados(self):
    from ..database import db
    
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tabela")
    resultado = cursor.fetchall()
    conn.close()  # Sempre fechar!
    return resultado

# ⚠️  Alternativa com try/finally
def salvar_dados(self, dados):
    conn = db.get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT ...", dados)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise
    finally:
        conn.close()
```

### 2. Tratamento de Erros

```python
# ✅ Correto - específico e com feedback ao usuário
def processar_venda(self):
    try:
        # Lógica aqui
        pass
    except ValueError as e:
        dialog = Adw.MessageDialog.new(
            self.get_root(),
            "Dados Inválidos",
            str(e)
        )
        dialog.add_response("ok", "OK")
        dialog.present()
    except sqlite3.IntegrityError:
        dialog = Adw.MessageDialog.new(
            self.get_root(),
            "Registro Duplicado",
            "Este item já existe no sistema"
        )
        dialog.add_response("ok", "OK")
        dialog.present()
    except Exception as e:
        print(f"Erro inesperado: {e}")  # Log para debug
        dialog = Adw.MessageDialog.new(
            self.get_root(),
            "Erro",
            "Ocorreu um erro inesperado. Tente novamente."
        )
        dialog.add_response("ok", "OK")
        dialog.present()
```

### 3. Limpeza de Widgets

```python
# ✅ Correto - sempre limpe antes de popular
def atualizar_lista(self):
    # Remover todos os filhos
    while child := self.list_box.get_first_child():
        self.list_box.remove(child)
    
    # Adicionar novos
    for item in self.dados:
        row = self.criar_row(item)
        self.list_box.append(row)

# ✅ Para múltiplas listas
def limpar_tudo(self):
    for lista in [self.lista1, self.lista2, self.lista3]:
        while child := lista.get_first_child():
            lista.remove(child)
```

### 4. Timer/Debounce para Busca

```python
def __init__(self):
    super().__init__()
    self.search_timeout_id = None
    
def on_search_changed(self, entry):
    """Busca com debounce"""
    # Cancelar timer anterior
    if self.search_timeout_id:
        GLib.source_remove(self.search_timeout_id)
    
    # Agendar nova busca em 300ms
    self.search_timeout_id = GLib.timeout_add(300, self.executar_busca)

def executar_busca(self):
    """Executa a busca de fato"""
    termo = self.search_entry.get_text()
    # ... buscar ...
    self.search_timeout_id = None
    return False  # Remove o timeout
```

## Debugging

### GTK Inspector

```bash
# Execute com inspector habilitado
GTK_DEBUG=interactive uv run vendamais

# Durante execução:
# - Pressione Ctrl+Shift+I ou Ctrl+Shift+D
# - Ou F12 (dependendo da configuração)

# Inspetor permite:
# - Ver hierarquia de widgets
# - Inspecionar propriedades
# - Modificar CSS em tempo real
# - Ver signals conectados
```

### Logs e Debug

```python
# Logs básicos
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

logger.debug("Informação detalhada para debug")
logger.info("Informação geral")
logger.warning("Aviso")
logger.error("Erro")

# Print temporário (remover antes de commit)
print(f"DEBUG: valor = {valor}")
print(f"DEBUG: tipo = {type(valor)}")
```

### Breakpoints

```python
# Python debugger
import pdb

def minha_funcao():
    x = calcular_algo()
    pdb.set_trace()  # Breakpoint aqui
    y = processar(x)
    return y

# Comandos no pdb:
# n (next) - próxima linha
# s (step) - entra na função
# c (continue) - continua execução
# p variavel - printa variável
# l - mostra código ao redor
# q - sai do debugger
```

## Testes

### Estrutura de Testes (Planejado)

```python
# tests/test_database.py
import pytest
from vendamais.database import db

@pytest.fixture
def db_temporario():
    """Cria banco em memória para testes"""
    # Implementar...
    yield db

def test_adicionar_produto(db_temporario):
    """Testa adição de produto"""
    # Implementar...
    pass
```

### Executar Testes

```bash
# Instalar pytest
uv pip install pytest pytest-cov

# Rodar testes
pytest tests/

# Com cobertura
pytest --cov=vendamais tests/

# Teste específico
pytest tests/test_database.py::test_adicionar_produto

# Verbose
pytest -v tests/
```

## Contribuindo

### Fluxo de Trabalho Git

```bash
# 1. Fork do repositório no GitHub

# 2. Clone do seu fork
git clone https://github.com/seu-usuario/VendaMais.git
cd VendaMais

# 3. Adicione upstream
git remote add upstream https://github.com/original/VendaMais.git

# 4. Crie branch para feature
git checkout -b feature/minha-feature

# 5. Faça suas alterações e commits
git add .
git commit -m "Adiciona funcionalidade X"

# 6. Mantenha atualizado com upstream
git fetch upstream
git rebase upstream/main

# 7. Push para seu fork
git push origin feature/minha-feature

# 8. Abra Pull Request no GitHub
```

### Mensagens de Commit

```bash
# Formato: <tipo>: <descrição curta>

# Tipos:
# feat: nova funcionalidade
# fix: correção de bug
# docs: documentação
# style: formatação, sem mudança de código
# refactor: refatoração sem mudar comportamento
# test: adição de testes
# chore: tarefas de manutenção

# Exemplos:
git commit -m "feat: adiciona seleção de cliente no PDV"
git commit -m "fix: corrige cálculo de margem de lucro"
git commit -m "docs: atualiza README com novas features"
git commit -m "refactor: extrai lógica de cupom para método separado"
```

### Checklist Antes do Pull Request

- [ ] Código segue os padrões do projeto (PEP 8)
- [ ] Não há imports não utilizados
- [ ] Docstrings adicionadas/atualizadas
- [ ] Type hints quando aplicável
- [ ] Funcionalidade testada manualmente
- [ ] Sem erros no console GTK
- [ ] Documentação atualizada (README, ARCHITECTURE)
- [ ] Commit messages descritivas
- [ ] Branch baseada em main atualizado

## Recursos Úteis

### Documentação Oficial
- [GTK4 Documentation](https://docs.gtk.org/gtk4/)
- [Libadwaita Docs](https://gnome.pages.gitlab.gnome.org/libadwaita/doc/main/)
- [PyGObject Tutorial](https://pygobject.readthedocs.io/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Matplotlib Gallery](https://matplotlib.org/stable/gallery/index.html)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)

### Ferramentas Recomendadas
- [Cambalache](https://flathub.org/apps/ar.xjuan.Cambalache) - UI Designer GTK4
- [Icon Library](https://flathub.org/apps/org.gnome.design.IconLibrary) - ícones GNOME
- [DB Browser for SQLite](https://sqlitebrowser.org/) - Visualizar banco
- [VSCode](https://code.visualstudio.com/) com extensões Python e TOML

### Comunidade e Suporte
- [GNOME Discourse](https://discourse.gnome.org/)
- [PyGObject Matrix](https://matrix.to/#/#python:gnome.org)
- [Python Brasil](https://python.org.br/)

## Troubleshooting

### "gi.repository not found"
```bash
# Ubuntu/Debian
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-4.0

# Fedora
sudo dnf install python3-gobject gtk4

# Arch
sudo pacman -S python-gobject gtk4
```

### "No module named 'Adw'"
```bash
# Ubuntu/Debian
sudo apt install gir1.2-adw-1

# Fedora
sudo dnf install libadwaita

# Arch
sudo pacman -S libadwaita
```

### "matplotlib not building font cache"
```bash
# Aguarde primeira execução ou:
rm -rf ~/.cache/matplotlib
python -c "import matplotlib.pyplot as plt"
```

### Banco de dados corrompido
```bash
# Backup e recriação
mv data/vendamais.db data/vendamais.db.old
uv run vendamais  # Cria novo banco
```

### Interface não atualiza
```python
# Force refresh da lista
self.atualizar_lista()  # Método específico da view

# Ou:
GLib.idle_add(self.atualizar_lista)
```

## Performance Tips

1. **Lazy Loading**: Carregue dados sob demanda, use LIMIT
2. **Índices**: Adicione índices em campos de busca frequente
3. **Transações**: Agrupe múltiplas operações em uma transação
4. **Debounce**: Use timers para busca interativa (300ms)
5. **Prepared Statements**: Sempre use placeholders `?`
6. **Matplotlib Agg**: Use backend 'Agg' para gráficos sem display

## Roadmap

### V1.2 (Q1 2026)
- [ ] Testes automatizados (pytest)
- [ ] Sistema de backup automático  
- [ ] Validação de CPF/CNPJ
- [ ] Modo escuro forçado

### V2.0 (Q2 2026)
- [ ] Multi-usuário com autenticação
- [ ] Logs de auditoria
- [ ] Relatórios em PDF
- [ ] Integração com impressora fiscal

### Futuro
- [ ] API REST
- [ ] App mobile complementar
- [ ] Sincronização cloud
- [ ] Sistema de plugins
- [ ] Multi-loja/Multi-caixa

---

**Última atualização:** 2026-01-30
**Versão do documento:** 1.1
