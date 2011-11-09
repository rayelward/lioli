# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################



def index():
    redirect(URL('recents'))
    return dict()
    
fields = [db.lioli_main.id, db.lioli_main.unique_id, db.lioli_main.body, db.lioli_main.loves, db.lioli_main.leaves, db.lioli_main.age, db.lioli_main.gender]
#Shows 10 submissions for a user to vote on.
def recents():
    page = request.args(0) or 0
    items_per_page = 5
    page_min = int(page) * items_per_page
    page_max = page_min + items_per_page
    where_clause = (db.lioli_main.accepted == 1)
    rows = db(where_clause).select(limitby=(page_min, page_max), orderby=~db.lioli_main.id, *fields)
    return dict(rows=rows, page=int(page), items_per_page=items_per_page)
    
#Shows a random set of 10 submissions for a user to vote on.
def random():
    where_clause = (db.lioli_main.accepted == 1)
    rows = db(where_clause).select(limitby=(0, 10), orderby='<random>', *fields)
    return dict(rows=rows)

##uses ajax to bring up a search via keywords for people.
def search():
    return dict(form=FORM(INPUT(_id='keyword', _name='keyword',
        _onkeyup="ajax('bg_find', ['keyword'], 'target');")),
        target_div=DIV(_id='target'))
        
##shows the searched for data in more detail
def show():
    u_id = request.args(0) or redirect(URL('search'))
    row = db((db.lioli_main.accepted==1) & (db.lioli_main.unique_id==u_id)).select().first()
    return dict(row=row)

##gets user submissions and enters them into the database.
def submit():
    message = 'Please input a submission'
    form = SQLFORM.factory(
        Field('body', 'text', requires=IS_NOT_EMPTY()),
        Field('age', requires= IS_IN_SET((range(12, 125))), widget = SQLFORM.widgets.options.widget),
        Field('gender', requires = IS_IN_SET((('F', 'M'))), widget = SQLFORM.widgets.radio.widget))
    if form.process().accepted:
        unique_id = insert_into_my_db(form.vars.body, form.vars.age, form.vars.gender)
        message = "Thank you for your submission.  Please refer to %s in the future to see how people have voted on it" % (unique_id)
        response.flash = 'accepted'
    return dict(form=form, message=message)
    
##leads to default/about.html which gives a description of the application:
def about():
    return dict()
    
##function called by ajax to display search results
def bg_find():
    pattern = '%' + request.vars.keyword.lower() + '%'
    where_clause = ((db.lioli_main.body.lower().like(pattern)) |(db.lioli_main.unique_id.like(pattern))) & (db.lioli_main.accepted==1)
    pages = db(where_clause).select(orderby=('<random>'), limitby=(0,10))
    items = [DIV(A(row.unique_id, _href=URL('show', args=row.unique_id)), P(row.body, _class="search_preview")) for row in pages]
    return UL(*items).xml()





##functions for voting::

##called by AJAX used for voting up by one 
def add_loves():
    row = db(db.lioli_main.id == request.vars.id).select().first()
    new_loves = row.loves + 1
    row.update_record(loves=new_loves)
    return str(new_loves)
    
##called by AJAX used for voting up by one
def add_leaves():
    row = db.lioli_main[request.vars.id]
    new_leaves = row.leaves + 1
    row.update_record(leaves=new_leaves)
    return str(new_leaves)





def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())
