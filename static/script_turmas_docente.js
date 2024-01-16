var containerDiv = document.getElementById('container-geral-lista-disciplinas_docente');

nomes.forEach(function(nome) {
    var div = document.createElement('div');
    div.textContent = nome[0]
    div.className = "div-lista-disciplinas_docente";

    var paragrafo = document.createElement('p');
    paragrafo.className = "informacao-cod-turma";
    paragrafo.textContent = "Turma: " + nome[1];

    div.onclick = function() {
        informacoesDisciplinas_docente(this);
    };
    containerDiv.appendChild(div);
    containerDiv.appendChild(paragrafo);
});


 function informacoesDisciplinas_docente(divPai) {
    var divFilha = divPai.querySelector('.informacoes-disciplina_docente');
    if (divFilha) {
        // Se a div filha já existe, remova-a
        //divPai.removeChild(divFilha);
        //divPai.style.height = "70px";
    } else {
        // Se a div filha não existe, crie-a

        divFilha = document.createElement("div");
        divFilha.className = "informacoes-disciplina_docente";


        // criar div para colocar o nome, np1, np2 e np3
        divInformacoesNomeNp1Np2Np3 = document.createElement("div");
        divInformacoesNomeNp1Np2Np3.className = "divInformacoesNomeNp1Np2Np3";

        // criar colunas com o nome
        divNomeAluno = document.createElement("div");
        divNomeAluno.className = "lista-alunos";
        divNomeAluno.textContent = "ALUNO";

        // criar colunas com np1
        divNotaNP1 = document.createElement("div");
        divNotaNP1.className = "nota-docente_lancar_np1";
        divNotaNP1.textContent = "NP1";

        // criar colunas com np2
        divNotaNP2 = document.createElement("div");
        divNotaNP2.className = "nota-docente_lancar_np2";
        divNotaNP2.textContent = "NP2";

        // criar colunas com np3
        divNotaNP3 = document.createElement("div");
        divNotaNP3.className = "nota-docente_lancar_np3";
        divNotaNP3.textContent = "NP3";

        // criar colunas com cod_nota
        divCodNota = document.createElement("div");
        divCodNota.className = "cod-nota-aluno";
        divCodNota.textContent = "Cod. Nota";

        //criar botao para fechar a div
        var button = document.createElement("button");
        button.className = "button-fechar-div";
        var iconButton = document.createElement("i");
        iconButton.className = "bi bi-arrow-up-short";
        button.appendChild(iconButton);

        iconButton.onclick = function(event) {
            event.stopPropagation(); // Impede a propagação do evento para a div pai
            closeDiv();
          };

        function closeDiv() {
            divPai.removeChild(divFilha);
            divPai.style.height = "70px";
        };


        divInformacoesNomeNp1Np2Np3.appendChild(divNomeAluno);
        divInformacoesNomeNp1Np2Np3.appendChild(divNotaNP1);
        divInformacoesNomeNp1Np2Np3.appendChild(divNotaNP2);
        divInformacoesNomeNp1Np2Np3.appendChild(divNotaNP3);
        divInformacoesNomeNp1Np2Np3.appendChild(divCodNota);
        divInformacoesNomeNp1Np2Np3.appendChild(button);


        divFilha.appendChild(divInformacoesNomeNp1Np2Np3);


        // percorrer o array com os nomes dos alunos
        for (let i = 0; i < lista_cod_turma_e_nome_disciplina_e_seus_respectivos_alunos_e_id_notas.length; i += 2) {
            // Acesse os elementos do array com índices i e i + 1
            //const codTurma = lista_cod_turma_e_nome_disciplina_e_seus_respectivos_alunos_e_id_notas[i][0];
            const nomeDisciplina = lista_cod_turma_e_nome_disciplina_e_seus_respectivos_alunos_e_id_notas[i][1];

            // quando ele encontra o mesmo nome da discilina:
            if (divPai.innerText == nomeDisciplina) {

            for (let j = 0; j <= lista_cod_turma_e_nome_disciplina_e_seus_respectivos_alunos_e_id_notas[i+1].length; j++) {
                if (lista_cod_turma_e_nome_disciplina_e_seus_respectivos_alunos_e_id_notas[i+1][j] == undefined) {
                break;
                }

                //inserir nome do aluno
                pNomeAluno = document.createElement("p");
                pNomeAluno.textContent = lista_cod_turma_e_nome_disciplina_e_seus_respectivos_alunos_e_id_notas[i+1][j][0];
                divNomeAluno.appendChild(pNomeAluno);

                //inserir input np1 do aluno
                inputNP1 = document.createElement("input")
                divNotaNP1.appendChild(inputNP1);

                //inserir input np2 do aluno
                inputNP2 = document.createElement("input")
                divNotaNP2.appendChild(inputNP2);

                //inserir input np3 do aluno
                inputNP3 = document.createElement("input")
                divNotaNP3.appendChild(inputNP3);

                //inserir cod. nota do aluno
                codNotaAluno = document.createElement("p");
                codNotaAluno.textContent = lista_cod_turma_e_nome_disciplina_e_seus_respectivos_alunos_e_id_notas[i+1][j][1];
                divCodNota.appendChild(codNotaAluno);
            }

            break;

            }

        }

        //Criar botao "Atualizar"
        var buttonAtualizar = document.createElement("button");
        buttonAtualizar.innerText = "Atualizar";
        buttonAtualizar.className = "buttonAtualizarNotas";
        buttonAtualizar.onclick = function() {
            obterNomes_novas_notas_e_id_notas(divPai);
        };
        divNomeAluno.appendChild(buttonAtualizar);



        divPai.appendChild(divFilha);
        divPai.style.height = "auto";
    }
 }

 function obterNomes_novas_notas_e_id_notas(divPai) {
    var firstChild = divPai.firstChild;
    if (firstChild.nodeType === Node.TEXT_NODE) {
      // Imprimir o innerText no console
      //console.log(firstChild.nodeValue.trim());
    }

    //pegar o nome dos alunos
    const nomes_array = [];
    const elementosP = divPai.querySelectorAll('.lista-alunos p');

    elementosP.forEach((elementoP) => {
      nomes_array.push(elementoP.textContent);
    });


    //pegar nota np1 dos alunos
    const np1_array = [];
    const notas_np1_input_value = divPai.querySelectorAll('.nota-docente_lancar_np1 input');

    notas_np1_input_value.forEach((inputValue) => {
      np1_array.push(inputValue.value);
    });

    //pegar nota np2 dos alunos
    const np2_array = [];
    const notas_np2_input_value = divPai.querySelectorAll('.nota-docente_lancar_np2 input');

    notas_np2_input_value.forEach((inputValue) => {
      np2_array.push(inputValue.value);
    });


    //pegar nota np3 dos alunos
    const np3_array = [];
    const notas_np3_input_value = divPai.querySelectorAll('.nota-docente_lancar_np3 input');

    notas_np3_input_value.forEach((inputValue) => {
      np3_array.push(inputValue.value);
    });


    //pegar os id_notas dos alunos
    const id_notas_array = [];
    const elementos_id_notas_P = divPai.querySelectorAll('.cod-nota-aluno p');

    elementos_id_notas_P.forEach((elementoP) => {
      id_notas_array.push(elementoP.textContent);
    });




    fetch('/receber_notas_alunos_do_arquivo_js', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            array_np1: np1_array,
            array_np2: np2_array,
            array_np3: np3_array,
            array_id_notas: id_notas_array
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Resposta do servidor:', data);
    })
    .catch(error => {
        console.error('Erro na requisição:', error);
    });






    console.log(nomes_array);
    console.log(np1_array);
    console.log(np2_array);
    console.log(np3_array);
    console.log(id_notas_array);


  }