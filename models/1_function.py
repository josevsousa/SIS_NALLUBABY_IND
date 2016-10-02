# -*- coding: utf-8 -*-
		
#esconde campos da tabela passada por parametro
def hide_fields(tablename, fields):
	for field in fields:
		db[tablename][field].writable = \
			db[tablename][field].readable = False

#trata o id passado por parametro add zero a esquerda
def slugfy(product):
	template = "%(id_formatado)s-%(name)s"
	id_formatado = str(product.id).zfill(5)
	return template % dict(id_formatado=id_formatado, name=product.name)

# formato de moeda
def format_price(value):
	valor = "R$ %.2f"% float(value)
	return valor.replace('.',',')

# new code product
def new_code_product():
	n = 0
	for item in db(db.product).select():
		nn = item.code
		if int(n) < int(nn):
			n = nn
			pass
		pass		
	return str(n+1)

def uf_full(est):
	for i in UF:
		newUf = i['sigla']
		if newUf == est:
			return i['nome']
			pass #for	
		pass #if	
	pass #def

class UF_FULL(object):
	def __init__(self, estado):
		self.estado = estado

	def uf_nome(self):
		for i in UF:
			newUf = i['sigla']
			if newUf == self.estado:
				return i['nome']
				break
