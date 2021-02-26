from flask import render_template
from flask_app.forms import *
from flask_app import app
from flask_app.elastic import *

mongo_elastic()
# Home page
# Frontend in the file: 'flask_app/templates/index.html'
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

# Page to search for specific document based on ID or other field
# Frontend in file: 'flask_app/templates/search.html'
@app.route('/search', methods=['GET', 'POST'])
def search():
    formForID = QueryByIDForm()
    formForField = QueryByFieldForm()

    # If user is searching based on ID
    if formForID.submit1.data and formForID.validate_on_submit():    
        mydata = searchByID(formForID.id.data)
        num_docs = mydata.pop(0)

        # Return front-end template w/ fields filled out to refer to the relevant forms
        return render_template('search.html', title='Search Harvard Dataverse', formForID=formForID, formForField=formForField, docs1 = mydata, num_docs1=num_docs)
    
    # If user is searching based on field and value
    if formForField.submit2.data and formForField.validate_on_submit():    
        mydata = searchByField(formForField.field.data, formForField.val.data)
        num_docs = mydata.pop(0)

        # Return front-end template w/ fields filled out to refer to the relevant forms
        return render_template('search.html', title='Search Harvard Dataverse', formForID=formForID, formForField=formForField, docs2 = mydata, num_docs2=num_docs)
   
    # Default web page w/ empty forms
    return render_template('search.html', title='Search Harvard Dataverse', formForID=formForID, formForField=formForField)
    
# Page for debugging purposes
# Accessible if you wanted to see all documents in index 'harvard'
@app.route('/all', methods=['GET'])
def show_all():
    return find_all()

# Page to play the "Color Game" if you want to take a break from navigating the Harvard Dataverse
@app.route('/color_game', methods=['GET'])
def color_game():
    return render_template('colorGame.html', title='Color Game')

# Error handler if user navigates to a page that does not exist
@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404
