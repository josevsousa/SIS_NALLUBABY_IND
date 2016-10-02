# -*- coding: utf-8 -*-
import json

#funcao pra criar o json da tabela
def productjson():
	nome = request.vars.nome #?nome= 
	if nome:
		query = db.product.name.like("%%%s%%"%name)
		print 'ok'
	else:
		query = db.product.select('name')
		print "nao"
	# as_list para retornar json
	products = db(query).select()
	print products
	pass	
	# return json.dumps(products)
