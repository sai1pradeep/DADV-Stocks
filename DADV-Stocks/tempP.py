
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import json
import os.path
from tornado.options import define, options
import os

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("top10gainers.html")
    
    
    
class SparkHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("Rprjct.html")

settings = dict(
                template_path=os.path.join(os.path.dirname(__file__),"templates"),
                static_path = os.path.join(os.path.dirname(__file__), "static"),
                debug=True)
application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/spark", SparkHandler),    
],**settings)

if __name__ == '__main__':
    application.listen(8080)
    tornado.autoreload.start()
    tornado.ioloop.IOLoop.instance().start()
    tornado.autoreload.wait()