import os
import re
import time
import shutil
import datetime
from zipfile import ZipFile
import py7zr
import rarfile
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from plyer import notification

# Caminhos
MONITOR_FOLDER = "C:/TESTES"
LOG_FILE = os.path.join(MONITOR_FOLDER, "LOGS_TESTES.txt")
ERROR_FILE = os.path.join(MONITOR_FOLDER, "LOGS_ERRO.txt")
DEST_A = "C:/MULT/DYGNUS"
DEST_B = "C:/MULT/DYGNUS/SETUP"
DEST_C = "C:/MULT/DYGNUS/SETUP/APP"
DEST_PDV = "C:/MULT/PDV"
DEST_NFE = "C:/MULT/NFE"
SEM_NUMERO = ["DYGNUS.7z", "DYGNUS_ETIQUETAS.7z", "DYGNUS_WAVES_ECOMMERCE_ONE.7z", "DYGNUS_WOO.7z", "DYGNUS-WAVE.7z", "NFE.7z", "PDVLINE.7z"]

# Garante que os diretórios de destino existem
for path in [DEST_A, DEST_B, DEST_C, DEST_PDV, DEST_NFE]:
    os.makedirs(path, exist_ok=True)

# REGEX para pegar o número da demanda no nome do arquivo
def extrair_numero(nome_arquivo):
    match = re.match(r"(\d+)\s", nome_arquivo)
    return match.group(1) if match else "??????"

def registrar_log(nome_arquivo):
    hora = datetime.datetime.now().strftime("%H:%M")
    if nome_arquivo in SEM_NUMERO:
        link = f"{nome_arquivo} - {hora}\n\n"
    else:
        numero = extrair_numero(nome_arquivo)
        link = f"[{numero}: \"(nome da demanda)\"](https://mantis.multilogica.com.br/view.php?id={numero}) {hora}\n\n"
        
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(link)

def registrar_log_erro(nome_arquivo, erro):
    hora = datetime.datetime.now().strftime("%H:%M")
    text = f"{hora} - {nome_arquivo} - Erro {erro}\n"
    with open(ERROR_FILE, "a", encoding="utf-8") as f:
        f.write(text)

def mover_arquivo(origem, destinos):
    for destino in destinos:
        shutil.copy2(origem, destino)

def processar_arquivos_extraidos(temp_dir):
    for nome in os.listdir(temp_dir):
        caminho = os.path.join(temp_dir, nome)
        nome_upper = nome.upper()
        if nome_upper == "DYGNUS.EXE":
            mover_arquivo(caminho, [DEST_A, DEST_C])
        elif nome_upper == "DYGNUS_START.EXE":
            mover_arquivo(caminho, [DEST_A, DEST_B])
        elif nome_upper == "DYGNUS_UPDATE.EXE":
            mover_arquivo(caminho, [DEST_A, DEST_C])
        elif nome_upper == "PDVLINE.EXE":
            mover_arquivo(caminho, [DEST_PDV, DEST_C])
        elif nome_upper == "NFE.EXE":
            mover_arquivo(caminho, [DEST_NFE])
        elif nome_upper == "DYGNUS_ETIQUETAS.EXE":
            mover_arquivo(caminho, [DEST_A, DEST_C])
        elif nome_upper == "DYGNUS_WAVES_ECOMMERCE_ONE.EXE":
            mover_arquivo(caminho, [DEST_A, DEST_C])
        elif nome_upper == "DYGNUS_WOO.EXE":
            mover_arquivo(caminho, [DEST_A, DEST_C])
        elif nome_upper == "PDV_NFCE_SAT.EXE":
            mover_arquivo(caminho, [DEST_PDV])

def aguardar_estabilidade(caminho, tentativas=10, intervalo=1):
    tamanho_anterior = -1
    iguais = 0
    for _ in range(tentativas * 2):
        if not os.path.exists(caminho):
            time.sleep(intervalo)
            continue
        tamanho_atual = os.path.getsize(caminho)
        if tamanho_atual == tamanho_anterior:
            iguais += 1
            if iguais >= tentativas:
                return True
        else:
            iguais = 0
            tamanho_anterior = tamanho_atual
        time.sleep(intervalo)
    return False

class Handler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return

        caminho = event.src_path
        nome_arquivo = os.path.basename(caminho)

        extensao = os.path.splitext(nome_arquivo)[1].lower()
        if extensao not in [".zip", ".rar", ".7z"]:
            return

        if not aguardar_estabilidade(caminho):
            notification.notify(
                title="Atenção!", 
                message=f"x Arquivo {nome_arquivo} não estabilizou. Ignorando.", 
                timeout=5)
            
            return

        notification.notify(
            title=f"{nome_arquivo}",
            message=f"Processando o arquivo {nome_arquivo}...",
            timeout=3
        )

        temp_dir = os.path.join(MONITOR_FOLDER, "TEMP")

        # Limpa diretório temporário se existir
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.makedirs(temp_dir, exist_ok=True)

        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir, exist_ok=True)
    
        try:
            if extensao == ".zip":
                with ZipFile(caminho, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
            elif extensao == ".7z":
                with py7zr.SevenZipFile(caminho, mode='r') as z:
                    z.extractall(path=temp_dir)
            elif extensao == ".rar":
                with rarfile.RarFile(caminho) as rar:
                    rar.extractall(path=temp_dir)

            processar_arquivos_extraidos(temp_dir)
            registrar_log(nome_arquivo)
            os.remove(caminho)
            shutil.rmtree(temp_dir)

            notification.notify(
                title=f"{nome_arquivo}",
                message=f"Arquivo {nome_arquivo} processado com sucesso.",
                timeout=3
            )

        except Exception as e:
            notification.notify(
                title=f"Falha durante processamento do arquivo {nome_arquivo}", 
                message=f"{str(e)}", 
                timeout=5
            )

            # Registra log do erro
            registrar_log_erro(nome_arquivo, e)


def main():
    notification.notify(
        title="Atenção!",
        message=f"Iniciando monitoramento da pasta: `{MONITOR_FOLDER}`",
        timeout=3
    )

    os.makedirs(MONITOR_FOLDER, exist_ok=True)
    observer = Observer()
    observer.schedule(Handler(), MONITOR_FOLDER, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()