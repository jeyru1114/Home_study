import numpy as np
from flask import Flask, request, render_template, jsonify
import random
import sympy as sp
import matplotlib.pyplot as plt
from  sympy import *
import io
import base64

app = Flask(__name__)



# generalize_equation 함수를 정의합니다.
def generalize_equation(equation):
    # 'x^2'를 'x**2'로 변환
    #equation = equation.replace(r'(\d*)x\^2', r'\1*x**2', equation)
    equation = equation.replace('^', '**')  # '^'를 '**'로 변환
    # 'x'를 'x'로 변환
    equation = equation.replace('x', '*x')  # '^'를 '**'로 변환

    return equation


import sympy as sp

import sympy as sp
import numpy as np
import matplotlib.pyplot as plt


def find_minimum(equation):
    x = sp.symbols('x')
    equation_expr = sp.sympify(equation)
    derivative = sp.diff(equation_expr, x)
    minimum_points = sp.solve(derivative, x)

    if not minimum_points:
        return None

    minimum_values = [equation_expr.subs(x, min_point) for min_point in minimum_points]

    # 최소값 x 좌표와 해당하는 y 좌표를 튜플로 반환
    return list(zip(minimum_points, minimum_values))



# 랜덤 2차 방정식을 생성하는 함수
def generate_quadratic_equation():
    a = random.randint(1, 10)
    b = random.randint(1, 10)
    c = random.randint(1, 10)
    equation = f"{a}x^2 + {b}x + {c}"
    return equation
def root_solve_sympy(a, b ,c):
    str1=''
    a_str= str(a)
    b_str= str(b)
    c_str=str(c)
    str1+=a_str+'*x**2+'  +b_str + '*x+'+ c_str
    if b**2 - 4*a *c >=0: return solve(str1)
    else: return None

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

    minimum = find_minimum(equation_expr)
    if minimum:
        print(f"최소값: {minimum}")
    else:
        print("최소값이 없음")

    # 최소값 표시
    if minimum:
        for min_point in minimum:
            x_min, y_min = min_point
            plt.scatter([x_min], [y_min], color='red', label=f'Minimum ({x_min:.2f}, {y_min:.2f})')
            plt.annotate(f'Minimum: ({x_min:.2f}, {y_min:.2f})', (x_min, y_min), textcoords="offset points",
                         xytext=(0, 10),
                         ha='center', fontsize=10, color='red')

    plt.grid(True)
    # plt.legend()
    # plt.show()
    # 이미지를 파일로 저장
    img_path = 'static/equation_plot.png'  # 이미지 파일 경로 (static 폴더에 저장)
    plt.savefig(img_path, format='png')
    plt.close()  # 그래프 창 닫기

    return img_path  # 이미지 파일 경로 반환


@app.route('/', methods=['GET', 'POST'])
def index():
    equations = []
    if request.method == 'POST':
        num_equations = int(request.form['num_equations'])
        equations = [generate_quadratic_equation() for _ in range(num_equations)]
    return render_template('index.html', equations=equations)

@app.route('/plot', methods=['POST'])
def plot_equation():
    equation = request.form['equation']
    equation = generalize_equation(equation)
    print(equation)
    x = sp.symbols('x')
    equation_expr = sp.sympify(equation)

    img_tag = save_equation_plot(equation_expr)
    # 이미지를 Base64로 인코딩
    with open(img_tag, 'rb') as img_file:
        img_data = base64.b64encode(img_file.read()).decode('utf-8')
    return jsonify({'image': img_data})


if __name__ == '__main__':
    app.run(debug=True)
