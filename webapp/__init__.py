from flask import Flask

"""
Author 김윤철
Date 2020.07.20
"""

app = Flask(__name__,
            static_url_path='', 
            static_folder='static',
            template_folder='template')
from webapp import routes