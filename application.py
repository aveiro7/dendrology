from flask import Flask, render_template

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def show_tree():
    return render_template('show_tree.html')

@app.route('/register')
def register():
    return "register"

@app.route('/login')
def login():
    return "login"

@app.route('/logout')
def logout():
    return "logout"

if __name__ == "__main__":
    app.run()