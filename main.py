#Para fazer este código e o do templete html, utilizei o tutorial do link a seguir: https://www.codementor.io/adityamalviya/python-flask-mysql-connection-rxblpje73
from flask import Flask, jsonify, request, render_template
from flask_mysqldb import MySQL
import json
import boto3
import base64
import urllib.parse
import re

client = boto3.client("lambda")

app = Flask('ProjetoFinal')

root = input("Insira o nome de usuário para acessar o seu MySQL: ")
password = input("Insira a senha para acessar o seu MySQL: ")
db = input("Insira o nome do Database onde está a table Jobs do seu MySQL: ")

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = root
app.config['MYSQL_PASSWORD'] = password
app.config['MYSQL_DB'] = db
mysql = MySQL(app)

@app.route('/', methods = ['GET']) #Retornará erro caso execução tiver return != 0
# GET: devolve um JSON contendo uma lista de jobs seguindo o padrão:
# [ { “job_id”: int, “uid”: int, “status”: [“DONE” | “ERROR” | “WAITING” | “RUNNING”], “result”: string} ]

def getHandler(uid=None):
	ms = mysql.connection.cursor()
	if request.method == "GET":
		#ms = mysql.connection.cursor()
		ms.execute("SELECT * FROM Jobs;")
		jobs = ms.fetchall()
		#print(jobs)
		list_jobs = ""
		for job in jobs:
			list_jobs = list_jobs + "<br>" + "{" + '"job_id": {}, "uid": {}, "status": {}, "result": {}'.format(job[0], job[1], job[2], job[3]) + "}"
		ms.close()
		#return jsonify(list_jobs)
	#print(list_jobs)
	file = open("./templates/GET.html", "r")
	html = file.read()
	file.close()
	view = html.replace('***', list_jobs)
	view = view.replace("~", "")
	return view

# POST: envia um código para ser rodado no nosso serviço
#entrada = {"uid": int, "code": string, "input": string}
@app.route('/jobs/', methods = ['GET', 'POST'])
def postHandler(uid=None):
	ms = mysql.connection.cursor()
	if request.method == "POST":
		content = request.form
		uid = content['uid']
		try:
			int(uid)
			if int(uid) <= 0:
				return("UserID precisa ser maior que 0.")
		except:
			return("UserID precisa ser número inteiro.")

		code = content['code']
		if "." not in str(code):
			return("Code precisa ser nome de um arquivo.")

		inputt = content['inputt']
		try:
			inputt = json.loads(inputt)
			if type(inputt) != type({"a": 1}):
				return("Input precisa ser um dicionário.")
		except:
			return("Input precisa ser um dicionário.")

		print("input:", type(inputt))
		f = open(code, "r")
		code = f.read()
		f.close()
		#codigo = urllib.parse.urlencode({"code": code})
		status = "RUNNING"
		result = None
		ms.execute("INSERT INTO Jobs (uid, status, result) VALUES (%s, %s, %s);", (int(uid), status, result))
		mysql.connection.commit()
		response = client.invoke(
				FunctionName='meulambda',
				InvocationType='RequestResponse',
				Payload=bytes(json.dumps({"input":inputt, "code": code}), "utf-8")
			)
		data = response['Payload'].read()
		if ("errorMessage" in data.decode("utf-8")):
			status = "ERROR"
			print("Exec não funcionou.", data.decode("utf-8"))
			data = None
		#print(data.decode("utf-8")[1])
		elif int(data.decode("utf-8")[1]) != 0:
			status = "ERROR"
			print("Exec não funcionou.")
			data = None
		else:
			data = int(data[4:-1].decode("utf-8"))
			status = "DONE"
		#print(data)
		#print(jsonify(retorno))
		jobId = ms.lastrowid #execute('SELECT @@identity;')# OR ("SELECT LAST_INSERT_ID();")
		#print("Jobid: ", jobId)
		retorno = {"job_id": jobId}
		print(retorno)
		ms.execute('UPDATE Jobs SET status=%s, result=%s WHERE jobId=%s;', (status, data, jobId))
		mysql.connection.commit()
		ms.close()
		if status == "DONE":
			return ("<center>Adicionado com sucesso! <br> {}</center>".format(retorno))
		elif status == "ERROR":
			return ("<center>Adicionado, porém com erro! <br> {}</center>".format(retorno))

	if request.method == "GET":
		#ms = mysql.connection.cursor()
		ms.execute("SELECT * FROM Jobs;")
		jobs = ms.fetchall()
		#print(jobs)
		list_jobs = ""
		for job in jobs:
			list_jobs = list_jobs + "<br>" + "{" + '"job_id": {}, "uid": {}, "status": {}, "result": {}'.format(job[0], job[1], job[2], job[3]) + "}"
		ms.close()
		#return jsonify(list_jobs)
	#print(list_jobs)
	file = open("./templates/POST.html", "r")
	html = file.read()
	file.close()
	view = html.replace('***', list_jobs)
	view = view.replace("~", "")
	return view

