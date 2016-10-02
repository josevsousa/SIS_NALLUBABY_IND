$(document).ready(function(){
	$("select").on('change',function(){
		if ($("#no_table_cliente").val() != "" && $("#no_table_representante").val() != "" ){
			$('#1').addClass('etapa_edit');
		}else{
			$('#1').removeClass('etapa_edit, etapa_ok');
		}
	})
})