#!/usr/bin/env python3

# ################################################### #
# main.py: A simple Flask app to host this portfolio. #
# ################################################### #

import logging
import os
import sys

import flask

app = flask.Flask(__name__, template_folder=os.getcwd(), static_folder="static")
app.config["TEMPLATES_AUTO_RELOAD"] = True

logging.basicConfig()
logger = logging.getLogger("resume-webpage")
logger.setLevel(logging.DEBUG)


@app.route('/')
def landing():
    "Render landing.html"
    lev_snippet = open("snippets/lev.lisp", "r", encoding="UTF-8").read()
    lev_deps_snippet = open("snippets/lev-dependencies.lisp", "r", encoding="UTF-8").read()
    serve_snippet = open(__file__, "r", encoding="UTF-8").read()
    landing_snippet = open("landing.html", "r", encoding="UTF-8").read()
    mainjs_snippet = open("static/javascript/main.js", "r", encoding="UTF-8").read()
    stylesheet_snippet = open("stylesheet.css", "r", encoding="UTF-8").read()
    return flask.render_template("landing.html",
                                 metaprog_snippet_1=lev_snippet,
                                 metaprog_snippet_2=lev_deps_snippet,
                                 website_snippet_1=serve_snippet,
                                 website_snippet_2=landing_snippet,
                                 website_snippet_3=mainjs_snippet,
                                 website_snippet_4=stylesheet_snippet)


def main():
    "Main function"
    logger.debug("Running git pull...")
    os.system("git pull")
    logger.debug("Serving landing.html")
    app.run("0.0.0.0")
    logger.debug("Program exited (0)")


if __name__ == "__main__":
    main()
