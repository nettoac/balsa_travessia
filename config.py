import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///balsa.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'root')

# Verifique se a chave secreta está sendo carregada corretamente
print("SECRET_KEY:", Config.SECRET_KEY)