from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# here we start organzing code for 

class Category(db.Model):
    c_id = db.Column(db.Integer(),primary_key=True)
    c_name = db.Column(db.String(),unique=True,nullable=False)
    c_products = db.relationship('Product',backref="p_category")

class Product(db.Model):
    p_id = db.Column(db.Integer(),primary_key=True)
    p_name = db.Column(db.String(),unique=True,nullable=False)
    p_quantity = db.Column(db.Integer(),nullable=False)
    p_expiry = db.Column(db.String())
    p_rate = db.Column(db.Integer(),nullable=False)
    p_unit = db.Column(db.Integer(),nullable=False)
    p_category_id =db.Column(db.Integer(),db.ForeignKey("category.c_id"),nullable=False)

class Cart(db.Model):
    c_id = db.Column(db.Integer(),primary_key=True)
    c_name=db.Column(db.String(),nullable=False)
    c_rate =db.Column(db.Integer(),nullable=False)
    c_quantity = db.Column(db.Integer(),nullable=False)
    c_totalprice = db.Column(db.Integer(),nullable=False)
    c_user = db.Column(db.Integer(),db.ForeignKey("user.id"), nullable=False)


# give product quantity max 
class User(db.Model):
    id = db.Column(db.Integer(),primary_key= True)
    username = db.Column(db.String(80),unique=True,nullable=False)
    password = db.Column(db.String(80),nullable=False)
    cart_item = db.relationship('Cart',backref="usr")

class Manager(db.Model):
    id =db.Column(db.Integer(),primary_key=True)
    managername= db.Column(db.String(80),unique=True,nullable=False)
    password = db.Column(db.String(80),nullable=False)

