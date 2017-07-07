from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import tushare as ts

def transfer(x):
    ntype = ''
    if x >= 9.9:
        ntype = '10'
    elif x >= 5:
        ntype = '5-10'
    elif x >= 0:
        ntype = '0-5'
    elif x >= -5:
        ntype = '-5- 0'
    elif x > -9.9:
        ntype = '-10- -5'
    else:
        ntype = '-10'
    return ntype

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.debug = True
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('socketio.html')



@socketio.on('client_event')
def client_msg(msg):
    df = ts.get_today_all()
    df['c'] = df.apply(lambda x: transfer(x['changepercent']), axis=1)
    cnt = df.groupby(df['c']).size().astype(float)
    labels = list(cnt.index)
    values = list(cnt)
    l=["dsfdsfds","llalala","ssdsds","1234","3cddddd","dfddfdf","fdfdfdfdfdfdfd"]
    v=[20,30,49,37,2,9,8]
    j={'sum':labels,'data':values}
    emit('server_response',j )


@socketio.on('connect_event')
def connected_msg(msg):
    emit('server_response', {'data': msg['data']})


if __name__ == '__main__':
    socketio.run(app)
