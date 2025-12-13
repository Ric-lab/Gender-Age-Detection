import os
import requests
import tarfile
import shutil

# URL direta para o UTKFace (Aligned & Cropped) - Mirror confiável
# Este arquivo tem ~100MB
DATASET_URL = "https://susanqq.github.io/UTKFace/UTKFace.tar.gz" # Link oficial as vezes é lento/quebrado. 
# Alternativa: usar um dataset do HuggingFace se este falhar, mas vamos tentar o oficial ou um mirror conhecido.
# Vou usar um link direto mais estável se possível. 
# O link oficial da SusanQQ muitas vezes redireciona para GDrive que precisa de interação.
# Vamos tentar baixar de um repositório público que hospeda o arquivo raw.

# Fallback para um mirror público no HF (muito mais rápido e direto)
DATASET_URL = "https://huggingface.co/datasets/py97/UTKFace-Cropped/resolve/main/UTKFace.tar.gz"

DEST_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
TAR_PATH = os.path.join(DEST_DIR, 'UTKFace.tar.gz')

def download_and_extract():
    if not os.path.exists(DEST_DIR):
        os.makedirs(DEST_DIR)

    # 1. Download
    print(f"Baixando dataset UTKFace (~100MB)...")
    print(f"URL: {DATASET_URL}")
    
    try:
        response = requests.get(DATASET_URL, stream=True)
        if response.status_code == 200:
            with open(TAR_PATH, 'wb') as f:
                total_length = response.headers.get('content-length')
                dl = 0
                for chunk in response.iter_content(chunk_size=4096):
                    dl += len(chunk)
                    f.write(chunk)
                    if total_length:
                        done = int(50 * dl / int(total_length))
                        # Barra de progresso visual simples
                        # print(f"\r[{'=' * done}{' ' * (50-done)}] {dl//1024} KB", end='')
            print("\nDownload concluído.")
        else:
            print(f"Falha no download. Status: {response.status_code}")
            return
    except Exception as e:
        print(f"Erro no download: {e}")
        return

    # 2. Extract
    print("Extraindo arquivos...")
    try:
        with tarfile.open(TAR_PATH, "r:gz") as tar:
            tar.extractall(path=DEST_DIR)
        print("Extração concluída!")
        
        # O tar geralmente cria uma subpasta 'UTKFace'. Vamos mover os arquivos para a raiz de 'data' se quiser, 
        # ou ajustar o loader. Vamos ajustar mover para 'data/images' para ficar limpo.
        
        extracted_folder = os.path.join(DEST_DIR, 'UTKFace')
        if os.path.exists(extracted_folder):
            print(f"Movendo arquivos de {extracted_folder} para {DEST_DIR}...")
            # Mover arquivos
            for file in os.listdir(extracted_folder):
                shutil.move(os.path.join(extracted_folder, file), DEST_DIR)
            
            # Remover pasta vazia
            os.rmdir(extracted_folder)
            
        # Limpar o tar
        os.remove(TAR_PATH)
        print("Limpeza concluída. Dataset pronto para uso.")
        
    except Exception as e:
        print(f"Erro na extração: {e}")

if __name__ == "__main__":
    download_and_extract()
