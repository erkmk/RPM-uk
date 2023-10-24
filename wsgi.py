from serverNew import app
from app import create_app, init_app

application = create_app()
init_app(application)

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=5002, debug=True)
