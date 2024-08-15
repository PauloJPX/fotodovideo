import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import subprocess
import threading

def select_video():
    home_directory = os.path.expanduser("~")  # Obtém o caminho para o diretório Home
    video_path = filedialog.askopenfilename(initialdir=home_directory, title="Selecione um arquivo de vídeo", filetypes=[("Video files", "*.mp4 *.avi *.mkv")])
    if video_path:
        video_path_label.config(text=video_path)

def select_output_dir():
    home_directory = os.path.expanduser("~")
    output_dir = filedialog.askdirectory(initialdir=home_directory, title="Selecione o diretório para salvar as fotos")
    if output_dir:
        output_dir_label.config(text=output_dir)

def run_ffmpeg(video_path, interval, output_dir):
    try:
        script_path = "./capture_frames_ffmpeg.sh"
        command = f"bash {script_path} \"{video_path}\" {interval} \"{output_dir}\""
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            messagebox.showinfo("Sucesso", "Frames capturados com sucesso!")
        else:
            messagebox.showerror("Erro", f"Erro ao capturar frames: {result.stderr}")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Erro", f"Erro ao capturar frames: {e.stderr}")
    finally:
        progress_bar.stop()

def ping_contador(interval):
    if thread.is_alive():  # Verifica se a thread ainda está rodando
        global contador
        contador += 1
        contador_label.config(text=str(contador))
        root.after(int(interval * 1000), lambda: ping_contador(interval))  # Chama esta função novamente após o intervalo especificado

def generate_photos():
    global contador, thread
    video_path = video_path_label.cget("text")
    output_dir = output_dir_label.cget("text")
    interval = interval_entry.get()

    if not video_path or not output_dir or not interval:
        messagebox.showerror("Erro", "Selecione o arquivo de vídeo, o diretório de saída e o intervalo de tempo")
        return

    try:
        interval = float(interval)
        progress_bar.start()
        thread = threading.Thread(target=run_ffmpeg, args=(video_path, interval, output_dir))
        thread.start()
        ping_contador(interval)  # Começa a incrementar o contador com base no intervalo de tempo
    except ValueError:
        messagebox.showerror("Erro", "Intervalo de tempo deve ser um número.")

# Configuração da interface
contador = 0
root = tk.Tk()
root.title("Gerador de Frames de Vídeo")

tk.Label(root, text="Arquivo de Vídeo:").grid(row=0, column=0, padx=10, pady=5)
video_path_label = tk.Label(root, text="")
video_path_label.grid(row=0, column=1, padx=10, pady=5)
tk.Button(root, text="Selecionar", command=select_video).grid(row=0, column=2, padx=10, pady=5)

tk.Label(root, text="Diretório de Saída:").grid(row=1, column=0, padx=10, pady=5)
output_dir_label = tk.Label(root, text="")
output_dir_label.grid(row=1, column=1, padx=10, pady=5)
tk.Button(root, text="Selecionar", command=select_output_dir).grid(row=1, column=2, padx=10, pady=5)

tk.Label(root, text="Intervalo (segundos):").grid(row=2, column=0, padx=10, pady=5)
interval_entry = tk.Entry(root)
interval_entry.grid(row=2, column=1, padx=10, pady=5)

progress_bar = ttk.Progressbar(root, mode='indeterminate')
progress_bar.grid(row=3, column=0, columnspan=3, padx=10, pady=10)


contador_label = tk.Label(root, text=str(contador), font=("Arial", 24, "bold"))
contador_label.grid(row=3, column=2, padx=10, pady=10)



tk.Button(root, text="Gerar Frames", command=generate_photos).grid(row=4, column=0, columnspan=3, padx=10, pady=20)

root.mainloop()
