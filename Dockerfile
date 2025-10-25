# Utiliser l’image officielle Python
FROM python:3.9

# Créer le dossier de travail
WORKDIR /app

# Copier tous les fichiers du projet
COPY . .

# Installer les dépendances nécessaires
RUN pip install streamlit pymongo pillow

# Exposer le port Streamlit
EXPOSE 8501

# Lancer ton application
CMD ["streamlit", "run", "stream.py", "--server.port=8501", "--server.address=0.0.0.0"]
