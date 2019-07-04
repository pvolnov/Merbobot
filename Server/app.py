from flask import Flask, send_from_directory, redirect, request, render_template, send_file
from supf import *
app = Flask(__name__)


@app.route('/')
def root():
    return render_template('index.html')

@app.route('/com',methods=['POST'])
def com():
    c=request.values

    if (c['action']=="reg_lot"):
        if len(Lotery.select().where(Lotery.ef_id==int(c['lid'])))>0:
            return "Вы уже зарегестрированы"
        try:
            Lotery(ef_id=int(c['lid']),name=c['name'],
                   secondname= c['secondname'],email=c['email'],phone=c['phone']).save()
            send_to(c['lid'],regtext)
            return "Вы зарегестрированы"
        except Exception as e:
            print(e)
            return "Error"

    if (c['action']=="new_mes"):
        new_mes(c['text'])

        return "Сообщения отправлены"

    if (c['action']=="new_shop"):
        new_shop(c['slat'],c['slon'],c['sname'])
        return "Магазин добавлен"

    if (c['action']=="new_quiz"):
        new_quiz(c['text'],c['qA']+';'+c['qB']+';'+c['qC']+';'+c['qD'])
        return "Вопорс добавлен"

    if (c['action']=="reddata"):
        st=0
        if(c['stut']=='good'):
            st=1
        if(c['stut']=='spam'):
            Dset.get(Dset.name == c['name']).delete_instance()
            return redirect('/datared')

        Dset.update({Dset.stutus:st}).where(Dset.name==c['name'])
        return redirect('/datared')

    if (c['action']=="del_quiz"):
        Quiz.get(Quiz.id==c['qid']).delete_instance()
        return redirect('/quizs')
    print(c)
    return redirect('/')

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

@app.route('/users/<id>')
def users(id):
    top=Users.select().order_by(Users.balance).limit(25)

    return render_template('user_page.html', top=top,id=id)

@app.route('/datared')
def datared():
    d=Dset.select().where(Dset.stutus==-1).limit(25)
    return render_template('datared.html',photos=d)


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('static/js', path)
@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('static/css', path)
@app.route('/res/<path:path>')
def send_res(path):
    return send_from_directory('../res/',path)

if __name__ == '__main__':
    app.run(host=lhost,port=port)
