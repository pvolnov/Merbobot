from flask import Flask, send_from_directory, redirect, request, render_template
from Server.supf import *
app = Flask(__name__)


@app.route('/')
def root():
    return render_template('index.html')



@app.route('/com',methods=['POST'])
def com():
    c=request.values


    if (c['action']=="new_mes"):
        new_mes(c['text'])

        return "Сообщения отправлены"

    if (c['action']=="new_shop"):
        new_shop(c['slat'],c['slon'].c['sname'])
        return "Магазин добавлен"

    if (c['action']=="new_quiz"):
        new_quiz(c['text'],c['qA']+';'+c['qB']+';'+c['qC']+';'+c['qD'])
        return "Вопорс добавлен"

    if (c['action']=="del_quiz"):
        Quiz.get(Quiz.id==c['qid']).delete_instance()
        return redirect('/quizs')

    return "not correct"

@app.route('/shops')
def shops():
    data=[]
    for s in Shops.select():
        blocs = []

        for i in Info.select().where(Info.shopname==s.name):

            d={'name':str(i.datatime),
                'res':i.status
                }

            blocs.append(d)
        print(blocs)

        dd={
            'name':s.name,
            'r':blocs,
            'id':s.id
        }
        data.append(dd)

    return render_template('shops.html',data=data)

@app.route('/quizs')
def quizs():
    data=[]
    for q in Quiz.select():
        blocs=[]
        for i in range(4):
            d={'name':q.answers.split(';')[i],
            'res':q.results.split(';')[i]
               }
            blocs.append(d)
        dd={
            'name':q.text,
            'r':blocs,
            'id':q.id
        }
        data.append(dd)


    return render_template('quizs.html',data=data)


@app.route('/', methods=['POST'])
def upload_view():
    file =  request.files['TEST']
    print(file)
    #file.save('ff.txt')
    pass




@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('static/js', path)
@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('static/css', path)



if __name__ == '__main__':
    app.run()
