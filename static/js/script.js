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
			ppf = calcularPontosPorFator( notasChefia[i], notasServidor[i] );
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


    $(".notaSelect").change(function(){
        var name = $(this).attr("name");
        var nota = $(this).val();
        var notaChefia = $("input[name='"+name+"_CHEFIA']").val();

        var ppf = calcularPontosPorFator(nota, notaChefia);
        var span = "span."+name;

        if (ppf >= 7){
				$(span).css("background-color", "#AEE8AC");
			}
			else{
				$(span).css("background-color", "#E8BBAC");
			}

        console.log(ppf);
        $(span).text(ppf);
    });

});

function calcularPontosPorFator(notaChefia, notaServidor){
	return ( parseInt(notaChefia,10) + parseInt(notaServidor,10) ) / 2;
}