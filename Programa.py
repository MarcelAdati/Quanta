import streamlit as st
import pickle
import requests
import base64


REPO_OWNER = "MarcelAdati"
REPO_NAME = "Quanta"
MODEL_PATH = "trained_model.sav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" 
GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]


url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{MODEL_PATH}"


headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}


def carregar_modelo_do_github():
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        file_content = response.json().get('content')
        if file_content:

            decoded_content = base64.b64decode(file_content)
            
            model = pickle.loads(decoded_content)
            st.success("Modelo carregado com sucesso!")
            return model
        else:
            st.error("O conteúdo do arquivo está vazio.")
    elif response.status_code == 404:
        st.error("Arquivo não encontrado no GitHub.")
    else:
        st.error(f"Erro ao baixar o arquivo do GitHub: {response.status_code}")

    return None


def main():
    st.title("Classificador de Diabetes")
    st.write("Preencha as informações abaixo para verificar a probabilidade de diabetes.")

    pregnancies = st.number_input("Número de vezes grávida", min_value=0, format="%d")
    glucose = st.number_input("Concentração de glicose", min_value=0.0)
    blood_pressure = st.number_input("Pressão sanguínea", min_value=0.0)
    skin_thickness = st.number_input("Espessura da pele", min_value=0.0)
    insulin = st.number_input("Insulina", min_value=0.0)
    bmi = st.number_input("IMC", min_value=0.0)
    diabetes_pedigree = st.number_input("Função de pedigree de diabetes", min_value=0.0)
    age = st.number_input("Idade", min_value=0, format="%d")

    model = carregar_modelo_do_github()


    if model and st.button("Classificar"):

        features = [[pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, diabetes_pedigree, age]]
        
        prediction = model.predict(features)

        if prediction[0] == 1:
            st.error("**Resultado: Portador de diabetes**")
        else:
            st.success("**Resultado: Não portador de diabetes**")

if __name__ == "__main__":
    main()
