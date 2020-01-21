#!/usr/bin/env python

import os
import subprocess
import sys

from programlibrary.app import create_app

if __name__ == '__main__':
    args = sys.argv
    
    # check for required environment variables
    if "PGPASSWORD" not in os.environ:
        print("Please export PGPASSWORD=<postgres password>")
        exit()

    if len(args) < 2:
        app = create_app()
        app.run(debug=True)
    elif args[1] == "--seed":
        # reset everything
        if "USERNAME" not in os.environ:
            print("Please export USERNAME=<postgres username>")
            exit()

        uname = os.environ['USERNAME']

        nuke = subprocess.call(["psql", "-U" + uname, "-a", "-f", "nuke.sql", "-w"])
        if nuke != 0:
            print("Error reseting db")
            exit()
        repopulate = subprocess.call(["psql", "-U" + uname, "-a", "-f", "bootstrap/bootstrap.sql", "-w"])
        if repopulate != 0:
            print("Error creating and populating db")
            exit()
        app = create_app()
        # run app
        app.run(debug=True)