import os

class Config:

    SQLALCHEMY_DATABASE_URI = 'sqlite:///tasks.db' 
    SQLALCHEMY_TRACK_MODIFICATIONS = False