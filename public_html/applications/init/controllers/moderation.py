# coding: utf8
# try something like



##this is where we give a session varible to people that know the password,
##it allows them to access a number of other functions in the folder.

##it is strongly recommeded to add a web2py reCAPTCHA to this to prevent spamming 
#to get into the moderation side.
#this only sets up moderation for entering new entries into the database. You must
#use the admin interface if you want to remove something that was already entered into 
#system.
def index():
    pw = 'web2pyisawesome'
    #message to show for the form
    message = "Please enter the password"
    #creates the input form
    form = SQLFORM.factory(Field('password', 'password'))
    #checks if the user submitted the correct password
    if ((form.process().accepted) and (form.vars.password == pw)):
        #gives feedback that the moderator was correct
        response.flash = 'yay, accepted'
        #sets the session for the moderator
        session.approved = 'yes'
        #sends the user to check the new entries.
        redirect(URL('new_entries'))
        #else the user entered the wrong password.
    else:
        #tells the person they are wrong.
        response.flash = 'nooo!!!'
            
    return dict(message=message, form=form)
    
#TODO show new entries to be allowed in or deleted from the database.
def new_entries():
    
    if session.approved != 'yes': redirect(URL('default','index'))
    where_clause = (db.lioli_main.accepted == 0)
    fields = [db.lioli_main.unique_id, db.lioli_main.body, db.lioli_main.age, db.lioli_main.gender]
    rows = db(where_clause).select(limitby=(0, 10), orderby=db.lioli_main.id, *fields)
    
    
    return dict(rows=rows)
    
#TODO takes a specific entry asks for a confirmation to delete or accept, 
#then updates database, then redirects to new_entries.
def specific_entry():
    if session.approved != 'yes': redirect(URL('default','index'))
    u_id = request.args(0) or redirect(URL('default', 'index'))
    row = db(db.lioli_main.unique_id==u_id).select().first()
    return dict(row=row)
    
    
#this method does the actual deletion of the entry. then redirects to the new entries
def delete_entry():
    if session.approved != 'yes': redirect(URL('default','index'))
    u_id = request.args(0) or redirect(URL('default', 'index'))
    db(db.lioli_main.unique_id == u_id).delete()
    redirect(URL('new_entries'))
    return dict()
    
#this method does the actual accepting of an entry. then redirects to the new entries
def accept_entry():
    if session.approved != 'yes': redirect(URL('default','index'))
    u_id = request.args(0) or redirect(URL('default', 'index'))
    db(db.lioli_main.unique_id == u_id).update(accepted=1)
    redirect(URL('new_entries'))
    return dict()
