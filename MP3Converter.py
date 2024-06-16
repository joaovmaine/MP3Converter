from tkinter import *
from tkinter import ttk, filedialog
from pytube import YouTube
from pydub import AudioSegment
from pydub.utils import which
import os

# especificar o caminho completo para ffmpeg e ffprobe
AudioSegment.converter = which("ffmpeg")
AudioSegment.ffprobe = which("ffprobe")


def download_audio():
    url = url_entry.get()
    if url == placeholder_text:
        status_label.config(text="Por favor, insira uma URL válida.", foreground="#F44336")  # cor vermelha
        return

    try:
        # verifica se a URL é válida
        yt = YouTube(url)

        # obtendo as streams de áudio
        audio_streams = yt.streams.filter(only_audio=True)
        if not audio_streams:
            status_label.config(text="Nenhum áudio encontrado para este vídeo.", foreground="#F44336")
            return

        # selecionando a melhor stream de áudio disponível (maior taxa de bits)
        audio_stream = audio_streams.order_by('abr').desc().first()

        # abrir a caixa de diálogo para selecionar o diretório de destino
        destination_folder = filedialog.askdirectory()
        if not destination_folder:
            status_label.config(text="Download cancelado pelo usuário.", foreground="#F44336")
            return

        # download do áudio (em formato WEBM)
        download_path = audio_stream.download(output_path=destination_folder)

        # caminho do arquivo convertido
        base, ext = os.path.splitext(download_path)
        mp3_path = base + '.mp3'

        # converter para MP3 usando pydub
        audio = AudioSegment.from_file(download_path)
        audio.export(mp3_path, format='mp3')

        # remover o arquivo WebM original
        os.remove(download_path)

        status_label.config(text="Download e conversão para MP3 concluídos com sucesso!",
                            foreground="#4CAF50")  # cor verde
        save_path_label.config(text=f"Salvo em: {mp3_path}",
                                    foreground="#8A2BE2")  # cor roxa

    except Exception as e:
        status_label.config(text="Ocorreu um erro durante o download ou conversão do áudio.",
                            foreground="#F44336")  # cor vermelha


def on_entry_click(event):
    """remove o placeholder do campo de entrada quando o usuário clica no campo"""
    if url_entry.get() == placeholder_text:
        url_entry.delete(0, "end")  # limpa o conteúdo do campo de entrada
        url_entry.config(foreground="black")


def on_focusout(event):
    """adiciona o placeholder se o campo de entrada estiver vazio quando o usuário sair do campo"""
    if url_entry.get() == "":
        url_entry.insert(0, placeholder_text)
        url_entry.config(foreground="grey")


# tkinter
janela = Tk()
janela.title("MP3Converter")
janela.geometry("500x200")

# estilo
cor_fundo = "#FFDEF9"  # background rosa claro
janela.configure(bg=cor_fundo)
style = ttk.Style(janela)
style.theme_use('clam')  # usando o tema clam para permitir a alteração de cores

# configurando estilos
cor_roxa_botao = "#8A2BE2"  # cor roxa
style.configure('TButton', background=cor_roxa_botao, foreground='white', font=('Arial', 10), padding=5)
style.map('TButton', background=[('active', '#5E2E7A')])  # mudança de cor ao clicar
style.configure('TLabel', background=cor_fundo, foreground='#34495E', font=('Arial', 12))

# placeholder
placeholder_text = "Digite ou cole o link aqui:"

# layout
texto_orientacao = ttk.Label(janela, text="Baixe e converta vídeos do YouTube em formato MP3", style='TLabel')
texto_orientacao.grid(column=0, row=0, pady=(20, 5), padx=10)

url_entry = ttk.Entry(janela, width=78, foreground="grey")
url_entry.grid(column=0, row=1, padx=10)
url_entry.insert(0, placeholder_text)
url_entry.bind('<FocusIn>', on_entry_click)
url_entry.bind('<FocusOut>', on_focusout)

# criação do botão de download
botao = ttk.Button(janela, text="Download", command=download_audio, style='TButton')
botao.grid(column=0, row=2, pady=(10, 5), padx=10)

# labels de status
status_label = ttk.Label(janela, text="", font=('Arial', 10, 'italic'), background=cor_fundo)
status_label.grid(column=0, row=3, pady=(5, 5), padx=10)

save_path_label = ttk.Label(janela, text="", font=('Arial', 9), background=cor_fundo)
save_path_label.grid(column=0, row=4, pady=(0, 10), padx=10)

janela.mainloop()
