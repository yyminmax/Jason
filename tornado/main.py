#!/usr/bin/env python
# -*- coding; utf-8 -*-

import tornado.ioloop
import tornado.httpserver
import tornado.options
import tornado.web
import os.path

from tornado.options import define, options

define("port", default=8000, help="run the given port", type=int)

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("userpid")

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")
    def post(self):
        self.render("index.html")

class SigninHandler(BaseHandler):
    def get(self):
        print self.application.settings["template_path"]
        self.render("signin.html")
    def post(self):
        if self.get_argument("username") == "yyminmax" and self.get_argument("password") == "password":
            self.set_secure_cookie("userpid", "yyminmax")
            self.redirect("/user")

class UserHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("user.html", user=self.current_user)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', IndexHandler),
            (r'/signin', SigninHandler),
            (r'/user', UserHandler),
        ]
        settings = dict(
            template_path = os.path.join(os.path.dirname(__file__), "template"),
            static_path = os.path.join(os.path.dirname(__file__), "static"),
            debug = True,
            cookie_secret = "7840GFhHSZC6xUl66a5EV3J4XNrdckv0ginaF5XY1jE=",
            login_url = "/",
        )
        tornado.web.Application.__init__(self, handlers, **settings)

def make_app():
    app = tornado.web.Application(
        handlers=[
            (r'/', IndexHandler),
            (r'/signin', SigninHandler),
            (r'/user', UserHandler),
        ],
        settings=dict(
            template_path = os.path.join(os.path.dirname(__file__), "template"),
            static_path = os.path.join(os.path.dirname(__file__), "static"),
            debug = True,
            cookie_secret = "7840GFhHSZC6xUl66a5EV3J4XNrdckv0ginaF5XY1jE=",
            login_url = "/",
        )
    )
    return app;

if __name__ == "__main__":
    tornado.options.parse_command_line()
    httpserver = tornado.httpserver.HTTPServer(Application())
    print options.port
    httpserver.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
