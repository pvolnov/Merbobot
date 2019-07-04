import pickle

from flask import Flask, redirect

app = Flask(__name__)


@app.route('/')
def root():
    favorite_color = pickle.load(open("id.txt", "rb"))
    url=favorite_color['url']
    return redirect(url)

@app.route('/url/<path:url>')
def newurl(url):
    favorite_color = {"url": url}
    pickle.dump(favorite_color, open("id.txt", "wb"))
    return "URL UPDATE"

if __name__ == '__main__':
    favorite_color = {"url": "https://yandex.ru/"}
    pickle.dump(favorite_color, open("id.txt", "wb"))

    app.run(
        port=5050)#host='0.0.0.0'
