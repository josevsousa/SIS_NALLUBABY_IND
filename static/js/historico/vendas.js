$(document).ready(function(){

    //=== BUSCAR REGISTRO
    $('.print').on('click',function(){
        var td = this.id;
        
        var URL = "romaneio?cod="+td;

        var width = 690;
        var height = 920;
         
        var left = 70;
        var top = 30;
         
        window.open(URL,'janela', 'width='+width+', height='+height+', top='+top+', left='+left+', scrollbars=yes, status=no, toolbar=no, location=no, directories=no, menubar=no, resizable=no, fullscreen=no');
    });
        //=== BUSCAR REGISTRO
    $('.etiquetas').on('click',function(){
        var td = this.id;
        console.log(td)
        var URL = "printEtiqueta?code="+td;

        var width = 690;
        var height = 920;
         
        var left = 70;
        var top = 30;
         
        window.open(URL,'janela', 'width='+width+', height='+height+', top='+top+', left='+left+', scrollbars=yes, status=no, toolbar=no, location=no, directories=no, menubar=no, resizable=no, fullscreen=no');
    });


}); //fim do ready