# 🎹 Piano Virtual Python

Um piano virtual interativo desenvolvido em Python, com recursos avançados de aprendizado, gravação e exportação de áudio.

## 📋 Descrição

Este projeto implementa um piano virtual com interface gráfica usando Tkinter. uma experiência musical completa permitindo tocar notas, aprender melodias, gravar performances e exportar áudio.

## ✨ Funcionalidades

### 🎵 Piano
- Teclas brancas e pretas com visual 3D
- Suporte a mouse e teclado
- Feedback visual ao pressionar teclas
- Controle de duração das notas

### 🎼 Melodias Predefinidas
- Ode à Alegria
- Parabéns
- Escala Completa
- Sistema de parada/reprodução

### 🎓 Modo Aprendizado
- Tutorial passo a passo
- Sistema de pontuação
- Feedback visual em tempo real
- Dicas de teclas
- Acompanhamento de progresso

### 🎙️ Sistema de Gravação
- Gravação em tempo real
- Reprodução de gravações
- Salvamento de gravações
- Carregamento de gravações anteriores
- Lista de gravações salvas

### 💾 Exportação de Áudio
- Exportação para formato WAV
- Suporte a gravações e melodias
- Alta qualidade de áudio (44.1kHz, 16-bit)
- Timing preciso entre notas

## 🛠️ Tecnologias Utilizadas

- **Python 3.x**
- **Tkinter**: Interface gráfica
- **winsound**: Geração de sons
- **wave**: Exportação de áudio
- **threading**: Processamento assíncrono
- **JSON**: Armazenamento de gravações

## 📁 Estrutura do Projeto

### piano_virtual.py
Arquivo principal do projeto, contendo:
- Interface gráfica completa
- Sistema de notas e melodias
- Gravação e reprodução
- Exportação de áudio
- Modo aprendizado

### demo_sons.py
Arquivo de demonstração que inclui:
- Exemplos de uso do sistema de som
- Interface simplificada para testes
- Demonstração de diferentes funcionalidades
- Amostras de melodias

## 🚀 Como Executar

1. **Requisitos**:
   ```bash
   pip install tkinter
   ```

2. **Executar o Piano Virtual**:
   ```bash
   python piano_virtual.py
   ```

3. **Executar a Demo**:
   ```bash
   python demo_sons.py
   ```

## 💡 Como Usar

### Tocar Notas
- Use o mouse para clicar nas teclas
- Use o teclado (A-L para teclas brancas, W,E,T,Y,U,O,P para teclas pretas)
- Ajuste a duração das notas com o slider

### Gravar
1. Clique em "🔴 Iniciar Gravação"
2. Toque as notas desejadas
3. Clique em "⏹ Parar Gravação"
4. Use "▶️ Reproduzir Última" para ouvir

### Exportar
1. Grave uma sequência ou escolha uma melodia
2. Clique em "💾 Exportar" (gravação ou melodia)
3. O arquivo WAV será salvo na pasta `exports`

### Modo Aprendizado
1. Clique em "✏️ Iniciar Modo Aprendizado"
2. Escolha uma música
3. Siga as instruções na tela
4. Use "💡 Mostrar Dica" se precisar de ajuda

## 📂 Estrutura de Diretórios
```
.
├── piano_virtual.py    # Aplicação principal
├── demo_sons.py       # Demonstração de sons
├── gravacoes/         # Gravações salvas
├── exports/          # Arquivos WAV exportados
└── README.md         # Este arquivo
```

## 🤝 Contribuições

Contribuições são bem-vindas! Algumas ideias:
- Adicionar mais instrumentos/timbres
- Implementar suporte a MIDI
- Adicionar efeitos sonoros (reverb, eco)
- Criar mais melodias predefinidas
- Melhorar a qualidade do áudio

## 📝 Notas de Desenvolvimento

- Interface organizada em duas colunas para melhor usabilidade
- Sistema de áudio otimizado para baixa latência
- Uso de threading para evitar travamentos
- Código modular e bem documentado
- Design responsivo e intuitivo

## ⚖️ Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.
