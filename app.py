from flask import Flask,render_template,request,url_for,redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////cp.db'
db = SQLAlchemy(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/newuser")
def newuser():
    return render_template("new_user.html")

@app.route("/adduser",methods=["POST"])
def adduser():
    username = request.form.get("username")
    password = request.form.get("password")

    new_user = Users(username=username,password=password)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    return render_template("index.html")

@app.route("/login",methods=["GET","POST"])
def login():
    
    username = request.args.get("username")
    password = request.args.get("password")
    print(username)
    print(password)
    user = Users.query.filter(Users.username==username,Users.password==password).first()
    
    if user:
        categories = Category.query.all()
        return render_template("category1.html",categories=categories,username=username)
    else:
        return render_template("wrong.html")

@app.route("/subcategory/<string:id>/<string:name>")
def subcategory(id,name):

    products = Products.query.filter(Products.category_id==id).all()
    categories = Category.query.all()
    return render_template("subcategory.html",products=products,username=name,id=id,categories=categories)

@app.route("/category/<string:username>")
def category(username):

    categories = Category.query.all()

    return render_template("category.html",categories=categories,username=username)

@app.route("/home/<string:username>")
def home(username):

    categories = Category.query.all()

    return render_template("category1.html",categories=categories,username=username)


@app.route("/add/<string:username>",methods=["GET","POST"])
def add(username):
    if Users.query.filter(Users.username==username).first():

        category = request.args.get("category")
              
        if not(category is None):
                
            new_cat = Category()
            new_cat.category=category
            db.session.add(new_cat)
            db.session.commit()
            
            categories = Category.query.all()

            return render_template("category.html",categories=categories,username=username)

    else:
        return redirect(url_for("index"))

@app.route("/addsub/<string:username>/<string:id>",methods=["GET","POST"])
def addsub(username,id):
    if Users.query.filter(Users.username==username).first():

        subcategory = request.args.get("subcategory")
              
        if not(subcategory is None):
                
            new_sub = Products()
            new_sub.name=subcategory
            new_sub.category_id=id
            db.session.add(new_sub)
            db.session.commit()
            
            products = Products.query.filter(Products.category_id==id).all()
            categories = Category.query.all()
            return render_template("subcategory.html",products=products,username=username,id=id,categories=categories)

    else:
        return redirect(url_for("index"))


@app.route("/delete/<string:id>/<string:name>/<string:username>")
def delete(id,name,username):
    categories = Category.query.all()
    
    if name=="category":
        cat = Category.query.filter(Category.id==id).first()
        db.session.delete(cat)
        db.session.commit()
        
        return render_template("category.html",categories=categories,username=username)
    
    else:
        sub = Products.query.filter(Products.id==id).first()
        category_id=sub.category_id
        db.session.delete(sub)
        db.session.commit()
        products = Products.query.filter(Products.category_id==category_id).all()
        return render_template("subcategory.html",products=products,username=username,id=category_id,categories=categories)

@app.route("/update/<string:id>/<string:name>/<string:username>")
def update(id,name,username):
    
    categories = Category.query.all()
    
    if name=="category":
        category = request.args.get("category") 
        cat = Category.query.filter(Category.id==id).first()
        cat.category=category
        db.session.commit()
        
        return render_template("category.html",categories=categories,username=username)
    
    else:
        subcategory = request.args.get("subcategory") 
        sub = Products.query.filter(Products.id==id).first()
        category_id=sub.category_id
        sub.name = subcategory
        db.session.commit()
        products = Products.query.filter(Products.category_id==category_id).all()

        return render_template("subcategory.html",products=products,username=username,categories=categories)


class Category(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    category = db.Column(db.String(80))


class Users(db.Model):
    username = db.Column(db.String(80),primary_key=True)
    password = db.Column(db.Integer)


class Products(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id', ondelete='CASCADE'))
    name = db.Column(db.String(80))


if __name__ == "__main__":
    app.run(debug=True)