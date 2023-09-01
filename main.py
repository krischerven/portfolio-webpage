#!/usr/bin/env python3

######################################################
# main.py: A simple Flask app to host the portfolio. #
# https://git.krischerven.info/dev/portfolio-webpage #
#                                                    #
# Usage:                                             #
#   ./main.py                                        #
#   ./main.py +debug                                 #
#                                                    #
######################################################

import logging
import os
import sys

import flask

from work import server_work

app = flask.Flask(__name__, template_folder=os.getcwd(), static_folder="static")
app.config["TEMPLATES_AUTO_RELOAD"] = True

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


@app.route('/')
def landing():
    "Render landing.html"
    lev_snippet = read_file("snippets/lev.lisp")
    lev_deps_snippet = read_file("snippets/lev-dependencies.lisp")
    serve_snippet = read_file(__file__)
    landing_snippet = read_file("landing.html")
    maints_snippet = read_file(static_file("javascript/main.ts"))
    stylesheet_snippet = read_file("stylesheet.css")
    return flask.render_template("landing.html",
                                 metaprog_snippet_1=lev_snippet,
                                 metaprog_snippet_2=lev_deps_snippet,
                                 website_snippet_1=serve_snippet,
                                 website_snippet_2=landing_snippet,
                                 website_snippet_3=maints_snippet,
                                 website_snippet_4=stylesheet_snippet,
                                 metaprog_download_1=download("lev.lisp"),
                                 metaprog_download_2=download("lev-dependencies.lisp"),
                                 website_download_1=download("main.py"),
                                 website_download_2=download("landing.html"),
                                 website_download_3=download("main.ts"),
                                 website_download_4=download("stylesheet.css"))


def main():
    "Main function"
    logger.debug("Serving landing.html")
    debug_mode = len(sys.argv) > 1 and sys.argv[1] == "+debug"
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
    server_work()
    main()
