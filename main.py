from flask import Flask, render_template, request, redirect, url_for
import random
import json
import math

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/encrypt', methods=['GET', 'POST'])
def encrypt():
    num1 = 0
    num2 = 0
    num3 = 0
    form = request.form
    text = ""
    reduce_num = []
    enc_str = ""
    successful = False
    characters = [' ', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                  't',
                  'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
                  'O',
                  'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'X', 'Y', 'Z', ';', ',', '"', '@', '?', '{', '}', "'", '(', ')',
                  '1',
                  '2', '3', '4', '5', '6', '7', '8', '9', '#']
    try:
        num1 = int(request.form['num1'])
        num2 = int(request.form['num2'])
        num3 = int(request.form['num3'])
        if num3 == 0 or num2 == 0 or num1 == 0:
            return render_template('encrypt.html', enc_str="The numbers cannot be 0")
        text = str(request.form['text'])
    except:
        return render_template('encrypt.html', enc_str="")
    reduce_num = []
    enc_str = ""
    for x in text:
        index = characters.index(x)
        if index > 36:
            rand_int = int(
                (-1) * random.randint(0, 37) * abs(math.sin((num1 + num2 - num3) * num1 / num3)))
        else:
            rand_int = int(random.randint(0, 37) * abs(math.sin((num1 + num2 - num3) * num1 / num3)))
        reduce_num.append(rand_int)
        x = characters[index + rand_int]
        enc_str += x
    key = ""
    for x in range(10):
        key += characters[random.randint(0, 71)]

    output_key = key
    key = str(num1) + str(num2) + str(num1 + num2) + key + str(num3) + str(num1 + num2 + num3)

    data = {key: [enc_str, reduce_num]}
    with open('static/data.txt', 'a') as data_file:
        if enc_str == "None":
            return render_template('encrypt.html', enc_str="")
        else:
            data_file.write(json.dumps(data))
            data_file.write("\n")
            successful = True
            return render_template('encrypt.html', enc_str=enc_str, successful=successful, key=key, output_key=output_key)


@app.route('/decrypt', methods=['GET', 'POST'])
def decrypt():
    characters = [' ', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                  't',
                  'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
                  'O',
                  'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'X', 'Y', 'Z', ';', ',', '"', '@', '?', '{', '}', "'", '(', ')',
                  '1',
                  '2', '3', '4', '5', '6', '7', '8', '9', '#']
    num1 = int(request.form.get('num1', False))
    num2 = int(request.form.get('num2', False))
    num3 = int(request.form.get('num3', False))
    key = str(request.form.get('key', False))
    key = str(num1) + str(num2) + str(num1 + num2) + key + str(num3) + str(num1 + num2 + num3)
    text = str(request.form.get('text', False))
    reduce_num = []
    found = False
    started = False
    with open('static/data.txt', 'r') as data_file:
        data = data_file.readlines()
        for x in data:
            if key in x:
                reduce_num = json.loads(x)[key][1]
                break

    decr_str = ""
    j = 0
    if len(reduce_num) == 0:
        return render_template('decrypt.html', text=text, decr_str="")
    else:
        for x in text:
            decr_str += characters[characters.index(x) - reduce_num[j]]
            j += 1
    return render_template('decrypt.html', text=text, decr_str=decr_str)


if __name__ == '__main__':
    app.run(debug=True)
