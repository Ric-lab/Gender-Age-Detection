# 👤 Gender & Age Detection with Deep Learning

Este projeto é uma aplicação de **Visão Computacional** capaz de estimar o Gênero e a Idade de uma pessoa a partir de uma foto.
Utiliza **TensorFlow/Keras** para o modelo de Deep Learning e **Streamlit** para a interface web.

## 🚀 Funcionalidades

- **Detecção de Gênero**: Classificação Binária (Masculino / Feminino).
- **Estimativa de Idade**: Regressão numérica (Anos).
- **Interface Gráfica**: Upload de imagem simples e rápido via navegador.

## 🛠️ Tecnologias

- Python 3.10+
- TensorFlow 2.x (CNN Customizada)
- Streamlit (Web UI)
- OpenCV (Processamento de Imagem)

## 📦 Instalação

1. Clone este repositório:
```bash
git clone https://github.com/SEU_USUARIO/Gender-Age-Detection.git
cd Gender-Age-Detection
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## ▶️ Como Rodar

Basta executar o comando abaixo na raiz do projeto:

```bash
streamlit run src/app.py
```

O navegador abrirá automaticamente em `http://localhost:8501`.

## 🧠 Treinamento do Modelo

O modelo foi treinado utilizando o dataset **UTKFace** (~23.000 imagens).
Devido a limitações de hardware local, o treinamento foi otimizado para rodar no **Google Colab (GPU Free)**.

- **Arquivo de Treino**: `colab_training.ipynb`
- **Arquitetura**: Custom CNN com Multi-Output (Duas ramificações: Gênero e Idade).
- **Estratégia**: Early Stopping com Restore Best Weights e Learning Rate Scheduling.

Para treinar novamente:
1. Abra o arquivo `colab_training.ipynb` no Google Colab.
2. Selecione o Runtime **T4 GPU**.
3. Execute todas as células.
4. Baixe o arquivo `.h5` gerado e coloque na pasta `models/`.

## 📂 Estrutura do Projeto

```
/
├── data/               # Dataset (ignorado pelo git)
├── models/             # Pesos do modelo treinado (.h5)
├── src/
│   ├── app.py          # Aplicação Streamlit
│   ├── dataset.py      # Carregamento de dados
│   └── train.py        # Script de definição do modelo
├── colab_training.ipynb # Notebook para treino na nuvem
├── requirements.txt    # Dependências
└── README.md           # Este arquivo
```

---
Desenvolvido como projeto de portfólio em Machine Learning.
