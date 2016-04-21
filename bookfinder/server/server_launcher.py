from bookfinder.errors import EnvironmentException


def server_launcher(debug=False):
    try:
        from bookfinder.server.app.finder_app import app
        from bookfinder.server.controllers import finder_controller
        from bookfinder.server.controllers import book_controller
        app.run(debug=True)
    except EnvironmentException as e:
        print e.message

if __name__ == '__main__':
    server_launcher(True)
