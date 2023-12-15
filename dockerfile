# Utilisez une image de base Python
FROM python:3.10

# Copiez le fichier requirements.txt dans le conteneur
COPY requirements.txt /app/requirements.txt

# Définissez le répertoire de travail dans le conteneur
WORKDIR /app

# Installez les dépendances à l'aide de pip
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copiez le reste de l'application dans le conteneur
COPY . /app

# Commande par défaut pour exécuter votre application
CMD ["python", "__main__.py", "run_api"]