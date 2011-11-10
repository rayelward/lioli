# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.title = 'LIOLI'
response.subtitle = 'love it or leave it'

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Raymond Elward <feedback.lioli@gmail.com'
response.meta.description = 'Love it or Leave it'
response.meta.keywords = 'leave, love, entertainment, love it, leave it, love it or leave it, fun, iOS, heart, relationship, relationships'
response.meta.generator = 'Web2py Web Framework'
response.meta.copyright = 'Copyright 2012'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

response.menu = [
    (T('Recents'), False, URL('default','recents'), []),
    (T('Random'),False, URL('default','random'), []),
    (T('Search'),False, URL('default','search'), []),
    (T('Submit'),False, URL('default','submit'), []),
    (T('About'),False, URL('default','about'), [])
    ]

#########################################################################
## provide shortcuts for development. remove in production
#########################################################################
