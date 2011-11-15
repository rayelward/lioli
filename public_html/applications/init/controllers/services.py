# coding: utf8

from gluon.tools import Service
service = Service()

def call():
    """
    ./services/call/json/add_leaves/[unique_id]
    ./services/call/json/add_loves/[unique_id]
    ./services/call/json/get_entry/[unique_id]
    ./services/call/json/recents/[page] (page is optional)
    ./services/call/json/random_ten/
    ./services/call/json/submit/ ... send a post or get request, recieve the ID to let the user know.
    """
    session.forget()
    return service()

@service.json
def recents(page=0):
    """
    function to return recent objects from the database
    IN:page or nothing=first page
    OUT:10 database objects
    """
    page_min = int(page) * 10
    page_max = page_min + 10
    where_clause = (db.lioli_main.accepted == 1)
    fields = [db.lioli_main.unique_id, db.lioli_main.body, db.lioli_main.loves, db.lioli_main.leaves, db.lioli_main.age, db.lioli_main.gender]
    rows = db(where_clause).select(limitby=(page_min, page_max), orderby=~db.lioli_main.id, *fields).as_list()
    return rows
    
@service.json
def random_ten():
    """
    function to return 1 random object
    IN:n/a
    OUT:10 database objects
    """
    where_clause = (db.lioli_main.accepted == 1)
    fields = [db.lioli_main.unique_id, db.lioli_main.body, db.lioli_main.loves, db.lioli_main.leaves, db.lioli_main.age, db.lioli_main.gender]
    rows = db(where_clause).select(limitby=(0, 10), orderby='<random>', *fields).as_list()
    return rows

@service.json
def submit(body, age, gender):
    """
    function that recieves a POST or GET request with an object to add to the database
    IN:a body, age and gender for submission.
    OUT:the new unique_id
    """
    unique_id = insert_into_my_db(body, age, gender)
    return dict(unique_id=unique_id)

@service.json
def add_loves(u_id):
    """
    function that add 1 to loves for an entry
    IN:unique_id
    OUT: new love count.
    """
    where_clause = (db.lioli_main.unique_id == u_id)
    row = db(where_clause).select().first()
    if row == None:
        return dict(wrongid='wrongid')
    row.update_record(loves=(row.loves+1))
    return dict(newloves=row.loves)
    
@service.json
def add_leaves(u_id):
    """
    function that adds 1 to leaves for an entry
    IN:unique_id
    OUT: new leave count
    """
    where_clause = (db.lioli_main.unique_id == u_id)
    row = db(where_clause).select().first()
    if row == None:
        return dict(wrongid='wrongid')
    row.update_record(leaves=(row.leaves+1))
    return dict(newleaves=row.leaves)
    
@service.json
def get_entry(u_id):
    """
    shows all the information for an entry
    IN:unique_id
    OUT:the DB object
    """
    where_clause = (db.lioli_main.unique_id == u_id) &(db.lioli_main.accepted==1)
    fields = [db.lioli_main.unique_id, db.lioli_main.body, db.lioli_main.loves, db.lioli_main.leaves, db.lioli_main.age, db.lioli_main.gender]
    row = db(where_clause).select(*fields).first()
    if row == None:
        return dict(wrongid='wrongid')
    return row
