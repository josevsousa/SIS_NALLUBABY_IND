# -*-coding: utf-8 -*-

# mostar dados para o grafico da tela vendas
def grafico_receitaa():

	# lista com o total de cada mes
	total_meses = []
	# busca de 1 a 12
	for i in range(1,13):
		print datatime.now().strftime('Y')
		# total_meses.append(i+10)

	print total_meses		

	#db(db.product.date_create.like('2016-09%')).select('date_create')	
	return [80,10,10,10,40,40,40,40,50,100,50,100]

