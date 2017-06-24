from flask import Flask

pt = Flask(__name__)

@pt.route('/')
def home():
    return 'hello world'

if __name__ == '__main__':
    pt.run()
