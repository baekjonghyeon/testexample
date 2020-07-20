from flask import Flask, render_template

app = Flask(__name__,
            static_url_path='', 
            static_folder='static',
            template_folder='template')

@app.route('/')
def hello_world():
	return 'Hello World!'

if __name__=="__main__":
    app.run(host='0.0.0.0', port="80")