import sys
from app import create_app, create_manager

sys.path.insert(0, "/root/flask-hellogit")


app = create_app('test')
manager = create_manager(app)

if __name__ == "__main__":
    manager.run()
