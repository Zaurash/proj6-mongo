"""
Flask web app connects to Mongo database.
Keep a simple list of dated memoranda.

Representation conventions for dates: 
   - We use Arrow objects when we want to manipulate dates, but for all
     storage in database, in session or g objects, or anything else that
     needs a text representation, we use ISO date strings.  These sort in the
     order as arrow date objects, and they are easy to convert to and from
     arrow date objects.  (For display on screen, we use the 'humanize' filter
     below.) A time zone offset will 
   - User input/output is in local (to the server) time.  
"""

import flask
from flask import render_template
from flask import request
from flask import url_for

import json
import logging

# Date handling 
import datetime

# Mongo database
from pymongo import MongoClient
from bson.objectid import ObjectId


###
# Globals
###
import CONFIG

app = flask.Flask(__name__)

try: 
    dbclient = MongoClient(CONFIG.MONGO_URL)
    db = dbclient.memos
    collection = db.dated

except:
    print("Failure opening database.  Is Mongo running? Correct password?")
    sys.exit(1)

import uuid
app.secret_key = str(uuid.uuid4())

###
# Pages
###

@app.route("/")
@app.route("/index")
def index():
  app.logger.debug("Main page entry")
  flask.session['memos'] = get_memos()
  for memo in flask.session['memos']:
      app.logger.debug("Memo: " + str(memo))
  return flask.render_template('index.html')


@app.route("/create")
def create():
    app.logger.debug("Create")
    return flask.render_template('create.html')
    
@app.route("/_save", methods = ["POST"])
def save():
    record = { "type": "memos",
           "date": request.form["memoDate"],
           "text": request.form["memoBox"]
          }
    collection.insert(record)
    app.logger.debug("Saved Memo")
    return flask.redirect(url_for("index"))
    
    
@app.route("/_update", methods = ["POST"])
def update():
    memoId = request.form["ObjectID"]
    collection.remove({"_id": ObjectId(memoId)})
    record = { "type": "memos",
           "date":  request.form["memoDate"],
           "text": request.form["memoBox"]
          }
    collection.insert(record)
    app.logger.debug("Updated Memo")
    return flask.redirect(url_for("index"))
    

@app.route("/_delete", methods = ["POST"])
def delete():
    memoId = request.form["ObjectID"]
    collection.remove({"_id": ObjectId(memoId)})
    app.logger.debug("Deleted Memo")
    return flask.redirect(url_for("index"))
    
    
@app.route("/_clear", methods = ["POST"])
def clear():
    collection.drop()
    app.logger.debug("Cleared Memos")
    return flask.redirect(url_for("index"))


@app.route("/_edit", methods = ["POST"])
def edit():
    date = datetime.datetime.strptime(request.form["date"], "%Y-%m-%d %H:%M:%S").date()
    flask.session["memo"] = {"_id": request.form["ObjectID"], "text":  request.form["text"], "date":date.strftime("%m-%d-%Y")}
    app.logger.debug("Edit")
    return flask.render_template('edit.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    return flask.render_template('page_not_found.html',
                                 badurl=request.base_url,
                                 linkback=url_for("index")), 404

#################
#
# Functions used within the templates
#
#################

# NOT TESTED with this application; may need revision 
#@app.template_filter( 'fmtdate' )
# def format_arrow_date( date ):
#     try: 
#         normal = arrow.get( date )
#         return normal.to('local').format("ddd MM/DD/YYYY")
#     except:
#         return "(bad date)"

@app.template_filter( 'humanize' )
def humanize( date ):
    """
    Date is internal UTC ISO format string.
    Output should be "today", "yesterday", "in 5 days", etc.
    Arrow will try to humanize down to the minute, so we
    need to catch 'today' as a special case. 
    """
    try:
        today = datetime.date.today()
        date = date.date()
        dateDif = date - today

        if date == today:
            human = "Today"
        elif date == datetime.date.today() + datetime.timedelta(days=1):
            human = "Tomorrow"
        elif date == datetime.date.today() - datetime.timedelta(days=1):
            human = "Yesterday"
        else:
            # if in the future
            if dateDif.days > 0:
                if dateDif.days <= 30:
                    human = "in " + str(dateDif.days) + " days"
                elif 30 < dateDif.days < 365:
                    human = "in " + str(dateDif.days//30) + " months"
                elif dateDif.days >= 365:
                    human = "in " + str(dateDif.days//365) + " years"

            else:
                # if in the past
                if dateDif.days <= 30:
                    human = str(abs(dateDif.days)) + " days ago"
                elif 30 < dateDif.days < 365:
                    human = str(abs(dateDif.days)//30) + " months ago"
                elif dateDif.days >= 365:
                    human = str(abs(dateDif.days)//365) + " years ago"

    except: 
        human = date
    return human


#############
#
# Functions available to the page code above
#
##############
def get_memos():
    """
    Returns all memos in the database, in a form that
    can be inserted directly in the 'session' object.
    """
    records = [ ]
    for record in collection.find( { "type": "memos" } ):
        record['date'] = datetime.datetime.strptime(record['date'], "%m-%d-%Y")
        record['_id'] = str(record['_id'])
        records.append(record)
    records = sorted(records, key=lambda k: k['date'])
    return records


if __name__ == "__main__":
    # App is created above so that it will
    # exist whether this is 'main' or not
    # (e.g., if we are running in a CGI script)
    app.debug=CONFIG.DEBUG
    app.logger.setLevel(logging.DEBUG)
    # We run on localhost only if debugging,
    # otherwise accessible to world
    if CONFIG.DEBUG:
        # Reachable only from the same computer
        app.run(port=CONFIG.PORT)
    else:
        # Reachable from anywhere 
        app.run(port=CONFIG.PORT,host="0.0.0.0")

    
