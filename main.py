#!/usr/bin/env python3

######################################################
# main.py: A simple Flask app to host the portfolio. #
# https://git.krischerven.info/dev/portfolio-webpage #
#                                                    #
# Usage (brackets represent optional arguments):     #
#   ./main.py                                        #
#   ./main.py [+debug] [+skip-npm]                   #
#                                                    #
######################################################

import logging
import os
import sqlite3
import sys
from hashlib import md5
from threading import Lock, Thread

import flask
from flask import request

from work import server_work

app = flask.Flask(__name__, template_folder=os.getcwd(), static_folder="static")
app.config["TEMPLATES_AUTO_RELOAD"] = True

database = sqlite3.connect("./portfolio-webpage.db", check_same_thread=False)
database.execute("""
    create table if not exists hashed_ips (id integer primary key, timestamp datetime
                                           default current_timestamp not null,
                                           checksum text not null,
                                           page text not null)
    """)

mutex = Lock()

logging.basicConfig()
logger = logging.getLogger("portfolio-webpage")
logger.setLevel(logging.DEBUG)


def static_file(dir):
    "Return [static]/[dir], where [static] is Flask's static folder."
    return app.static_folder.split("/")[-1] + "/" + dir


def download(dir):
    "Return [static]/downloads/[dir], where [static] is Flask's static folder."
    return app.static_folder.split("/")[-1] + "/downloads/" + dir


def read_file(file):
    "Shorthand for open([file], 'r').read()"
    return open(file).read()


def get_client_address():
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        return request.environ['REMOTE_ADDR']
    # if behind a proxy
    else:
        return request.environ['HTTP_X_FORWARDED_FOR']


def store_hashed_address(raw_address, page):
    with mutex:
        database.execute("insert into hashed_ips (checksum, page) values(?, ?)",
                         (md5(raw_address.encode()).hexdigest(), page))
        database.commit()


@app.route('/')
def landing():
    "Render landing.html"
    Thread(target=store_hashed_address, args=(get_client_address(), "landing")).start()
    search_for_users_snippet = read_file("snippets/search-for-users.kt")
    lev_snippet = read_file("snippets/lev.lisp")
    lev_deps_snippet = read_file("snippets/lev-dependencies.lisp")
    serve_snippet = read_file(__file__)
    maints_snippet = read_file(static_file("javascript/main.ts"))
    landing_snippet = read_file("landing.html")
    stylesheet_snippet = read_file("stylesheet.css")
    chatbot_snippet = read_file("portfolio-chatbot/main.go")
    return flask.render_template("landing.html",
                                 search_for_users_snippet_1=search_for_users_snippet,
                                 metaprog_snippet_1=lev_snippet,
                                 metaprog_snippet_2=lev_deps_snippet,
                                 website_snippet_1=serve_snippet,
                                 website_snippet_2=maints_snippet,
                                 website_snippet_3=landing_snippet,
                                 website_snippet_4=stylesheet_snippet,
                                 chatbot_snippet_1=chatbot_snippet,
                                 search_for_users_download_1=download(
                                     "search-for-users.kt"),
                                 metaprog_download_1=download("lev.lisp"),
                                 metaprog_download_2=download("lev-dependencies.lisp"),
                                 website_download_1=download("main.py"),
                                 website_download_2=download("main.ts"),
                                 website_download_3=download("landing.html"),
                                 website_download_4=download("stylesheet.css"),
                                 chatbot_download_1=download("main.go"))


@app.route('/contact')
def contact():
    "Render contact.html"
    Thread(target=store_hashed_address, args=(get_client_address(), "contact")).start()
    return flask.render_template("contact.html")


@app.route("/question/<uuid>/<question>")
def question(uuid, question):
    "Answer a question by invoking portfolio-chatbot --uuid $uuid --question $question"
    hashed_address = md5(get_client_address().encode()).hexdigest()
    cmd = f"cd portfolio-chatbot && ./portfolio-chatbot \"{uuid}\" \"{hashed_address}\" \"{question}\""
    return {"response": os.popen(cmd).read()}


def main():
    "Main function"
    logger.debug("Serving landing.html")
    debug_mode = "+debug" in sys.argv
    app.run("0.0.0.0", debug=debug_mode)
    logger.debug("Program exited (0)")


if __name__ == "__main__":
    # server_work() should only run be run here for local testing (ie ./main.py), because
    # some of the processes in server_work() require sudo. There is no guarantee that
    # NOPASSWD will be set for all of these, which can cause server_work() to hang if it
    # is run in the background via gunicorn. gunicorn also has a tendency to execute this
    # file three times (<2023-08-30 Wed> - test via print outside this scope), which is
    # problematic if we run server_work() here.
    #
    # For gunicorn, server_work() runs as part of the update-webpage bash script.
    server_work(tscompile_npm_work=("+skip-npm" not in sys.argv))
    main()
