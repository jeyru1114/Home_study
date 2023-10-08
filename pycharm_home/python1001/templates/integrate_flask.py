# app.py
from flask import Flask, render_template, request, jsonify


# SymPy의 integrate()함수
import sympy as sp

app = Flask(__name__)

def sympy_integrate(f, a,b):
    x = sp.Symbol('x')
    result = sp.integrate(f(x),(x,a,b)) # cos(x)함수를 0 ~ pi/2 범위
    return result

def limit_of_sum(f, a, b, n=10000): #첫번째(함수)  두번째,세번째(구간),  네번째(몇개로 분할)
    delta_x = (b - a) / n
    result = 0.0

    for k in range(1, n):
        x_k = a + k * delta_x  #x_k ,k번째 datq
        result += f(x_k) #함수값을 누적한후  

    result *= delta_x #누적된 함수 값에 delta_x(직사각형의 밑변) 을 곱한 후 결과 반환
    return result

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_message', methods=['POST'])
def get_message():
    data = request.get_json()
    print(data)
    f= data['f']
    a= int(data['a'])
    b = int( data['b'])
    function_string = "lambda x: " +f   # 예: 이 문자열은 입력을 받아 두 배로 만드는 람다 함수입니다.
    f_evaled = eval(function_string)
    result = limit_of_sum(f_evaled , a, b)
    result_sympy = sympy_integrate(f_evaled , a, b)
    print(result, result_sympy)
    return jsonify({'result': str(result), 'result_sympy': str(result_sympy)})

if __name__ == '__main__':
    app.run(debug=True)
