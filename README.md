# Orquestrador de Jobs

Este projeto tem como objetivo a implementação de um orquestrador que gerencie a execução de jobs. Ele foi desenvolvido em _Python_, com a biblioteca _Flask_, o serviço _Amazon Lambda_ e o _MySQL_ como banco de dados. Os requisitos deste projeto são encontrados no arquivo __Requisitos.pdf__, encontrados neste mesmo repositório do git.

Com ele o usuário poderá enviar um código escrito em python e os parâmetros e inputs necessários para que este código funcione e será executado no serviço Lambda da AWS, que retornará o resultado obtido ou um erro caso ele ocorra.

### Como utilizar
Para utilizar este projeto é necessário primeiro ter o MySQL e o Python 3 instalados, assim como as bibliotecas flask, flask_mysqldb, json, boto3 e base64 do Python instaladas.

É necessário baixar este repositório git e também preparar o banco de dados local para que o projeto possa acessá-lo. Para isso, será necessário criar um Database no seu MySQL caso você queira utilizar um novo e você pode fazer isso utilizando o comando a seguir:
```
DROP DATABASE IF EXISTS nome_do_database;

CREATE DATABASE nome_do_database;

USE nome_do_database;
```
A seguir, você pode rodar o arquivo `scripts.sql` encontrado neste mesmo repositório do git na interface do MySQL (como o MySQL Workbench) ou digitar cada comando presente no arquivo no terminal do seu SO após logar no seu MySQl por ele.

Se nenhum erro acontecer até aqui, o seu ambiente está pronto para rodar este projeto.

Para isto, abra o seu terminal e navegue até o diretório que você baixou deste projeto. 
Utilize o comando a seguir para executar a aplicação:

`python3 main.py`

Digite o __nome do usuário__ do MySQL utilizado para criar o Database e dê enter.
Digite a __senha do usuário__ do MySQL utilizado para criar o Database e dê enter.
Digite o __nome do Database__ que você criou anteriormente e dê enter.

Pronto, você subiu a aplicação e entrando no link _http://localhost:5000/_ com o seu navegador de preferência você encontrará a interface do projeto.

No endpoint '/' você encontrará __todos os jobs existentes e suas respectivas informações__, como resultado, ID do usuário que criou o job e etc. Como você acabou de criar o banco de dados, apenas a query inicial aparecerá neste momento.

No endpoint '/jobs/' além de encontrar os jobs existentes você também poderá __criar um novo job e excutá-lo no serviço Lambda da Amazon__. 
Para isso é necessário que o __UserID__ inserido seja um número _inteiro e maior do que 0_. 
O campo __Code__ precisa ser preenchido com o _nome do arquivo que contém o código_ que você deseja rodar no serviço Amazon Lambda, e é de extrema importância que neste arquivo contenha uma função que englobe as operaçes que você deseja fazer, que você dê _RETURN_ no que deseja que seja o retorno da função e que logo em seguida você _PRINTE_ a chamada da função, só assim o código irá funcionar. Este arquivo precisa estar no mesmo diretório que o arquivo `main.py` . Um exemplo de como o seu código pode ser escrito encontra-se no arquivo `teste.py` deste mesmo repositório git.
O campo __Input__ precisa ser preenchido com um _dicionário python_ com os _argumentos e inputs_ que você deseja substituir no seu código. Um exemplo de input para que o código do arquivo `teste.py` funcione é o {"a":5, "b":3}.
Para concluir a ação aperte o botão "Enviar".
Caso o seu código funcione e retorne antes de 10 segundos o resultado, você verá a mensagem __"Adicionado com sucesso!"__ e o ID do job que você acabou de criar. Ao voltar para algum dos endpoints já apresentados aqui, você poderá encontrar o status desse job e caso ele tenha terminado, você encontrará também o valor de retorno dele.
Caso o seu código não funcione, dê algum tipo de erro, tenha recebido um input incorreto ou tenha excedido o timeout de 10 segundos, a mensagem exibida será __"Adicionado, porém com erro!"__ e ao voltar para algum dos endpoints já apresentados aqui você poderá encontrar o status desse job.

No endpoint '/jobs/<job_id>' sendo __job_id__ um _número inteiro maior que 0_, você encontrará as __informações do job com o ID especificado__.

No endpoint '/users/<user_id>' sendo __user_id__ um _número inteiro maior que 0_, você encontrará __todos os jobs criados pelo usuário com o ID especificado__.

No terminal que você rodou a aplicação, você poderá verificar eventuais _erros_ que possam ter acontecido durante alguma ação, os _job_id's criados_ desde que o programa está sendo executado e também o _tipo dos inputs_, para verificar se está sempre sendo do tipo dicionário python ou se você está tentando fazer o input com algum tipo não permitido.
