# gui_calcolatore_margini.py

import tkinter as tk
from tkinter import ttk, messagebox
from margini_modulo import (
    calcola_prezzo_vendita,
    calcola_margine,
    calcola_da_lordo,
    markup_da_margine,
    markup_da_margine,
    rotazione,
    calcola_prezzo_finale,
    ottimizza_prezzo
)

class CalcolatoreMarginiGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🛒 Calcolatore Margini Caffè & Capsule")
        self.root.geometry("950x700")

        # Menu Bar
        menubar = tk.Menu(root)
        root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self.confirm_exit)

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

        # Selezione tipo prodotto
        self.tipo_prodotto = tk.StringVar(value="Caffè")
        ttk.Label(root, text="Seleziona tipo prodotto:", font=("Arial", 12, "bold")).pack(pady=10)
        frame_tipo = ttk.Frame(root)
        frame_tipo.pack()
        ttk.Radiobutton(frame_tipo, text="Caffè (IVA 22%)", variable=self.tipo_prodotto, value="Caffè").pack(side=tk.LEFT)
        ttk.Radiobutton(frame_tipo, text="Non caffè (IVA 10%)", variable=self.tipo_prodotto, value="Altro").pack(side=tk.LEFT)

        # Tasto Esci
        ttk.Button(root, text="Esci", command=self.confirm_exit).pack(side=tk.BOTTOM, pady=10)

        # Notebook per schede calcolo
        notebook = ttk.Notebook(root)
        notebook.pack(expand=True, fill='both', padx=10, pady=10)

        # Tab 0: Margine da Prezzo Lordo (NUOVO TAB)
        tab0 = ttk.Frame(notebook)
        notebook.add(tab0, text="Margine da Prezzo Lordo")
        self._setup_tab_margine_da_lordo(tab0)

        # Tab 1: Margine da Prezzo Netto
        tab1 = ttk.Frame(notebook)
        notebook.add(tab1, text="Margine da Prezzo Netto")
        self._setup_tab_margine(tab1)

        # Tab 2: Prezzo da Margine
        tab2 = ttk.Frame(notebook)
        notebook.add(tab2, text="Prezzo da Margine")
        self._setup_tab_pv_da_margine(tab2)

        # Tab 3: Scorporo IVA
        tab3 = ttk.Frame(notebook)
        notebook.add(tab3, text="Scorporo IVA")
        self._setup_tab_scorporo_iva(tab3)

        # Tab 4: Markup Equivalente
        tab4 = ttk.Frame(notebook)
        notebook.add(tab4, text="Markup Equivalente")
        self._setup_tab_markup(tab4)

        # Tab 5: Rotazione Merci
        tab5 = ttk.Frame(notebook)
        notebook.add(tab5, text="Rotazione Merci")
        self._setup_tab_rotazione(tab5)

        # Tab 6: Calcolatore Completo
        tab6 = ttk.Frame(notebook)
        notebook.add(tab6, text="Calcolatore Completo")
        self._setup_tab_calcolatore_completo(tab6)

        # Tab 7: Ottimizzazione Prezzo
        tab7 = ttk.Frame(notebook)
        notebook.add(tab7, text="Ottimizzazione Prezzo")
        self._setup_tab_ottimizzazione(tab7)

    def confirm_exit(self):
        if messagebox.askyesno("Conferma Uscita", "Sei sicuro di voler uscire?"):
            self.root.destroy()

    def show_about(self):
        messagebox.showinfo("About", "Calcolatore Margini Caffè & Capsule\nVersione 1.0\n\nUno strumento per calcolare margini, prezzi e rotazione stock.")

    def get_iva(self):
        return 22 if self.tipo_prodotto.get() == "Caffè" else 10

    # === TAB 0: Margine da Prezzo Lordo (NUOVO) ===
    def _setup_tab_margine_da_lordo(self, parent):
        # Frame input
        input_frame = ttk.LabelFrame(parent, text="Input Dati", padding=10)
        input_frame.pack(fill='x', padx=10, pady=5)

        ttk.Label(input_frame, text="Costo Netto Fornitore (€):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.costo_netto_lordo_entry = ttk.Entry(input_frame, width=15)
        self.costo_netto_lordo_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="PV Lordo Finale (€):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.pv_lordo_finale_entry = ttk.Entry(input_frame, width=15)
        self.pv_lordo_finale_entry.grid(row=1, column=1, padx=5, pady=5)

        btn_calcola = ttk.Button(input_frame, text="Calcola Margine", command=self.calcola_margine_da_lordo_click)
        btn_calcola.grid(row=2, column=0, padx=5, pady=10)
        ttk.Button(input_frame, text="Pulisci", command=self.clear_tab0).grid(row=2, column=1, padx=5, pady=10)

        # Frame risultati
        result_frame = ttk.LabelFrame(parent, text="Risultati", padding=10)
        result_frame.pack(fill='x', padx=10, pady=5)
        self.result_label_0 = ttk.Label(result_frame, text="", justify=tk.LEFT)
        self.result_label_0.pack()

        # Frame spiegazione
        explain_frame = ttk.LabelFrame(parent, text="Spiegazione Calcolo", padding=10)
        explain_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        explanation = """
🎯 Quando usarla: Hai deciso il prezzo FINALE di vendita (lordo) e vuoi sapere che margine ottieni.

🔧 Flusso del calcolo:
1. Scorporo IVA: PV_lordo ÷ (1 + IVA/100) = PV_netto
2. Calcolo margine: (PV_netto - Costo) ÷ PV_netto × 100

📝 Esempio pratico:
• Costo netto: 10€
• PV lordo finale: 18€  
• IVA: 22%

Calcoli:
1. PV_netto = 18 ÷ 1.22 = 14.75€
2. Margine = (14.75-10) ÷ 14.75 × 100 = 32.20%

📋 Risultati ottenuti:
• Margine percentuale
• PV netto effettivo
• Importo IVA
• Profitto assoluto

💡 Utile quando il cliente ti dice "voglio vendere a 18€ compreso IVA"
        """.strip()
        
        explain_text = tk.Text(explain_frame, height=15, wrap=tk.WORD)
        explain_text.insert(tk.END, explanation)
        explain_text.config(state=tk.DISABLED)
        scrollbar = ttk.Scrollbar(explain_frame, orient=tk.VERTICAL, command=explain_text.yview)
        explain_text.configure(yscrollcommand=scrollbar.set)
        explain_text.pack(side=tk.LEFT, fill='both', expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def calcola_margine_da_lordo_click(self):
        try:
            costo = float(self.costo_netto_lordo_entry.get())
            pv_lordo = float(self.pv_lordo_finale_entry.get())
            iva = self.get_iva()
            
            # Prima scorporiamo l'IVA per ottenere il PV netto
            pv_netto = calcola_da_lordo(pv_lordo, iva)
            
            # Poi calcoliamo il margine usando il PV netto
            risultato = calcola_margine(costo, pv_netto, iva)
            testo = "\n".join([f"{k.replace('_', ' ').title()}: {v}" for k, v in risultato.items()])
            self.result_label_0.config(text=testo)
        except Exception as e:
            messagebox.showerror("Errore", f"Inserisci valori numerici validi!\n{str(e)}")

    def clear_tab0(self):
        self.costo_netto_lordo_entry.delete(0, tk.END)
        self.pv_lordo_finale_entry.delete(0, tk.END)
        self.result_label_0.config(text="")

    # === TAB 1: Margine da Prezzo Netto ===
    def _setup_tab_margine(self, parent):
        # Frame input
        input_frame = ttk.LabelFrame(parent, text="Input Dati", padding=10)
        input_frame.pack(fill='x', padx=10, pady=5)

        ttk.Label(input_frame, text="Costo Netto Fornitore (€):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.costo_netto_entry = ttk.Entry(input_frame, width=15)
        self.costo_netto_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="PV Netto Proposto (€):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.pv_netto_entry = ttk.Entry(input_frame, width=15)
        self.pv_netto_entry.grid(row=1, column=1, padx=5, pady=5)

        btn_calcola = ttk.Button(input_frame, text="Calcola Margine", command=self.calcola_margine_click)
        btn_calcola.grid(row=2, column=0, padx=5, pady=10)
        ttk.Button(input_frame, text="Pulisci", command=self.clear_tab1).grid(row=2, column=1, padx=5, pady=10)

        # Frame risultati
        result_frame = ttk.LabelFrame(parent, text="Risultati", padding=10)
        result_frame.pack(fill='x', padx=10, pady=5)
        self.result_label_1 = ttk.Label(result_frame, text="", justify=tk.LEFT)
        self.result_label_1.pack()

        # Frame spiegazione
        explain_frame = ttk.LabelFrame(parent, text="Spiegazione Calcolo", padding=10)
        explain_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        explanation = """
Formula Margine % = (PV_netto - Costo_netto) ÷ PV_netto × 100
Formula PV_lordo = PV_netto × (1 + IVA/100)
Formula Profitto € = PV_netto - Costo_netto
Formula IVA € = PV_lordo - PV_netto

🎯 Quando usarla: Hai già deciso il prezzo vendita NETTO e vuoi verificare il margine effettivo.

📝 Esempio: Costo 10€, PV_netto 14.8€, IVA 22%
• Margine: (14.8-10)÷14.8×100 = 32.43% (sotto target 33-40%)
• PV_lordo: 14.8×1.22 = 18.06€
• Profitto: 14.8-10 = 4.8€
• IVA: 18.06-14.8 = 3.26€
        """.strip()
        
        explain_text = tk.Text(explain_frame, height=12, wrap=tk.WORD)
        explain_text.insert(tk.END, explanation)
        explain_text.config(state=tk.DISABLED)
        scrollbar = ttk.Scrollbar(explain_frame, orient=tk.VERTICAL, command=explain_text.yview)
        explain_text.configure(yscrollcommand=scrollbar.set)
        explain_text.pack(side=tk.LEFT, fill='both', expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def calcola_margine_click(self):
        try:
            costo = float(self.costo_netto_entry.get())
            pv_netto = float(self.pv_netto_entry.get())
            iva = self.get_iva()
            risultato = calcola_margine(costo, pv_netto, iva)
            testo = "\n".join([f"{k.replace('_', ' ').title()}: {v}" for k, v in risultato.items()])
            self.result_label_1.config(text=testo)
        except Exception as e:
            messagebox.showerror("Errore", f"Inserisci valori numerici validi!\n{str(e)}")

    def clear_tab1(self):
        self.costo_netto_entry.delete(0, tk.END)
        self.pv_netto_entry.delete(0, tk.END)
        self.result_label_1.config(text="")

    # === TAB 2: Prezzo da Margine ===
    def _setup_tab_pv_da_margine(self, parent):
        # Frame input
        input_frame = ttk.LabelFrame(parent, text="Input Dati", padding=10)
        input_frame.pack(fill='x', padx=10, pady=5)

        ttk.Label(input_frame, text="Costo Netto Fornitore (€):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.costo_margine_entry = ttk.Entry(input_frame, width=15)
        self.costo_margine_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Margine Desiderato (%):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.margine_entry = ttk.Entry(input_frame, width=15)
        self.margine_entry.grid(row=1, column=1, padx=5, pady=5)

        btn_calcola = ttk.Button(input_frame, text="Calcola Prezzo di Vendita", command=self.calcola_pv_click)
        btn_calcola.grid(row=2, column=0, padx=5, pady=10)
        ttk.Button(input_frame, text="Pulisci", command=self.clear_tab2).grid(row=2, column=1, padx=5, pady=10)

        # Frame risultati
        result_frame = ttk.LabelFrame(parent, text="Risultati", padding=10)
        result_frame.pack(fill='x', padx=10, pady=5)
        self.result_label_2 = ttk.Label(result_frame, text="", justify=tk.LEFT)
        self.result_label_2.pack()

        # Frame spiegazione
        explain_frame = ttk.LabelFrame(parent, text="Spiegazione Calcolo", padding=10)
        explain_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        explanation = """
Formula PV_netto = Costo_netto ÷ (1 - Margine/100)
Formula PV_lordo = PV_netto × (1 + IVA/100)

🎯 Quando usarla: Conosci costo fornitore, cerchi prezzo per margine esatto 33-40%.

📝 Esempio: Costo 10€, margine 33%, IVA 22%
PV_netto: 10÷(1-0.33) = 10÷0.67 = 14.93€
PV_lordo: 14.93×1.22 = 18.21€

💡 Target commerciale: 33-40% su PV netto
☕ IVA caffè: 22% | Solubili: 10%
        """.strip()
        
        explain_text = tk.Text(explain_frame, height=12, wrap=tk.WORD)
        explain_text.insert(tk.END, explanation)
        explain_text.config(state=tk.DISABLED)
        scrollbar = ttk.Scrollbar(explain_frame, orient=tk.VERTICAL, command=explain_text.yview)
        explain_text.configure(yscrollcommand=scrollbar.set)
        explain_text.pack(side=tk.LEFT, fill='both', expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def calcola_pv_click(self):
        try:
            costo = float(self.costo_margine_entry.get())
            margine = float(self.margine_entry.get())
            iva = self.get_iva()
            risultato = calcola_prezzo_vendita(costo, margine, iva)
            testo = "\n".join([f"{k.replace('_', ' ').title()}: {v}" for k, v in risultato.items()])
            self.result_label_2.config(text=testo)
        except Exception as e:
            messagebox.showerror("Errore", f"Inserisci valori numerici validi!\n{str(e)}")

    def clear_tab2(self):
        self.costo_margine_entry.delete(0, tk.END)
        self.margine_entry.delete(0, tk.END)
        self.result_label_2.config(text="")

    # === TAB 3: Scorporo IVA ===
    def _setup_tab_scorporo_iva(self, parent):
        # Frame input
        input_frame = ttk.LabelFrame(parent, text="Input Dati", padding=10)
        input_frame.pack(fill='x', padx=10, pady=5)

        ttk.Label(input_frame, text="PV Lordo Cliente (€):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.pv_lordo_entry = ttk.Entry(input_frame, width=15)
        self.pv_lordo_entry.grid(row=0, column=1, padx=5, pady=5)

        btn_calcola = ttk.Button(input_frame, text="Calcola PV Netto", command=self.scorpora_iva_click)
        btn_calcola.grid(row=1, column=0, padx=5, pady=10)
        ttk.Button(input_frame, text="Pulisci", command=self.clear_tab3).grid(row=1, column=1, padx=5, pady=10)

        # Frame risultati
        result_frame = ttk.LabelFrame(parent, text="Risultati", padding=10)
        result_frame.pack(fill='x', padx=10, pady=5)
        self.result_label_3 = ttk.Label(result_frame, text="", justify=tk.LEFT)
        self.result_label_3.pack()

        # Frame spiegazione
        explain_frame = ttk.LabelFrame(parent, text="Spiegazione Calcolo", padding=10)
        explain_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        explanation = """
Formula PV_netto = PV_lordo ÷ (1 + IVA/100)

🎯 Quando usarla: Cliente dice "fammi 18€", serve l'imponibile per fattura.

📝 Esempio: PV_lordo 20€, IVA 22%
PV_netto: 20÷1.22 = 16.39€
(IVA implicita: 20-16.39 = 3.61€)

📋 Utilità: Per calcolare l'imponibile da inserire in fattura quando il cliente paga un importo comprensivo di IVA.
        """.strip()
        
        explain_text = tk.Text(explain_frame, height=12, wrap=tk.WORD)
        explain_text.insert(tk.END, explanation)
        explain_text.config(state=tk.DISABLED)
        scrollbar = ttk.Scrollbar(explain_frame, orient=tk.VERTICAL, command=explain_text.yview)
        explain_text.configure(yscrollcommand=scrollbar.set)
        explain_text.pack(side=tk.LEFT, fill='both', expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def scorpora_iva_click(self):
        try:
            pv_lordo = float(self.pv_lordo_entry.get())
            iva = self.get_iva()
            pv_netto = calcola_da_lordo(pv_lordo, iva)
            self.result_label_3.config(text=f"P.V. Netto: {pv_netto} €")
        except Exception as e:
            messagebox.showerror("Errore", f"Inserisci un valore numerico valido!\n{str(e)}")

    def clear_tab3(self):
        self.pv_lordo_entry.delete(0, tk.END)
        self.result_label_3.config(text="")

    # === TAB 4: Markup Equivalente ===
    def _setup_tab_markup(self, parent):
        # Frame input
        input_frame = ttk.LabelFrame(parent, text="Input Dati", padding=10)
        input_frame.pack(fill='x', padx=10, pady=5)

        ttk.Label(input_frame, text="Margine Desiderato (%):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.markup_margine_entry = ttk.Entry(input_frame, width=15)
        self.markup_margine_entry.grid(row=0, column=1, padx=5, pady=5)

        btn_calcola = ttk.Button(input_frame, text="Calcola Markup", command=self.calcola_markup_click)
        btn_calcola.grid(row=1, column=0, padx=5, pady=10)
        ttk.Button(input_frame, text="Pulisci", command=self.clear_tab4).grid(row=1, column=1, padx=5, pady=10)

        # Frame risultati
        result_frame = ttk.LabelFrame(parent, text="Risultati", padding=10)
        result_frame.pack(fill='x', padx=10, pady=5)
        self.result_label_4 = ttk.Label(result_frame, text="", justify=tk.LEFT)
        self.result_label_4.pack()

        # Frame spiegazione
        explain_frame = ttk.LabelFrame(parent, text="Spiegazione Calcolo", padding=10)
        explain_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        explanation = """
🎯 DIFFERENZA TRA MARGINE E MARKUP:

MARGINE (% sul prezzo di vendita):
• Formula: (Vendita - Costo) / Vendita × 100
• Esempio: Compro a 10€, vendo a 15€
• Margine = (15-10)/15 × 100 = 33.33%

MARKUP (% sul costo di acquisto):  
• Formula: (Vendita - Costo) / Costo × 100
• Stesso esempio: (15-10)/10 × 100 = 50%

FORMULA CONVERSIONE:
Markup % = Margine % ÷ (100 - Margine %) × 100

📝 Esempio pratico:
Se vuoi un margine del 33%:
Markup = 33 ÷ (100-33) × 100 = 33 ÷ 67 × 100 = 49.25%

📊 Tabella comparativa:
Margine 30% → Markup 42.86%
Margine 33% → Markup 49.25% 
Margine 35% → Markup 53.85%
Margine 40% → Markup 66.67%

🤝 QUANDO USARLO:
• Confronto fornitori: uno offre margine 35%, l'altro markup 55% - chi è più conveniente?
• Trasformare quotazioni: fornitore A dà margine, fornitore B dà markup
• Controllo coerenza: verifica che i tuoi prezzi siano coerenti tra margine e markup

💡 Ricorda: stesso profitto, percentuali diverse!
        """.strip()
        
        explain_text = tk.Text(explain_frame, height=15, wrap=tk.WORD)
        explain_text.insert(tk.END, explanation)
        explain_text.config(state=tk.DISABLED)
        scrollbar = ttk.Scrollbar(explain_frame, orient=tk.VERTICAL, command=explain_text.yview)
        explain_text.configure(yscrollcommand=scrollbar.set)
        explain_text.pack(side=tk.LEFT, fill='both', expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def calcola_markup_click(self):
        try:
            margine = float(self.markup_margine_entry.get())
            markup = markup_da_margine(margine)
            self.result_label_4.config(text=f"Markup Equivalente: {markup}%")
        except Exception as e:
            messagebox.showerror("Errore", f"Inserisci un valore numerico valido!\n{str(e)}")

    def clear_tab4(self):
        self.markup_margine_entry.delete(0, tk.END)
        self.result_label_4.config(text="")

    # === TAB 5: Rotazione Merci ===
    def _setup_tab_rotazione(self, parent):
        # Frame input
        input_frame = ttk.LabelFrame(parent, text="Input Dati", padding=10)
        input_frame.pack(fill='x', padx=10, pady=5)

        ttk.Label(input_frame, text="Vendite Annue (unità):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.vendite_entry = ttk.Entry(input_frame, width=15)
        self.vendite_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Stock Medio (unità):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.stock_entry = ttk.Entry(input_frame, width=15)
        self.stock_entry.grid(row=1, column=1, padx=5, pady=5)

        btn_calcola = ttk.Button(input_frame, text="Calcola Rotazione", command=self.calcola_rotazione_click)
        btn_calcola.grid(row=2, column=0, padx=5, pady=10)
        ttk.Button(input_frame, text="Pulisci", command=self.clear_tab5).grid(row=2, column=1, padx=5, pady=10)

        # Frame risultati
        result_frame = ttk.LabelFrame(parent, text="Risultati", padding=10)
        result_frame.pack(fill='x', padx=10, pady=5)
        self.result_label_5 = ttk.Label(result_frame, text="", justify=tk.LEFT)
        self.result_label_5.pack()

        # Frame spiegazione
        explain_frame = ttk.LabelFrame(parent, text="Spiegazione Calcolo", padding=10)
        explain_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        explanation = """
Formula Rotazione = Vendite_annue_unità ÷ Stock_medio_unità

🎯 Quando usarla: Controllare se lo stock "gira" velocemente (efficienza magazzino).

📊 Valutazione rotazione:
• 10-20x/anno: 🏆 Ottimo
• 5-10x/anno: 👍 Buono  
• 3-5x/anno: ⚠️ Sufficiente
• <3x/anno: 🚨 Migliora stock

📝 Esempio pratico:
1200 capsule vendute/anno, stock medio 100 unità
Rotazione: 1200÷100 = 12x/anno (🏆 Ottimo!)

🔄 Significato: Quante volte all'anno rinnovi completamente il tuo stock.
        """.strip()
        
        explain_text = tk.Text(explain_frame, height=12, wrap=tk.WORD)
        explain_text.insert(tk.END, explanation)
        explain_text.config(state=tk.DISABLED)
        scrollbar = ttk.Scrollbar(explain_frame, orient=tk.VERTICAL, command=explain_text.yview)
        explain_text.configure(yscrollcommand=scrollbar.set)
        explain_text.pack(side=tk.LEFT, fill='both', expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def calcola_rotazione_click(self):
        try:
            vendite = float(self.vendite_entry.get())
            stock = float(self.stock_entry.get())
            rotaz = rotazione(vendite, stock)
            valutazione = ""
            if rotaz >= 10:
                valutazione = "🏆 Ottimo"
            elif rotaz >= 5:
                valutazione = "👍 Buono"
            elif rotaz >= 3:
                valutazione = "⚠️ Sufficiente"
            else:
                valutazione = "🚨 Migliora stock"

            self.result_label_5.config(
                text=f"Rotazione: {rotaz}x/anno\nValutazione: {valutazione}"
            )
        except Exception as e:
            messagebox.showerror("Errore", f"Inserisci valori numerici validi!\n{str(e)}")

    def clear_tab5(self):
        self.vendite_entry.delete(0, tk.END)
        self.stock_entry.delete(0, tk.END)
        self.result_label_5.config(text="")

    # === TAB 6: Calcolatore Completo ===
    def _setup_tab_calcolatore_completo(self, parent):
        # Frame input
        input_frame = ttk.LabelFrame(parent, text="Input Dati", padding=10)
        input_frame.pack(fill='x', padx=10, pady=5)

        # Prezzo Totale
        ttk.Label(input_frame, text="Prezzo Totale Lotto (€):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.completo_prezzo_entry = ttk.Entry(input_frame, width=15)
        self.completo_prezzo_entry.grid(row=0, column=1, padx=5, pady=5)

        # Numero Componenti
        ttk.Label(input_frame, text="Numero Componenti:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.completo_componenti_entry = ttk.Entry(input_frame, width=15)
        self.completo_componenti_entry.insert(0, "1")
        self.completo_componenti_entry.grid(row=1, column=1, padx=5, pady=5)

        # IVA
        ttk.Label(input_frame, text="IVA (%):").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.completo_iva_var = tk.DoubleVar(value=22.0)
        iva_frame = ttk.Frame(input_frame)
        iva_frame.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Radiobutton(iva_frame, text="22%", variable=self.completo_iva_var, value=22.0).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(iva_frame, text="10%", variable=self.completo_iva_var, value=10.0).pack(side=tk.LEFT, padx=5)

        # Margine
        ttk.Label(input_frame, text="Margine Desiderato (%):").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.completo_margine_entry = ttk.Entry(input_frame, width=15)
        self.completo_margine_entry.grid(row=3, column=1, padx=5, pady=5)

        # Bottoni
        btn_calcola = ttk.Button(input_frame, text="Calcola Dettagli", command=self.calcola_completo_click)
        btn_calcola.grid(row=4, column=0, padx=5, pady=10)
        ttk.Button(input_frame, text="Pulisci", command=self.clear_tab6).grid(row=4, column=1, padx=5, pady=10)

        # Output Area (Text widget per output dettagliato)
        output_frame = ttk.LabelFrame(parent, text="Dettaglio Calcoli", padding=10)
        output_frame.pack(fill='both', expand=True, padx=10, pady=5)

        self.completo_output_text = tk.Text(output_frame, height=15, width=60, font=("Consolas", 10))
        self.completo_output_text.pack(side=tk.LEFT, fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(output_frame, orient=tk.VERTICAL, command=self.completo_output_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.completo_output_text.config(yscrollcommand=scrollbar.set)

    def calcola_completo_click(self):
        try:
            prezzo_totale = float(self.completo_prezzo_entry.get())
            componenti = int(self.completo_componenti_entry.get())
            iva = self.completo_iva_var.get()
            margine = float(self.completo_margine_entry.get())

            risultato = calcola_prezzo_finale(prezzo_totale, componenti, iva, margine)
            
            # Formattazione output (simile a stampa_risultato ma su stringa)
            lines = []
            if risultato['numero_componenti'] > 1:
                lines.append(f"{'='*60}")
                lines.append(f"💼 LOTTO ({risultato['numero_componenti']} componenti)")
                lines.append(f"Costo totale lotto:    €{risultato['prezzo_totale']:>10.2f}")
                lines.append(f"Costo unitario:        €{risultato['prezzo_unitario']:>10.2f}")
                lines.append(f"{'='*60}")
                lines.append(f"📦 CALCOLO UNITARIO")
                lines.append(f"Prezzo unitario:       €{risultato['prezzo_unitario']:>10.2f}")
                lines.append(f"IVA ({risultato['iva_percentuale']:>2.0f}%):             €{risultato['importo_iva_unitario']:>10.2f}")
                lines.append(f"Prezzo con IVA:        €{risultato['prezzo_unitario_con_iva']:>10.2f}")
                lines.append(f"Margine ({risultato['margine_percentuale']:>2.0f}%):          €{risultato['importo_margine_unitario']:>10.2f}")
                lines.append(f"{'='*60}")
                lines.append(f"💰 PREZZO FINALE UNITARIO: €{risultato['prezzo_finale_unitario']:>10.2f}")
                lines.append(f"{'='*60}")
                lines.append(f"🔢 TOTALI LOTTO COMPLETO")
                lines.append(f"Ricavo totale:         €{risultato['totale_finale']:>10.2f}")
                lines.append(f"Guadagno totale:       €{risultato['totale_finale'] - risultato['totale_con_iva']:>10.2f}")
                lines.append(f"{'='*60}")
            else:
                lines.append(f"{'='*50}")
                lines.append(f"Prezzo base:        €{risultato['prezzo_unitario']:>10.2f}")
                lines.append(f"IVA ({risultato['iva_percentuale']:>2.0f}%):          €{risultato['importo_iva_unitario']:>10.2f}")
                lines.append(f"Prezzo con IVA:     €{risultato['prezzo_unitario_con_iva']:>10.2f}")
                lines.append(f"Margine ({risultato['margine_percentuale']:>2.0f}%):       €{risultato['importo_margine_unitario']:>10.2f}")
                lines.append(f"{'='*50}")
                lines.append(f"PREZZO FINALE:      €{risultato['prezzo_finale_unitario']:>10.2f}")
                lines.append(f"{'='*50}")

            # Aggiorna Widget Testo
            self.completo_output_text.delete(1.0, tk.END)
            self.completo_output_text.insert(tk.END, "\n".join(lines))

        except Exception as e:
            messagebox.showerror("Errore", f"Errore nel calcolo:\n{str(e)}")

    def clear_tab6(self):
        self.completo_prezzo_entry.delete(0, tk.END)
        self.completo_componenti_entry.delete(0, tk.END)
        self.completo_componenti_entry.insert(0, "1")
        self.completo_margine_entry.delete(0, tk.END)
        self.completo_output_text.delete(1.0, tk.END)

    # === TAB 7: Ottimizzazione Prezzo ===
    def _setup_tab_ottimizzazione(self, parent):
        # Frame input
        input_frame = ttk.LabelFrame(parent, text="Dati Scenari (per stima domanda)", padding=10)
        input_frame.pack(fill='x', padx=10, pady=5)

        # Costo Prodotto
        ttk.Label(input_frame, text="Costo Prodotto (€):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.opt_costo_entry = ttk.Entry(input_frame, width=15)
        self.opt_costo_entry.grid(row=0, column=1, padx=5, pady=5)

        # Scenario A (Attuale)
        ttk.Label(input_frame, text="SCENARIO A (Attuale)", font=("Arial", 10, "bold")).grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=10)
        
        ttk.Label(input_frame, text="Prezzo Vendita (€):").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.opt_p_old_entry = ttk.Entry(input_frame, width=15)
        self.opt_p_old_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Vendite (Unità):").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.opt_q_old_entry = ttk.Entry(input_frame, width=15)
        self.opt_q_old_entry.grid(row=3, column=1, padx=5, pady=5)

        # Scenario B (Nuovo/Test)
        ttk.Label(input_frame, text="SCENARIO B (Test/Passato)", font=("Arial", 10, "bold")).grid(row=1, column=2, columnspan=2, sticky=tk.W, pady=10, padx=20)

        ttk.Label(input_frame, text="Prezzo Vendita (€):").grid(row=2, column=2, sticky=tk.W, padx=5, pady=5)
        self.opt_p_new_entry = ttk.Entry(input_frame, width=15)
        self.opt_p_new_entry.grid(row=2, column=3, padx=5, pady=5)

        ttk.Label(input_frame, text="Vendite (Unità):").grid(row=3, column=2, sticky=tk.W, padx=5, pady=5)
        self.opt_q_new_entry = ttk.Entry(input_frame, width=15)
        self.opt_q_new_entry.grid(row=3, column=3, padx=5, pady=5)

        # Bottoni
        btn_calcola = ttk.Button(input_frame, text="Calcola Ottimizzazione", command=self.calcola_ottimizzazione_click)
        btn_calcola.grid(row=4, column=0, columnspan=2, pady=15)
        ttk.Button(input_frame, text="Pulisci", command=self.clear_tab7).grid(row=4, column=2, columnspan=2, pady=15)

        # Output Area
        output_frame = ttk.LabelFrame(parent, text="Analisi e Risultati", padding=10)
        output_frame.pack(fill='both', expand=True, padx=10, pady=5)

        self.opt_output_text = tk.Text(output_frame, height=15, width=60, font=("Consolas", 10))
        self.opt_output_text.pack(side=tk.LEFT, fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(output_frame, orient=tk.VERTICAL, command=self.opt_output_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.opt_output_text.config(yscrollcommand=scrollbar.set)

    def calcola_ottimizzazione_click(self):
        try:
            costo = float(self.opt_costo_entry.get())
            p_old = float(self.opt_p_old_entry.get())
            q_old = float(self.opt_q_old_entry.get())
            p_new = float(self.opt_p_new_entry.get())
            q_new = float(self.opt_q_new_entry.get())

            risultato = ottimizza_prezzo(costo, p_old, q_old, p_new, q_new)
            
            if 'error' in risultato:
                messagebox.showerror("Errore", risultato['error'])
                return

            # Interpretazione Elasticità
            ela = risultato['elasticita']
            if abs(ela) > 1:
                ela_desc = "Elastica (Sensibile al prezzo)"
                consiglio = "Ridurre il prezzo potrebbe aumentare i ricavi totali."
            elif abs(ela) < 1:
                ela_desc = "Anelastica (Poco sensibile)"
                consiglio = "Aumentare il prezzo potrebbe aumentare i ricavi senza perdere troppe vendite."
            else:
                ela_desc = "Unitaria"
                consiglio = "Siamon in un punto di equilibrio dei ricavi."

            lines = [
                f"{'='*50}",
                f"📊 ANALISI DELLA DOMANDA",
                f"{'='*50}",
                f"Elasticità calcolata: {ela}",
                f"Tipo domanda:         {ela_desc}",
                f"",
                f"Curva Domanda stimata: Q = {risultato['domanda_a']} {risultato['domanda_b']} * P",
                f"{'='*50}",
                f"🏆 PREZZO OTTIMALE (Massimizzazione Profitto)",
                f"{'='*50}",
                f"Prezzo Suggerito:     € {risultato['prezzo_ottimale']}",
                f"Quantità Stimata:       {risultato['quantita_stimata']} unità",
                f"Profitto Stimato:     € {risultato['profitto_stimato']}",
                f"Ricavo Stimato:       € {risultato['ricavo_stimato']}",
                f"{'='*50}",
                f"💡 CONSIGLIO:",
                f"{consiglio}"
            ]

            self.opt_output_text.delete(1.0, tk.END)
            self.opt_output_text.insert(tk.END, "\n".join(lines))

        except Exception as e:
            messagebox.showerror("Errore", f"Inserisci valori numerici validi!\n{str(e)}")

    def clear_tab7(self):
        self.opt_costo_entry.delete(0, tk.END)
        self.opt_p_old_entry.delete(0, tk.END)
        self.opt_q_old_entry.delete(0, tk.END)
        self.opt_p_new_entry.delete(0, tk.END)
        self.opt_q_new_entry.delete(0, tk.END)
        self.opt_output_text.delete(1.0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = CalcolatoreMarginiGUI(root)
    root.mainloop()