# coding: utf8

db.define_table('lioli_main',
    Field('unique_id', 'integer', notnull=True),
    Field('body', 'text', notnull=True),
    Field('loves', 'integer', default=0, notnull=True),
    Field('leaves', 'integer', default=0, notnull=True),
    Field('age', 'integer', notnull=True),
    Field('gender', notnull=True),
    Field('accepted', 'integer', default=0, notnull=True))

def rand_unique_id():
    """
    this is needed for the buildin python random number generator
    gets a random 10 digit number for us.
    IN:n/a
    OUT:random number between 1 and 2000000000
    """
    import random
    return random.randrange(1, 2000000000, 1)

def get_new_unique_id():
    """
    checks if the randomly generated number is already in the database.
    it uses tail recursion if the random number is already in the database
    IN:n/a
    OUT:new random unique_id
    """
    ran_num = rand_unique_id()
    row = db(db.lioli_main.unique_id==ran_num).select().first()
    if row == None:
        return ran_num
    else:
        return get_new_unique_id()
        
def insert_into_my_db(body, age, gender):
    """
    gets input and puts it in the database, returning the new unique
    IN:body, age, gender of post
    OUT:unique_id for post
    """
    unique_id = get_new_unique_id() 
    db.lioli_main.insert(unique_id=unique_id, body=body, age=age, gender=gender)
    return unique_id
