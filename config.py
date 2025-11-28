import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:pastel@localhost/mc_sonae'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'pastel'