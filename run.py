from livereload import Server

from app import app


app.debug = True
server = Server(app.wsgi_app)
server.watch('src')
server.watch('templates')
server.serve()
