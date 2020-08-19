""" Nome do módulo :        Server
    Ano de criação :        2020/01
    Descrição do módulo :   Módulo que roda o servidor json-rpc
    Versão :                1.0
    Pré-requisitos :        json-rpc
    Membros :               Lorena "Ino" Bassani
"""

from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple

from jsonrpc import JSONRPCResponseManager, dispatcher

""" Nome da função :        run_aplication_server
    Intenção da função :    roda o web service
    Pré-requisitos :        nenhum web service já rodando na porta dada
    Efeitos colaterais :    roda um serviço na porta especificada
    Parâmetros :            functions : Dict com as funções no formato {"nome_func" : callable}
                            host (default = localhost) : local onde rodará o serviço
                            port (default = 4002) : porta onde rodará o serviço
    Retorno :               nenhum
"""

def run_aplication_server(functions, host = 'localhost', port = 4002):
    @Request.application
    def application(request):
        response = JSONRPCResponseManager.handle(request.data, functions)
        return Response(response=response.json, mimetype='application/json')
    run_simple(host, port, application)
