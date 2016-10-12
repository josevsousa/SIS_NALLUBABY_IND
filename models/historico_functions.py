# -*-coding: utf-8 -*-

# grafico
def grafico_receita():
	ano_atual = datetime.now().strftime("%Y")
	# lista com o total de cada mes
	total_meses = []
	# busca o ano atual com cada um dos meses do ano
	for i in range(1,13): # busca de 1 a 12
		n = str(i).zfill(2) # arredonda de 1 a 9 para 01,02,03... etc
		seach = ('%s-%s'%(ano_atual,n)) # monta o ano e o mes tipo 2001-05
		seach += '%' # adciona o operador % para o like do db tipo 2001-05%
		# varre a tabela historico venda e soma todas as colunas valor_subtotal
		total_mes = sum(n['valor_subtotal'] for n in db(db.historico_venda.date_create.like(seach)).select('valor_subtotal'))
		total_meses.append(total_mes) # adiciona o resultado de cada soma a  array total_meses
	
	return total_meses	

# historico
def GRID_HISTORICO(cod):
	# montar objeto historico
	historico = db(db.historico_venda.id == cod).select()[0] # criando objeto historico

	# grid_representante
	grid_representante = TABLE(
						TBODY(
							TR(
								TH("código",_class="tit_1"),
								TD(historico['codigo_venda']),
								TH("representante",_class="tit_1"),
								TD(historico['nome_representante']['code'])	
								)
							),
						_class="table table-bordered print_model_romaneio")

	# grid_cliente
	grid_cliente = TABLE(
						TBODY(
							TR(
								TH("Cliente",_class="tit_1"),
								TD(historico['nome_cliente']['name'] or ''),
								TH("Tel",_class="tit_1"),
								TD(historico['nome_cliente']['fixo'] or '')	
								),
							TR(
								TH("Bairro",_class="tit_1"),
								TD(historico['nome_cliente']['bairro'] or ''),
								TH("Cep",_class="tit_1"),
								TD(historico['nome_cliente']['cep'] or '')
								),
							TR(
								TH("End",_class="tit_1"),
								TD(historico['nome_cliente']['endereco'] or ''),
								TH("Número",_class="tit_1"),
								TD(historico['nome_cliente']['numero'] or '')
								),
							TR(
								TH("Cidade",_class="tit_1"),
								TD(historico['nome_cliente']['cidade'] or ''),
								TH("UF",_class="tit_1"),
								TD(historico['nome_cliente']['uf'] or '')
								),
							TR(
								TH("Cnpj",_class="tit_1"),
								TD(historico['nome_cliente']['cnpj_cpf'] or ''),
								TH("Insc",_class="tit_1"),
								TD(historico['nome_cliente']['insc'] or '')
								)
							),
						_class="table table-bordered print_model_romaneio")

	# grid itens
	itens_itens = db(db.itens.codigo_venda == cod).select() # objeto com a lista de itens desse pedido
	tbody_itens = TBODY()
	for iten in itens_itens:
		tbody_itens.append(
			TR( 
				TD(iten['codigo_produto'],_class="ref_"),
				TD(iten['nome_produto'],_class="des_"),
				TD(iten['qtd'], _class="qtd_"),
				TD(format_price(iten['valor_uni_item']),_class="pre_"),
				TD(format_price(iten['valor_total_item']),_class="tot_"),
				)
			)
	grid_itens = TABLE(
						THEAD(
							TR(
								TH("Ref",_class="tit_1 ref_"),
								TH("Descrição",_class="tit_1 des_"),
								TH("Qtde",_class="tit_1 qtd_"),
								TH("Preço",_class="tit_1 pre_"),
								TH("Total",_class="tit_1 tot_"),
								)
							),
						tbody_itens,
						_class="table table-bordered print_model_romaneio", _id="grid_itens")

	# total com ou sem parcelas
	grid_price = DIV()

	# ver se tem parcelas add em grid_price 
	if historico['qtd_parcelas'] > 0:
		table_pacelas= TABLE(						THEAD(
							TR(
								TH("Parcela",_class="tit_1 mod-p"),
								TH("Valor",_class="tit_1"),
								TH("Vencimento",_class="tit_1"),
								)
							),_class="table table-bordered print_model_romaneio")
		tbody_parcelas = TBODY()
		for parcela in db(db.parcelas.codigo_venda == cod).select():
			tbody_parcelas.append(
				TR(	
					TD(parcela['parcela'],_class="mod-p"),
					TD(format_price(parcela['valor_parcela'])),
					TD((parcela['data_vencimento']).strftime('%d/%m/%Y'))
					)
			)			
			pass
		table_pacelas.append(tbody_parcelas)	
		grid_price.append(table_pacelas)
		pass

	# grid total
	table_total = TABLE(_class="table table-bordered print_model_romaneio")
	tbody_total = TBODY(
						TR(
							TH("Tipo pagamento",_class="tit_1"),
							TD(historico['tipo_pagamento'] or ''),
							TH("Total",_class="tit_1"),
							TD(format_price(historico['valor_total']) or '')
							),
						TR(
							TH("Desconto",_class="tit_1"),
							TD(format_price(historico['desconto_valor']) or ''),
							TH("Sub Total",_class="tit_1"),
							TD(format_price((float(historico['valor_total']))-(float(historico['desconto_valor']))) or '')
							)
						)
	table_total.append(tbody_total)
	# add a grid table_total em grid_price pra enviar pra view
	grid_price.append(table_total)

	return dict(grid_price=grid_price,grid_representante=grid_representante,grid_cliente=grid_cliente, grid_itens=grid_itens)

