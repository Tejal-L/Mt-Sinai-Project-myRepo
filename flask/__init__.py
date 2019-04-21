import logging
from flask import Flask

# app = Flask(__name__)

from . import receive
from . import nlu

	
# if __name__ == '__main__':
#     app.run(debug=True,host='0.0.0.0')