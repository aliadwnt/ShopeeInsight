from flask import Flask, render_template, request, redirect, url_for, session
import pymysql

app = Flask(__name__)
app.secret_key = 'secret'  # Ganti dengan secret key yang aman

# Fungsi koneksi ke database
def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='shopeeshopee',  # Ganti dengan nama database yang digunakan
        cursorclass=pymysql.cursors.DictCursor
    )

# ======================
# Route Publik
# ======================
@app.route('/')
@app.route('/home')
def index():
    return render_template('pages/user/home.html')

@app.route('/user/about-us')
def about_us():
    return render_template('pages/user/about-us.html')

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
            user = cursor.fetchone()

        conn.close()

        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('admin_dashboard'))  # redirect bisa disesuaikan
        else:
            error = 'Username atau password salah.'

    return render_template('pages/admin/login.html', error=error)

# ======================
# Route Admin
# ======================
@app.route('/admin/dashboard')
def admin_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('/admin/login'))
    return render_template('pages/admin/dashboard.html')

@app.route('/admin/history')
def admin_history():
    if 'user_id' not in session:
        return redirect(url_for('/admin/login'))
    return render_template('pages/admin/history.html')

@app.route('/admin/dataset')
def admin_dataset():
    if 'user_id' not in session:
        return redirect(url_for('/admin/login'))
    return render_template('pages/admin/dataset.html')

@app.route('/admin/evaluation')
def dna_evaluation():
    if 'user_id' not in session:
        return redirect(url_for('/admin/login'))
    return render_template('pages/admin/evaluation.html')

# ======================
# Logout
# ======================
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('/admin/login'))

@app.route('/scraping', methods=['GET', 'POST'])
def scraping():
    hasil = None
    if request.method == 'POST':
        shop_id = request.form.get('shop_id')
        user_id = request.form.get('user_id')

        if shop_id and user_id:
            hasil = scrape_toko_api(shop_id, user_id)
        else:
            hasil = {"error": "Shop ID dan User ID harus diisi."}

    return render_template('base2.html', hasil=hasil)

# ======================
# Jalankan aplikasi
# ======================
if __name__ == '__main__':
    app.run(debug=True)
