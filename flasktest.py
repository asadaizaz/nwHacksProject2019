from flask import Flask, render_template,request,redirect
import stats
import parser
import grapher




app = Flask(__name__)

@app.route("/")
@app.route("/home")

def hello():
    return render_template('home.html')



@app.route("/about")
def about():
    return "<h1> About Page </h1>"

@app.route('/', methods=['GET','POST'])
def send():
     if request.method == 'POST':
         stats.loadData()
         grapher.heatMap()
         return redirect('/dashboard')

@app.route('/dashboard')
def dash():
    return render_template('index.html')
@app.route('/heatmap')
def heatmap():
    return render_template('heatmap.html')






if __name__ == "__main__":
    app.run(debug=True)
