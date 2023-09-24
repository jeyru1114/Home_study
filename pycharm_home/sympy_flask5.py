from flask import Flask, request, render_template, jsonify
import random
import sympy as sp
import matplotlib.pyplot as plt
app = Flask(__name__)
from  sympy import *
import base64
import  numpy as np
# 가능한 함수 리스트
functions = ['x', 'x**2','x**3','x**4', 'cos(x)', 'sin(x)', 'exp(x)', 'cos(2*x)', 'sin(2*x)','cos(3*x)','sin(3*x**2)']

# 랜덤한 수식 생성 함수
def generate_random_expression(depth=3):
    if depth == 0:
        return random.choice(functions)
    else:
        function = random.choice(functions)
        if function == 'x':
            return 'x*' + generate_random_expression(depth - 1)
        elif 'x**' in function:
            n = random.randint(2, 8)  # 숫자 범위를 원하는 대로 조절하세요
            return function.replace('**', f'^{n}')
        elif 'x' in function:
            return function +'*'+ generate_random_expression(depth - 1)
        else:
            return function + '*(' + generate_random_expression(depth - 1) + ')*'


# 랜덤 수식 생성 및 파싱 예제
def generate_random_equation():
    num_terms = random.randint(1, 5)  # 랜덤한 항의 개수
    equation = ''
    for _ in range(num_terms):
        term = generate_random_expression(random.randint(1, 3))
        coefficient = random.randint(1, 10)
        equation += f'{coefficient}*{term} + '

    equation = equation.rstrip(' + ')
    return equation

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

    img_path = 'static/latex_derivative_plot.png'  # 이미지 파일 경로 (static 폴더에 저장)
    plt.savefig(img_path, format='png')
    plt.close()  # 그래프 창 닫기

    return img_path  # 이미지 파일 경로 반환

# 루트 경로에 대한 렌더링
@app.route('/')
def index():
    return render_template('index5.html')

@app.route('/', methods=['GET', 'POST'])
def chain_rule_calculator():

        try:
            # 입력된 함수와 변수로 심볼과 수식을 생성
            # 랜덤 수식 생성 및 파싱
            random_equation = generate_random_equation()

            print("파싱된 수식:", random_equation)
            x = sp.symbols('x')
            expr = sp.sympify(random_equation)
            print('expr;',expr)
            save_equation_plot(expr)
            # 도함수를 LaTeX 형식으로 변환
            org_latex = sp.latex(expr)
            derivative_latex = sp.latex(diff(expr,x))

            result_org = f"\\({org_latex}\\)"
            result_dir = f"\\({derivative_latex}\\)"

        except Exception as e:
            result_dir = f"오류: {str(e)}"

        return jsonify({'result_dir': result_dir,'result_org':result_org})
@app.route('/plot', methods=['POST'])
def plot_equation():

    img_tag = 'static/latex_derivative_plot.png'  # 이미지 파일 경로 (static 폴더에 저장)
    # 이미지를 Base64로 인코딩
    with open(img_tag, 'rb') as img_file:
        img_data = base64.b64encode(img_file.read()).decode('utf-8')
    return jsonify({'image': img_data})
if __name__ == '__main__':
    app.run(debug=True)
