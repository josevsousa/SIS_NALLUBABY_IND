# -*- decoding: utf-8 -*-

# ============ LOYOUT HTML ========================
def etapa_1():
	#controla se os dois campos estão preenchidos
	if session.etapa_1:
		cliente_nome = session.etapa_1['nome_cliente']
		representante_nome = session.etapa_1['nome_representante']
	else:
		cliente_nome = ""
		representante_nome =""
	
	# formularios dos campos cliente e representante
	form_etapa1 = SQLFORM.factory(
		Field("cliente","string",default=cliente_nome ,requires=IS_IN_DB(db(db.registration.status == "Cliente"),db.registration.name)),
		Field("representante","string",default=representante_nome ,requires=IS_IN_DB(db(db.registration.status == "Representante"),db.registration.name)),
		_class="form-inlined", _id="cli_rep")
	form_etapa1.elements(_type='submit')[0].attributes["_value"] = "Proxima etapa"
	form_etapa1.elements(_type='submit')[0].attributes["_class"] = "btn btn-default btn-lg"

	if form_etapa1.process().accepted:
		# se não existir a session.etapa_1. criar com os valores passados ou alterar se existir
		session.etapa_1 = {
			"nome_cliente": form_etapa1.vars.cliente,
			"id_cliente": db(db.registration.name == form_etapa1.vars.cliente).select('id')[0]['id'],
			"nome_representante": form_etapa1.vars.representante,
			"id_representante": db(db.registration.name == form_etapa1.vars.representante).select('id')[0]['id']
		}
		redirect(URL("etapa_2"))		
	elif form_etapa1.errors:
		# se existir essa session.etapa_1 delete-a
		if session.etapa_1:
			session.__delitem__('etapa_1')
		# alerta 	
		response.flash = "Formulário incompleto"
	return dict(form_etapa1=form_etapa1)

def etapa_2():
 	# se não tinver sessao crie uma nova 
	if not session.caixa:
		session.caixa = {"sub_total":'0.0',"total":'0.0',"desconto":'0','tipo':'','por':'0','din':'0.00','parcelas':'0'}	
		
	return dict(total=format_price(session.caixa['total']),table=table_cart())

def etapa_3():

	tipo = session.caixa['tipo']

	# form_caixa
	form_caixa = SQLFORM.factory(
		Field("tipo", default=tipo, requires=IS_IN_SET(['1-Avista','2-Credito','3-Boleto','4-Cheque']),widget = SQLFORM.widgets.radio.widget),
		Field("por","integer", default=session.caixa['por']),
		Field("din","string", default=session.caixa['din']),
		Field("parcelas",requires=IS_IN_SET(['',1,2,3,4],), default=session.caixa['parcelas'])
		)
	# estilizando elementos do form_caixa
	form_caixa.elements('input[type=submit]')[0].attributes['_class'] = 'btn btn-success btn-lg'
	form_caixa.elements('input[type=submit]')[0].attributes['_id'] = 'enviar'
	form_caixa.elements('#enviar')[0].attributes['_value'] = 'FINALIZAR'

	if tipo == '':
		form_caixa.elements('#no_table_por')[0].attributes['_disabled'] = True
		form_caixa.elements('#no_table_din')[0].attributes['_disabled'] = True
		form_caixa.elements('#no_table_parcelas')[0].attributes['_disabled'] = True
		form_caixa.elements('#enviar')[0].attributes['_disabled'] = True
		pass

	if form_caixa.process():
		# valida os dados passado
		if form_caixa.accepted:
			form_caixa.elements('#enviar')[0].attributes['_value'] = 'enviando.'
		else:
			# erros
			for i in form_caixa.errors:
				if 'parcelas':
					form_caixa.elements('select')[0].attributes['_class'] = 'erro_my_form'	
				elif '':
					pass
			# limpar erros e não enviar a view	
			form_caixa.errors.clear()
			pass
	else:
		print'não foi processado'		
		pass

	btns = BUTTON('Cancelar',_type="text", _id="cancelar" ,_class="btn btn-danger btn-lg")

	if (session.caixa['parcelas'] != '0'):
		grid_parcelas = gerar_grid_parcelas()
	else:
		grid_parcelas = '--'

	return dict(buttons=btns, form=form_caixa, grid_parcelas = grid_parcelas)	

# ============ functions ==========================

