from main_folder.menuapp import *

if __name__ == "__main__":
    socket_.run(app,  allow_unsafe_werkzeug=True)
    # socket_.run(app, host='0.0.0.0', port=5000, debug=True)
