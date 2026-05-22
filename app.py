from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

DATABASE = 'store.db'


# =========================
# DATABASE CONNECTION
# =========================

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# =========================
# CREATE TABLE
# =========================

def create_table():
    conn = get_db_connection()

    conn.execute('''
    CREATE TABLE IF NOT EXISTS products(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price INTEGER NOT NULL,
        description TEXT NOT NULL,
        image TEXT NOT NULL
    )
    ''')
    
    conn.execute('''
    CREATE TABLE IF NOT EXISTS reviews(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    customer_name TEXT,
    review TEXT,
    rating INTEGER,

    FOREIGN KEY(product_id)
    REFERENCES products(id)
)
''')

    conn.commit()
    conn.close()


# =========================
# HOME PAGE
# =========================

@app.route('/')
def home():

    conn = get_db_connection()

    products = conn.execute(
        'SELECT * FROM products'
    ).fetchall()

    conn.close()

    return render_template(
        'index.html',
        products=products
    )
    
# =========================
# ADMIN DASHBOARD
# =========================

@app.route('/admin')
def admin():

    conn = get_db_connection()

    products = conn.execute(
        'SELECT * FROM products'
    ).fetchall()

    conn.close()

    return render_template(
        'admin.html',
        products=products
    )    
    


# =========================
# PRODUCTS PAGE
# =========================

@app.route('/products')
def products():

    conn = get_db_connection()

    products = conn.execute(
        'SELECT * FROM products'
    ).fetchall()

    conn.close()

    return render_template(
        'products.html',
        products=products
    )


# =========================
# ABOUT PAGE
# =========================

@app.route('/about')
def about():
    return render_template('about.html')


# =========================
# SERVICES PAGE
# =========================

@app.route('/services')
def services():
    return render_template('services.html')


# =========================
# CONTACT PAGE
# =========================

@app.route('/contact')
def contact():
    return render_template('contact.html')


# =========================
# ADD PRODUCT
# =========================

@app.route('/add-product', methods=['GET', 'POST'])
def add_product():

    if request.method == 'POST':

        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        image = request.form['image']

        conn = get_db_connection()

        conn.execute('''
        INSERT INTO products(name, price, description, image)
        VALUES (?, ?, ?, ?)
        ''', (name, price, description, image))

        conn.commit()
        conn.close()

        return redirect('/products')

    return render_template('add_product.html')


# =========================
# DELETE PRODUCT
# =========================

@app.route('/delete-product/<int:id>')
def delete_product(id):

    conn = get_db_connection()

    conn.execute(
        'DELETE FROM products WHERE id = ?',
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/products')


# =========================
# UPDATE PRODUCT
# =========================

@app.route('/edit-product/<int:id>', methods=['GET', 'POST'])
def edit_product(id):

    conn = get_db_connection()

    product = conn.execute(
        'SELECT * FROM products WHERE id = ?',
        (id,)
    ).fetchone()

    if request.method == 'POST':

        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        image = request.form['image']

        conn.execute('''
        UPDATE products
        SET name = ?,
            price = ?,
            description = ?,
            image = ?
        WHERE id = ?
        ''', (name, price, description, image, id))

        conn.commit()
        conn.close()

        return redirect('/products')

    conn.close()

    return render_template(
        'edit_product.html',
        product=product
    )


# =========================
# RUN APPLICATION
# =========================

if __name__ == '__main__':

    create_table()

    app.run(debug=True)