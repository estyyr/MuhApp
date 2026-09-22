import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR,'muhasebe.db')}"

SECRET_KEY = "muhapp-gizli-anahtar-2026"

APP_NAME = "MuhApp"

KDV_ORANI = 20

PARA_BIRIMI = "₺"

DEBUG = True