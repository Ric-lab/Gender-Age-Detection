import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split

def load_data(data_dir, img_size=(128, 128)):
    """
    Loads images from the specified directory.
    Expected filename format: [age]_[gender]_[race]_[date].jpg
    Example: 25_0_0_2017010402.jpg.chip.jpg
    Gender: 0 - Male, 1 - Female
    """
    images = []
    ages = []
    genders = []
    
    files = [f for f in os.listdir(data_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    processed_count = 0
    print(f"Encontradas {len(files)} imagens em {data_dir}. Processando...")
    
    for file in files:
        # Tentar extrair idade e gênero do nome do arquivo
        try:
            parts = file.split('_')
            # O formato do UTKFace geralmente começa com idade, depois genero
            age = int(parts[0])
            gender = int(parts[1])
            
            # Carregar imagem
            path = os.path.join(data_dir, file)
            img = cv2.imread(path)
            if img is not None:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img = cv2.resize(img, img_size)
                
                images.append(img)
                ages.append(age)
                genders.append(gender)
                processed_count += 1
                
                if processed_count % 1000 == 0:
                    print(f"Carregadas {processed_count} imagens...", end='\r')
            else:
                print(f"Erro ao ler imagem: {file}")

        except Exception as e:
            # Se o nome do arquivo não estiver no formato esperado, ignorar
            # print(f"Format ignored for file: {file} - {e}")
            pass
            
    print(f"Concluído! Total: {processed_count} imagens carregadas.")
            
    if processed_count == 0:
        print("AVISO: Nenhuma imagem válida retornada. Verifique se os arquivos seguem o padrão 'idade_genero_....jpg'.")
        return None, None, None

    images = np.array(images, dtype='float32') / 255.0
    ages = np.array(ages, dtype='float32')
    genders = np.array(genders, dtype='float32')
    
    return images, ages, genders

def split_data(images, ages, genders, test_size=0.2):
    if images is None:
        return None, None, None, None, None, None
        
    X_train, X_test, y_gender_train, y_gender_test, y_age_train, y_age_test = train_test_split(
        images, genders, ages, test_size=test_size, random_state=42
    )
    
    return X_train, X_test, y_gender_train, y_gender_test, y_age_train, y_age_test
