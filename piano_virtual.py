import tkinter as tk
from tkinter import ttk, messagebox
import winsound
import threading
import time
import json
import os
from datetime import datetime
import wave
import struct
import math

class PianoVirtual:
    def __init__(self, master):
        self.master = master
        self.master.title("Piano Virtual Python")
        self.master.geometry("800x800")  
        self.master.configure(bg='#1a1a1a')

        # Configurações de gravação
        self.gravando = False
        self.notas_gravadas = []
        self.tempo_inicial = 0
        self.diretorio_gravacoes = "gravacoes"
        if not os.path.exists(self.diretorio_gravacoes):
            os.makedirs(self.diretorio_gravacoes)

        # Configurações de áudio para exportação
        self.sample_rate = 44100  # Hz
        self.amplitude = 0.5
        self.diretorio_exports = "exports"
        if not os.path.exists(self.diretorio_exports):
            os.makedirs(self.diretorio_exports)

        # Cores e estilos
        self.cores = {
            'bg': '#1a1a1a',
            'fg': '#ffffff',
            'tecla_branca': '#ffffff',
            'tecla_branca_pressed': '#cccccc',
            'tecla_preta': '#1a1a1a',
            'tecla_preta_pressed': '#4a4a4a',
            'botao': '#2d2d2d',
            'botao_hover': '#3d3d3d',
            'destaque': '#00ff00',
            'gravando': '#ff4444'
        }

        # Estilo para os widgets
        style = ttk.Style()
        style.configure("TScale",
                      background=self.cores['bg'],
                      troughcolor=self.cores['botao'],
                      darkcolor=self.cores['botao_hover'],
                      lightcolor=self.cores['botao_hover'])

        # Dicionário de notas musicais e suas frequências
        self.notas = {
            'Dó': 261,    'Dó#': 277,
            'Ré': 293,    'Ré#': 311,
            'Mi': 329,
            'Fá': 349,    'Fá#': 370,
            'Sol': 392,   'Sol#': 415,
            'Lá': 440,    'Lá#': 466,
            'Si': 493,
            'Dó²': 523,   'Dó²#': 554,
            'Ré²': 587,   'Ré²#': 622,
            'Mi²': 659
        }

        # Mapeamento de teclas do teclado para notas
        self.teclas_para_notas = {
            'a': 'Dó',    'w': 'Dó#',
            's': 'Ré',    'e': 'Ré#',
            'd': 'Mi',
            'f': 'Fá',    't': 'Fá#',
            'g': 'Sol',   'y': 'Sol#',
            'h': 'Lá',    'u': 'Lá#',
            'j': 'Si',
            'k': 'Dó²',   'o': 'Dó²#',
            'l': 'Ré²',   'p': 'Ré²#',
            ';': 'Mi²'
        }

        # Dicionário de músicas
        self.musicas = {
            'Ode à Alegria': [
                ('Mi', 400), ('Mi', 400), ('Fá', 400), ('Sol', 400),
                ('Sol', 400), ('Fá', 400), ('Mi', 400), ('Ré', 400),
                ('Dó', 400), ('Dó', 400), ('Ré', 400), ('Mi', 400),
                ('Mi', 600), ('Ré', 200), ('Ré', 800)
            ],
            'Parabéns': [
                ('Dó', 300), ('Dó', 300),
                ('Ré', 600),
                ('Dó', 600),
                ('Fá', 600),
                ('Mi', 1200),
                ('Dó', 300), ('Dó', 300),
                ('Ré', 600),
                ('Dó', 600),
                ('Sol', 600),
                ('Fá', 1200)
            ],
            'Fur Elise': [
                ('Mi²', 200), ('Ré²#', 200), ('Mi²', 200), ('Ré²#', 200), ('Mi²', 200),
                ('Si', 200), ('Ré²', 200), ('Dó²', 200), ('Lá', 400),
                ('Dó', 200), ('Mi', 200), ('Lá', 200), ('Si', 400)
            ]
        }

        self.teclas_botoes = {}  
        self.criar_interface()
        self.configurar_atalhos()
        
        self.tocando = False
        self.nota_atual = None
        self.modo_aprendizado = False
        self.nota_esperada = None
        self.indice_atual = 0
        self.pontuacao = 0
        self.musica_atual = None
        self.total_notas = 0

    def configurar_atalhos(self):
        self.master.bind('<KeyPress>', self.tecla_pressionada)
        self.master.bind('<KeyRelease>', self.tecla_solta)

    def tecla_pressionada(self, evento):
        if evento.char in self.teclas_para_notas:
            nota = self.teclas_para_notas[evento.char]
            self.destacar_tecla(nota)
            self.tocar_nota(self.notas[nota], nota)

            # Verificar se está no modo aprendizado
            if self.modo_aprendizado and self.nota_esperada:
                if nota == self.nota_esperada:
                    self.pontuacao += 1
                    self.label_pontuacao.configure(
                        text=f"Pontuação: {self.pontuacao}/{self.total_notas}"
                    )
                    self.indice_atual += 1
                    self.master.after(300, self.proxima_nota)

    def tecla_solta(self, evento):
        if evento.char in self.teclas_para_notas:
            nota = self.teclas_para_notas[evento.char]
            self.restaurar_tecla(nota)

    def destacar_tecla(self, nota):
        if nota in self.teclas_botoes:
            btn = self.teclas_botoes[nota]
            if '#' in nota:
                btn.configure(bg=self.cores['tecla_preta_pressed'])
            else:
                btn.configure(bg=self.cores['tecla_branca_pressed'])

    def restaurar_tecla(self, nota):
        if nota in self.teclas_botoes:
            btn = self.teclas_botoes[nota]
            if '#' in nota:
                btn.configure(bg=self.cores['tecla_preta'])
            else:
                btn.configure(bg=self.cores['tecla_branca'])

    def criar_interface(self):
        # Estilo
        style = ttk.Style()
        style.configure('TButton', padding=5)

        # Frame principal
        main_frame = tk.Frame(self.master, bg=self.cores['bg'])
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)

        # Título
        tk.Label(main_frame,
                text="Piano Virtual Python",
                font=('Helvetica', 24, 'bold'),
                bg=self.cores['bg'],
                fg=self.cores['fg']).pack(pady=10)

        # Container para as duas colunas
        colunas_frame = tk.Frame(main_frame, bg=self.cores['bg'])
        colunas_frame.pack(expand=True, fill='both')

        # Coluna esquerda (Piano e Controles)
        coluna_esquerda = tk.Frame(colunas_frame, bg=self.cores['bg'])
        coluna_esquerda.pack(side='left', fill='both', expand=True, padx=10)

        # Piano
        piano_frame = tk.LabelFrame(coluna_esquerda,
                                  text="Piano",
                                  font=('Helvetica', 12),
                                  bg=self.cores['bg'],
                                  fg=self.cores['fg'])
        piano_frame.pack(fill='x', pady=5)

        # Criar teclas do piano
        self.criar_teclas(piano_frame)

        # Controles básicos
        controles_frame = tk.LabelFrame(coluna_esquerda,
                                      text="Controles",
                                      font=('Helvetica', 12),
                                      bg=self.cores['bg'],
                                      fg=self.cores['fg'])
        controles_frame.pack(fill='x', pady=5)

        tk.Label(controles_frame,
                text="Duração (ms):",
                bg=self.cores['bg'],
                fg=self.cores['fg']).pack(side='left', padx=5)

        self.duracao = ttk.Scale(controles_frame,
                               from_=50,
                               to=1000,
                               orient='horizontal')
        self.duracao.set(300)
        self.duracao.pack(side='left', fill='x', expand=True, padx=5)

        # Coluna direita (Funções)
        coluna_direita = tk.Frame(colunas_frame, bg=self.cores['bg'])
        coluna_direita.pack(side='left', fill='both', expand=True, padx=10)

        # Frame para gravação e exportação
        gravacao_frame = tk.LabelFrame(coluna_direita,
                                     text="Gravação e Exportação",
                                     font=('Helvetica', 12),
                                     bg=self.cores['bg'],
                                     fg=self.cores['fg'])
        gravacao_frame.pack(fill='x', pady=5)

        # Botões de gravação
        botoes_gravacao = tk.Frame(gravacao_frame, bg=self.cores['bg'])
        botoes_gravacao.pack(fill='x', pady=5)

        self.btn_gravar = tk.Button(botoes_gravacao,
                                  text="🔴 Iniciar Gravação",
                                  command=self.alternar_gravacao,
                                  bg=self.cores['botao'],
                                  fg=self.cores['fg'],
                                  relief=tk.FLAT,
                                  width=20)
        self.btn_gravar.pack(side='left', padx=5)

        self.btn_reproduzir = tk.Button(botoes_gravacao,
                                      text="▶️ Reproduzir Última",
                                      command=self.reproduzir_gravacao,
                                      bg=self.cores['botao'],
                                      fg=self.cores['fg'],
                                      relief=tk.FLAT,
                                      width=20,
                                      state='disabled')
        self.btn_reproduzir.pack(side='left', padx=5)

        # Botões de exportação
        botoes_export = tk.Frame(gravacao_frame, bg=self.cores['bg'])
        botoes_export.pack(fill='x', pady=5)

        self.btn_export_gravacao = tk.Button(botoes_export,
                                           text="💾 Exportar Última Gravação",
                                           command=self.exportar_gravacao,
                                           bg=self.cores['botao'],
                                           fg=self.cores['fg'],
                                           relief=tk.FLAT,
                                           width=20,
                                           state='disabled')
        self.btn_export_gravacao.pack(side='left', padx=5)

        self.btn_export_melodia = tk.Button(botoes_export,
                                          text="💾 Exportar Melodia",
                                          command=self.escolher_melodia_export,
                                          bg=self.cores['botao'],
                                          fg=self.cores['fg'],
                                          relief=tk.FLAT,
                                          width=20)
        self.btn_export_melodia.pack(side='left', padx=5)

        # Lista de gravações
        self.lista_gravacoes = tk.Listbox(gravacao_frame,
                                        bg=self.cores['botao'],
                                        fg=self.cores['fg'],
                                        selectmode=tk.SINGLE,
                                        height=3)
        self.lista_gravacoes.pack(fill='x', padx=5, pady=5)
        self.atualizar_lista_gravacoes()

        # Botão para carregar gravação
        tk.Button(gravacao_frame,
                 text="📂 Carregar Gravação Selecionada",
                 command=self.carregar_gravacao,
                 bg=self.cores['botao'],
                 fg=self.cores['fg'],
                 relief=tk.FLAT).pack(fill='x', padx=5, pady=5)

        # Frame para melodias predefinidas
        melodias_frame = tk.LabelFrame(coluna_direita,
                                     text="Melodias Predefinidas",
                                     font=('Helvetica', 12),
                                     bg=self.cores['bg'],
                                     fg=self.cores['fg'])
        melodias_frame.pack(fill='x', pady=5)

        # Grid de botões para melodias
        for i, (nome_musica, _) in enumerate(self.musicas.items()):
            btn = tk.Button(melodias_frame,
                          text=nome_musica,
                          command=lambda n=nome_musica: self.tocar_musica(n),
                          bg=self.cores['botao'],
                          fg=self.cores['fg'],
                          relief=tk.FLAT,
                          width=20)
            btn.pack(pady=2)

        self.btn_parar = tk.Button(melodias_frame,
                                 text="⏹ Parar",
                                 command=self.parar_musica,
                                 bg=self.cores['botao'],
                                 fg=self.cores['fg'],
                                 relief=tk.FLAT,
                                 width=20,
                                 state='disabled')
        self.btn_parar.pack(pady=5)

        # Frame para modo aprendizado
        aprendizado_frame = tk.LabelFrame(coluna_direita,
                                        text="Modo Aprendizado",
                                        font=('Helvetica', 12),
                                        bg=self.cores['bg'],
                                        fg=self.cores['fg'])
        aprendizado_frame.pack(fill='x', pady=5)

        # Informações do aprendizado
        self.info_aprendizado = tk.Frame(aprendizado_frame, bg=self.cores['bg'])
        self.info_aprendizado.pack(fill='x', pady=5)

        self.label_proxima_nota = tk.Label(self.info_aprendizado,
                                         text="",
                                         font=('Helvetica', 12),
                                         bg=self.cores['bg'],
                                         fg=self.cores['destaque'])
        self.label_proxima_nota.pack()

        self.label_pontuacao = tk.Label(self.info_aprendizado,
                                      text="Pontuação: 0",
                                      font=('Helvetica', 12),
                                      bg=self.cores['bg'],
                                      fg=self.cores['fg'])
        self.label_pontuacao.pack()

        # Botões do modo aprendizado
        botoes_aprendizado = tk.Frame(aprendizado_frame, bg=self.cores['bg'])
        botoes_aprendizado.pack(fill='x', pady=5)

        self.btn_aprendizado = tk.Button(botoes_aprendizado,
                                       text="✏️ Iniciar Modo Aprendizado",
                                       command=self.alternar_modo_aprendizado,
                                       bg=self.cores['botao'],
                                       fg=self.cores['fg'],
                                       relief=tk.FLAT,
                                       width=20)
        self.btn_aprendizado.pack(side='left', padx=5)

        self.btn_dica = tk.Button(botoes_aprendizado,
                                text="💡 Mostrar Dica",
                                command=self.mostrar_dica,
                                bg=self.cores['botao'],
                                fg=self.cores['fg'],
                                relief=tk.FLAT,
                                width=15,
                                state='disabled')
        self.btn_dica.pack(side='left', padx=5)

    def alternar_modo_aprendizado(self):
        self.modo_aprendizado = not self.modo_aprendizado
        if self.modo_aprendizado:
            self.btn_aprendizado.configure(text="⏹ Parar Modo Aprendizado",
                                         bg=self.cores['gravando'])
            self.btn_dica.configure(state='normal')
            self.escolher_musica_aprendizado()
        else:
            self.btn_aprendizado.configure(text="✏️ Iniciar Modo Aprendizado",
                                         bg=self.cores['botao'])
            self.btn_dica.configure(state='disabled')
            self.label_proxima_nota.configure(text="")
            self.resetar_destaque_teclas()
            self.musica_atual = None

    def escolher_musica_aprendizado(self):
        # Criar janela de escolha
        escolha = tk.Toplevel(self.master)
        escolha.title("Escolha uma música")
        escolha.geometry("300x400")
        escolha.configure(bg=self.cores['bg'])

        tk.Label(escolha,
                text="Escolha uma música para aprender:",
                font=('Helvetica', 12),
                bg=self.cores['bg'],
                fg=self.cores['fg']).pack(pady=10)

        for nome in self.musicas.keys():
            tk.Button(escolha,
                     text=nome,
                     command=lambda n=nome: self.iniciar_aprendizado(n, escolha),
                     bg=self.cores['botao'],
                     fg=self.cores['fg'],
                     relief=tk.FLAT,
                     width=25).pack(pady=2)

    def iniciar_aprendizado(self, nome_musica, janela_escolha):
        self.musica_atual = nome_musica
        self.indice_atual = 0
        self.pontuacao = 0
        self.total_notas = len(self.musicas[nome_musica])
        self.proxima_nota()
        janela_escolha.destroy()
        self.label_pontuacao.configure(text=f"Pontuação: 0/{self.total_notas}")

    def proxima_nota(self):
        if not self.modo_aprendizado or not self.musica_atual:
            return

        if self.indice_atual < len(self.musicas[self.musica_atual]):
            nota, _ = self.musicas[self.musica_atual][self.indice_atual]
            self.nota_esperada = nota
            self.label_proxima_nota.configure(
                text=f"Próxima nota: {nota} (Use a tecla {self.encontrar_tecla(nota)})"
            )
            # Piscar a tecla como dica inicial
            self.piscar_tecla(nota)
        else:
            # Música completada
            porcentagem = (self.pontuacao / self.total_notas) * 100
            messagebox.showinfo(
                "Parabéns!",
                f"Você completou a música!\nPontuação final: {self.pontuacao}/{self.total_notas} ({porcentagem:.1f}%)"
            )
            self.alternar_modo_aprendizado()

    def encontrar_tecla(self, nota):
        for tecla, n in self.teclas_para_notas.items():
            if n == nota:
                return tecla.upper()
        return "?"

    def piscar_tecla(self, nota):
        self.destacar_tecla(nota)
        self.master.after(500, lambda: self.restaurar_tecla(nota))

    def mostrar_dica(self):
        if self.nota_esperada:
            self.piscar_tecla(self.nota_esperada)

    def criar_teclas(self, frame):
        teclas_frame = tk.Frame(frame, bg=self.cores['bg'])
        teclas_frame.pack()

        for nota, freq in self.notas.items():
            # Determinar se é tecla preta (sustenido)
            is_sustenido = '#' in nota
            
            # Configurar aparência 3D
            if is_sustenido:
                bg_color = self.cores['tecla_preta']
                fg_color = self.cores['fg']
                altura = 3  
                relevo = tk.RAISED
                borda = 2
            else:
                bg_color = self.cores['tecla_branca']
                fg_color = self.cores['tecla_preta']
                altura = 5
                relevo = tk.RAISED
                borda = 2

            # Encontrar a tecla correspondente
            tecla = [k for k, v in self.teclas_para_notas.items() if v == nota]
            tecla_texto = f"{nota}\n{freq}Hz\n[{tecla[0].upper()}]" if tecla else f"{nota}\n{freq}Hz"

            btn = tk.Button(teclas_frame,
                          text=tecla_texto,
                          width=6,
                          height=altura,
                          bg=bg_color,
                          fg=fg_color,
                          relief=relevo,
                          bd=borda)
            
            # Efeitos de hover e clique
            btn.bind('<Enter>', lambda e, b=btn: self.hover_enter(b))
            btn.bind('<Leave>', lambda e, b=btn: self.hover_leave(b))
            btn.bind('<Button-1>', lambda e, f=freq, n=nota: self.clicar_tecla(f, n))
            btn.bind('<ButtonRelease-1>', lambda e, n=nota: self.soltar_tecla(n))
            
            btn.pack(side='left', padx=1)
            self.teclas_botoes[nota] = btn

    def alternar_gravacao(self):
        self.gravando = not self.gravando
        if self.gravando:
            self.notas_gravadas = []
            self.tempo_inicial = time.time()
            self.btn_gravar.configure(text="⏹ Parar Gravação",
                                    bg=self.cores['gravando'])
            self.btn_reproduzir.configure(state='disabled')
            self.btn_salvar.configure(state='disabled')
            self.btn_export_gravacao.configure(state='disabled')
        else:
            self.btn_gravar.configure(text="🔴 Iniciar Gravação",
                                    bg=self.cores['botao'])
            if self.notas_gravadas:
                self.btn_reproduzir.configure(state='normal')
                self.btn_salvar.configure(state='normal')
                self.btn_export_gravacao.configure(state='normal')

    def tocar_nota(self, frequencia, nota=None):
        def tocar():
            winsound.Beep(frequencia, int(self.duracao.get()))
        threading.Thread(target=tocar, daemon=True).start()

        # Gravar a nota se estiver gravando
        if self.gravando and nota:
            tempo_atual = time.time() - self.tempo_inicial
            self.notas_gravadas.append({
                'nota': nota,
                'frequencia': frequencia,
                'tempo': tempo_atual,
                'duracao': int(self.duracao.get())
            })

    def reproduzir_gravacao(self):
        if not self.notas_gravadas:
            return

        def reproduzir():
            tempo_anterior = 0
            for nota in self.notas_gravadas:
                # Esperar o tempo correto entre as notas
                espera = nota['tempo'] - tempo_anterior
                if espera > 0:
                    time.sleep(espera)
                
                # Destacar a tecla
                self.destacar_tecla(nota['nota'])
                winsound.Beep(nota['frequencia'], nota['duracao'])
                self.restaurar_tecla(nota['nota'])
                
                tempo_anterior = nota['tempo']

        threading.Thread(target=reproduzir, daemon=True).start()

    def salvar_gravacao(self):
        if not self.notas_gravadas:
            return

        nome = f"gravacao_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        caminho = os.path.join(self.diretorio_gravacoes, nome)
        
        with open(caminho, 'w') as f:
            json.dump(self.notas_gravadas, f)
        
        self.atualizar_lista_gravacoes()
        messagebox.showinfo("Sucesso", f"Gravação salva como {nome}")

    def carregar_gravacao(self):
        selecao = self.lista_gravacoes.curselection()
        if not selecao:
            return

        nome_arquivo = self.lista_gravacoes.get(selecao[0])
        caminho = os.path.join(self.diretorio_gravacoes, nome_arquivo)
        
        with open(caminho, 'r') as f:
            self.notas_gravadas = json.load(f)
        
        self.btn_reproduzir.configure(state='normal')
        messagebox.showinfo("Sucesso", "Gravação carregada com sucesso!")

    def atualizar_lista_gravacoes(self):
        self.lista_gravacoes.delete(0, tk.END)
        for arquivo in os.listdir(self.diretorio_gravacoes):
            if arquivo.endswith('.json'):
                self.lista_gravacoes.insert(tk.END, arquivo)

    def hover_enter(self, btn):
        btn.configure(bg=self.cores['botao_hover'])

    def hover_leave(self, btn):
        if '#' in btn.cget('text'):
            btn.configure(bg=self.cores['tecla_preta'])
        else:
            btn.configure(bg=self.cores['tecla_branca'])

    def clicar_tecla(self, freq, nota):
        self.destacar_tecla(nota)
        self.tocar_nota(freq, nota)

    def soltar_tecla(self, nota):
        self.restaurar_tecla(nota)

    def tocar_musica(self, nome_musica):
        if self.tocando:
            return
            
        self.tocando = True
        self.btn_parar.configure(state='normal')
        
        def reproduzir():
            for nota, duracao in self.musicas[nome_musica]:
                if not self.tocando:
                    break
                self.destacar_tecla(nota)
                winsound.Beep(self.notas[nota], duracao)
                self.restaurar_tecla(nota)
                time.sleep(0.05)
            
            self.tocando = False
            self.btn_parar.configure(state='disabled')
            
        threading.Thread(target=reproduzir, daemon=True).start()

    def parar_musica(self):
        self.tocando = False
        self.btn_parar.configure(state='disabled')

    def resetar_destaque_teclas(self):
        for nota, btn in self.teclas_botoes.items():
            self.restaurar_tecla(nota)

    def gerar_tom(self, frequencia, duracao_ms):
        """Gera um tom senoidal com a frequência e duração especificadas"""
        num_samples = int((duracao_ms / 1000.0) * self.sample_rate)
        audio_data = []
        
        for i in range(num_samples):
            t = float(i) / self.sample_rate
            sample = self.amplitude * math.sin(2 * math.pi * frequencia * t)
            audio_data.append(sample)
            
        return audio_data

    def exportar_para_wav(self, nome_arquivo, dados_audio):
        """Exporta os dados de áudio para um arquivo WAV"""
        caminho = os.path.join(self.diretorio_exports, nome_arquivo)
        
        with wave.open(caminho, 'w') as wav_file:
            # Configurar parâmetros do arquivo WAV
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 2 bytes por amostra
            wav_file.setframerate(self.sample_rate)
            
            # Converter dados float para int16
            dados_packed = b''
            for sample in dados_audio:
                # Converter para int16 (-32768 a 32767)
                valor_int = int(sample * 32767)
                dados_packed += struct.pack('h', valor_int)
            
            wav_file.writeframes(dados_packed)
        
        messagebox.showinfo("Sucesso", f"Arquivo exportado: {nome_arquivo}")

    def exportar_gravacao(self):
        """Exporta a última gravação para WAV"""
        if not self.notas_gravadas:
            messagebox.showerror("Erro", "Nenhuma gravação disponível!")
            return

        # Gerar nome do arquivo
        nome = f"gravacao_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
        
        # Gerar dados de áudio
        audio_data = []
        tempo_total = 0
        
        for nota in self.notas_gravadas:
            # Adicionar silêncio antes da nota (timing)
            silencio_samples = int((nota['tempo'] - tempo_total) * self.sample_rate)
            audio_data.extend([0] * silencio_samples)
            
            # Adicionar a nota
            audio_data.extend(self.gerar_tom(nota['frequencia'], nota['duracao']))
            tempo_total = nota['tempo'] + (nota['duracao'] / 1000.0)

        self.exportar_para_wav(nome, audio_data)

    def escolher_melodia_export(self):
        """Abre janela para escolher qual melodia exportar"""
        escolha = tk.Toplevel(self.master)
        escolha.title("Exportar Melodia")
        escolha.geometry("300x400")
        escolha.configure(bg=self.cores['bg'])

        tk.Label(escolha,
                text="Escolha uma melodia para exportar:",
                font=('Helvetica', 12),
                bg=self.cores['bg'],
                fg=self.cores['fg']).pack(pady=10)

        for nome in self.musicas.keys():
            tk.Button(escolha,
                     text=nome,
                     command=lambda n=nome: self.exportar_melodia(n, escolha),
                     bg=self.cores['botao'],
                     fg=self.cores['fg'],
                     relief=tk.FLAT,
                     width=25).pack(pady=2)

    def exportar_melodia(self, nome_melodia, janela_escolha):
        """Exporta uma melodia predefinida para WAV"""
        nome = f"{nome_melodia}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
        
        # Gerar dados de áudio
        audio_data = []
        for nota, duracao in self.musicas[nome_melodia]:
            audio_data.extend(self.gerar_tom(self.notas[nota], duracao))
            # Pequena pausa entre as notas
            audio_data.extend([0] * int(0.1 * self.sample_rate))

        self.exportar_para_wav(nome, audio_data)
        janela_escolha.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = PianoVirtual(root)
    root.mainloop()
