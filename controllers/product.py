# -*- coding: utf-8 -*-

def show():
	# pegar produto no bando de dados
	# buscar pelo slug //qualquer campo != id
	# acessar api do twitte
	#slice //pega registro por outro campo da tabela
	db.product.tax_price = Field.Virtual(lambda row: row.product.unit_price * origins.get(row.product.origin, 1))

	try: #se for passado o id
		pid = int(request.args(0))
		product = db.product[pid]
	except Exception: # se for pegar outro campo
		try:
			pid = int(request.args(0)[:5])
			product = db.product[pid]
		except Exception:
			redirect(URL('home','index'))

	# poderia esta no db
	colors = ["amarelo","azul", "vermelho"]

	fields = [
		Field("qtd", "integer", label=T("Quantity"), requires=IS_NOT_EMPTY(error_message=T("You have to information quantity"))),
		Field("pid", default="%s"% product.id ),
		Field("colors", label=T("Colors"), requires=IS_IN_SET(colors))
	]

	form = SQLFORM.factory(*fields, 
		submit_button=T("Add to cart"),
		_method="POST" #nao vai pela url. o valor é pego pelo nome dos fields la no metodo add
		)

	if form.process().accepted:
		session.cart = session.cart or [] #se session.cart não existir ele cria ela vazia
		item = {
			"id" :  product.id,
			"qtd" :  form.vars.qtd,
			"name" :  product.name,
			"thumbnail" :  product.thumbnail,
			"price" :  product.unit_price,
			"total" :  float(form.vars.qtd) * float(product.unit_price)
		}
		session.cart.append(item)
		redirect(URL('cart','show'))

	# alterando os elementos desse form
	btn = form.elements('input[type=submit]')
	btn[0]["_class"] = "jose"

	return dict(product=product, form=form)

def list():
    # hide_fields("product",["total_price"]) #esconder campos
	# campos virtuais pra tabela
	db.product.edit = Field.Virtual(lambda row: (\
		A(SPAN(_class="glyphicon glyphicon-eye-open"), _class="btt b_view", _href=URL("dados_product", args=row.product.id)),\
		A(SPAN(_class="glyphicon glyphicon-edit"), _class="btt b_edit", _href=URL("edit", args=row.product.id)),\
		A(SPAN(_class="glyphicon glyphicon-remove"), _class="btt b_delet", _id=row.product.id, _href="#")))
	
	db.product.img = Field.Virtual(lambda row: get_miniatura_sqlformgrid_products(row))	

	# query da busca no db
	query = db.product
	
	# nome dos headers e dos campos do db referente a cada header
	headers =["f", "Cod", "Nome","Valor unit","Edit"]
	fields = ["img", "code", "name","unit_price","edit"]

	# tabela vazia 
	table = TABLE(_id="minhaTabela", _class="table hover table-striped table-bordered")

	# thead vazio sendo populado pelo for
	thead = THEAD(TR())
	for header in headers:
		thead[0].append(TD(B(header)))
	table.append(thead)
	
	# montando todos os rows da tabela product
	rows = db(query).select()

	# navegando em todos os rows e populando os tr com o retorno 
	for row in rows:
		tr = TR(_id=row['id'])
		for field in fields:
			if field == "unit_price":
				tr.append(format_price(row[field]))
			else:
				tr.append(row[field])
		table.append(tr)
	return dict(table=table)

# @auth.requires_login()
# @auth.requires_membership("admin")

@auth.requires_membership("admin")
def edit(): 
	hide_fields("product",["id","backup_price"]) #esconder campos

	# pegar produto pelo id ou slug
	# criar formulario de edicao
	# apenas para admin
	p_id = request.args(0) or redirect(URL("home","index"))
	form = SQLFORM(db.product, int(p_id))
	if form.process().accepted:
		redirect(URL('product','list'))
	elif form.errors:
		response.flash = T("Dados com erro")
	return dict(form=form)

@auth.requires_membership("admin")
def new():
	hide_fields("product",["backup_price"]) #esconder campos
	form=SQLFORM(db.product)
	if form.process().accepted:
		redirect(URL('product','list'))
	elif form.errors:
		response.flash = T("Dados com erro")
	# cod = max(db(db.product).select('code'))['code'] #maior numero da coluna 'code'
	return dict(form=form)

def dados_product():
	pid = request.args(0)
	query = db(db.product.id == int(pid))
	return dict(products=query.select())

@auth.requires_membership("admin")
def remov():
	# remover item do carrinho via ajax
	index = request.vars.transitory
	idd = index[0]
	
	response.flash = "Item excluido"
	db(db.product.id == idd).delete()

	return "$('#%s').remove();"%(idd) 

