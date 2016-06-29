from flask import Flask, render_template

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def show_tree():
    return render_template('show_tree.html')

if __name__ == "__main__":
    app.run()