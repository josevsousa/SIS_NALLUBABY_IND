# -*- coding: utf-8 -*-
from smarthumb import SMARTHUMB

# new code registration
def new_code_registration():
	cod = str(uuid1()).split('-')[0]		
	return cod


# product table //tabela de produtos
db.product.name.requires=IS_NOT_EMPTY(error_message='nome obrigatório')
db.product.unit_price.requires=IS_NOT_EMPTY(error_message='valor obrigatório')
db.product.sexo.requires = IS_IN_SET(sexo)
db.product.sexo.widget = SQLFORM.widgets.radio.widget
db.product.thumbnail.compute = lambda row: SMARTHUMB(row.picture, (200, 200))

# empresa
db.empresa.thumbnail.compute = lambda row: SMARTHUMB(row.picture, (200,200))


# registration table //tabela de cadastro 
# db.registration.code.compute = lambda row: new_code_registration()
# db.registration.code.requires = CODE()
db.registration.thumbnail.compute = lambda row: SMARTHUMB(row.picture, (200, 200))
db.registration.name.requires = IS_NOT_EMPTY(error_message='nome obrigatório')
db.registration.tipo.requires = IS_IN_SET(tipo)
db.registration.status.requires = IS_IN_SET(status)
db.registration.sexo.requires = IS_IN_SET(sexo_regist)
db.registration.email.requires = IS_EMAIL()
db.registration.uf.requires = IS_IN_SET(UF_NOME, error_message="UF invalido") 
# db.registration.uf.requires = IS_IN_SET(uf)


# # se não tiver cadastrado nenhuma empresa cadastre a Story
# if db(db.empresa.id>0).count() == 0:
#      db(db.empresa.insert(name='Story'))

##########################################################################################



# chamada comum
def get_miniatura(row):
     if row.thumbnail: #se usar virtual field tem que ser "row.product.thumbnail"
          return IMG( _src=URL('home', 'download', args=[row.thumbnail]))
     else:
          return IMG(_width=50, _heigth=50,_src=URL('static','images/mini.png'))

# chamada de uma virtual field products
def get_miniatura_sqlformgrid_products(row):
     if row.product.thumbnail: #se usar virtual field tem que ser "row.product.thumbnail"
          return IMG(_width=50, _heigth=50, _src=URL('home', 'download', args=[row.product.thumbnail]))
     else:
          return IMG(_width=50, _heigth=50,_src=URL('static','images/mini.png'))

# chamada de uma virtual field registration
def get_miniatura_sqlformgrid_registration(row):
     if row.registration.thumbnail: #se usar virtual field tem que ser "row.registration.thumbnail"
          return IMG(_width=50, _heigth=50, _src=URL('home', 'download', args=[row.registration.thumbnail]))
     else:
          return IMG(_width=50, _heigth=50,_src=URL('static','images/mini.png'))



# 