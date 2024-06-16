import parso
from flask import Flask, render_template, request, jsonify

import subprocess
import time
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_text():
    data = request.json  # Get the JSON data from the request
    text = data['text']  # Extract the text from the JSON data
    language = data['language']  # Extract the language from the JSON data
    
    write_to_file("input.txt",str(text))

    # Example: Return a response with the processed text
    if language=='C':
        run_c_program("/Users/mcittkmims/Documents/SDA/Individual_Work/C_detection/c_comparasion")
    elif language=='Python':
        python_split()
        run_c_program("/Users/mcittkmims/Documents/SDA/Individual_Work/Py_detection/py_comparasion")

    elif language=='JavaScript':
        temp_file="/Users/mcittkmims/Documents/SDA/Individual_Work/Js_detection/temp.txt"
        write_dict_to_binary_file(temp_file,text)
        print(text)
        run_c_program("/Users/mcittkmims/Documents/SDA/Individual_Work/Py_detection/js_comparasion")
    
    score=read_from_file("score.txt")
    
    time.sleep(2)
    return jsonify({'processed_text': score})

def run_c_program(command):


    try:
        # Run the command without capturing output
        subprocess.run(command, shell=True)
        print("C program executed successfully.")
    except subprocess.CalledProcessError as e:
        # Handle any errors or exceptions
        print("Error:", e)

def write_to_file(filename, data):
    with open(filename, "w") as file:
        file.write(data)
        file.close()

def read_from_file(filename):
    with open(filename, "r") as file:
        data = file.read()
        file.close()
        return data

def extract_python_code(file_path):
    with open(file_path, 'r') as file:
        code = file.read()
    file.close()
    return code


def parse_python_code_with_comments(code):
    try:
        tree = parso.parse(code)
        return tree, None
    except Exception as e:
        return None, e

def extract_functions_and_classes(tree):
    classes = []
    functions = []

    for node in tree.children:
        if node.type == 'classdef':
            classes.append(node)
        elif node.type == 'funcdef':
            functions.append(node)

    return classes, functions

def extract_other_code(tree, classes, functions):
    other_code = []

    for node in tree.children:
        if node not in classes and node not in functions:
            other_code.append(node)

    # Concatenate the lines of code into a single string
    code_text = ''
    for node in other_code:
        code_text += node.get_code()
    
    return code_text.strip()

def main_function(file_path):
    # Example Python code with comments and invalid syntax
    code = extract_python_code(file_path)

    tree, error = parse_python_code_with_comments(code)
    if error:
        print("Error:", error)
    else:
        classes, functions = extract_functions_and_classes(tree)
        other_code = extract_other_code(tree, classes, functions)
        temp_file="/Users/mcittkmims/Documents/SDA/Individual_Work/Js_detection/temp.txt"
        write_string_to_binary_file(temp_file,classes,functions,other_code)


def write_string_to_binary_file(file_path, classes, functions, other_code):
    with open(file_path, 'wb') as file:
        for class_node in classes:
            text = class_node.get_code().strip()
            length = len(text) + 1
            file.write(length.to_bytes(4, byteorder='little'))
            file.write(text.encode('utf-8'))
            file.write(b'\0')
        for func_node in functions:
            text = func_node.get_code().strip()
            length = len(text) + 1
            file.write(length.to_bytes(4, byteorder='little'))
            file.write(text.encode('utf-8'))
            file.write(b'\0')
        
        text = other_code
        length = len(text) + 1
        file.write(length.to_bytes(4, byteorder='little'))
        file.write(text.encode('utf-8'))
        file.write(b'\0')
        file.close()
        

def python_split():
    file_path = "/Users/mcittkmims/Documents/SDA/Individual_Work/website/input.txt"  # Replace with the path to your text file containing Python code
    main_function(file_path)


def write_dict_to_binary_file(file_path, parsed_code):
    with open(file_path, 'wb') as file:
        for class_node in parsed_code['classes']:
            text = class_node
            length = len(text) + 1
            file.write(length.to_bytes(4, byteorder='little'))
            file.write(text.encode('utf-8'))
            file.write(b'\0')
        for func_node in parsed_code['functions']:
            text = func_node
            length = len(text) + 1
            file.write(length.to_bytes(4, byteorder='little'))
            file.write(text.encode('utf-8'))
            file.write(b'\0')
        
        text = parsed_code['otherCode']
        length = len(text) + 1
        file.write(length.to_bytes(4, byteorder='little'))
        file.write(text.encode('utf-8'))
        file.write(b'\0')
        file.close()


if __name__ == '__main__':
    app.run()

