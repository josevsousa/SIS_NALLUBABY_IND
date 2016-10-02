# -*- coding: utf-8 -*-

# Listas
sexo_regist = ("masculino",'feminino')
tipo = ('Pessoa_física','Pessoa_jurídica')
status = ('Cliente','Representante','Funcionario')
sexo = ("masculino",'feminino','unisex')

# Category
db.define_table("category",
	Field("name", length=128, notnull=True, unique=True ),
	Field("description", "text" ),
	format='%(name)s'
	)

# Product
db.define_table("product",
	Field("name","string"),
	Field("code","integer", unique=True),
	Field("category", "reference category"),
	Field("tamanho", default="P/M/G"),
	Field("sexo","string", default="unisex"),
	Field("description","text"),
	Field("estoque", "integer", default=0, readable=False, writable=False),
	Field("unit_price","double", label= "Preço"),
	Field("backup_price","double", default=0), # computed fields
	Field("picture","upload"),
	Field("thumbnail","upload"),
	Field("featured","boolean", label="destaque",default=False),
	Field('date_create','datetime', default=request.now, readable=False,  writable=False),
	Field('date_change','datetime', default=request.now, readable=False,  writable=False)
	)

# Registration
db.define_table('registration',
    Field('code','string'),
    Field('tipo', 'string', default='Pessoa_física'),
    Field('status', 'string', label='Status'),
	Field("sexo","string"),
    Field('name','string',label='Nome'), 
    Field('cel',"list:string", label="Celular"),
    Field('fixo',"list:string", label='Tel fixo'),
    Field('email', 'string', label='E-mail'),
    Field('cnpj_cpf', 'string', label='CNPJ/CPF'),
    Field('insc', 'string', label="INSC"),
    Field('cep', 'string', label='CEP'),
    Field('uf', 'string', label='UF', default='-'),
    Field('bairro', 'string', label='Bairro'),
    Field('cidade', 'string', label='Cidade'),
    Field('endereco', 'string', label='Endereço'),
    Field('numero' , 'string',label='Número'),
    Field('picture','upload', label='Foto'),
	Field("thumbnail","upload"),
	Field('date_create','datetime', default=request.now, readable=False,  writable=False),
	format = '%(name)s'
    )	

# Historico
db.define_table('historico_venda',
	Field('codigo_venda','string'),
	Field('nome_cliente','reference registration'),
	Field('nome_representante','reference registration'),
	Field('valor_total','double', default=0.0),
	Field('desconto_valor','double', default=0.0),
	Field('desconto_por','integer', default=0),
	Field('desconto_din','double', default=0.0),
	Field('valor_subtotal','double', default=0.0),
	Field('qtd_parcelas','integer', default=0),
	Field('tipo_pagamento','string'),
	Field('status_do_operacional','string',default='separando'),
	Field('qtd_embalagens','integer', default=0),
	Field('date_create','datetime', default=request.now, readable=False,  writable=False),
	Field('date_change','datetime', default=request.now, readable=False,  writable=False),
	format = '%(codigo_venda)s'
	)

# Parcelas
db.define_table('parcelas',
	Field('codigo_venda','reference historico_venda'),
	Field('parcela','integer'),
	Field('num_cheque','string'),
	Field('num_boleto','string'),
	Field('valor_parcela','double'),
	Field('data_vencimento', 'datetime'),
	Field('data_pagamento','datetime'),
	Field('status_parcela','string', default='aguardando'),
	Field('date_change','datetime', default=request.now, readable=False,  writable=False)
	)

# Itens
db.define_table('itens',
	Field('codigo_venda','reference historico_venda'),
	Field('codigo_produto','string'),
	Field('nome_produto','string'),
	Field('qtd','integer'),
	Field('valor_uni_item','double'),
	Field('valor_total_item','double'),
	Field('status_entrega','string',default='aguardando'),
	Field('obs_operacional','text'),
	Field('date_change','datetime', readable=False,  writable=False)
	)

# Empresa
db.define_table('empresa',
	Field('name','string',label='Nome'), 
	Field('Cel',"list:string", label="Celular"),
	Field('fixo',"list:string", label='Tel fixo'),
	Field('email',label='E-mail'),
	Field('site','string'),
	Field('cnpj_cpf', label='CNPJ/CPF'),
	Field('cep', label='CEP'),
	Field('uf', label='UF', default='-'),
	Field('bairro', label='Bairro'),
	Field('cidade', label='Cidade'),
	Field('endereco', label='Endereço'),
	Field('numero' ,label='Número'),
	Field('picture','upload', label='Logo'),
	Field("thumbnail","upload")
	)