# etapa_3 painel a esquerda
def etapa_3_box_1():
	# box_1
	div_row = UL(
				LI(
					form_caixa.custom.widget.tipo,
					_class="list-group-item", _id="tipo_pagamento"),
				LI(
					SPAN('Desconto',_id="label"),
					DIV(
						' % : 	',
						form_caixa.custom.widget.por,
						' R$ : ',
						form_caixa.custom.widget.din,
						_class="rp"),
					_class="list-group-item grade", _id="desconto"),
				LI(
					SPAN('Parcelas'),
					form_caixa.custom.widget.parcelas,
					_class="list-group-item grade", _id="parcelas"),
				_class="list-group")
				

	return div_row

# etapa_3 painel a direita
def etapa_3_box_2():
	ul = UL(_class="list-group")
	ul.append(LI('Total',
			SPAN(
				format_price(float(session.caixa['total'])),
				_id="total"),
			_class="list-group-item"))
	ul.append(LI('Desconto',
			SPAN(
				format_price(float(session.caixa['desconto'])),
				_id="desconto_real"),
			_class="list-group-item"))
	ul.append(LI('Sub Total',
			SPAN(
				format_price(float(session.caixa['sub_total'])),
				_id="subTotal"),
			_class="list-group-item"))
	return ul

# etapa_3 limpar registro da etapa_3
def etapa_3_clear():
	session.caixa['desconto'] = '0.00'
	session.caixa['din'] = '0.00'
	session.caixa['por'] = '0'
	session.caixa['tipo'] = ''
	session.caixa['parcelas'] = '0'
	session.caixa['sub_total'] = session.caixa['total']
	pass

def gravar_venda():
	# gravar session
	grid_parcelas_db = request.vars.transitory
	gravar_session_db(grid_parcelas_db)
	pass	

# gera a grid parcelas
def iniciar_grid_parcelas():
	n_parcelas = request.vars.transitory

	# gravar 0 em vez de ''
	if n_parcelas == '':
		session.caixa['parcelas'] = ''
		grid = ''
	else:	
		session.caixa['parcelas'] = n_parcelas
		grid = gerar_grid_parcelas()	
		pass
	return grid
def gerar_grid_parcelas():
	n_parcelas = session.caixa['parcelas']
	
	# headers table
	headers = ["N","Data parcelas","Valor parcela"]
	fields = []	

	# object table
	table = TABLE(_class="table table-hover animated fadeIn",_id="gri_parcelamento")

	# object thead
	thead = THEAD(TR())
	for header in headers:
		thead[0].append(TH(header))
		pass

	table.append(thead)	

	# object tbody
	tbody = TBODY(_id='grid_parcelas_db')
	# gera a tabela

	total = float(session.caixa['sub_total'])
	total = total/int(n_parcelas)
	for i in range(int(n_parcelas)):
		cont = i+1
		## contar a data
		meses = (cont)
		dias_por_mes = 30
		hoje = datetime.now()
		dt_parcela = hoje + timedelta(dias_por_mes*meses)		
		
		# data da parcela
		data = INPUT(_value=dt_parcela.strftime('%Y-%m-%d'),_type="date",_id="grid_data")

		# valor da parcela
		valor = INPUT(_value="%.2f"%total, _type="number",_id="grid_parcelas")

		tbody.append(TR(TD(cont),TD(data),TD("R$ ",valor),_id=cont))
		pass
	
	table.append(tbody)
	return table

# table cart
def table_cart():
	# headers table
	headers = ["Cod","Nome","Preço Un","Qtd","Total","Remove"]
	fields = ["code", "name", "price", "qtd", "total", "remove"]	

	# object table
	table = TABLE()

	# object thead
	thead = THEAD(TR())
	for header in headers:
		thead[0].append(TD(header))
		pass

	table.append(thead)	

	# navegando na session.cart 
	if session.cart:
		for item in session.cart:
			tr = TR(_id=item['id']) #para cada linha da tabela tera o id do produto
			for field in fields:
				#field = botao_remove
				if field == "remove": #field = botao_remove	
					a = A(SPAN(_class="glyphicon glyphicon-remove"),
					_class="btn btn-danger btn-xs removebutton",
					_data=item['id']) #chama a funão pra excluir o item da lista da session.cart
					tr.append(a)
				elif field in ["price","total"]:
					valor_formt = format_price(item[field])
					tr.append(valor_formt)
				else:
					tr.append(item[field])
					pass
				pass	
			table.append(tr)
			pass
		pass	


	# add class a tabela
	table["_class"] = "table table-hover table-bordered table=condensed list"

	# session.SUBTOTAL = sum(item['total'] for item in session.cart)
	# session.etapa_3 = {'desconto':0,'subTotal':subtotal,'tipo':0,'desc_din':0,'desc_por':0,'parcelas':0}
	return table

