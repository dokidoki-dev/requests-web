from web_backend import create_app
from flask_script import Manager

app = create_app()
manger = Manager(app=app)

if __name__ == '__main__':
    manger.run()
