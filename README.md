# 🧾 Controle de Validade de Softwares (CQMED)

Sistema desenvolvido em **Python** com interface gráfica em **Tkinter** para gerenciamento e monitoramento de licenças de software, datas de expiração e chaves de ativação.

O projeto possui:

- Interface gráfica para gestão (CRUD)
- Script automatizado para verificação e alertas de vencimento

---

## 🚀 Funcionalidades

### 🖥️ Interface de Gerenciamento (`ui_editor.py`)

#### 📊 Painel Visual
Listagem de softwares com indicadores por cor:

- 🟢 **Verde:** Validade OK ou licença vitalícia
- 🟠 **Laranja:** Expira em menos de 90 dias
- 🔴 **Vermelho:** Licença vencida

#### ✏️ CRUD Completo
- Adicionar softwares
- Editar softwares
- Remover softwares

#### 🔄 Controle de Renovação
- Checkbox para indicar se o software deve ser renovado ou descontinuado

#### 🔎 Filtros e Busca
- Pesquisa por nome
- Filtros rápidos:
  - Todos
  - Próximos do vencimento
  - Vencidos

#### 📑 Ordenação
Ordenação clicando nas colunas:

- Nome
- Data de validade
- Dias restantes

#### 🖱️ Interatividade
- **Duplo clique:** Abre links de ativação ou usuário no navegador
- **Botão direito:** Menu de contexto para copiar dados da célula

---

### ⏰ Monitoramento Automático (`agenda_softwares.py`)

- Verificação automática do banco JSON
- Exibição de popup caso existam softwares:
  - Vencidos
  - Próximos do vencimento (≤ 90 dias)
  - Marcados para renovação

---

## 📂 Estrutura do Projeto

```text
ControleValidadeDeSoftware/
│
├── ui_editor.py          # Interface principal (GUI)
├── agenda_softwares.py   # Verificação automática de vencimentos
├── data_handler.py       # Manipulação segura do arquivo JSON
├── software_agenda.json  # Banco de dados
├── iniciar_agenda.bat    # Script para inicialização automática (Windows)
├── checked.png           # Ícone checkbox marcado
└── unchecked.png         # Ícone checkbox desmarcado


---

## 🛠️ Pré-requisitos

- Python 3.x

Bibliotecas utilizadas (todas padrão do Python):

- `tkinter`
- `json`
- `datetime`
- `os`
- `webbrowser`

Não é necessário instalar dependências via `pip`.

---

## ⚙️ Como Utilizar

### 1️⃣ Gerenciamento de Softwares

Execute o editor visual:

```bash
python ui_editor.py
```

### 📅 Formatos de Data Aceitos

- `YYYY-MM-DD` (ISO)
- `DD-MM-YYYY` (Formato brasileiro)

---

### ♾️ Licenças Vitalícias

Digite no campo de validade:
 Vitalício

 
O sistema irá ignorar o cálculo de dias restantes.

---

### 2️⃣ Verificação Manual

Para verificar manualmente softwares expirando:

```bash
python agenda_softwares.py
```

3️⃣ Inicialização Automática no Windows

Para executar a verificação automaticamente ao iniciar o Windows:

✔️ Passo 1 — Verifique o Caminho

Clique com botão direito em iniciar_agenda.bat

Selecione Editar

Confirme se o caminho para agenda_softwares.py está correto

Salve o arquivo

✔️ Passo 2 — Criar Atalho

Clique com botão direito no arquivo .bat e selecione:

Criar atalho

✔️ Passo 3 — Abrir Pasta de Inicialização

Pressione Win + R

Digite:

shell:startup


Pressione Enter

✔️ Passo 4 — Mover Atalho

Arraste o atalho criado para a pasta aberta.

✔️ Pronto!
Agora o sistema executará automaticamente ao iniciar o Windows e exibirá alertas somente quando necessário.

💾 Estrutura de Dados (JSON)

O arquivo software_agenda.json é criado automaticamente e segue o formato:

{
  "softwares": [
    {
      "nome": "Nome do Software",
      "validade": "2026-12-31",
      "ativacao": "Chave ou URL",
      "usuario": "email@dominio.com",
      "numero_licencas": "10",
      "renovacao": "sim"
    }
  ]
}

📌 Finalidade

Ferramenta desenvolvida para auxiliar no controle e gerenciamento de ativos de software do CQMED.