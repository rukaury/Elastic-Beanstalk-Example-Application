from data_explorer import create_app
import os

application = app = create_app()

print(os.environ['DB_HOST'])
if __name__ == '__main__':
    app.run()
