import streamlit as st
import tensorflow as tf
import cv2
import numpy as np
from PIL import Image
import os

# Configurações
IMG_SIZE = (128, 128)
MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models', 'gender_age_model_v3.h5')

@st.cache_resource
def load_model():
    if not os.path.exists(MODEL_PATH):
        return None
    model = tf.keras.models.load_model(MODEL_PATH, compile=False)
    return model

def process_image(image_file):
    # Converter PIL Image para Numpy Array
    img_array = np.array(image_file.convert('RGB'))
    # Redimensionar para o tamanho esperado pelo modelo
    img_resized = cv2.resize(img_array, IMG_SIZE)
    # Normalizar (0-1)
    img_normalized = img_resized.astype('float32') / 255.0
    # Expandir dimensões para batch (1, 128, 128, 3)
    img_batch = np.expand_dims(img_normalized, axis=0)
    return img_array, img_batch

def main():
    st.set_page_config(page_title="Detector de Gênero e Idade", page_icon="👤")
    
    st.title("👤 Detector de Gênero e Idade (IA)")
    st.write("Faça upload de uma foto para detectar o gênero e se a pessoa é maior de idade (>18).")

    model = load_model()

    if model is None:
        st.error(f"Modelo não encontrado em `{MODEL_PATH}`.")
        st.info("Por favor, execute o script de treinamento `src/train.py` primeiro para gerar o arquivo `.h5`. É necessário ter imagens na pasta `data`.")
        return

    uploaded_file = st.file_uploader("Escolha uma imagem...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file)
            original_img, processed_img = process_image(image)
            
            st.image(original_img, caption='Imagem Carregada', use_container_width=True)
            
            if st.button('Analisar'):
                with st.spinner('Analisando...'):
                    # Predição
                    predictions = model.predict(processed_img)
                    gender_pred = predictions[0][0][0] # Saída 0 é Gênero
                    age_pred = predictions[1][0][0]    # Saída 1 é Idade
                    
                    # Interpretação
                    # 0 = Masculino, 1 = Feminino (Assumindo label encoding do UTKFace usual: 0=Male, 1=Female)
                    # O modelo retorna probabilidade de ser 1 (Female)
                    # 0 = Masculino, 1 = Feminino
                    gender_label = "Feminino" if gender_pred > 0.5 else "Masculino"
                    confidence = gender_pred if gender_pred > 0.5 else 1 - gender_pred
                    
                    is_adult = "Sim (> 18)" if age_pred >= 18 else "Não (< 18)"
                    
                    st.success("Análise Concluída!")
                    
                    width_pct = int(confidence * 100)
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric("Gênero Predito", gender_label, f"{confidence*100:.1f}% confiança")
                        st.caption(f"Raw Output: {gender_pred:.4f} (0=M, 1=F)")
                    
                    with col2:
                        st.metric("Idade Estimada", f"{int(age_pred)} anos")
                    
                    st.info(f"Maior de 18 anos? **{is_adult}**")

        except Exception as e:
            st.error(f"Erro ao processar a imagem: {e}")

if __name__ == "__main__":
    main()
