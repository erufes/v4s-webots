# v4s webots
Projeto Very Small Size Soccer Simulation (V4S) pelo Webots, utilizando comunicação tcp/ip.

## Sobre
![Robo girando](docs/midia/robo-girando.gif)<br>
Base de uma simulação de um time de Very Small Size Soccer feita no webots. Os robôs receberão os comandos através de protocolo tcp/ip e o simulador irá rodar a partida.<br>

A ideia é poder simular de forma realista e personalizável o time de Very Small Size Soccer da ERUS, mas pode ser modificada para simular outros robôs de Very Small Size Soccer.

## Webots PROTOs
De acordo com o [manual de referência do Webots](https://www.cyberbotics.com/doc/reference/proto-definition): 


    "A PROTO node is defined in a PROTO file. A PROTO file ends with a .proto extension. It lists the fields of the PROTO and defines how these fields impact the underlying object which is defined using base nodes and/or PROTO nodes."

Neste projeto estão definidos quatro PROTOs. Neles, temos alguns campos que podem ser modificados:

### v4s_soccer_field

- fieldName : String<br>
O nome do objeto v4s_soccer_field
- fieldTexture : [url]<br>
url da textura do campo

### soccer_referee_supervisor

- supervisorRange : float
- supervisorBaudRate : int
- robotController : String

### Ball
- translation : float[3]<br>
Posição do objeto na simulação
- rotation : rotation<br>
Rotação do objeto na simulação
- radius : float<br>
Raio da bola
- mass : float<br>
Massa do objeto

### V4SRobot

- translation : float[3]<br>
Posição do objeto na simulação
- rotation : rotation<br>
Rotação do objeto na simulação
- bodyMass : float<br>
Massa do corpo do robô
- wheelsMass : float<br>
Massa de cada roda
- robotController : String<br>
Controlador (código) do robô
- robotName : String<br>
Nome do robô
- robotAppearance : Appearance<br>
Aparência do robô
- wheelsAppearance : Appearance<br>
Aparência de cada roda
- synchronization : Boolean<br>

## Controles
Os controles disponíveis neste projeto permitem controlar os robôs de very small size soccer de forma remota através de protocolo tcp/ip. Os robôs abrem cada um uma porta de acordo com seu time e id:

| Time/id |   1   |   2   |   3   |
|:-------:|:-----:|:-----:|:-----:|
| Blue    | 40001 | 40002 | 40003 |
| Yellow  | 30001 | 30002 | 30003 |

E utilizam JSON-RPC, um protocolo de chamada de procedimento remoto codificado em JSON, para responder aos comandos. Para fazer um robô mover-se, basta enviar para o endereço dele um objeto JSON:


    {
        'method'  : 'move',
        'params'  : [vel-dir, vel-esq],
        'jsonrpc' : '2.0',
        'id'      : id
    }

Para controlar e obter informações da simulação, um controle é aberto na porta 4002. Os serviços disponíveis são:

- stop_sim : parar a simulação
- start_sim : iniciar a simulação
- reset_sim : reiniciar a simulação
- reset_objects : reposicionar os objetos na posição inicial
- get_state : obter estado de jogo (responde um dict python)

## Dados da Equipe:
O VSSS-ERUS é uma equipe dedicada a implementação do desafio Very Small Size Soccer para competições. É um projeto da ERUS - Equipe de Robótica da UFES, e diversos documentos sobre o projeto podem ser encontrados no site da equipe.

 - Site da ERUS : http://erus.ufes.br/
 - E-mail da ERUS : erus@inf.ufes.br
 - E-mail do VSSS-ERUS : vssserus@gmail.com

### Trabalhando neste sub-projeto
- [Lorena Bassani](https://github.com/LBBassani)