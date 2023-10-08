import sympy as sp
import matplotlib.pyplot as plt
import numpy as np
import base64
from flask import Flask, render_template, request, jsonify
import  itertools

app = Flask(__name__)


def remove_zero_values(lst):
    non_zero_results = []
    for dict1 in lst:
        non_zero_results.append([{key: value} for key, value in dict1.items() if value != 0])
    return non_zero_results


def derivative_partial(f, variables):
    list_partial = []
    variables_list = variables.split(" ")

    for i in range(1, len(variables_list) + 1):
        combinations = itertools.combinations(variables_list, i)
        for combo in combinations:
            partial_derivative = f
            for var in combo:
                partial_derivative = sp.diff(partial_derivative, var)
            list_partial.append({','.join(combo): partial_derivative})
    filtered_list = remove_zero_values(list_partial)
    merged_dict = {}
    try:
        for item in filtered_list:
            for sub_item in item:
                merged_dict.update(sub_item)
    except ValueError:
        print('ValueError 발생: 오류')
    return merged_dict


@app.route('/')
def index():
    return render_template('2.html')


@app.route('/sympy', methods=['POST'])
def calculate():
    data = request.get_json()
    expression = sp.sympify(data['expression'])
    partial_derivative_variables = data['partial_derivative_variable'].split(',')
    output_variable = sp.symbols(data['outputVariable'])
    input =data['input']
    print('1) ',expression , partial_derivative_variables ,output_variable ,input )
    input_values = [sp.sympify(value) for value in input]
    print('2) ', input_values)
    substitution_dict = {sp.symbols(partial_derivative_variables[i]): input_values[i] for i in
                         range(len(partial_derivative_variables))}
    print('3) ', substitution_dict)
    expression_with_values = expression.subs(substitution_dict)
    print('4) ', expression_with_values)
    derivative = sp.diff(expression_with_values, output_variable)
    print('5) ', derivative)

    # 함수 파싱
    expr = derivative

    # 함수에서 사용된 변수 추출 (영문자)
    # 함수에서 사용된 변수 추출 (영문자)
    variables = [str(symbol) for symbol in expr.free_symbols if isinstance(symbol, sp.Symbol) and str(symbol).isalpha()]
    print('6) ', variables)

    # 변수 중복 제거
    unique_variables = list(set(variables))
    print('7) ', unique_variables)

    # 두 번째 변수 선택 (첫 번째 변수는 미분 대상)
    variable_to_replace = unique_variables[1]
    print('8) ', variable_to_replace)

    # 선택한 변수를 특정 숫자로 대체 (예시: 5)
    substitution_dict = {sp.symbols(variable_to_replace): 5}
    print('9) ', substitution_dict)
    derivative_with_value = derivative.subs(substitution_dict)
    print('10) ', derivative_with_value)

    # 남은 변수 선택
    remaining_variable = unique_variables[0]
    print('11) ', remaining_variable)

    # 변수 'q'의 범위 설정 (예시 범위: 0에서 10까지)
    q_values = np.linspace(0, 10, 100)

    # 함수를 계산하고 결과 저장
    results = [derivative_with_value.subs({sp.symbols(remaining_variable): q}).evalf() for q in q_values]
    print('12) ', results)
    # 그래프 그리기
    plt.plot(q_values, results)
    plt.xlabel(remaining_variable)
    plt.ylabel('Function Value')
    plt.title(f'Graph of {derivative_with_value} with respect to {remaining_variable}')
    img_path = 'static/latex_derivative_plot.png'
    plt.savefig(img_path, format='png')
    plt.close()

    return jsonify({'result': 50})


@app.route('/plot', methods=['POST'])
def plot_equation():
    img_tag = 'static/latex_derivative_plot.png'
    with open(img_tag, 'rb') as img_file:
        img_data = base64.b64encode(img_file.read()).decode('utf-8')
    return jsonify({'image': img_data})


if __name__ == '__main__':
    app.run(debug=True)
