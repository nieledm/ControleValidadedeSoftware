import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
from data_handler import load_data, save_data
import datetime, webbrowser

BR_FMT = "%d-%m-%Y"
ISO_FMT = "%Y-%m-%d"

def parse_date_any(s: str):
    """Tenta parsear data nos formatos ISO (YYYY-MM-DD) e BR (DD-MM-YYYY)."""
    for fmt in (ISO_FMT, BR_FMT):
        try:
            return datetime.datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    return None

def parse_date_iso(s: str):
    try:
        return datetime.datetime.strptime(s, ISO_FMT).date()
    except ValueError:
        return None

def to_iso_string(d: datetime.date) -> str:
    return d.strftime(ISO_FMT)

def to_br_string(d: datetime.date) -> str:
    return d.strftime(BR_FMT)

# ====================================================
# Classe auxiliar para manter popups em primeiro plano
# ====================================================
class TopmostDialogHelper:
    def __init__(self, parent):
        self.parent = parent
        self.dialog = None
    
    def ask_string(self, title, prompt, initial=""):
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.attributes("-topmost", True)
        self.dialog.grab_set()  # Impede interação com a janela principal
        self.dialog.withdraw()
        
        # Usando 'initial' em vez de 'initialvalue'
        result = simpledialog.askstring(title, prompt, initialvalue=initial, parent=self.dialog)
        
        self.dialog.grab_release()
        self.dialog.destroy()
        self.dialog = None
        return result
    
    def ask_yesno(self, title, prompt):
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.attributes("-topmost", True)
        self.dialog.grab_set()
        self.dialog.withdraw()
        
        result = messagebox.askyesno(title, prompt, parent=self.dialog)
        
        self.dialog.grab_release()
        self.dialog.destroy()
        self.dialog = None
        return result
    
    def show_warning(self, title, prompt):
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.attributes("-topmost", True)
        self.dialog.grab_set()
        self.dialog.withdraw()
        
        messagebox.showwarning(title, prompt, parent=self.dialog)
        
        self.dialog.grab_release()
        self.dialog.destroy()
        self.dialog = None
    
    def show_error(self, title, prompt):
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.attributes("-topmost", True)
        self.dialog.grab_set()
        self.dialog.withdraw()
        
        messagebox.showerror(title, prompt, parent=self.dialog)
        
        self.dialog.grab_release()
        self.dialog.destroy()
        self.dialog = None
    
    def show_info(self, title, prompt):
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.attributes("-topmost", True)
        self.dialog.grab_set()
        self.dialog.withdraw()
        
        messagebox.showinfo(title, prompt, parent=self.dialog)
        
        self.dialog.grab_release()
        self.dialog.destroy()
        self.dialog = None

