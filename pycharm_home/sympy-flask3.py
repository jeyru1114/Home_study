from flask import Flask, render_template, request, jsonify
import sympy as sp
from  sympy import *
import  numpy as np
import matplotlib.pyplot as plt
import io
import base64
app = Flask(__name__)

    # 그래프를 이미지 파일로 저장하는 함수
def save_equation_plot(equation_expr):
    print('save: ' ,equation_expr)
    # 변수 및 수식을 정의합니다.
    x = sp.symbols('x')
    x_values = np.linspace(-10, 10, 400)  # x값 범위 설정
    y_values = [equation_expr.evalf(subs={x: x_val}) for x_val in x_values]
    derivative_values = [diff(equation_expr, x).evalf(subs={x: x_val}) for x_val in x_values]

    plt.plot(x_values, y_values, label='Equation')  # label을 설정하여 레이블을 지정
    plt.plot(x_values, derivative_values, label='Derivative')  # 미분 그래프 추가


    # plt.legend()
    # plt.show()
    # 이미지를 파일로 저장
    img_path = 'static/derivative_plot.png'  # 이미지 파일 경로 (static 폴더에 저장)
    plt.savefig(img_path, format='png')
    plt.close()  # 그래프 창 닫기

    return img_path  # 이미지 파일 경로 반환


@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        data = request.get_json()
        func1 = sp.sympify((data['func1']))
        func2 = sp.sympify((data['func2']))
        func3 = sp.sympify((data['func3']))

        # 두 함수의 곱 구하기
        product = func1 * func2 * func3

        # 곱의 미분 계산
        derivative = sp.diff(product)

        return jsonify({'result':str(derivative)})

    return render_template('index3.html')


# @app.route('/calculate_derivative', methods=['POST'])
# def calculate_derivative():
#     data = request.get_json()
#     func1 = sp.sympify(data['func1'])
#     func2 = sp.sympify(data['func2'])
#     func3 = sp.sympify(data['func3'])
#
#     # 두 함수의 곱 구하기
#     product = func1 * func2 *func3
#
#     # 곱의 미분 계산
#     derivative = sp.diff(product)
#
#     return jsonify({'result': str(derivative)})
@app.route('/plot', methods=['POST'])
def plot_equation():
    equation = request.form['equation']
    x = sp.symbols('x')
    equation_expr = sp.sympify(equation)

    # 그래프를 그립니다
    x_values = np.linspace(-10,10,400) #수정: numpy의 linspace사용
    y_values = [equation_expr.evalf(subs={x:x_val}) for x_val in x_values]
    #이미지를 저장
    img_tag = save_equation_plot(equation_expr)
    # 이미지를 Base64로 인코딩
    with open(img_tag, 'rb') as img_file:
        img_data = base64.b64encode(img_file.read()).decode('utf-8')
    return jsonify({'image': img_data})

if __name__ == '__main__':
    app.run(debug=True)
