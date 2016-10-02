# -*- coding: utf-8 -*-

# @auth.requires_login()
def show():
	# exibir carrinho de compras
	# criar sessao caso nao exista
	# formulario para tipo de pagamento

	headers = ["Img","Name","Price","Qtd","Total","Remove"]
	fields = ["thumbnail", "name", "price", "qtd", "total", "remove"]

	# tabela vazia 
	table = TABLE()

	# thead vazio sendo populado pelo for
	thead = THEAD(TR())
	for header in headers:
		thead[0].append(TD(B(header)))
	table.append(thead)
	
	# navegando na session.cart 
	for item in session.cart:
		tr = TR(_id=item['id']) #para cada linha da tabela tera o id do produto
		for field in fields:
			#field = thumbnail ou botao_remove
			# field = img
			if field == "thumbnail":
				if not item['thumbnail']:
					img = IMG( _widht=32, _height=32, _src='http://placehold.it/32x32')
				else:
					img = IMG( _widht=32, _height=32 ,_src=URL('home','download', args=item['thumbnail']))
				tr.append(img)
			elif field == "remove": #field = botao_remove	
				a = A(SPAN(_class="glyphicon glyphicon-trash"),
				_class="btn btn-danger btn-xs removebutton",
				_data=item['id']) #chama a funão pra excluir o item da lista da session.cart
				tr.append(a)
			elif field in ["price","total"]:
				valor_formt = format_price(item[field])
				tr.append(valor_formt)
			else:
				tr.append(item[field])

		table.append(tr)
	
	# add class a tabela
	table["_class"] = "table table-striped table-bordered table=condensed list"
	
	# somar o preço de todos os totais de cada row
	total = sum(item['total'] for item in session.cart)
	total = format_price(total)
	return dict(table=table, total=total)

def remove():
	# remover item do carrinho via ajax
	pid = request.vars.transitory
	newcart = []
	valorDesconto = 0.0 #valor do iten a ser retirado da lista
	total = sum(item['total'] for item in session.cart) #soma do valor total antes da retirada do item
	

	for item in session.cart:
		if int(item['id']) != int(pid):
			newcart.append(item) #adiciona o item que NAO vai ser deletado da lista ao newcart monstando a nova lista sem o item que foi passado "deletado"
		else:
			valorDesconto = item['total'] #guarda o valor unit_price do item a ser deletado da lista pra ser descontado do total

	session.cart = newcart		


	subTotal = "%.2f"%((float(total) - float(valorDesconto))) #total - valorDesconto "valor guardado antes de ser deletado da lista"

	return "$('#%s').remove();$('#total h3').text('TOTAL:R$%s')"%(pid,subTotal.replace(".",",")) 


		

def clear():
	# limpar carrinho
	pass

def checkout():
	# apenas para usuario logado
	# gerar pedido
	# enviar email o cliente
	pass