#/jobs/<job_id> (GET) - retorna o status do job_id passado.
#{“job_id”: int, “uid”: int, “status”: [“DONE” | “ERROR” | “WAITING” | “RUNNING”], “result”: string}
@app.route('/jobs/<job_id>', methods=['GET'])
def searchJob(job_id):
	try:
		int(job_id)	
		if int(job_id) <= 0:
			return("jobID precisa ser maior que 0.")
	except:
		return("jobID precisa ser número inteiro.")
	if request.method == "GET":
		ms = mysql.connection.cursor()
		ms.execute("SELECT * FROM Jobs WHERE jobId=%s;", (job_id))
		jobs = ms.fetchall()
		#print(jobs)
		list_jobs = ""
		for job in jobs:
			list_jobs = list_jobs + "<br>" + "{" + '"job_id": {}, "uid": {}, "status": {}, "result": {}'.format(job[0], job[1], job[2], job[3]) + "}"
		ms.close()
		#return jsonify(list_jobs)
	#print(list_jobs)
	file = open("./templates/GET.html", "r")
	html = file.read()
	file.close()
	view = html.replace('***', list_jobs)
	view = view.replace("~", "")
	return view

#/users/<uid> - lista todos os jobs de um certo usuário.
#[ { “job_id”: int, “uid”: int, “status”: [“DONE” | “ERROR” | “WAITING” | “RUNNING”], “result”: string} ]
@app.route('/users/<uid>', methods=['GET'])
def searchUser(uid):
	try:
		int(uid)	
		if int(uid) <= 0:
			return("userID precisa ser maior que 0.")
	except:
		return("userID precisa ser número inteiro.")
	if request.method == "GET":
		ms = mysql.connection.cursor()
		ms.execute("SELECT * FROM Jobs WHERE uid=%s;", (uid))
		jobs = ms.fetchall()
		#print(jobs)
		list_jobs = ""
		for job in jobs:
			list_jobs = list_jobs + "<br>" + "{" + '"job_id": {}, "uid": {}, "status": {}, "result": {}'.format(job[0], job[1], job[2], job[3]) + "}"
		ms.close()
		#return jsonify(list_jobs)
	#print(list_jobs)
	file = open("./templates/GET.html", "r")
	html = file.read()
	file.close()
	view = html.replace('***', list_jobs)
	view = view.replace("~", "do usuário {}".format(uid))
	return view


app.run(host="0.0.0.0")


'''
@app.route('/jobs/', methods = ['POST'])

def postJsonHandler(uid=None):
	file = open("ListaJobs.json", 'w+')
	with open('ListaJobs.json', 'r+') as f:
		lista = json.load(f)

	if request.is_json:
		content = request.get_json()
		##print (content)
		uid = int(content['uid'])
		code = str(content['code'])
		inputt = str(content['input'])
		f = open(code, "r")
		code = f.read()
		codigo = urllib.parse.urlencode({"code": code})
		print(code)
		print(codigo[5:])
		print(urllib.parse.unquote(codigo[5:]))
		response = client.invoke(
				FunctionName='meulambda',
				InvocationType='RequestResponse',
				Payload=bytes(json.dumps({"input":inputt, "code": code}), "utf-8")
			)
		retorno = {"job_id": uid}
		#[ {“result”: string} ]
		job_id = len(lista)
		lista.append({"job_id": job_id, "uid": uid, "status": "DONE", "result": inputt})
		print(lista)
		json.dump(lista, file)
		#print(response)
		data = response['Payload'].read()
		print(int(data.decode("utf-8")))
		return(jsonify(retorno))
		#uid.bulk_insert(request.json)
		#return 'Sucesso ao postar o JSON! :D\n'
	else:
		return("Error, the POST method only works with JSON inputs")

	lista = []
	if request.is_json:
		conteudo = request.get_json()
		for content in conteudo:
			idd = int(content['job_id'])
			uid = int(content['uid'])
			status = str(content['status'])
			result =  str(content['result'])
			retorno = {"job_id": idd, "uid": uid, "status": status, "result": result}
			lista.append(retorno)

		return(jsonify(lista))
	'''