# -*- coding: utf-8 -*-

def contact():
    form = FORM(
        INPUT(_type="text", _class="form-control", requires=IS_NOT_EMPTY(), _name="name", _placeholder="You name"),
        BR(),
        INPUT(_type="email", _class="form-control", requires=IS_EMAIL(), _name="email", _placeholder="You email"),
        BR(),
        BUTTON("Enviar")
        )
    form.process()
    return dict(form=form)


def index():
    query = db.registration
    cliente = db(query.status == 'Cliente').count()
    return dict(cliente=cliente)

def user(): 
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    if request.args(0) == 'not_authorized':
        redirect(URL('home','nao_autorizado'))
        pass
    if request.args(0) == 'login':
        redirect(URL('home','conta', vars=request.vars))
        pass
    if request.args(0) == 'register':
        redirect(URL('home','cadastro', vars=request.vars))
        pass
    if request.args(0) == 'request_reset_password':
        redirect(URL('home','reset_passwold', vars=request.vars))
        pass
    return dict(form=auth())

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

def conta():
    # logo da table empresa. 
    logo = IMG(_src=URL('static','images/logo/logo_m.png'),_width='150px')
    # registro.elements('input')[1].attributes['_class'] = "form-control" 
    return dict(login=auth.login(),logo=logo)

def cadastro():
    logo = IMG(_src=URL('static','images/logo/logo_m.png'),_width='150px')
    return dict(cadastro=auth.register(),logo=logo,login=auth.login())

def reset_passwold():
    logo = IMG(_src=URL('static','images/logo/logo_m.png'),_width='150px')
    reset = auth.request_reset_password()  
    return dict(reset=reset,logo=logo)

def nao_autorizado():
    logo ='ok'
    return dict(logo=logo)    