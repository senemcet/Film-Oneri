from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
import os
from content_based import ContentBasedRecommender

# İçerik tabanlı öneri sistemini başlat (islenmisveri.csv dosyasını kullanarak)
recommender = ContentBasedRecommender('islenmisveri.csv')

# Flask uygulaması oluştur
app = Flask(__name__, template_folder='filmoneri', static_folder='filmoneri')
app.secret_key = 'secret_key'  # Oturum verilerinin güvenliğini sağlamak için gerekli

# Veritabanı konfigürasyonu (SQLite kullanılarak)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "instance", "database.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# SQLAlchemy ORM başlat
db = SQLAlchemy(app)

# İzleme geçmişi tablosu modeli
class IzlemeGecmisi(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Birincil anahtar
    kullanici_id = db.Column(db.Integer, db.ForeignKey('kullanici.id'), nullable=False)  # Kullanıcı ID (yabancı anahtar)
    film_id = db.Column(db.Integer, db.ForeignKey('film.id'), nullable=False)  # Film ID (yabancı anahtar)
    izleme_tarihi = db.Column(db.DateTime, default=db.func.current_timestamp())  # İzleme zamanı (varsayılan: şimdiki zaman)

# Film tablosu modeli
class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Birincil anahtar
    title = db.Column(db.String(150), nullable=False)  # Film başlığı
    genres = db.Column(db.String(200), nullable=False)  # Türler
    runtime = db.Column(db.Integer, nullable=True)  # Süre
    vote_average = db.Column(db.Float, nullable=True)  # Kullanıcı puanı ortalaması
    popularity = db.Column(db.Float, nullable=True)  # Popülerlik
    overview = db.Column(db.Text, nullable=True)  # Film özeti

# Kullanıcı tablosu modeli
class Kullanici(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Birincil anahtar
    ad_soyad = db.Column(db.String(80), nullable=False)  # Kullanıcı adı
    eposta = db.Column(db.String(120), unique=True, nullable=False)  # E-posta adresi
    sifre = db.Column(db.String(200), nullable=False)  # Hash'lenmiş şifre

# Veritabanını oluştur
with app.app_context():
    db.create_all()

# Veritabanına filmleri yükler
def load_films():
    veri_dosyasi = os.path.join(basedir, 'islenmisveri.csv')
    if os.path.exists(veri_dosyasi):
        movies = pd.read_csv(veri_dosyasi)

        movies['genres'] = movies['genres'].fillna('Bilinmiyor')
        movies['runtime'] = movies['runtime'].fillna(0)
        movies['overview'] = movies['overview'].fillna('')

        for _, row in movies.iterrows():
            mevcut_film = Film.query.filter_by(title=row['title']).first()
            if mevcut_film:
                continue

            yeni_film = Film(
                title=row['title'],
                genres=row['genres'],
                runtime=row['runtime'],
                vote_average=row['vote_average'],
                popularity=row['popularity'],
                overview=row['overview']
            )
            db.session.add(yeni_film)

        db.session.commit()
# Kullanıcı kayıt olma rotası
@app.route('/kayitol', methods=['GET', 'POST'])
def kayitol():
    if request.method == 'POST':
        ad_soyad = request.form.get('ad_soyad')
        eposta = request.form.get('eposta')
        sifre = request.form.get('sifre')

        # Şifre hash'lenir
        hashed_password = generate_password_hash(sifre, method='pbkdf2:sha256')

        # Yeni kullanıcı oluşturulur
        yeni_kullanici = Kullanici(ad_soyad=ad_soyad, eposta=eposta, sifre=hashed_password)

        try:
            db.session.add(yeni_kullanici)
            db.session.commit()
            flash('Kayıt işlemi başarılı!', 'success')  # Başarı mesajı
            return redirect(url_for('giris'))
        except Exception as e:
            flash('Kayıt sırasında bir hata oluştu.', 'danger')  # Hata mesajı
    return render_template('kayitol.html')

# Kullanıcı giriş rotası
@app.route('/giris', methods=['GET', 'POST'])
def giris():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Kullanıcıyı bul
        kullanici = Kullanici.query.filter_by(eposta=email).first()

        if kullanici and check_password_hash(kullanici.sifre, password):
            # Oturum başlat
            session['user_id'] = kullanici.id
            session['user_name'] = kullanici.ad_soyad

            flash(f'Hoş geldiniz, {kullanici.ad_soyad}!', 'success')
            return redirect(url_for('anasayfa'))
        else:
            flash('E-posta veya şifre hatalı.', 'danger')
    return render_template('giris.html')

# Çıkış yapma rotası
@app.route('/cikis')
def cikis():
    session.clear()  # Oturum temizlenir
    flash("Başarıyla çıkış yaptınız.", "success")
    return redirect(url_for('giris'))


@app.route('/')
@app.route('/anasayfa')
def anasayfa():
    user_name = session.get('user_name')  # Oturumdaki kullanıcı adı
    önerilen_filmler = []
    populer_filmler = Film.query.order_by(Film.popularity.desc()).limit(3).all()  # Popüler ilk 3 film

    if 'user_id' in session:  # Kullanıcı oturum açmışsa
        # Kullanıcının izleme geçmişini al
        izleme_gecmisi = IzlemeGecmisi.query.filter_by(kullanici_id=session['user_id']).all()
        izlenen_film_basliklari = [Film.query.get(gecmis.film_id).title for gecmis in izleme_gecmisi]

        if izlenen_film_basliklari:
            # İzleme geçmişine göre kullanıcı profili vektörü oluştur
            öneriler = recommender.kullanici_tabanli_oner(izleme_gecmisi=izlenen_film_basliklari, k=50)

            # İzleme geçmişinde zaten izlenen filmleri önerilerden çıkar
            öneriler = [film for film in öneriler if film not in izlenen_film_basliklari]

            # Öneri skoru hesapla (TF-IDF benzerliklerine göre)
            öneri_skorlar = []
            for öneri in öneriler:
                try:
                    idx_öneri = recommender.veri[recommender.veri['title'] == öneri].index[0]
                    benzerlik_skoru = max([
                        recommender.cosine_sim[idx_öneri][recommender.veri[recommender.veri['title'] == izlenen].index[0]]
                        for izlenen in izlenen_film_basliklari
                    ])
                    öneri_skorlar.append((öneri, benzerlik_skoru))
                except IndexError:
                    continue

            # Önerileri benzerlik skorlarına göre sırala ve en iyi 4 filmi seç
            öneri_skorlar = sorted(öneri_skorlar, key=lambda x: x[1], reverse=True)[:4]
            önerilen_filmler_titler = [öneri[0] for öneri in öneri_skorlar]

            # Önerilen filmleri veritabanından al
            önerilen_filmler = Film.query.filter(Film.title.in_(önerilen_filmler_titler)).all()
    else:
        # Oturum açmamış kullanıcılar için popüler filmleri öner
        önerilen_filmler = Film.query.order_by(Film.popularity.desc()).limit(4).all()

    # Anasayfa için tüm filmleri listele
    filmler = Film.query.order_by(Film.vote_average.desc()).limit(500).all()

    return render_template(
        'anasayfa.html',
        user_name=user_name,
        onerilen_filmler=önerilen_filmler,
        filmler=filmler,
        populer_filmler=populer_filmler
    )


# @app.route('/film/<int:film_id>') #özete göre önerme
# def film_detay(film_id):
#     film = Film.query.get(film_id)
#     if not film:
#         flash("Film bulunamadı.", "danger")
#         return redirect(url_for('anasayfa'))

#     # Film önerilerini al ve benzerlik skorlarını hesapla
#     öneriler = recommender.film_oner(film.title, k=4)  # Film başlığına göre 4 öneri
#     önerilen_filmler = []

#     print(f"'{film.title}' için önerilen filmler ve benzerlik skorları:")
#     for öneri in öneriler:
#         try:
#             idx_film = recommender.veri[recommender.veri['title'] == film.title].index[0]
#             idx_öneri = recommender.veri[recommender.veri['title'] == öneri].index[0]
#             benzerlik_skoru = recommender.cosine_sim[idx_film, idx_öneri]

#             print(f"Film: {öneri}, Benzerlik Skoru: {benzerlik_skoru:.4f}")

#             film_detay = Film.query.filter_by(title=öneri).first()
#             if film_detay:
#                 önerilen_filmler.append(film_detay)  # Sadece Film nesnelerini ekle
#         except IndexError:
#             print(f"'{öneri}' için indeks bulunamadı. Veride eksik olabilir.")

#     trailer_url = "https://www.youtube.com/embed/dummy_trailer_id"

#     return render_template(
#         'film_detay.html',
#         film=film,
#         trailer_url=trailer_url,
#         önerilen_filmler=önerilen_filmler  # Sadece Film nesneleri gönderiliyor
#     )

# #türe göre
@app.route('/film/<int:film_id>')
def film_detay(film_id):
    film = Film.query.get(film_id)
    if not film:
        flash("Film bulunamadı.", "danger")
        return redirect(url_for('anasayfa'))

    # Film önerilerini türe göre al ve benzerlik skorlarını hesapla
    öneriler = recommender.film_oner_ture_gore(film.title, k=4)  # Film başlığına göre türe göre 4 öneri
    önerilen_filmler = []

    print(f"'{film.title}' için türe göre önerilen filmler ve benzerlik skorları:")
    for öneri in öneriler:
        try:
            idx_film = recommender.veri[recommender.veri['title'] == film.title].index[0]
            idx_öneri = recommender.veri[recommender.veri['title'] == öneri].index[0]
            benzerlik_skoru = recommender.genre_cosine_sim[idx_film, idx_öneri]  # Türlere göre benzerlik skoru

            print(f"Film: {öneri}, Tür Benzerlik Skoru: {benzerlik_skoru:.4f}")

            film_detay = Film.query.filter_by(title=öneri).first()
            if film_detay:
                önerilen_filmler.append(film_detay)  # Sadece Film nesnelerini ekle
        except IndexError:
            print(f"'{öneri}' için indeks bulunamadı. Veride eksik olabilir.")

    trailer_url = "https://www.youtube.com/embed/dummy_trailer_id"

    return render_template(
        'film_detay.html',
        film=film,
        trailer_url=trailer_url,
        önerilen_filmler=önerilen_filmler  # Sadece Film nesneleri gönderiliyor
    )



# Kullanıcının izleme geçmişine film ekleme
@app.route('/add_to_history', methods=['POST'])
def gecmise_ekle():
    veri = request.get_json()
    film_id = veri.get('film_id')
    kullanici_id = session.get('user_id')

    try:
        mevcut_kayit = IzlemeGecmisi.query.filter_by(kullanici_id=kullanici_id, film_id=film_id).first()
        if not mevcut_kayit:
            yeni_kayit = IzlemeGecmisi(kullanici_id=kullanici_id, film_id=film_id)
            db.session.add(yeni_kayit)
            db.session.commit()
            return jsonify({'mesaj': 'Geçmişe eklendi'}), 200
        else:
            return jsonify({'mesaj': 'Film zaten geçmişte var'}), 200
    except Exception as e:
        return jsonify({'mesaj': 'Bir hata oluştu'}), 500



# Uygulama çalıştırılır
if __name__ == '__main__':
    with app.app_context():
        load_films()
    app.run(debug=True)

