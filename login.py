from flask import Flask, render_template,request,session,flash,jsonify,redirect


app = Flask(__name__)

@app.route('/')
def index():
	return render_template('form.html')

@app.route('/login', methods=['GET','POST'])
def login():
	if(request.method=="POST"):
		name = request.form['name']
		password = request.form['password']
		if(name=="rahul" and password=="sameer"):
			return jsonify({'success' : 'logged'})
	return jsonify({'error' : 'wrong pass!'})


if __name__ == '__main__':
	app.run(debug=True)