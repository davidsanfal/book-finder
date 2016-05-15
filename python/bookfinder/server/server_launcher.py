from bookfinder.errors import EnvironmentException


def server_launcher(debug=False, host='127.0.0.1', port=5000):
    '''Function to config and launch the app'''
    try:
        from bookfinder.server.app.finder_app import app
        from bookfinder.server.controllers import error_controller
        from bookfinder.server.controllers import finder_controller
        from bookfinder.server.controllers import book_controller
        app.run(debug=debug, host=host, port=port)
    except EnvironmentException as e:
        print e.message

if __name__ == '__main__':
    server_launcher(True)
