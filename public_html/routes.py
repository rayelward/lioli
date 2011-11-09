# -*- coding: utf-8 -*-


default_application='init'
default_controller = 'default'
default_function = 'recents'


routes_in = (
             ('/favicon.ico', '/init/static/favicon.ico'),
             ('/recents/$p', '/init/default/recents/$p'),
             ('/show/$p', '/init/default/show/$p'),
             ('/$f', '/init/default/$f'),
             ('/$c/$f', '/init/$c/$f'),
             )



routes_out = [(x, y) for (y, x) in routes_in]