# valida code
def valida_code():
	code = request.vars.codigo
	if (code != '') & (code != '0'):
		try:
			# name = db(db.product.code == code).select('name')[0]['name']
			item = db(db.product.code == code).select('name','unit_price')
			name = "%s: %s"%(item[0]['name'],format_price(item[0]['unit_price']))
			return "$('#codigo').removeClass('codigoError').val('%s'),$('#produto').attr('disabled',false).val('%s'),$('#qtd').attr('disabled',false).focus()"%(code,name)
		except Exception:
			return "$('#codigo').addClass('codigoError').focus(),$('#qtd').val('').removeClass('codigoError').attr('disabled',true),$('#produto').val('')"
	else:
		if code == '0':
			return "$('#qtd').removeClass('codigoError'),$('#submit').attr('disabled',true),$('#codigo').removeClass('codigoError').val(''),$('#produto').attr('disabled',false).focus()"
		elif code == '':	
			return "$('#qtd').removeClass('codigoError'),$('#submit').attr('disabled',true),$('#codigo').removeClass('codigoError'),$('#qtd').val('').attr('disabled',true),$('#produto').val('').attr('disabled',false).focus()"

# lista de produtos
def listaProdutos():
	# tabela dos produtos
	products = db(db.product).select()	
	# vars enviadas via ajax
	index =	request.vars.transitory
	index = index.split(';')
	codigo = index[0]
	qtd = index[1]
	produto = index[2]

	# pegar o preco do produto na tabela product 'ja pronta acima do process().accepted'
	for product in products:
		if product.code == int(codigo):
			price = product.unit_price
			name = product.name
			pid = product.id
	pass

	# ADD ITEM A LISTA
	session.cart = session.cart or [] #se session.cart não existir ele cria ela vazia
	item = {
		"id" : pid,
		"code" : codigo,
		"name" : name,
		"price" : price,
		"qtd" : qtd,
		"total" : float(qtd) * float(price)
	}
	session.cart.insert(0, item)

	# calucar o total
	if session.cart:
		soma = sum(item['total'] for item in session.cart)
		session.caixa['sub_total'] = soma
		session.caixa['total'] = soma

	# retorno pra view
	jquary = "$('#total').text('%s');" \
			"$('#qtd,#submit').attr('disabled',true);$('#codigo').focus();" \
			"$('#load').hide();" \
			"$('#table_list').html('%s');" \
			"remove();" \
			%(format_price(float(session.caixa['sub_total'])),table_cart()) 

	etapa_3_clear() #limpar registro da etapa_3
	return jquary

# remove item
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
			valorDesconto = item['total'] #guarda o valor price do item a ser deletado da lista pra ser descontado do total

	session.cart = newcart		

	subTotal = "%.2f"%((float(total) - float(valorDesconto))) #total - valorDesconto "valor guardado antes de ser deletado da lista"
	session.caixa['total'] = subTotal
	etapa_3_clear() #limpar registro da etapa_3
	return "$('#%s').remove();$('#total').text('%s')"%(pid,format_price(subTotal))

# grava o tipo na session
def gravar_tipo():
	session.caixa['tipo'] = request.vars.transitory
	pass

# grava os descontos na session
def calc_subtotal():
	index = (request.vars.transitory).split(';')
	por = (index[0] if index[0] != '' else '0')
	din = (index[1] if index[1] != '' else '0.00')
	total = session.caixa['total']
	
	# calcular o desconto
	desconto = (float(din)+((float(total)*int(por))/100))
	subtotal =  (float(total) - desconto)	
	 
	# gravar na session	
	session.caixa['por'] = por
	session.caixa['din'] = din
	session.caixa['desconto'] = desconto
	session.caixa['sub_total'] = subtotal

	return etapa_3_box_2()

# valida qtd
def valida_qtd():
	qtd = request.vars.qtd
	if (qtd != '') & (qtd != '0'):
		return "$('#qtd').removeClass('codigoError'),$('#submit').attr('disabled',false).focus()"
	else:
		return "$('#qtd').addClass('codigoError').val('').focus(),$('#submit').attr('disabled',true)"

# cancelar venda
def cancelar_venda():
	session.__delitem__('cart')
	session.__delitem__('caixa')
	session.__delitem__('etapa_1')
	pass
