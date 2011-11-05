# coding: utf8
# try something like



##this is where we give a session varible to people that know the password,
##it allows them to access a number of other functions in the folder.

##it is strongly recommeded to add a web2py reCAPTCHA to this to prevent spamming 
#to get into the moderation side.
#this only sets up moderation for entering new entries into the database. You must
#use the admin interface if you want to remove something that was already entered into 
#system.
@auth.requires_membership(role='moderation')
def index():
    redirect(URL('moderation','new_entries'))
    return dict()
    
#TODO show new entries to be allowed in or deleted from the database.
@auth.requires_membership(role='moderation')
def new_entries():
    
    where_clause = (db.lioli_main.accepted == 0)
    fields = [db.lioli_main.unique_id, db.lioli_main.body, db.lioli_main.age, db.lioli_main.gender]
    rows = db(where_clause).select(limitby=(0, 10), orderby=db.lioli_main.id, *fields)
   
    row_count = db(where_clause).count()
    return dict(rows=rows, row_count=row_count)
    
#TODO takes a specific entry asks for a confirmation to delete or accept, 
#then updates database, then redirects to new_entries.
@auth.requires_membership(role='moderation')
def specific_entry():
    u_id = request.args(0) or redirect(URL('moderation', 'new_entries'))
    row = db(db.lioli_main.unique_id==u_id).select().first()
    return dict(row=row)
    
    
#this method does the actual deletion of the entry. then redirects to the new entries
@auth.requires_membership(role='moderation')
def delete_entry():
    u_id = request.args(0) or redirect(URL('moderation', 'new_entries'))
    db(db.lioli_main.unique_id == u_id).delete()
    redirect(URL('new_entries'))
    return dict()
    
#this method does the actual accepting of an entry. then redirects to the new entries
@auth.requires_membership(role='moderation')
def accept_entry():
    u_id = request.args(0) or redirect(URL('moderation', 'new_entries'))
    db(db.lioli_main.unique_id == u_id).update(accepted=1)
    redirect(URL('new_entries'))
    return dict()
    
    
    
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
