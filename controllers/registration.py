# -*- coding: utf-8 -*-

# new
@auth.requires_membership("admin")
def new():
	hide_fields("product",["backup_price"]) #esconder campos
	d = ""
	form=SQLFORM(db.registration)
	if form.process().accepted:
		redirect(URL('registration','tela_registration'))
	elif form.errors:
		response.flash = "Dados com erro"
	# cod = max(db(db.product).select('code'))['code'] #maior numero da coluna 'code'
	return dict(form=form)

def tela_registration():
	query = db.registration
	query2 = db.product
	clientes = db(query.status == 'Cliente').count()
	representantes = db(query.status == 'Representante').count() 
	funcionarios = db(query.status == 'Funcionario').count()
	produtos = db(query2.id>0).count()
	return dict(tc=clientes,tr=representantes,tf=funcionarios,tp=produtos)

def list():
	status = request.vars.status or request.args(0) 
	try:
		if status == 'Representante':
			title = 'Cadastro representante'
			table = list_registro('Representante')
		elif status == 'Funcionario':
			title = 'Cadastro Funcionario'
			table = list_registro('Funcionario')
		elif status == 'Cliente':
			title = "Cadastro clientes"
			table = list_registro("Cliente")
		else:
			redirect(URL('registration','tela_registration'))	
	except Exception:
		redirect(URL('registration','tela_registration'))		
	
	return dict(table=table,title=title)

def list_registro(status):
	# query que busca: clientes, funcionarios, representante
	#criar if para decidir qual query montar
	query = db.registration.status == status

    # hide_fields("registration",["total_price"]) #esconder campos
	# campos virtuais pra tabela
	db.registration.edit = Field.Virtual(lambda row: (\
		A(SPAN(_class="glyphicon glyphicon-eye-open"), _class="btt b_view", _href=URL("dados_registro", args=[row.registration.id,status])),\
		A(SPAN(_class="glyphicon glyphicon-edit"), _class="btt b_edit", _href=URL("edit", args=[row.registration.id,status])),\
		A(SPAN(_class="glyphicon glyphicon-remove"), _class="btt b_delet", _id=row.registration.id, _href="#")))
	
	db.registration.img = Field.Virtual(lambda row: get_miniatura_sqlformgrid_registration(row))	
	
	# nome dos headers e dos campos do db referente a cada header
	headers =["f","Cod", "Nome","Edit"]
	fields = ["img", "code","name","edit"]

	# tabela vazia 
	table = TABLE(_id="minhaTabela", _class="table hover table-striped table-bordered")

	# thead vazio sendo populado pelo for
	thead = THEAD(TR())
	for header in headers:
		thead[0].append(TD(B(header)))
	table.append(thead)
	
	# montando todos os rows da tabela registration
	rows = db(query).select()

	# navegando em todos os rows e populando os tr com o retorno 
	for row in rows:
		tr = TR(_id=row['id'])
		for field in fields:
			tr.append(row[field])
			pass #fim do for field
		table.append(tr)
		pass #fim do for row
		
	return table	

@auth.requires_membership("admin")
def remov():
	# remover item do carrinho via ajax
	index = request.vars.transitory
	idd = index[0]
	
	response.flash = "Item excluido"
	# altera o status do registro para Falso
	db(db.registration.id == idd).update(status = 'deletado') 

	return "$('#%s').remove();"%(idd) 

# @auth.requires_login()
@auth.requires_membership("admin")
def edit(): 
	hide_fields("registration",["id","thumbnail","code"]) #esconder campos

	# pegar produto pelo id ou slug
	# criar formulario de edicao
	# apenas para admin
	p_id = request.args(0) or redirect(URL("home","index"))
	form = SQLFORM(db.registration, int(p_id))
	if form.process().accepted:
		redirect(URL("list?status=%s"%request.args(1)))
	elif form.errors:
		response.flash = T("Dados com erro")
	
	return dict(form=form)

def dados_registro():
	pid = request.args(0)
	query = db(db.registration.id == int(pid))
	return dict(registrations=query.select())