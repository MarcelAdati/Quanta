import streamlit as st
import pickle



def load_model():
    model = pickle.load(open(r'trained_model.sav', 'rb'))
    return model

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

    model = load_model()

    if st.button("Classificar"):
        features = [[pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, diabetes_pedigree, age]]
        
        prediction = model.predict(features)

        if prediction[0] == 1:
            st.error("**Resultado: Portador de diabetes**")
        else:
            st.success("**Resultado: Não portador de diabetes**")

if __name__ == '__main__':
    main()
