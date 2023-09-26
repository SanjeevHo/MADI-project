from flask import Flask , render_template ,request,redirect,flash,session
from products import *
import custom_filters


app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key_is_my_number'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Product.sqlite3"
db.init_app(app)
app.app_context().push()
app.jinja_env.filters['limit'] = custom_filters.limit
 
# ======= Controller ===============


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/loginmanager',methods=['GET','POST'])
def Managerlogin():
    if request.method == 'POST':
        managername = request.form['managername']
        password    = request.form['password']
        manager = Manager.query.filter_by(managername=managername,password=password).first()
        if manager:
            return redirect('/Manager')
        else:
            flash("error,Invalid username or password ,Please provide the correct username and Password")
    return render_template('Managerlogin.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username= request.form['username']
        password= request.form['password']
        user = User.query.filter_by(username=username,password=password).first()
        if user:
            flash(f'User Login: Username: {username}, Password: {password}', 'success')
            session['user_id']=user.id
            return redirect('/MyShop')
        else:
            flash('Invalid username or password. Please try again.', 'error')
    return render_template('login.html')

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        existing_user = User.query.filter_by(username=username,password=password).first()
        if existing_user:
            flash('User Already Present , Please choose different username')
        else:
            new_user = User(username=username,password=password)
            db.session.add(new_user)
            db.session.commit()
            flash("user account created succesfully!You can now log in ")
            return ('/login')
    return render_template('register.html')

@app.route('/Manager',methods=['GET','POST'])
def Manager_():
    catg = Category.query.all()
    return render_template('manager.html',catg=catg)

@app.route('/add_category',methods=['GET','POST'])
def Add_Category():
    if request.method=='POST':
        try:
            catg_name =str( request.form.get('Category_name'))
            newvalue= Category(c_name=catg_name)
            db.session.add(newvalue)
            db.session.commit()
            return redirect('/Manager')
        except:
            return render_template('error.html')
    if request.method=='GET':
        return render_template('Add_Category.html')

@app.route('/Category_delete/<int:id>',methods=['GET','POST'])
def Manager_delete_product(id):
    Category_delete = Category.query.filter_by(c_id=id).first()
    Product_delete = Category_delete.c_products
    print(Product_delete,'hello')
    for product in Product_delete:
        print(product,Product_delete)
        db.session.delete(product)
        db.session.commit()
    db.session.delete(Category_delete)
    db.session.commit()
    return redirect('/Manager')

@app.route('/Category_update/<int:id>',methods=['GET','POST'])
def Category_up(id):
   Category_obj = Category.query.filter_by(c_id=id).first()
   if request.method == 'POST':
       try :
        update_name = str(request.form.get("updated_name"))
        Category_obj.c_name = update_name
        db.session.commit()
        print(update_name,"this is updated name",Category_obj.c_name)
        return redirect('/Manager')
       except:
           return render_template('error_c.html',id = id)
   if request.method == 'GET':
       return render_template("upd_category.html",Category_obj=Category_obj)

@app.route('/confirmation/<int:id>',methods=['GET','POST'])
def confirm_delete(id):
    Category_obj = Category.query.filter_by(c_id=id).first()
    if request.method =='POST':
       return redirect('/Category_delete/{}'.format(id))
    else:
        return render_template('/confirm.html',Category_obj=Category_obj)

@app.route('/Manager_Product/<int:id>',methods=['GET','POST'])
def Manage_Product(id):
    catg_obj = Category.query.get(id)
    list_product = catg_obj.c_products
    return render_template('Manager_products.html',list_product=list_product,catg_obj=catg_obj)

@app.route('/Product_delete/<int:id>',methods=['GET','POST'])
def delete_Product(id):
    del_produ = Product.query.get(id)
    print(del_produ)
    key = int(del_produ.p_category_id)
    print(key)
    cart_item = Cart.query.all()
    for i in cart_item:
        print(i.c_name,"this is second print",del_produ.p_name)
        if i.c_name == del_produ.p_name :
            db.session.delete(i)
    db.session.delete(del_produ)
    db.session.commit()
    print(key,"this is key")
    return redirect('/Manager_Product/{}'.format(key))

@app.route('/Product_update/<int:id>',methods=['GET','POST'])
def update_produ(id):
    var = "Product"
    update_obj = Product.query.filter_by(p_id=id).first()
    print(update_obj,"this is object")
    if update_obj:
        key=int(update_obj.p_category_id)
        print(key,"this is key")
        if request.method=='POST':
            try:
                print(update_obj.p_name)
                update_name =request.form.get('productname')
                update_quantity = request.form.get('produ_quantity')
                update_price = request.form.get('productprice')
                update_expiry = request.form.get('expirydate')
                update_obj.p_name = update_name
                update_obj.p_rate = update_price
                update_obj.p_expiry =update_expiry
                update_obj.p_quantity = update_quantity
                db.session.commit()
                print(update_obj)
                print(update_obj.p_name,update_obj.p_rate,update_obj.p_expiry)
                return redirect('/Manager_Product/{}'.format(key))
            except:
                return render_template('error_c.html',id=id,var = var)
        if request.method == 'GET':
            return render_template('update_product.html',update_obj=update_obj)
    else :
        return "product not found"

@app.route('/Product_add',methods=['GET','POST'])
def Product_add():
    obj = Category.query.all()
    var = "Product"
    if request.method=='POST':
        try:
            name=request.form.get('productname')
            quantity = request.form.get('produ_quantity')
            price = request.form.get('productprice')
            expiry = request.form.get('expirydate')
            unit = request.form.get('p_unit')
            assign_ctg = request.form.get('assign_ctg')
            obj = Product(p_name=name,p_quantity=quantity,p_expiry=expiry,p_rate=price,p_unit=unit,p_category_id=assign_ctg)
            db.session.add(obj)
            db.session.commit()
            print(obj)
            return redirect('/Manager_Product/{}'.format(assign_ctg))
        except:
            return  render_template('error.html',var=var)
    if request.method=='GET':
        return render_template('add_product.html',id=id,obj=obj)

@app.route('/search',methods=['GET','POST'])
def search():
    query = request.args.get('query')
    matched_catg = Category.query.filter(Category.c_name.ilike(f'%{query}%')).all()
    matched_prod = Product.query.filter(Product.p_name.ilike(f'%{query}%')).all()
    matched_price = Product.query.filter(Product.p_rate.ilike(f'%{query}%')).all()
    matched_date =  Product.query.filter(Product.p_expiry.ilike(f'%{query}%')).all()

    print(matched_catg,matched_prod,"hello",query)
    return render_template("search_result.html",matched_catg=matched_catg,matched_prod=matched_prod,matched_price=matched_price,matched_date=matched_date,query=query)

@app.route('/search_u',methods=['GET','POST'])
def user_Search():
    query = request.args.get('query')
    matched_catg = Category.query.filter(Category.c_name.ilike(f'%{query}%')).all()
    matched_prod = Product.query.filter(Product.p_name.ilike(f'%{query}%')).all()
    matched_price = Product.query.filter(Product.p_rate.ilike(f'%{query}%')).all()
    matched_date =  Product.query.filter(Product.p_expiry.ilike(f'%{query}%')).all()

    print(matched_catg,matched_prod,"hello",query,matched_date)
    return render_template("u_search_result.html",matched_catg=matched_catg,matched_prod=matched_prod,matched_price=matched_price,matched_date=matched_date,query=query)


@app.route('/MyShop',methods=['GET','POST'])
def  Prod_by_category():
    if request.method == 'GET':
        catg = Category.query.all()
        messages = session.pop('_flashes', [])
        return render_template('P.html',catg = catg)

@app.route('/category/<int:id>',methods=['GET','POST'])
def Category_prod(id):
    Categ = Category.query.get(id)
    catg = Category.query.all()

    return render_template('Products.html',Categ=Categ,catg=catg)

    

@app.route('/MYCART' , methods=['GET','POST'])
def My_Cart():
    
    user_id = session.get('user_id')
    user_obj= User.query.filter_by(id=user_id).first()
    carts = user_obj.cart_item
    if request.method=='GET' :
        grandtotal=0
        for cart in carts:
            grandtotal+=int(cart.c_totalprice)
        return render_template('Cart.html',carts=carts,grandtotal=grandtotal)

    
@app.route('/cartdelete/<int:id>',methods=['GET','POST'])
def cart_delete(id):
    user_id = session.get('user_id')
    user_obj= User.query.filter_by(id=user_id).first()
    cart_iteam = user_obj.cart_item
    for i in cart_iteam:
        if int(i.c_id) == id :
            obj = Product.query.filter_by(p_name =i.c_name).first()
            obj.p_quantity += i.c_quantity
            db.session.delete(i)
    db.session.commit()
    return redirect("/MYCART")

@app.route('/UpdateCartIteam/<int:id>',methods=['GET','POST'])
def Update_buyiteam(id):
    cart_iteam = Cart.query.filter_by(c_id=id).first()
    product_obj = Product.query.filter_by(p_name=cart_iteam.c_name).first()
    print(cart_iteam)
    old_quantity = int(cart_iteam.c_quantity)
    if request.method=='GET':
        return render_template("update_cart.html",cart_iteam=cart_iteam,product_obj=product_obj)
    else:
        quantity = int(request.form.get("produ_quantity"))
        cart_iteam.c_quantity = quantity
        cart_iteam.c_totalprice= int(quantity)*int(cart_iteam.c_rate)
        product_obj.p_quantity+= old_quantity -quantity
        db.session.commit()
        return redirect('/MYCART')
    
@app.route('/MYCART/BUYALL')
def Thanks():
    user_id = session.get('user_id')
    user_obj= User.query.filter_by(id=user_id).first()
    cart_iteam = user_obj.cart_item
    for i in cart_iteam:
        db.session.delete(i)
    db.session.commit()
    return render_template("Thanks.html")



@app.route('/buy/<int:id>',methods=['GET','POST'])
def Buy_Product(id):
    product = Product.query.get(id)
    user_id = session.get('user_id')
    print("hello buy",product,user_id,"getting NOne")
    
    if request.method == 'GET' :
        return render_template('buyproduct.html',product=product)
    if user_id:
        if request.method == 'POST' :
            quantity = int(request.form.get("produ_quantity"))
            prate = int(product.p_rate)
            answer = quantity*prate
            c = Cart(c_name=product.p_name,c_rate=product.p_rate,c_quantity=quantity,c_totalprice=answer,c_user=user_id)
            product.p_quantity -= quantity 
            db.session.add(c)
            db.session.commit()
            return redirect('/MyShop')
    else:
        return render_template('loginproblem.html')
    

@app.route('/logout')
def logout():
    session.clear() 
    return redirect("/") 





if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)