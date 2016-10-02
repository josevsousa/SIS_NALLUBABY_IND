# -*- coding: utf-8 -*-
def vendas():
	# grafico
	grafico = grafico_receita()

	# tabela 	
	table = table_grid()['table']

	return dict(receita=grafico,grid=table)

def romaneio():
	codigo_id = request.vars.cod

	# grid com dados da empresa, cliente, representante
	logo = HEADER()['logo']
	empresa_dados = HEADER()['empresa_dados']
	site = HEADER()['site']
	
	# grids para view romaneio
	grid_historico = GRID_HISTORICO(codigo_id) # object que gera as grids 

	return dict(
		logo=logo,
		empresa_dados=empresa_dados,
		site=site,
		representante=grid_historico['grid_representante'],
		cliente=grid_historico['grid_cliente'],
		lista=grid_historico['grid_itens'],
		grid_price=grid_historico['grid_price']
		)

def printEtiqueta():
	code = request.vars.code
	return dict(code=code)

def etiquetas_print():
	index = request.vars.transitory # qtd, cliente_id
	index = index.split(';')
	qtd = index[0]
	cliente_id = index[1]

	if (qtd != '') or (qtd != '0'):
		return GERAR_ETIQUETAS(qtd,cliente_id)
	else:
		return H2('Valor invalido!')
		pass
	pass	
	# return GERAR_ETIQUETAS(request.vars.qtd)