# header do historico
def HEADER():
	# empresa_dados, logo
	end = ('%s, %s - %s - %s %s - %s'%(file_settings[8],file_settings[9],file_settings[7],file_settings[6],file_settings[5],file_settings[2])).upper()
	empresa_dados = DIV(
		H3(file_settings[0]),
		H4(file_settings[1]),
		H5(file_settings[3]),
		H6(end)
		)	
	# site
	site = 'www.minhaempresa.com'
	logo = IMG(_width='100px', _src=URL('static','images/logo/logoPrint.png'))

	return dict(logo=logo, empresa_dados=empresa_dados,site=site)

# grid
def table_grid():
	# campos virtuais pra tabela
	db.historico_venda.romaneio = Field.Virtual(lambda row: (\
		A(SPAN(_class="glyphicon glyphicon-eye-open"), _class="btt b_view print", _id="%s"%row.historico_venda.id),\
	))
	db.historico_venda.etiquetas = Field.Virtual(lambda row: (\
		A(SPAN(_class="glyphicon glyphicon-tag"), _class="btt b_view etiquetas", _id="%s"%row.historico_venda.nome_cliente),\
	))

	# query da busca no db
	query = db.historico_venda.id

	# nome dos headers e dos campos do db referente a cada header
	headers =["Código", "Cliente", "Representante","Valor Total","Data da venda","Status","Romaneio","Etiquetas"]
	fields = ["codigo_venda", "nome_cliente", "nome_representante","valor_total","date_create","status_do_operacional","romaneio","etiquetas"]

	# tabela vazia 
	table = TABLE(_id="tableHistorico", _class="table table-hover table-condensed")

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
			if field == "valor_total":
				total_menos_desconto = (float(row[field]) - float(row['desconto_valor']))
				tr.append(format_price(total_menos_desconto))
			elif field == "nome_representante":
				tr.append(row[field].name)
			elif field == "nome_cliente":
				tr.append(row[field].name)
			else:
				tr.append(row[field])
		table.append(tr)

	return dict(table=table)

# regar etiquetas
def GERAR_ETIQUETAS(qtd,cliente_id):
	# objeto cliente
	cliente = db(db.registration.id == cliente_id).select()[0]
	print cliente['name']
	# as 2 rows da etiqueta
	row_two_tags = []
	tags = []

	# row one tag
	row_one = LI(
		IMG(_src=URL('static','images/logo/logoPrint.png')),
		XML(
			'<address>' \
			  '<strong>De: %s</strong><br>' \
			  '%s %s, %s<br>' \
			  '%s, %s %s<br>' \
			  '<abbr title="Phone">P:</abbr> %s<br>' \
			  '<strong>Site: </strong>%s - <strong>Email:</strong>' \
			  '<a href="mailto:#">%s</a>' \
			'</address>'%(file_settings[0],file_settings[8],file_settings[9],file_settings[7],file_settings[6],file_settings[5],file_settings[4],file_settings[2],file_settings[1],file_settings[3])
			),
		_class="list-group-item grid_etiquetas_titulo")
	row_two_tags.append(row_one) # add row one and row_two_tags

	# row two tag
	row_two = LI(
		IMG(_src=URL('static','images/destinatario.png')),
		XML(
			'<address>' \
			  '<strong>Para: %s</strong><br>' \
			  '%s %s, %s<br>' \
			  '%s, %s %s<br>' \
			  '<abbr title="Phone">P:</abbr> %s<br>' \
			  '<strong>Email:</strong>' \
			  '<a href="mailto:#">%s</a>' \
			'</address>'%(cliente['name'],cliente['endereco'],cliente['numero'],cliente['bairro'],cliente['cidade'],cliente['uf'],cliente['cep'],cliente['fixo'],cliente['email'])
			),		
		_class="list-group-item grid_etiquetas_titulo")
	row_two_tags.append(row_two) # add row two and row_two_tags
	
	# tags
	for i in range(int(qtd)):
		tags.append(
			LI(
				UL(
					row_two_tags,
					_class="list-group linha")

				)
			)	
		pass
	
	# grid
	grid_etiquetas = UL(
		tags,
		_id="grid_etiquetas")


	return grid_etiquetas