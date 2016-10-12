# -*- coding: utf-8 -*-

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Hello World")
    return dict(message=T('Welcome to web2py!'))

def produtos():
    query = db.product
    rows = db(query).select()
    return dict(rows = rows)

def produto_destaque():
    produto = db(db.product.id == request.args(0)).select()[0]
    return dict(produto=produto)

def login():
    return dict(msg="jose")

def dialogo():
    return dict(msg="teste")
