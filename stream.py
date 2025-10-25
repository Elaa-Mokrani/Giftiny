import streamlit as st
from PIL import Image
from recommender import recommend
import pymongo
# Charger l'image localement
logo = Image.open("Giftiny.png")

# Centrer l'image et réduire les marges
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image(logo, width=320)
# Réduire les marges globales
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 0px;
        padding-bottom: 0rem !important;
    }
    h3 {
        margin-top: -90px !important;  /* réduit l’espace au-dessus du titre */
        font-size: 25px !important;    /* diminue la taille du titre */
        text-align: center;            /* centre le texte */
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown("### Please enter your details to get personalized gift suggestions ")


# --- User Inputs ---
age = st.number_input("Age", min_value=5, max_value=100, step=1)
gender = st.selectbox("Gender", ["Female", "Male", "Other"])
interests = st.multiselect(
    "Interests",
    ["Technology", "Fashion", "Sports", "Books", "Music", "Art", "Travel", "Cooking"]
)
favorite_color = st.color_picker("Favorite Color")

# --- Submit Button ---
if st.button("Submit"):
    user_data = {
        "age": age,
        "gender": gender,
        "interests": interests,
        "favorite_color": favorite_color
    }

    # Obtenir recommandations
    results = recommend(user_data, top_n=5)

    if results:
        st.subheader("🎁 Recommended Gifts")
        for r in results:
            st.markdown(f"**{r['name']}** — score: {r['score']}")
    else:
        st.warning("No recommendations found.")
