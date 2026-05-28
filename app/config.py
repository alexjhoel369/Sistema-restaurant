import os

class Config:
    SECRET_KEY = 'super_secret_key'

    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:admin@localhost:5432/restaurante'

    SQLALCHEMY_TRACK_MODIFICATIONS = False