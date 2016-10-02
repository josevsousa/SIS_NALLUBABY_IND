# -*- coding: utf-8 -*-

# gravar session no db
def gravar_session_db(grid_parcelas_db):
	codigo_venda = datetime.now().strftime("%y%m%d%H%M%S")

	# session
	caixa = session.caixa
	cliente = session.etapa_1
	itens = session.cart

	try:
		#gravar no db
		db(db.historico_venda.insert(
			codigo_venda=codigo_venda,
			nome_cliente=cliente['id_cliente'], #gravar id
			nome_representante=cliente['id_representante'], #gravar id
			valor_total=caixa['total'],
			desconto_valor=caixa['desconto'],
			desconto_por=caixa['por'],
			desconto_din=caixa['din'],
			valor_subtotal=caixa['sub_total'],
			qtd_parcelas=caixa['parcelas'],
			tipo_pagamento=caixa['tipo']))

		# # fk do historico_venda
		fk = db(db.historico_venda.codigo_venda == codigo_venda).select('id')[0]['id']

		# itens
		for row in itens:
			db(db.itens.insert(
				codigo_venda=fk,
				codigo_produto=row['code'],
				nome_produto=row['name'],
				qtd=row['qtd'],
				valor_uni_item=row['price'],
				valor_total_item=row['total']
				))
			pass

		# parecelas 
		if grid_parcelas_db != 'False':
			grid = grid_parcelas_db.split(';')
			for row in grid: # percorre todos itens 
				if row != '': # menos o ultimo que é vazio
					row = row.split(',') 
					# grava no db parcelas
					db(db.parcelas.insert(
						codigo_venda=fk,
						parcela=int(row[0]),
						valor_parcela=float(row[1]),
						data_vencimento=("%s 00:00:00"%row[2])
						))
					pass
			pass

		# limpar sessions 
		limpar_sessions()
	except:
		response.flash = "Error contate o administrador"	
	pass # fim gravar session no db

# fechar a venda 
def limpar_sessions():
	##### apagar sessions: etapa_1, etapa_2, cart
	session.__delitem__('cart')
	session.__delitem__('caixa')
	session.__delitem__('etapa_1')
	pass