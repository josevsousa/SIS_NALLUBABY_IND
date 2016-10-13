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
    # logo da table empresa.
    logo = IMG(_src=URL('static','images/logo/logo_m.png'), _class="home_img_logo" ,_width='150px')
    # registro.elements('input')[1].attributes['_class'] = "form-control"
    return dict(login=auth.login(),logo=logo)

def dialogo():
    return dict(msg="teste")
