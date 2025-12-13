import os
import tensorflow as tf
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization
from tensorflow.keras.models import Model
import dataset_loader
import matplotlib.pyplot as plt

# Configurações com defaults, podem ser ajustadas
IMG_SIZE = (128, 128)
BATCH_SIZE = 16 # Reduzido para evitar erro de memória (OOM)
EPOCHS = 20
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models', 'gender_age_model.h5')

def build_model(input_shape):
    inputs = Input(shape=input_shape)
    
    # Camadas Convolucionais Compartilhadas (Arquitetura Original "Sua Rede")
    x = Conv2D(32, (3, 3), activation='relu')(inputs)
    x = BatchNormalization()(x)
    x = MaxPooling2D((2, 2))(x)
    
    x = Conv2D(64, (3, 3), activation='relu')(x)
    x = BatchNormalization()(x)
    x = MaxPooling2D((2, 2))(x)
    
    x = Conv2D(128, (3, 3), activation='relu')(x)
    x = BatchNormalization()(x)
    x = MaxPooling2D((2, 2))(x)
    
    x = Conv2D(256, (3, 3), activation='relu')(x)
    x = BatchNormalization()(x)
    x = MaxPooling2D((2, 2))(x)
    
    x = Flatten()(x)
    x = Dense(256, activation='relu')(x)
    x = Dropout(0.4)(x)
    
    # Ramo para Gênero (Binário: 0=Masculino, 1=Feminino)
    gender_branch = Dense(128, activation='relu')(x)
    gender_output = Dense(1, activation='sigmoid', name='gender_output')(gender_branch)
    
    # Ramo para Idade (Regressão)
    age_branch = Dense(128, activation='relu')(x)
    age_output = Dense(1, activation='relu', name='age_output')(age_branch) # ReLU pois idade >= 0
    
    model = Model(inputs=inputs, outputs=[gender_output, age_output])
    
    return model

def main():
    print("--- Iniciando Script de Treinamento (Original CNN - Otimizado) ---")
    
    # 1. Carregar Dados
    print(f"Buscando dados em: {DATA_DIR}")
    images, ages, genders = dataset_loader.load_data(DATA_DIR, IMG_SIZE)
    
    if images is None:
        print("CRÍTICO: Não foi possível carregar o dataset. O treinamento será abortado.")
        return

    print(f"Total de imagens carregadas: {len(images)}")
    
    # 2. Dividir Treino/Teste
    X_train, X_test, y_gender_train, y_gender_test, y_age_train, y_age_test = dataset_loader.split_data(images, ages, genders)
    
    # 3. Construir e Compilar Modelo
    model = build_model(IMG_SIZE + (3,))
    
    model.compile(optimizer='adam',
                  loss={'gender_output': 'binary_crossentropy', 'age_output': 'mse'},
                  loss_weights={'gender_output': 1.0, 'age_output': 0.05}, 
                  metrics={'gender_output': 'accuracy', 'age_output': 'mae'})
    
    model.summary()
    
    # 4. Treinar
    print(f"Iniciando treinamento por {EPOCHS} épocas (Batch Size: {BATCH_SIZE})...")
    
    # Adicionar Checkpoint para salvar a cada época
    checkpoint = tf.keras.callbacks.ModelCheckpoint(
        MODEL_PATH, 
        monitor='val_loss', # Salva sempre que melhorar o loss de validação
        verbose=1, 
        save_best_only=False, # Salva todo final de época para garantir (pode sobrescrever)
        mode='auto'
    )
    
    history = model.fit(X_train, 
                        {'gender_output': y_gender_train, 'age_output': y_age_train},
                        validation_data=(X_test, {'gender_output': y_gender_test, 'age_output': y_age_test}),
                        epochs=EPOCHS,
                        batch_size=BATCH_SIZE,
                        callbacks=[checkpoint])
                        
    # 5. Salvar Modelo Final
    model.save(MODEL_PATH)
    print(f"Modelo salvo em: {MODEL_PATH}")

if __name__ == "__main__":
    main()
