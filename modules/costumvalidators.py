# -*- coding: utf-8 -*-

class IS_VALID_BARCODE(object):
    """docstring for IS_VALID_BARCODE"""
    def __init__(self, start_with="", error_message="INVALID BARCOD"):
        self.error_message=error_message
        self.start_with = start_with

    def __call__(self, value): #funcao execultada no submit
        error = None
        #startswith "funcao do python"
        if not value.startswith(self.start_with):
            return (value, self.error_message)
        else:
            return (value, None)

class VALIDATOR(object):
    def __init__(self, error_message="SOMETHING WRONG"):
        self.error_message = error_message

    def __call__(self, value):
        error = None
        # CONDITION COMES HERE
        if "ERROR":
            error = self.error_message

        # IF error != None - value is invalid 
        return (value, error)

class TRANSFORMATION(object):
    def __init__(self, search, replace):
        self.search = search
        self.replace = replace

    def __call__(self, value):
        error = None
        try:
            # TRANSFORMATION COMES HERE
            value = value.replace(self.search, self.replace)
        except:
            error = "Not possible to transform"
        return (value, error)

class IS_ALLOWED_ZIP_CODE(object):
    def __init__(self, zip_area, error_message="Zip code not allowed"):
        self.zip_area = zip_ares
        self.error_message = error_message

    def __call__(self, value):
        error = None
        value = value.strip()
        if not value.startswith(self.zip_area):
            error = self.error_message
        return (value, error)

class REPLACE_TEXT(object):
    def __init__(self, search, replace):
        self.search = str(search)
        self.replace = str(replace)

    def __call__(self, value):
        error = None
        try:
             value = value.replace(self.search, self.replace)
        except:
            error = "Error replacing"
        return (value, error)

class CODE_AUTO(object):
    def __init__(self, product, field):
        self.product = product
        self.field = field
        self.num = 0

    def gerar(object):
        tabela = self.product
        field = self.field
        for item in db(db.self.product).select():
            nn = item.self.field
            if int(n) < int(nn):
                n = nn
                pass
            pass   
        return str(n+1).zfill(5)    