# ====================================================
# Classe Principal
# ====================================================
class SoftwareEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Softwares CQMED")
        self.geometry("900x520")
        
        # Inicializações
        self.data = load_data()
        self.filtered_data = list(self.data.get("softwares", []))
        self.sort_key = "date"
        self.sort_asc = True
        self.dialogs = TopmostDialogHelper(self)  # Helper para diálogos
        
        # Configuração da UI
        self._setup_ui()
        
        # Carrega dados
        self.apply_filter()
    
    def _setup_ui(self):
        """Configura todos os elementos da interface"""
        self._create_menu()
        self._create_search_frame()
        self._create_treeview()
        self._create_buttons()
        self._create_status_bar()
    
    def _create_menu(self):
        menubar = tk.Menu(self)
        
        # Menu Arquivo
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Sair", command=self.quit)
        menubar.add_cascade(label="Arquivo", menu=file_menu)
        
        # Menu Ajuda
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Sobre", command=self._show_about)
        menubar.add_cascade(label="Ajuda", menu=help_menu)
        
        self.config(menu=menubar)
    
    def _show_about(self):
        about_text = "Softwares CQMED\nVersão 1.0\n\nGerenciador de licenças de software"
        self.dialogs.show_info("Sobre", about_text)
    
    def _create_status_bar(self):
        self.status_var = tk.StringVar()
        self.status_var.set("Pronto")
        status_bar = tk.Label(
            self, 
            textvariable=self.status_var, 
            bd=1, 
            relief=tk.SUNKEN, 
            anchor=tk.W
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def _create_search_frame(self):
        """Cria o frame de pesquisa"""
        search_frame = tk.Frame(self)
        search_frame.pack(fill=tk.X, padx=10, pady=6)

        tk.Label(search_frame, text="Pesquisar:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *args: self.apply_filter())
        tk.Entry(search_frame, textvariable=self.search_var).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=6)

        tk.Label(search_frame, text="Status:").pack(side=tk.LEFT, padx=6)
        self.status_var = tk.StringVar(value="Todos")
        status_cb = ttk.Combobox(
            search_frame, 
            textvariable=self.status_var, 
            values=["Todos", "Somente próximos", "Somente vencidos"], 
            width=18, 
            state="readonly"
        )
        status_cb.pack(side=tk.LEFT)
        status_cb.bind("<<ComboboxSelected>>", lambda e: self.apply_filter())
    
    def _create_treeview(self):
        """Cria a treeview e configura colunas"""
        columns = ("Nome", "Validade", "Licenças", "Dias restantes", "Ativação", "Username", "Renovar")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        self.tree["show"] = ("tree", "headings")  # habilita a coluna tree (#0)


        # Inserindo imagens (check/uncheck)
        self.checked_img = tk.PhotoImage(file="checked.png")
        self.unchecked_img = tk.PhotoImage(file="unchecked.png")

        # Coluna de checkbox (#0)
        self.tree.heading("#0", text="Renovar")
        self.tree.column("#0", width=80, anchor=tk.CENTER)

        self.tree.heading("Renovar", text="Renovar (hidden)")
        self.tree.column("Renovar", width=0, stretch=False)

        # Configura cabeçalhos
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Validade", text="Validade", command=self.sort_by_date)
        self.tree.heading("Licenças", text="Licenças")
        self.tree.heading("Dias restantes", text="Dias restantes", command=self.sort_by_days)
        self.tree.heading("Ativação", text="Ativação")
        self.tree.heading("Username", text="Username")

        # Configura colunas
        self.tree.column("Nome", width=130, anchor=tk.W)
        self.tree.column("Validade", width=100, anchor=tk.W)
        self.tree.column("Licenças", width=65, anchor=tk.W)
        self.tree.column("Dias restantes", width=80, anchor=tk.W)
        self.tree.column("Ativação", width=270, anchor=tk.W)
        self.tree.column("Username", width=150, anchor=tk.W)
        
        # Tags de estilo
        self.tree.tag_configure("ok", foreground="green")
        self.tree.tag_configure("warn", foreground="orange")
        self.tree.tag_configure("expired", foreground="red")
        
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.tree.bind("<Button-1>", self.toggle_checkbox)
        self.tree.bind("<Button-3>", self.show_context_menu) # Botão direito
        self.tree.bind("<Double-1>", self.on_double_click)   # Duplo clique


        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
                        
        # Cria o menu de contexto uma vez para reusar
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Copiar", command=self.copy_selection)
    
    def _create_buttons(self):
        """Cria os botões CRUD"""
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)
        
        buttons = [
            ("Adicionar", self.add_software),
            ("Editar", self.edit_software),
            ("Remover", self.remove_software)
        ]
        
        for text, command in buttons:
            tk.Button(btn_frame, text=text, command=command).pack(side=tk.LEFT, padx=5)   
    
    # ============================
    # Renderização
    # ============================
    def load_tree(self):
        self.tree.delete(*self.tree.get_children())
        today = datetime.date.today()
        
        for soft in self.filtered_data:
            nome = soft.get("nome", "")
            iso_str = soft.get("validade", "")
            ativ = soft.get("ativacao", "")
            license = soft.get("numero_licencas", "")
            username = soft.get("usuario", "")
            renovar = soft.get("renovacao", "")

            # Lógica para Vitalício
            if iso_str.lower() == "vitalício":
                validade_br = "Vitalício"
                dias = "∞"
                tag = "ok" # Fica verde
            else:
                d = parse_date_iso(iso_str)
                if d is None:
                    validade_br = iso_str
                    dias = "?"
                    tag = ""
                else:
                    validade_br = to_br_string(d)
                    dias = (d - today).days
                    if dias < 0:
                        tag = "expired"
                    elif dias <= 90:
                        tag = "warn"
                    else:
                        tag = "ok"

            img = self.checked_img if renovar == "sim" else self.unchecked_img

            item_id = self.tree.insert(
                "", "end",
                text="",
                image=img,
                values=(nome, validade_br, license, dias, ativ, username),
                tags=(tag,)
            )
            self.tree.set(item_id, "Renovar", renovar)

    def toggle_checkbox(self, event):
        """Alterna o estado do checkbox e salva no JSON"""
        region = self.tree.identify("region", event.x, event.y)
        if region != "tree":  # só reage se clicar na coluna de imagem
            return

        item_id = self.tree.identify_row(event.y)
        if not item_id:
            return

        # Estado atual vem do próprio tree
        current_state = self.tree.set(item_id, "Renovar")  # "sim" ou "nao"

        new_state = "nao" if current_state == "sim" else "sim"
        new_img = self.checked_img if new_state == "sim" else self.unchecked_img

        # Atualiza a Treeview
        self.tree.item(item_id, image=new_img)
        self.tree.set(item_id, "Renovar", new_state)

        # Atualiza a lista em memória
        idx = self.tree.index(item_id)
        soft = self.filtered_data[idx]
        soft["renovacao"] = new_state

        # Propaga para o dataset completo
        for s in self.data["softwares"]:
            if s["nome"] == soft["nome"]:  # se "nome" for único
                s["renovacao"] = new_state

        # Salva no JSON
        save_data(self.data)


    
    # ============================
    # Filtro + Ordenação
    # ============================
    def apply_filter(self):
        query = (self.search_var.get() or "").lower().strip()
        status = self.status_var.get()
        today = datetime.date.today()

        base = self.data.get("softwares", [])
        result = []
        for s in base:
            if query and query not in s.get("nome", "").lower():
                continue
            d = parse_date_iso(s.get("validade", ""))
            dias = (d - today).days if d else None

            if status == "Somente próximos" and not (dias is not None and 0 <= dias <= 90):
                continue
            if status == "Somente vencidos" and not (dias is not None and dias < 0):
                continue
            result.append(s)

        self.filtered_data = result
        self.apply_sort()
        self.load_tree()

    def apply_sort(self):
        def get_sort_date(s):
            val = s.get("validade", "")
            if val.lower() == "vitalício":
                return datetime.date(9999, 12, 31) # Data futura longínqua
            return parse_date_iso(val) or datetime.date.min

        if self.sort_key == "date":
            self.filtered_data.sort(
                key=get_sort_date,
                reverse=not self.sort_asc
            )
        elif self.sort_key == "days":
            today = datetime.date.today()
            def days_key(s):
                val = s.get("validade", "")
                if val.lower() == "vitalício":
                    return 999999 # Número alto de dias
                d = parse_date_iso(val)
                return (d - today).days if d else -999999
            
            self.filtered_data.sort(key=days_key, reverse=not self.sort_asc)

    def sort_by_date(self):
        if self.sort_key == "date":
            self.sort_asc = not self.sort_asc
        else:
            self.sort_key = "date"
            self.sort_asc = True
        self.apply_sort()
        self.load_tree()

    def sort_by_days(self):
        if self.sort_key == "days":
            self.sort_asc = not self.sort_asc
        else:
            self.sort_key = "days"
            self.sort_asc = True
        self.apply_sort()
        self.load_tree()
    
    # ================================
    # Interatividade (Copiar e Links)
    # ================================

    def show_context_menu(self, event):
        """Mostra menu 'Copiar' ao clicar com botão direito"""
        item = self.tree.identify_row(event.y)
        col = self.tree.identify_column(event.x)
        
        if item and col:
            # Seleciona a linha visualmente
            self.tree.selection_set(item)
            # Guarda onde clicou para usar na função de copiar
            self.clicked_item = item
            self.clicked_col = col
            self.context_menu.post(event.x_root, event.y_root)

    def copy_selection(self):
        """Copia o conteúdo da célula clicada para o clipboard"""
        try:
            # Pega o índice da coluna (ex: '#1' -> 0 se subtrair 1, mas lembre da coluna #0 oculta/imagem)
            # As colunas de dados values=(...) começam tecnicamente no índice 0 do displaycolumns
            # Mas o identify_column retorna #1 para a primeira coluna visível de dados se #0 for a tree
            
            col_id = int(self.clicked_col.replace('#', '')) - 1 
            # Nota: Sua coluna #0 é a imagem. Então #1 é "Nome". 
            # Os values=(Nome, Validade...) correspondem a indices 0, 1...
            
            values = self.tree.item(self.clicked_item, "values")
            
            if 0 <= col_id < len(values):
                text = values[col_id]
                self.clipboard_clear()
                self.clipboard_append(text)
                self.status_var.set(f"Copiado: {text}")
        except Exception as e:
            print(f"Erro ao copiar: {e}")

    def on_double_click(self, event):
        """Abre link no navegador se a célula começar com http"""
        region = self.tree.identify("region", event.x, event.y)
        if region != "cell": 
            return

        item = self.tree.identify_row(event.y)
        col = self.tree.identify_column(event.x)
        
        if item and col:
            col_id = int(col.replace('#', '')) - 1
            values = self.tree.item(item, "values")
            
            if 0 <= col_id < len(values):
                text = values[col_id]
                if text.startswith("http://") or text.startswith("https://"):
                    webbrowser.open(text)
                    self.status_var.set(f"Abrindo link: {text}")
                else:
                    # Opcional: Se não for link, tenta copiar ou editar
                    pass
                
    # ============================
    # CRUD
    # ============================
    def add_software(self):
        nome = self.dialogs.ask_string("Adicionar", "Nome do software:")
        if not nome: 
            return

        validade_in = self.dialogs.ask_string("Adicionar", "Data de validade (YYYY-MM-DD ou DD-MM-YYYY):")
        if not validade_in: 
            return
        
        d = parse_date_any(validade_in)
        if not d:
            self.dialogs.show_error("Erro", "Data inválida. Use YYYY-MM-DD ou DD-MM-YYYY.")
            return
        
        numero_licencas = self.dialogs.ask_string("Adicionar", "Total de licenças:")
        if not numero_licencas: 
            return

        ativacao = self.dialogs.ask_string("Adicionar", "Modo de ativação:") or ""

        username = self.dialogs.ask_string("Adicionar", "Nome do usuário (Username):")

        renovacao = self.dialogs.ask_string("Adicionar", "Sofwtare será renovado? digite sim ou nao:")
        if not renovacao: 
            return

        self.data["softwares"].append({
            "nome": nome, 
            "validade": to_iso_string(d),
            "numero_licencas": numero_licencas,
            "ativacao": ativacao,
            "usuario": username,
            "renovacao": renovacao
        })
        save_data(self.data)
        self.apply_filter()
        self.status_var.set(f"Software '{nome}' adicionado com sucesso")

    def edit_software(self):
        selected = self.tree.selection()
        if not selected:
            self.dialogs.show_warning("Aviso", "Selecione um software para editar.")
            return

        idx = self.tree.index(selected[0])
        soft = self.filtered_data[idx]

        current_name = soft.get("nome", "")
        current_date = parse_date_iso(soft.get("validade", ""))
        current_date_br = to_br_string(current_date) if current_date else soft.get("validade", "")
        current_num = soft.get("numero_licencas", "")
        current_ativ = soft.get("ativacao", "")
        current_user = soft.get("usuario", "")

        new_nome = self.dialogs.ask_string("Editar", "Nome do software:", initial=current_name)
        if new_nome is None: 
            return
        
        new_validade_in = self.dialogs.ask_string("Editar", "Data de validade (YYYY-MM-DD ou DD-MM-YYYY):", initial=current_date_br)
        if new_validade_in is None: 
            return
        
        d = parse_date_any(new_validade_in)
        if not d:
            self.dialogs.show_error("Erro", "Data inválida.")
            return
        
        new_num = self.dialogs.ask_string("Editar", "Total de licenças:", initial=current_num)
        if new_num is None: 
            return
        
        new_ativacao = self.dialogs.ask_string("Editar", "Modo de ativação:", initial=current_ativ)
        
        new_user = self.dialogs.ask_string("Editar", "Nome do usuário (username):", initial=current_user)
        
        soft["nome"] = new_nome
        soft["validade"] = to_iso_string(d)
        soft["numero_licencas"] = new_num
        soft["ativacao"] = new_ativacao
        soft["usuario"] = new_ativacao
        save_data(self.data)
        self.apply_filter()
        self.status_var.set(f"Software '{new_nome}' atualizado com sucesso")

    def remove_software(self):
        selected = self.tree.selection()
        if not selected:
            self.dialogs.show_warning("Aviso", "Selecione um software para remover.")
            return

        idx = self.tree.index(selected[0])
        soft = self.filtered_data[idx]
        nome = soft.get("nome", "")

        if self.dialogs.ask_yesno("Confirmar", f"Remover '{nome}'?"):
            self.data["softwares"].remove(soft)
            save_data(self.data)
            self.apply_filter()
            self.status_var.set(f"Software '{nome}' removido com sucesso")

if __name__ == "__main__":
    app = SoftwareEditor()
    app.mainloop()