import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

con = sqlite3.connect("pessoas.db")
cur = con.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS pessoas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    endereco TEXT NOT NULL,
    cep INTEGER NOT NULL
)
""")
con.commit()

registro_atual_id = None

def atualizar_grade():
    tabela.delete(*tabela.get_children())
    cur.execute("SELECT id, nome, endereco, cep FROM pessoas ORDER BY id DESC")
    for row in cur.fetchall():
        tabela.insert("", tk.END, values=row)
    atualizar_botoes()

def carregar_selecionado_no_campo(event=None):
    
    global registro_atual_id
    sel = tabela.selection()
    if not sel:
        return
    valores = tabela.item(sel[0], "values")
    registro_atual_id = int(valores[0])
    entrada_nome.delete(0, tk.END)
    entrada_nome.insert(0, valores[1])
    atualizar_botoes()

def novo():
    
    global registro_atual_id
    registro_atual_id = None
    entrada_nome.delete(0, tk.END)
    entrada_nome.focus()
    entrada_endereco.delete(0, tk.END)
    entrada_endereco.focus()
    entrada_cep.delete(0, tk.END)
    entrada_cep.focus()
    tabela.selection_remove(*tabela.selection())
    atualizar_botoes()

def salvar():
    
    global registro_atual_id
    nome = entrada_nome.get().strip()
    endereco = entrada_endereco.get().strip()
    cep = entrada_cep.get().strip()

    if nome == "" or endereco == "" or cep == "":
        messagebox.showwarning("Atenção", "Há campos a serem preenchidos!")
        return

    if registro_atual_id is None:
        
        cur.execute("INSERT INTO pessoas (nome, endereco, cep) VALUES (?,?,?)", (nome, endereco, cep))
        con.commit()
        messagebox.showinfo("Sucesso", f"A pessoa '{nome}' cadastrado!")
    else:
        
        cur.execute("UPDATE pessoas SET nome = ?, endereco = ?, cep = ? WHERE id = ?", (nome, endereco, cep, registro_atual_id))
        con.commit()
        messagebox.showinfo("Sucesso", f"Registro {registro_atual_id} atualizado!")

    novo()
    atualizar_grade()

def editar():
    
    global registro_atual_id
    sel = tabela.selection()
    if not sel:
        messagebox.showinfo("Info", "Selecione um registro para editar.")
        return
    valores = tabela.item(sel[0], "values")
    registro_atual_id = int(valores[0])
    #Editar nome
    entrada_nome.delete(0, tk.END)
    entrada_nome.insert(0, valores[1])
    entrada_nome.focus()
    #Editar Endereço
    entrada_endereco.delete(1, tk.END)
    entrada_endereco.insert(1, valores[2])
    entrada_endereco.focus()
    #Editar Cep
    entrada_cep.delete(2, tk.END)
    entrada_cep.insert(2, valores[3])
    entrada_cep.focus()
    atualizar_botoes()

def excluir():

    global registro_atual_id
    sel = tabela.selection()
    if not sel:
        messagebox.showinfo("Info", "Selecione um registro para excluir.")
        return
    valores = tabela.item(sel[0], "values")
    _id, _nome = int(valores[0]), valores[1]

    if messagebox.askyesno("Confirmar", f"Deseja excluir o registro {_id} - '{_nome}'?"):
        cur.execute("DELETE FROM pessoas WHERE id = ?", (_id,))
        con.commit()
        messagebox.showinfo("Sucesso", f"Registro {_id} excluído.")
        registro_atual_id = None
        entrada_nome.delete(0, tk.END)
        atualizar_grade()

def cancelar():
    
    novo()
    atualizar_grade()

def ao_selecionar(_event):
    
    atualizar_botoes()

def atualizar_botoes():
    
    tem_sel = len(tabela.selection()) > 0
    
    texto = entrada_nome.get().strip()
    endereco = entrada_endereco.get().strip()
    cep = entrada_cep.get().strip()
    btn_salvar.config(state=tk.NORMAL if texto != "" or registro_atual_id is not None else tk.NORMAL)
    btn_salvar.config(state=tk.NORMAL if endereco != "" or registro_atual_id is not None else tk.NORMAL)
    btn_salvar.config(state=tk.NORMAL if cep != "" or registro_atual_id is not None else tk.NORMAL)

    btn_editar.config(state=tk.NORMAL if tem_sel else tk.DISABLED)
    btn_excluir.config(state=tk.NORMAL if tem_sel else tk.DISABLED)

    em_edicao = registro_atual_id is not None or texto != ""
    btn_cancelar.config(state=tk.NORMAL if em_edicao else tk.DISABLED)

janela = tk.Tk()
janela.title("Cadastro de Nomes - CRUD")
janela.geometry("520x380")

frm_form = tk.Frame(janela)
frm_form.pack(fill="x", padx=10, pady=8)

tk.Label(frm_form, text="Nome:").grid(row=0, column=0, sticky="w", padx=(0,8))
entrada_nome = tk.Entry(frm_form, width=40)
entrada_nome.grid(row=0, column=1, sticky="w")
entrada_nome.bind("<KeyRelease>", lambda e: atualizar_botoes())

tk.Label(frm_form, text="Endereço:").grid(row=1, column=0, sticky="w", padx=(0,8))
entrada_endereco = tk.Entry(frm_form, width=40)
entrada_endereco.grid(row=1, column=1, sticky="w")
entrada_endereco.bind("<KeyRelease>", lambda e: atualizar_botoes())

tk.Label(frm_form, text="CEP:").grid(row=2, column=0, sticky="w", padx=(0,8))
entrada_cep = tk.Entry(frm_form, width=40)
entrada_cep.grid(row=2, column=1, sticky="w")
entrada_cep.bind("<KeyRelease>", lambda e: atualizar_botoes())

frm_btns = tk.Frame(janela)
frm_btns.pack(fill="x", padx=10, pady=(2,8))

btn_novo = tk.Button(frm_btns, text="Novo", width=10, command=novo)
btn_salvar = tk.Button(frm_btns, text="Salvar", width=10, command=salvar)
btn_editar = tk.Button(frm_btns, text="Editar", width=10, command=editar)
btn_excluir = tk.Button(frm_btns, text="Excluir", width=10, command=excluir)
btn_cancelar = tk.Button(frm_btns, text="Cancelar", width=10, command=cancelar)
btn_fechar = tk.Button(frm_btns, text="Fechar", width=10, command=janela.destroy)

btn_novo.grid(row=0, column=0, padx=4, pady=2)
btn_salvar.grid(row=0, column=1, padx=4, pady=2)
btn_editar.grid(row=0, column=2, padx=4, pady=2)
btn_excluir.grid(row=0, column=3, padx=4, pady=2)
btn_cancelar.grid(row=0, column=4, padx=4, pady=2)
btn_fechar.grid(row=0, column=5, padx=4, pady=2)

frm_tab = tk.Frame(janela)
frm_tab.pack(fill="both", expand=True, padx=10, pady=4)

tabela = ttk.Treeview(frm_tab, columns=("id", "nome","endereco", "cep"), show="headings", height=10)
tabela.heading("id", text="ID")
tabela.heading("nome", text="Nome")
tabela.heading("endereco", text="Endereço")
tabela.heading("cep", text="CEP")
tabela.column("id", width=60, anchor="center")
tabela.column("nome", width=360, anchor="w")
tabela.column("endereco", width=360, anchor="w")
tabela.column("cep", width=360, anchor="w")

scroll_y = ttk.Scrollbar(frm_tab, orient="vertical", command=tabela.yview)
tabela.configure(yscrollcommand=scroll_y.set)

tabela.grid(row=0, column=0, sticky="nsew")
scroll_y.grid(row=0, column=1, sticky="ns")

frm_tab.rowconfigure(0, weight=1)
frm_tab.columnconfigure(0, weight=1)

tabela.bind("<<TreeviewSelect>>", ao_selecionar)
tabela.bind("<Double-1>", carregar_selecionado_no_campo)

novo()
atualizar_grade()

janela.mainloop()

con.close()