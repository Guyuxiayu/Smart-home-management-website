from flask import Flask, render_template, request, flash
from data import user_list, device_list

app = Flask(__name__)
app.secret_key = '123456'

@app.route('/')
def hello_world():
    return render_template('login.html')
xss_payload=""

@app.route('/login', methods=["GET", "POST"])
def login():
    global xss_payload
    error_message = ''
    username = request.form.get('username', '')
    password = request.form.get('password', '')

    if request.args.get('xss', '')!=None and request.args.get('xss', '')!="":
        xss_payload = request.args.get('xss', '') #获取URL中的恶意脚本
        print(f"Received XSS payload: {xss_payload}")

    # 添加一个标记来指示是否登录成功
    login_successful = False

    if request.method == 'POST':
        # 模拟的用户验证逻辑
        for user in user_list:
            if username == user['username'] and password == user['password']:
                login_successful = True  # 标记登录成功
                break
        if not login_successful:
            error_message = 'Incorrect username or password'

    # 根据登录成功与否，决定渲染哪个模板
    if login_successful:
        return render_template('admin.html',username=username, password=password, device_list=device_list, xss_payload=xss_payload)
    else:
        return render_template('login.html', error_message=error_message, xss_payload=xss_payload, username=username)

'''
@app.route('/login', methods=["POST"])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    user_found = False
    password_correct = False
    for user in user_list:
        if username == user['username']:
            user_found = True
            if password == user['password']:
                password_correct = True
                break
    if not user_found:
        flash('Incorrect username', 'error')
        return render_template('login.html', error_message=f"Incorrect username: {username}", username=username)
    elif not password_correct:
        flash('Incorrect password', 'error')
        return render_template('login.html', error_message=f"Incorrect password for user: {username}", username=username)
    if user_found and password_correct:
        return render_template('admin.html', device_list=device_list)
    else:
        return render_template('login.html', username=username)
'''

@app.route('/admin')
def admin():
    return render_template('admin.html', device_list=device_list)

@app.route('/search')
def search():
    search_query = request.args.get('search', '').lower()
    filtered_devices = [device for device in device_list if search_query in device['DeviceName'].lower()]

    reflected_query = request.args.get('search', '')

    return render_template('admin.html', device_list=filtered_devices, reflected_query=reflected_query)


@app.route('/delete/<ID>')
def delete(ID):
    for device in device_list:
        if device['ID'] == ID:
            device_list.remove(device)
    return render_template('admin.html', device_list=device_list)


@app.route('/change/<ID>')
def change(ID):
    for device in device_list:
        if device['ID'] == ID:
            return render_template('change.html', user=device)
    return render_template('admin.html', device_list=device_list)


@app.route('/changed/<ID>', methods=["POST"])
def changed(ID):
    for device in device_list:
        if device['ID'] == ID:
            device['ID'] = request.form.get('ID')
            device['DeviceName'] = request.form.get('DeviceName')
            device['DateAdded'] = request.form.get('DateAdded')

    return render_template('admin.html', device_list=device_list)


if __name__ == '__main__':
    app.run()
