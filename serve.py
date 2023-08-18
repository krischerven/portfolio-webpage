#!/usr/bin/env python3

# ############################################## #
# Source code for the server rendering this page #
# ############################################## #

import logging
import os

import flask
import waitress

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
    return flask.render_template("landing.html",
                                 lisp_metaprog_snippet_1=lev_snippet,
                                 lisp_metaprog_snippet_2=lev_deps_snippet,
                                 serve_snippet=serve_snippet)


def main():
    "Main function"
    logger.debug("Serving landing.html")
    waitress.serve(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
