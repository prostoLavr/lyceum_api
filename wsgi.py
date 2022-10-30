from argparse import ArgumentParser
import app
from app import wsgi_app

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('-s', '--sqlite')
    args = parser.parse_args()
    app.init(args.sqlite)
    wsgi_app.run(host="0.0.0.0", port=8080)
else:
    app.init()

