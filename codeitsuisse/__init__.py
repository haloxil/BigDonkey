from flask import Flask
app = Flask(__name__)
import codeitsuisse.routes.square
import codeitsuisse.routes.ticker
import codeitsuisse.routes.crypto
import codeitsuisse.routes.magiccauldrons
import codeitsuisse.routes.calendar


