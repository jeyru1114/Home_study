import random

import sympy as sp
from flask import Flask, render_template, request, jsonify
import matplotlib.pyplot as plt
import numpy as np
import base64
import itertools
import  re
import os

app = Flask(__name__)

def find_extract_alphabet(expression):
    # 정규 표현식을 사용하여 영문자(소문자 및 대문자) 추출
    variables = re.findall(r'[a-zA-Z]+', expression)
    print('정규 표현식')
    # 중복된 문자 제거
    funcs = ["sin", "cos", "exp", "tan"]  # 함수 목록
    try:
        filtered_variables = [variable for variable in variables if variable not in funcs]
    except:
        return [False,expression] #상수
    unique_variables = list(set(filtered_variables))
    return [True,unique_variables]

def partial_derivative_variables(expression, *vars):
    if not vars:
        return expression

    var = vars[0]
    rest_vars = vars[1:]

    derivative = sp.diff(expression, var)

    if rest_vars:
        return partial_derivative_variables(derivative, *rest_vars)
    else:
        return derivative

def check_part_same(derivative , fixed_variable):
    all_same = all(char in str(derivative) for char in fixed_variable)
    if  all_same:
        return True
    else : return  False

@app.route('/')
def index():
    return render_template('2.html')

@app.route('/sympy', methods=['POST'])
def calculate():
    data = request.get_json()
    # Convert the expression to SymPy symbol
    expression = data['expression']
    partial_derivative_variables=''
    output_variable=''
    try:
        partial_derivative_variables = data['partial_derivative_variable'].split(',')
    except Exception:
        jsonify({'result': '죄송합니다 제가 실력이 부족해서 그런 수식은 지원하지 못합니다 ','error':'e'})
    try:
        output_variable = data['outputVariable']
    except Exception:
        jsonify({'result': '죄송합니다  출력할 변수가 없어요 ', 'error': 'e'})
    input_variable = data['input']
    print('1) ', '수식:', expression, '미분하려는 변수', partial_derivative_variables, '출력하려는 변수', output_variable,'미분하려는 변수와 출력하려는 변수를 제외한 나머지 값을 일정한 값으로 지정',input_variable)

    # 제거할 함수 이름 리스트
    functions_to_remove = ['cos', 'sin', 'tan', 'exp']
    # 함수 이름을 제외한 영문자 변수 추출을 위한 정규 표현식 패턴
    pattern = r'\b[a-zA-Z]+\b'

    # 정규 표현식을 사용하여 영문자 변수 추출 (함수 이름을 제외)
    variables = re.findall(pattern, expression)
    # 중복 제거 및 함수 이름 제거
    filtered_variables = list(set(variables) - set(functions_to_remove))

    print("2) 수식에 포함된 문자:", filtered_variables)

    fixed_variable = set(filtered_variables)- set(partial_derivative_variables)- set(output_variable)
    print("3) 수식에서 편미분할 변수와 출력할 변수 제거:", fixed_variable)

    try:
        
        derivative = sp.diff(expression, *partial_derivative_variables)
    except Exception:
        return jsonify({'result': '미분 오류','error':'미분오류'})
    try:
        derivative = int(derivative)
        print('ok',derivative)
        return jsonify({'result': derivative})
    except TypeError:
        is_same  = check_part_same(derivative,fixed_variable)
        if is_same:
            print('all same', derivative, 'fixed_variable',fixed_variable)
        else:
            print('any same', derivative, 'fixed_variable',fixed_variable)

    # 문자열에 문자가 포함되어 있는지 확인
    is_constant , variables=  find_extract_alphabet(str(derivative))
    found_characters=set(variables)
    print('4) 검색된 문자', found_characters)
    sub_diff = found_characters - set(output_variable)
    print('5) 검색된 문자에서 출력할 변수 제외', sub_diff)

    # 문자열을 숫자로 변환하여 딕셔너리 생성
    substitution_dict = {key: int(value) for item in input_variable for key, value in item.items() if
                         key in sub_diff}
    print('6) 수식에 있는 변수에 값을 대입하기 위한 dictionary ', substitution_dict)
    # SymPy 심볼에 값을 대입
    substituted_expr = derivative.subs(substitution_dict)
    print('7) 수식에 있는 변수에 값을 대입한 결과 ', substituted_expr)

    # 변수 추출
    is_constant , extracted_alphabet = find_extract_alphabet(str(substituted_expr))
    print('8) 수식에서 변수 추출', extracted_alphabet)
    diff_sub = set(extracted_alphabet) - set(output_variable)
    print('9) 미분한 결과의 수식의 변수에서 출력하려는 변수를 제외한 차집합  ', diff_sub)
    # 변수를 랜덤한 값으로 변경(편미분한 변수가 있을 경우 값을 랜덤한 갋으로 대입)
    #원래는  input  태그의 type=range 하여 선택할수 있도록 해야 하는데 너무 선택해야 하는 종류가 많아서 강제로 랜덤값 대입
    for variable in diff_sub:
        random_value = random.uniform(0, 10)  # 0에서 10 사이의 랜덤한 숫자 생성
        substitution_dict[variable] = random_value
    print('10) ', substitution_dict)
    # SymPy 식에 변수 대입
    substituted_expr = substituted_expr.subs(substitution_dict)
    print('11) 변수에 랜덤한 값을 대입한 결과  ', substituted_expr)
    is_constant, final_retured_data = find_extract_alphabet(str(substituted_expr))
    if final_retured_data:
        sp.symbols(*final_retured_data)
    print('12) sympy 심볼 변수 ', final_retured_data) #final_retured_data 를 풀어헤친후 가변 변수 전달
    values = np.linspace(0, 10, 100)  # 출력 변수  값 생성
    if len(final_retured_data) !=0 :
        # SymPy 식을 NumPy 함수로 변환
        func = sp.lambdify(sp.symbols(*final_retured_data), substituted_expr, 'numpy')
        # 주어진 식에 values  값을 적용하여 결과 계산
        result = func(values)
        plt.plot(values, result)
    # 그래프 그리기
    else : #수식에 변수가 없을 경우 상수 함수
        # 상수 함수 계산
        print('13)  상수 함수  ', substituted_expr)
        constant_function = np.full_like(values, substituted_expr)

        # 그래프 그리기
        plt.plot(values, constant_function, label=f'y = {substituted_expr}')
    directory= 'static'
    filename= 'latex_derivative_plot.png'
    img_path = directory+ '/'+ filename # 이미지 파일 경로 (static 폴더에 저장)
    # 파일이 존재하는 경우 삭제
    if os.path.exists(img_path):
        #print('파일 삭제1) ')
        os.remove(img_path)
        #print('파일 삭제2) ')
        plt.savefig(img_path, format='png')
        # 이미지를 Base64로 인코딩
        with open(img_path, 'rb') as img_file:
            img_data = base64.b64encode(img_file.read()).decode('utf-8')
        return jsonify({'image': img_data})

@app.route('/plot', methods=['POST'])
def plot_equation():
    img_tag = 'static/latex_derivative_plot.png'  # 이미지 파일 경로 (static 폴더에 저장)
    # 이미지를 Base64로 인코딩
    with open(img_tag, 'rb') as img_file:
        img_data = base64.b64encode(img_file.read()).decode('utf-8')
    return jsonify({'image': img_data})

if __name__ == '__main__':
    app.run(debug=True)
