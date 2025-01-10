import tkinter as tk
from tkinter import ttk
import winsound
import time
import threading

class DemoSons:
    def __init__(self, master):
        self.master = master
        self.master.title("Demonstração de Sons")
        self.master.geometry("600x800")
        self.master.configure(bg='#1a1a1a')

        # Notas musicais e suas frequências
        self.notas = {
            'Dó': 261,
            'Ré': 293,
            'Mi': 329,
            'Fá': 349,
            'Sol': 392,
            'Lá': 440,
            'Si': 493,
            'Dó+': 523
        }

        # Melodias predefinidas
        self.melodias = {
            'Parabéns': [
                (self.notas['Dó'], 300), (self.notas['Dó'], 300),
                (self.notas['Ré'], 300), (self.notas['Dó'], 300),
                (self.notas['Fá'], 300), (self.notas['Mi'], 500),
            ],
            'Ode à Alegria': [
                (self.notas['Mi'], 300), (self.notas['Mi'], 300),
                (self.notas['Fá'], 300), (self.notas['Sol'], 300),
                (self.notas['Sol'], 300), (self.notas['Fá'], 300),
                (self.notas['Mi'], 300), (self.notas['Ré'], 300),
            ],
            'Escala Completa': [(freq, 300) for freq in self.notas.values()]
        }

        self.criar_interface()

    def criar_interface(self):
        # Estilo
        style = ttk.Style()
        style.configure('TButton', padding=5)

        # Frame principal
        main_frame = tk.Frame(self.master, bg='#1a1a1a')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)

        # Título
        tk.Label(main_frame,
                text="Demonstração de Sons",
                font=('Helvetica', 24, 'bold'),
                bg='#1a1a1a',
                fg='white').pack(pady=20)

        # Frame para notas individuais
        notas_frame = tk.LabelFrame(main_frame,
                                  text="Notas Individuais",
                                  font=('Helvetica', 12),
                                  bg='#1a1a1a',
                                  fg='white')
        notas_frame.pack(fill='x', padx=10, pady=10)

        # Criar grid de botões para notas
        row, col = 0, 0
        for nota, freq in self.notas.items():
            btn = tk.Button(notas_frame,
                          text=f"{nota}\n{freq}Hz",
                          command=lambda f=freq: self.tocar_nota(f),
                          bg='#2d2d2d',
                          fg='white',
                          width=10,
                          height=2)
            btn.grid(row=row, column=col, padx=5, pady=5)
            col += 1
            if col > 3:
                col = 0
                row += 1

        # Frame para acordes
        acordes_frame = tk.LabelFrame(main_frame,
                                   text="Acordes",
                                   font=('Helvetica', 12),
                                   bg='#1a1a1a',
                                   fg='white')
        acordes_frame.pack(fill='x', padx=10, pady=10)

        # Botões para acordes
        acordes = {
            'Dó Maior': [self.notas['Dó'], self.notas['Mi'], self.notas['Sol']],
            'Ré Menor': [self.notas['Ré'], self.notas['Fá'], self.notas['Lá']],
            'Mi Menor': [self.notas['Mi'], self.notas['Sol'], self.notas['Si']],
            'Fá Maior': [self.notas['Fá'], self.notas['Lá'], self.notas['Dó+']]
        }

        for nome, notas in acordes.items():
            btn = tk.Button(acordes_frame,
                          text=nome,
                          command=lambda n=notas: self.tocar_acorde(n),
                          bg='#2d2d2d',
                          fg='white',
                          width=20)
            btn.pack(pady=5)

        # Frame para melodias
        melodias_frame = tk.LabelFrame(main_frame,
                                    text="Melodias",
                                    font=('Helvetica', 12),
                                    bg='#1a1a1a',
                                    fg='white')
        melodias_frame.pack(fill='x', padx=10, pady=10)

        # Botões para melodias
        for nome, melodia in self.melodias.items():
            btn = tk.Button(melodias_frame,
                          text=nome,
                          command=lambda m=melodia: self.tocar_melodia(m),
                          bg='#2d2d2d',
                          fg='white',
                          width=20)
            btn.pack(pady=5)

        # Controle de duração
        controle_frame = tk.LabelFrame(main_frame,
                                    text="Controles",
                                    font=('Helvetica', 12),
                                    bg='#1a1a1a',
                                    fg='white')
        controle_frame.pack(fill='x', padx=10, pady=10)

        tk.Label(controle_frame,
                text="Duração (ms):",
                bg='#1a1a1a',
                fg='white').pack(side='left', padx=5)

        self.duracao = ttk.Scale(controle_frame,
                               from_=50,
                               to=1000,
                               orient='horizontal')
        self.duracao.set(300)
        self.duracao.pack(side='left', fill='x', expand=True, padx=5)

    def tocar_nota(self, freq):
        def play():
            winsound.Beep(freq, int(self.duracao.get()))
        threading.Thread(target=play, daemon=True).start()

    def tocar_acorde(self, notas):
        def play():
            for freq in notas:
                winsound.Beep(freq, 300)
                time.sleep(0.05)
        threading.Thread(target=play, daemon=True).start()

    def tocar_melodia(self, melodia):
        def play():
            for freq, dur in melodia:
                winsound.Beep(freq, dur)
                time.sleep(0.1)
        threading.Thread(target=play, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = DemoSons(root)
    root.mainloop()
