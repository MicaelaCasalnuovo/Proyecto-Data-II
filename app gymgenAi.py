import streamlit as st
import random

try:
    import google.generativeai as genai
    GOOGLE_API_KEY = st.secrets["API_KEY"]
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-2.0-flash')
except ImportError as e:
    st.error(f"Error importing google.generativeai: {e}. Please make sure it's installed in your requirements.txt file.")
    st.stop()
except KeyError:
    st.error("API_KEY not found in Streamlit secrets. Please set it in Streamlit Cloud or in your local .streamlit/secrets.toml file.")
    st.stop()
except Exception as e:
    st.error(f"Error configuring google.generativeai: {e}")
    st.stop()

exercise_variations = {
    "chest": ["Press de banca", "Press de banca inclinado", "Press de banca declinado", "Aperturas con mancuernas"],
    "back": ["Dominadas", "Remo con barra", "Remo con mancuernas", "Jalones al pecho"],
    "legs": ["Sentadillas", "Peso muerto", "Zancadas", "Prensa de piernas"],
    "shoulders": ["Press militar", "Elevaciones laterales", "Elevaciones frontales", "Remo al mentón"],
    "arms": ["Curl de bíceps", "Curl de martillo", "Press francés", "Fondos en paralelas"],
    "cardio": ["Correr", "Nadar", "Ciclismo", "Saltar la cuerda"]
}

def generate_workout_routine(edad, peso, altura, objetivo, dias_entrenamiento):
    """Generates a workout routine using Google GenAI."""
    try:
        # Select exercise variations
        chest_exercises = random.sample(exercise_variations["chest"], 2)
        back_exercises = random.sample(exercise_variations["back"], 2)
        leg_exercises = random.sample(exercise_variations["legs"], 2)
        shoulder_exercises = random.sample(exercise_variations["shoulders"], 2)
        arm_exercises = random.sample(exercise_variations["arms"], 2)
        cardio_exercises = random.sample(exercise_variations["cardio"], 2)

        prompt = f"Genera una rutina de ejercicios detallada para una persona de {edad} años, que pesa {peso} kg, mide {altura} cm, y cuyo objetivo es {objetivo}. La rutina debe ser concisa, fácil de entender y no exceder las 300 palabras. Al inicio de la rutina, incluye recomendaciones generales sobre calentamiento, enfriamiento, nutrición e hidratación. Luego, la rutina debe durar {dias_entrenamiento} días, y cada día debe enfocarse en diferentes grupos musculares. Incluye ejercicios cardiovasculares y de fuerza. Especifica el número de repeticiones, series y el peso a usar para cada ejercicio.  Para el pecho, elige entre: {', '.join(chest_exercises)}. Para la espalda, elige entre: {', '.join(back_exercises)}. Para las piernas, elige entre: {', '.join(leg_exercises)}. Para los hombros, elige entre: {', '.join(shoulder_exercises)}. Para los brazos, elige entre: {', '.join(arm_exercises)}. Para cardio, elige entre: {', '.join(cardio_exercises)}. La rutina debe indicar los dias de descanso."
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error al generar la rutina: {e}"

st.title(f"💪 Generador de Rutina de Ejercicios 🏋️‍♀️")
st.markdown("✨ Una aplicación para crear tus propias rutinas de ejercicios 🚀")

# User input fields
edad = st.number_input("Edad:", min_value=10, max_value=100, value=25)
peso = st.number_input("Peso (kg):", min_value=30, max_value=200, value=70)
altura = st.number_input("Altura (cm):", min_value=100, max_value=250, value=170)
objetivo = st.text_input("Objetivo:", value="perder peso")
dias_entrenamiento = st.number_input("Días de entrenamiento por semana:", min_value=1, max_value=7, value=3)

with st.sidebar:
    st.subheader("Acerca de nosotros 👨‍💻")
    st.write("Somos un equipo de desarrolladores apasionados por la actividad y la tecnología. Nuestro objetivo es ayudarte a alcanzar tus metas de acondicionamiento físico a través de rutinas de ejercicios personalizadas.")

    st.subheader("Cómo usar la app 💡")
    st.write("Simplemente ingresa tu edad, peso, altura, objetivo y días de entrenamiento, y la aplicación generará una rutina de ejercicios personalizada para ti.")

    st.subheader("Información de contacto 📧")
    st.write("Si tienes alguna pregunta o comentario, no dudes en contactarnos en gymgenai@gmail.com")

# Generate routine button
if st.button("Generar Rutina"):
    with st.spinner("Generando rutina..."):
        rutina = generate_workout_routine(edad, peso, altura, objetivo, dias_entrenamiento)
        st.subheader("Rutina de Ejercicios:")
        st.write(rutina)
