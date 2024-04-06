import pandas as pd
from flask import Flask, request, jsonify
import random


caminho_arquivo = './dataset.csv'
df = pd.read_csv(caminho_arquivo, delimiter=';')
df.set_index('CO_CURSO', inplace=True)
dataset = df.to_dict(orient='index')

app = Flask(__name__)


@app.get("/course")
def getCourses():
    return jsonify(dataset)

@app.get("/course/<int:id>")
def getCourse(id):
    try:
        if dataset[id]:
            return {"curso": dataset[id]}, 200
    except KeyError:
        return {"erro": "Curso nao encontrado"}, 404    

@app.post("/course")
def addCourse():
    if request.is_json:
        course = request.get_json()
        idNewCourse = random.randint(100000, 999999);
        while True:
            try:
                dataset[idNewCourse]
                idNewCourse = random.randint(100000, 999999)
            except KeyError:
                break
        dataset[idNewCourse] = course
        return {'id': idNewCourse}, 201
    return {"erro":"Formato deve ser JSON"}, 415

@app.put("/course/<int:id>")
def updateCourse(id):
    if request.is_json:
        try:
            dataset[id]
        except KeyError:
            return {"erro":"ID não encontrado"}, 415
        course = request.get_json()
        dataset[id].update(course)    
        return {"msg":"Sucesso", "course": dataset[id]}, 200
    return {"erro":"Formato deve ser JSON"}, 415

@app.delete("/course/<int:id>")
def deleteCourse(id):
    try:
        dataset[id]
    except KeyError:
        return {"erro":"ID não encontrado"}, 415
    del dataset[id]
    return {"msg": 'Sucesso!'}, 200




