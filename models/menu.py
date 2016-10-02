# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# ----------------------------------------------------------------------------------------------------------------------
# Customize your APP title, subtitle and menus here
# ----------------------------------------------------------------------------------------------------------------------

# nome da barra de ferramenta
# se tiver cadastrado na table empresa mostra o nome na barra

nome_empresa = file_settings[0]
response.logo = A(SPAN(nome_empresa), XML('&trade;&nbsp;'),
                  _class="navbar-brand", _href="http://www.web2py.com/",
                  _id="web2py-logo")
response.title = request.application.replace('_', ' ').title()
response.subtitle = ''

# ----------------------------------------------------------------------------------------------------------------------
# read more at http://dev.w3.org/html5/markup/meta.name.html
# ----------------------------------------------------------------------------------------------------------------------
response.meta.author = myconf.get('app.author')
response.meta.description = myconf.get('app.description')
response.meta.keywords = myconf.get('app.keywords')
response.meta.generator = myconf.get('app.generator')

# ----------------------------------------------------------------------------------------------------------------------
# your http://google.com/analytics id
# ----------------------------------------------------------------------------------------------------------------------
response.google_analytics_id = None

# ----------------------------------------------------------------------------------------------------------------------
# this is the main application menu add/remove items as required
# ----------------------------------------------------------------------------------------------------------------------

response.menu = [
    (T('Home'), False, URL('home', 'index'), [])
]

DEVELOPMENT_MENU = True


# ----------------------------------------------------------------------------------------------------------------------
# provide shortcuts for development. remove in production
# ----------------------------------------------------------------------------------------------------------------------

def _():
    # ------------------------------------------------------------------------------------------------------------------
    # shortcuts
    # ------------------------------------------------------------------------------------------------------------------
    app = request.application
    ctr = request.controller
    # ------------------------------------------------------------------------------------------------------------------
    # useful links to internal and external resources
    # ------------------------------------------------------------------------------------------------------------------
    response.menu += [
        (T('Caixa'), False, URL('caixa', 'etapa_1')),
        (T('historico'), True, None, [
            (T('vendas finalizadas'), False, URL('historico', 'vendas')),
            # (T('vendas abertas'), False, URL('historico', 'vendas_abertas'))
        ]),
        (T('cadastros'), True, None, [
            (T('Tela de cadastro'), False, URL('registration','tela_registration')),
            (T('produtos'), False, URL('product','list')),
            (T('clientes'), False, URL('registration', 'list?status=Cliente')),
            (T('representantes'), False, URL('registration', 'list?status=Representante')),
            (T('funcionários'), False, URL('registration', 'list?status=Funcionario'))
        ])
    ]


if DEVELOPMENT_MENU:
    _()

if "auth" in locals():
    auth.wikimenu()
