from flask import Flask
app = Flask(__name__)
import codeitsuisse.routes.square
import codeitsuisse.routes.ticker
import codeitsuisse.routes.crypto
import codeitsuisse.routes.magiccauldrons
import codeitsuisse.routes.revesle
import codeitsuisse.routes.calendar
import codeitsuisse.routes.Quordle
import codeitsuisse.routes.rubiks
import codeitsuisse.routes.dnscache
import codeitsuisse.routes.swissstig
