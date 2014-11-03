// TODO todo esse arquivo está um lixo e representa todo o meu saco com frontend
$(document).ready(function(){
    var notasChefia = [];
    var notasServidor = [];
    var i = 0;

	$("input.chefia").each(function(){
		notasChefia.push($(this).val());
	});

	$("input.servidor").each(function(){
		notasServidor.push($(this).val());
		console.log('Nota Servidor ' + i + " : " + $(this).val() )
	});

	// ppf = span da célula de Pontos por Fator em anexo1 / pagina2
	$("span.ppf").each(function(){
		if (notasChefia[i] && notasServidor[i]){
			ppf = cacularPontosPorFator( notasChefia[i], notasServidor[i] );
			if (ppf >= 7){
				$(this).css("background-color", "#AEE8AC");
			}
			else{
				$(this).css("background-color", "#E8BBAC");
			}
		}
		else{
			ppf = '--';
		}

		$(this).text(ppf);
		i++;
	});

});

function cacularPontosPorFator(notaChefia, notaServidor){
	return ( parseInt(notaChefia,10) + parseInt(notaServidor,10) ) / 2;
}