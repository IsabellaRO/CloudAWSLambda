import json
import urllib.parse
import sys
from io import StringIO

def lambda_handler(event, context):
    code = event['code']
    inputt = event['input']
    #code = urllib.parse.unquote(code)
    #code = code.replace('\\n', '\n')
    #code = code.replace('\\t', '\t')
    #print(event['code'])
    #print(code)
    #Nas linhas a seguir tive ajuda do Lucas Chen, pois não conseguia realizar o exec do codigo da forma que ele chegava, apenas pelo print que acontece dentro do exec
    buffer = StringIO()
    sys.stdout = buffer
    try:
        exec(code, inputt)
    except:
        return(1, "ERROR")
    sys.stdout = sys.stdout
    #result = main()
    #print(result)
    #return ("statusCode: 200", "body: {}".format(json.dumps('Hello from Lambda!')), "Input: {}".format(event["input"]), "Code: {}".format(event["code"]), "Result: {}".format(int(buffer.getvalue())))
    retorno = {}
    retorno["statusCode"] = 200
    retorno["body"] = 'Hello from Lambda!'
    retorno["Input"] = event["input"]
    retorno["Code"] = event["code"]
    retorno["Result"] = int(buffer.getvalue())
    return (0, retorno["Result"])
