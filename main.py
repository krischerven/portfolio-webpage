#!/usr/bin/env python3

# ################################################## #
# main.py: A simple Flask app to host the portfolio. #
#                                                    #
# Usage:                                             #
#   ./main.py                                        #
#   ./main.py +debug                                 #
#                                                    #
# ################################################## #

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
    maints_snippet = open("static/javascript/main.ts", "r", encoding="UTF-8").read()
    stylesheet_snippet = open("stylesheet.css", "r", encoding="UTF-8").read()
    return flask.render_template("landing.html",
                                 metaprog_snippet_1=lev_snippet,
                                 metaprog_snippet_2=lev_deps_snippet,
                                 website_snippet_1=serve_snippet,
                                 website_snippet_2=landing_snippet,
                                 website_snippet_3=maints_snippet,
                                 website_snippet_4=stylesheet_snippet,
                                 metaprog_download_1="static/downloads/lev.lisp",
                                 metaprog_download_2="static/downloads/lev-dependencies.lisp",
                                 website_download_1="static/downloads/main.py",
                                 website_download_2="static/downloads/landing.html",
                                 website_download_3="static/downloads/main.ts",
                                 website_download_4="static/downloads/stylesheet.css")


def server_work():
    "Run important server work before anything goes live"
    if os.path.exists(".server-work.lock"):
        logger.debug(".server-work.lock exists; skipping running server_work()")
        return
    # NOTE: 0644 is default
    open(".server-work.lock", "w")
    logger.debug("Running git pull...")
    os.system("git pull")
    if os.system("which npx > /dev/null 2>&1") == 256:
        logger.debug("npx (npm) does not exist in the system path, so ./tscompile is "
                     "unrunnable. Aborting. Please install npm or make npx available "
                     "in the system path.")
        os.remove(".server-work.lock")
        exit(1)
    if os.system("which tsc > /dev/null 2>&1") == 256:
        logger.debug("tsc does not exist in the system path; installing it globally...")
        os.system("sudo npm install -g typescript")
    logger.debug("Running ./tscompile...")
    if os.system("./tscompile") == 256:
        logger.debug("./tscompile failed to run, aborting.")
        os.remove(".server-work.lock")
        exit(1)
    logger.debug("All done.")
    if os.path.exists(".server-work.lock"):
        os.remove(".server-work.lock")


def main():
    "Main function"
    logger.debug("Serving landing.html")
    debug_mode = len(sys.argv) > 1 and sys.argv[1] == "+debug"
    app.run("0.0.0.0", debug=debug_mode)
    logger.debug("Program exited (0)")


# server_work() must run when app is imported by another program
server_work()
if __name__ == "__main__":
    main()
