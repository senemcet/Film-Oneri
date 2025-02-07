
# # # Anasayfa rotası
# # @app.route('/')
# # @app.route('/anasayfa')
# # def anasayfa():
# #     user_name = session.get('user_name')  # Oturumdaki kullanıcı adı
# #     önerilen_filmler = []

# #     if 'user_id' in session:
# #         # Kullanıcının izleme geçmişini al
# #         izleme_gecmisi = IzlemeGecmisi.query.filter_by(kullanici_id=session['user_id']).all()
# #         izlenen_film_basliklari = [Film.query.get(gecmis.film_id).title for gecmis in izleme_gecmisi]

# #         if izlenen_film_basliklari:
# #             # Kullanıcının izlediği tüm filmlerin önerilerini birleştir
# #             tüm_öneriler = []
# #             for film_baslik in izlenen_film_basliklari:
# #                 öneriler = recommender.film_oner(film_baslik, k=10)  # Her film için 10 öneri al
# #                 tüm_öneriler.extend(öneriler)

# #             # Tekrar eden önerileri kaldır ve izlenen filmleri önerilerden çıkar
# #             öneriler_set = list(set(tüm_öneriler) - set(izlenen_film_basliklari))

# #             # Önerilen filmlerin benzerlik oranlarına göre sıralanması
# #             öneri_skorlar = []
# #             for öneri in öneriler_set:
# #                 idx_öneri = recommender.veri[recommender.veri['title'] == öneri].index[0]
# #                 sim_skor = max(
# #                     [recommender.cosine_sim[idx_öneri][recommender.veri[recommender.veri['title'] == film].index[0]]
# #                      for film in izlenen_film_basliklari]
# #                 )
# #                 öneri_skorlar.append((öneri, sim_skor))

# #             öneri_skorlar = sorted(öneri_skorlar, key=lambda x: x[1], reverse=True)[:4]  # En iyi 4 öneriyi al
# #             önerilen_filmler_titler = [öneri[0] for öneri in öneri_skorlar]

# #             # Önerilen filmleri veritabanından al
# #             önerilen_filmler = Film.query.filter(Film.title.in_(önerilen_filmler_titler)).all()
# #     else:
# #         # Giriş yapmayan kullanıcı için popüler filmleri göster
# #         önerilen_filmler = Film.query.order_by(Film.popularity.desc()).limit(4).all()

# #     # Anasayfa için yalnızca popüler ilk 500 filmi göster
# #     filmler = Film.query.order_by(Film.vote_average.desc()).limit(500).all()

# #     return render_template(
# #         'anasayfa.html',
# #         user_name=user_name,
# #         onerilen_filmler=önerilen_filmler,
# #         filmler=filmler
# #     )
# # ###
# # #
# # #
# # #
# # #
# # from flask import Flask, render_template, request, redirect, url_for, flash
# # from flask_sqlalchemy import SQLAlchemy
# # from werkzeug.security import generate_password_hash, check_password_hash
# # import pandas as pd
# # import os
# # from flask import Flask, render_template, request, redirect, url_for, flash, session
# # from flask import jsonify, request
# # from content_based import ContentBasedRecommender
# # from content_based import split_user_data, create_user_profile, evaluate_test_set, calculate_metrics



# # # Content-based modelini yükle
# # recommender = ContentBasedRecommender('islenmisveri.csv')

# # app = Flask(__name__, template_folder='filmoneri', static_folder='filmoneri')
# # app.secret_key = 'secret_key'

# # # Veritabanı ayarları
# # basedir = os.path.abspath(os.path.dirname(__file__))
# # app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "instance", "database.db")}'
# # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# # db = SQLAlchemy(app)

# # class IzlemeGecmisi(db.Model):
# #     id = db.Column(db.Integer, primary_key=True)
# #     kullanici_id = db.Column(db.Integer, db.ForeignKey('kullanici.id'), nullable=False)
# #     film_id = db.Column(db.Integer, db.ForeignKey('film.id'), nullable=False)
# #     izleme_tarihi = db.Column(db.DateTime, default=db.func.current_timestamp())

# # # Film modeli
# # class Film(db.Model):
# #     id = db.Column(db.Integer, primary_key=True)
# #     title = db.Column(db.String(150), nullable=False)  # Film adı
# #     genres = db.Column(db.String(200), nullable=False)  # Türler
# #     runtime = db.Column(db.Integer, nullable=True)  # Süre
# #     vote_average = db.Column(db.Float, nullable=True)  # Kullanıcı puanı
# #     popularity = db.Column(db.Float, nullable=True)  # Popülerlik
# #     overview = db.Column(db.Text, nullable=True)  # Film özeti

# # # Kullanıcı modeli
# # class Kullanici(db.Model):
# #     id = db.Column(db.Integer, primary_key=True)
# #     ad_soyad = db.Column(db.String(80), nullable=False)
# #     eposta = db.Column(db.String(120), unique=True, nullable=False)
# #     sifre = db.Column(db.String(200), nullable=False)

# # with app.app_context():
# #     db.create_all()


# # # Kayıt ol rotası
# # @app.route('/kayitol', methods=['GET', 'POST'])
# # def kayitol():
# #     if request.method == 'POST':
# #         ad_soyad = request.form.get('ad_soyad')
# #         eposta = request.form.get('eposta')
# #         sifre = request.form.get('sifre')

# #         # Şifreyi hash'le
# #         hashed_password = generate_password_hash(sifre, method='pbkdf2:sha256')

# #         # Kullanıcıyı oluştur
# #         yeni_kullanici = Kullanici(ad_soyad=ad_soyad, eposta=eposta, sifre=hashed_password)

# #         try:
# #             db.session.add(yeni_kullanici)
# #             db.session.commit()
# #             flash('Kayıt işlemi başarılı!', 'success')
# #             return redirect(url_for('giris'))
# #         except Exception as e:
# #             flash('Kayıt sırasında bir hata oluştu.', 'danger')
# #             print(f"Error: {e}")
# #     return render_template('kayitol.html')

# # # Giriş yap rotası
# # @app.route('/giris', methods=['GET', 'POST'])
# # def giris():
# #     if request.method == 'POST':
# #         email = request.form['email']
# #         password = request.form['password']

# #         # Kullanıcıyı veritabanından bul
# #         kullanici = Kullanici.query.filter_by(eposta=email).first()

# #         # Kullanıcı ve şifre kontrolü
# #         if kullanici and check_password_hash(kullanici.sifre, password): #veritabanında saklanan şifreyle, kullanıcının giriş formunda yazdığı şifre ile karşılaştırılır
# #             # Kullanıcı oturumu açılıyor
# #             session['user_id'] = kullanici.id
# #             session['user_name'] = kullanici.ad_soyad

# #             flash(f'Hoş geldiniz, {kullanici.ad_soyad}!', 'success')
# #             return redirect(url_for('anasayfa'))
# #         else:
# #             flash('E-posta veya şifre hatalı.', 'danger')   
# #     return render_template('giris.html')


# # @app.route('/cikis')
# # def cikis():
# #     # Oturum bilgilerini temizle
# #     session.clear()
# #     flash("Başarıyla çıkış yaptınız.", "success")
# #     return redirect(url_for('giris'))

# # def load_films():
# #     # İşlenmiş veri setini yükle
# #     veri_dosyasi = os.path.join(basedir, 'islenmisveri.csv')
# #     if os.path.exists(veri_dosyasi):
# #         movies = pd.read_csv(veri_dosyasi)

# #         # Boş veya eksik değerleri kontrol et ve doldur
# #         movies['genres'] = movies['genres'].fillna('Bilinmiyor')  # Türler boşsa 'Bilinmiyor' ekle
# #         movies['runtime'] = movies['runtime'].fillna(0)  # Süre boşsa 0 ekle
# #         movies['overview'] = movies['overview'].fillna('')  # Özet boşsa boş string ekle

# #         # Tüm işlenmiş veriyi veritabanına ekle
# #         for _, row in movies.iterrows():
# #             mevcut_film = Film.query.filter_by(title=row['title']).first()
# #             if mevcut_film:
# #                 continue  # Eğer film zaten veritabanında varsa atla

# #             yeni_film = Film(
# #                 title=row['title'],
# #                 genres=row['genres'],
# #                 runtime=row['runtime'],
# #                 vote_average=row['vote_average'],
# #                 popularity=row['popularity'],
# #                 overview=row['overview']
# #             )
# #             db.session.add(yeni_film)

# #         db.session.commit()
# #         print("Tüm işlenmiş veri başarıyla veritabanına kaydedildi!")


# # @app.route('/')
# # @app.route('/anasayfa')
# # def anasayfa():
# #     user_name = session.get('user_name')  # Oturumdaki kullanıcı adı
# #     önerilen_filmler = []

# #     if 'user_id' in session:
# #         # Kullanıcının izleme geçmişini al
# #         izleme_gecmisi = IzlemeGecmisi.query.filter_by(kullanici_id=session['user_id']).all()
# #         izlenen_film_basliklari = [Film.query.get(gecmis.film_id).title for gecmis in izleme_gecmisi]

# #         if izlenen_film_basliklari:
# #             # Kullanıcı geçmişine göre öneriler al
# #             önerilen_film_basliklari = recommender.kullanici_tabanli_oner(izlenen_film_basliklari, k=6)
# #             # Önerilen filmleri veritabanından al
# #             önerilen_filmler = Film.query.filter(Film.title.in_(önerilen_film_basliklari)).all()
# #     else:
# #         # Giriş yapmayan kullanıcı için popüler filmleri göster
# #         önerilen_filmler = Film.query.order_by(Film.popularity.desc()).limit(4).all()

# #     # Anasayfa için yalnızca popüler ilk 500 filmi göster
# #     filmler = Film.query.order_by(Film.vote_average.desc()).limit(500).all()

# #     return render_template(
# #         'anasayfa.html',
# #         user_name=user_name,
# #         onerilen_filmler=önerilen_filmler,
# #         filmler=filmler
# #     )

# # @app.route('/film/<int:film_id>')
# # def film_detay(film_id):
# #     print(f"Film Detay Rota Çağrıldı: {film_id}")

# #     # Tıklanan film bilgilerini al
# #     film = Film.query.get(film_id)
# #     if not film:
# #         flash("Film bulunamadı.", "danger")
# #         return redirect(url_for('anasayfa'))

# #     # Tıklanan filme göre öneri yap (ilk 4)
# #     öneriler = recommender.film_oner(film.title, k=4)
# #     # Önerilen filmleri veritabanından alın
# #     önerilen_filmler = Film.query.filter(Film.title.in_(öneriler)).all()

# #     # Benzerlik oranlarını hesapla ve terminalde göster
# #     benzerlik_skorlari = []
# #     try:
# #         # Tıklanan film için indeks bul
# #         idx_film = recommender.veri[recommender.veri['title'] == film.title].index[0]
# #         for önerilen_film in öneriler:
# #             # Önerilen filmler için indeks bul ve benzerlik hesapla
# #             idx_öneri = recommender.veri[recommender.veri['title'] == önerilen_film].index[0]
# #             benzerlik = recommender.cosine_sim[idx_film][idx_öneri]
# #             benzerlik_skorlari.append((önerilen_film, benzerlik))
# #     except Exception as e:
# #         print(f"Hata: {e}")

# #     # Terminalde benzerlik skorlarını yazdır
# #     print("\nBenzerlik Skorları:")
# #     for öneri, skor in benzerlik_skorlari:
# #         print(f"Film: {öneri}, Benzerlik Skoru: {skor:.4f}")

# #     # Fragman URL'si (geçici olarak sabit değer)
# #     trailer_url = "https://www.youtube.com/embed/dummy_trailer_id"

# #     return render_template(
# #         'film_detay.html',
# #         film=film,
# #         trailer_url=trailer_url,
# #         önerilen_filmler=önerilen_filmler  # Arayüzde göstermek için önerilen filmler
# #     )


# # @app.route('/add_to_history', methods=['POST'])
# # def gecmise_ekle():
# #     # Kullanıcı ve film ID'sini al
# #     veri = request.get_json()
# #     film_id = veri.get('film_id')
# #     kullanici_id = session.get('user_id')  # Oturumdaki kullanıcı ID'si

# #     # Veritabanında kontrol edip ekleme
# #     try:
# #         mevcut_kayit = IzlemeGecmisi.query.filter_by(kullanici_id=kullanici_id, film_id=film_id).first()
# #         if not mevcut_kayit:
# #             yeni_kayit = IzlemeGecmisi(kullanici_id=kullanici_id, film_id=film_id)
# #             db.session.add(yeni_kayit)
# #             db.session.commit()
# #             return jsonify({'mesaj': 'Geçmişe eklendi'}), 200
# #         else:
# #             return jsonify({'mesaj': 'Film zaten geçmişte var'}), 200
# #     except Exception as e:
# #         print(f"Hata oluştu: {e}")
# #         return jsonify({'mesaj': 'Bir hata oluştu'}), 500
    

# # @app.route('/film_izle/<int:film_id>', methods=['GET'])
# # def film_izle(film_id):
# #     try:
# #         # Kullanıcının giriş yapıp yapmadığını kontrol et
# #         if 'user_id' not in session:
# #             flash('Lütfen giriş yapınız.', 'danger')
# #             print("Oturum açılmamış.")
# #             return redirect(url_for('giris'))

# #         # Oturumdaki kullanıcıyı al
# #         kullanici_id = session['user_id']
# #         print(f"Kullanıcı ID: {kullanici_id}")

# #         # Film var mı kontrol et
# #         film = Film.query.get(film_id)
# #         if not film:
# #             flash('Film bulunamadı.', 'danger')
# #             print("Film bulunamadı.")
# #             return redirect(url_for('anasayfa'))

# #         # Daha önce bu film izlenmiş mi kontrol et
# #         mevcut_kayit = IzlemeGecmisi.query.filter_by(kullanici_id=kullanici_id, film_id=film_id).first()
# #         if not mevcut_kayit:
# #             # Eğer izlenmemişse ekle
# #             yeni_kayit = IzlemeGecmisi(kullanici_id=kullanici_id, film_id=film_id)
# #             db.session.add(yeni_kayit)
# #             db.session.commit()
# #             print(f"Film ({film.title}) izleme geçmişine eklendi.")
# #         else:
# #             print(f"Film ({film.title}) zaten izleme geçmişinde var.")
        
# #         flash(f"{film.title} izleme geçmişine eklendi.", 'success')
# #     except Exception as e:
# #         print(f"Hata oluştu: {e}")
# #         flash('Bir hata oluştu.', 'danger')

# #     return redirect(url_for('anasayfa'))


# # @app.route('/temizle_tekrarlar')
# # def temizle_tekrarlar():
# #     filmler = Film.query.all()
# #     unique_titles = set()
# #     for film in filmler:
# #         if film.title in unique_titles:
# #             db.session.delete(film)  # Tekrarlı kaydı sil
# #         else:
# #             unique_titles.add(film.title)
# #     db.session.commit()
# #     return "Tekrar eden kayıtlar temizlendi."


# # @app.route('/evaluate_user_recommendations', methods=['GET'])
# # def evaluate_user_recommendations():
# #     """
# #     Kullanıcının öneri sistemini değerlendirir:
# #     - Eğitim/Test setine ayırır.
# #     - Kullanıcı profili oluşturur.
# #     - Test seti önerilerini değerlendirir.
# #     - Performans metriklerini HTML'ye gönderir.
# #     """
# #     # Kullanıcının oturumunu kontrol et
# #     if 'user_id' not in session:
# #         flash("Lütfen giriş yapınız.", "danger")
# #         return redirect(url_for('giris'))

# #     # Kullanıcının izleme geçmişini al
# #     user_id = session['user_id']
# #     izleme_gecmisi = IzlemeGecmisi.query.filter_by(kullanici_id=user_id).all()
# #     if not izleme_gecmisi:
# #         flash("İzleme geçmişiniz boş. Öneri sistemi değerlendirilemez.", "danger")
# #         return redirect(url_for('anasayfa'))

# #     # İzleme geçmişindeki filmleri başlık olarak al
# #     izlenen_filmler = [Film.query.get(gecmis.film_id).title for gecmis in izleme_gecmisi]

# #     # Eğitim ve test setine ayır
# #     training_set, test_set = split_user_data(izlenen_filmler)

# #     # Kullanıcı profili oluştur
# #     user_profile = create_user_profile(training_set, recommender.veri)

# #     # Test setini değerlendir
# #     recommendations = evaluate_test_set(test_set, user_profile, recommender.veri)

# #     # Performans metriklerini hesapla
# #     precision, recall, f1_score = calculate_metrics(recommendations, test_set)

# #     # HTML şablonuna gönderilecek veriler
# #     return render_template(
# #         'evaluation_results.html',
# #         training_set=training_set,
# #         test_set=test_set,
# #         recommendations=recommendations,
# #         precision=precision,
# #         recall=recall,
# #         f1_score=f1_score
# #     )


# # if __name__ == '__main__':
# #     with app.app_context():
# #         load_films()  # Filmleri veri setinden yükleyin
# #     app.run(debug=True)



# # #
# # #
# # #
# # #
# # #
# # #
# # # @app.route('/kontrol_filmler')
# # # def kontrol_filmler():
# # #     filmler = Film.query.all()
# # #     for film in filmler:
# # #         print(f"Film ID: {film.id}, Başlık: {film.title}")
# # #     return "Filmler kontrol edildi. Lütfen terminali kontrol edin."


# # # # Content-based modelini yükle
# # # recommender = ContentBasedRecommender('islenmisveri.csv')

# # # @app.route('/oneriler', methods=['GET'])
# # # def oneriler():
# # #     if 'user_id' not in session:
# # #         flash('Lütfen giriş yapınız.', 'danger')
# # #         return redirect(url_for('giris'))

# # #     # Kullanıcının izleme geçmişini al
# # #     kullanici_id = session['user_id']
# # #     izleme_gecmisi = IzlemeGecmisi.query.filter_by(kullanici_id=kullanici_id).all()
# # #     izlenen_filmler = [Film.query.get(gecmis.film_id).title for gecmis in izleme_gecmisi]

# # #     # Kullanıcıya özel öneriler
# # #     öneriler = recommender.kullanici_tabanli_oner(izlenen_filmler)

# # #     # Sonuçları döndür
# # #     return render_template('oneriler.html', öneriler=öneriler, izlenen_filmler=izlenen_filmler)

# # # İletişim rotası
# # #@app.route('/iletisim', methods=['GET', 'POST'])
# # #def iletisim():
# # #    if request.method == 'POST':
# # #        isim = request.form.get('isim')
# # #        email = request.form.get('email')
# #  #       hizmet_turu = request.form.get('hizmet_turu')
# # #        mesaj = request.form.get('mesaj')
# #         # Verileri işleyin veya saklayın
# #  #       flash('Mesajınız başarıyla gönderildi.', 'success')
# # #        return redirect(url_for('iletisim'))
# # #    return render_template('iletisim.html')



# # Anasayfa rotası
# @app.route('/')
# @app.route('/anasayfa')
# def anasayfa():
#     user_name = session.get('user_name')  # Oturumdaki kullanıcı adı
#     önerilen_filmler = []
#     populer_filmler = Film.query.order_by(Film.popularity.desc()).limit(3).all()  # Popüler ilk 3 film

#     if 'user_id' in session:  # Eğer kullanıcı oturum açmışsa
#         # Kullanıcının izleme geçmişini al
#         izleme_gecmisi = IzlemeGecmisi.query.filter_by(kullanici_id=session['user_id']).all()
#         izlenen_film_basliklari = [Film.query.get(gecmis.film_id).title for gecmis in izleme_gecmisi]

#         if izlenen_film_basliklari:
#             # Kullanıcının izlediği filmlere göre öneri yap
#             tüm_öneriler = []
#             for film_baslik in izlenen_film_basliklari:
#                 öneriler = recommender.film_oner(film_baslik, k=10)  # Her film için 10 öneri
#                 tüm_öneriler.extend(öneriler)

#             # İzlenen filmleri çıkar ve tekrar eden önerileri filtrele
#             öneriler_set = list(set(tüm_öneriler) - set(izlenen_film_basliklari))

#             # Öneriler için benzerlik skorları hesaplanır
#             öneri_skorlar = []
#             for öneri in öneriler_set:
#                 idx_öneri = recommender.veri[recommender.veri['title'] == öneri].index[0]
#                 sim_skor = max(
#                     [recommender.cosine_sim[idx_öneri][recommender.veri[recommender.veri['title'] == film].index[0]]
#                      for film in izlenen_film_basliklari]
#                 )
#                 öneri_skorlar.append((öneri, sim_skor))

#             # Öneriler skorlarına göre sıralanır (en iyi 4 öneri seçilir)
#             öneri_skorlar = sorted(öneri_skorlar, key=lambda x: x[1], reverse=True)[:4]
#             önerilen_filmler_titler = [öneri[0] for öneri in öneri_skorlar]

#             # Önerilen filmler veritabanından alınır
#             önerilen_filmler = Film.query.filter(Film.title.in_(önerilen_filmler_titler)).all()
#     else:
#         # Oturum açmamış kullanıcılar için popüler filmler önerilir
#         önerilen_filmler = Film.query.order_by(Film.popularity.desc()).limit(4).all()

#     # Anasayfada gösterilecek filmler
#     filmler = Film.query.order_by(Film.vote_average.desc()).limit(500).all()

#     return render_template(
#         'anasayfa.html',
#         user_name=user_name,
#         onerilen_filmler=önerilen_filmler,
#         filmler=filmler
#     )











# @app.route('/test_ozet_benzerlik')
# def test_ozet_benzerlik():
#     # Test verisi: Kullanıcının izlediği film
#     test_filmleri = ["Film A"]  # Kullanıcının izlediği filmler (örnek test seti)
    
#     # Gerçek ilgili filmler (kullanıcının gerçekten beğendiği filmler)
#     gercek_ilgili_filmler = ["Film D", "Film E", "Film F"]

#     # Modelin önerdiği filmler
#     onerilen_filmler = recommender.film_oner("Film A", k=5)  # Özet üzerinden öneriler

#     # Doğruluk hesaplama
#     tp = len(set(onerilen_filmler) & set(gercek_ilgili_filmler))  # Doğru pozitif
#     fp = len(set(onerilen_filmler) - set(gercek_ilgili_filmler))  # Yanlış pozitif
#     fn = len(set(gercek_ilgili_filmler) - set(onerilen_filmler))  # Yanlış negatif

#     precision = tp / (tp + fp) if (tp + fp) > 0 else 0
#     recall = tp / (tp + fn) if (tp + fn) > 0 else 0
#     f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

#     # Sonuçları terminale yazdır
#     print(f"Precision: {precision:.2f}")
#     print(f"Recall: {recall:.2f}")
#     print(f"F1-Score: {f1:.2f}")

#     # Sonuçları kullanıcıya göster
#     return jsonify({
#         "Precision": round(precision, 2),
#         "Recall": round(recall, 2),
#         "F1-Score": round(f1, 2),
#         "Onerilen Filmler": onerilen_filmler,
#         "Gercek Ilgili Filmler": gercek_ilgili_filmler
#     })




#filmin türüne göre öneri
# # Film detay rotası
# @app.route('/film/<int:film_id>')
# def film_detay(film_id):
#     film = Film.query.get(film_id)
#     if not film:
#         flash("Film bulunamadı.", "danger")
#         return redirect(url_for('anasayfa'))

#     # Film önerilerini türlere göre al ve benzerlik skorlarını hesapla
#     öneriler = recommender.film_oner_ture_gore(film.title, k=4)  # Film başlığına göre türe dayalı 4 öneri
#     önerilen_filmler = []
    
#     print(f"'{film.title}' için türe göre önerilen filmler ve benzerlik skorları:")
#     for öneri in öneriler:
#         # Önerilen film için türlere dayalı benzerlik skoru hesapla
#         idx_film = recommender.veri[recommender.veri['title'] == film.title].index[0]
#         idx_öneri = recommender.veri[recommender.veri['title'] == öneri].index[0]
#         benzerlik_skoru = recommender.genre_cosine_sim[idx_film, idx_öneri]

#         # Terminale yazdır
#         print(f"Film: {öneri}, Benzerlik Skoru: {benzerlik_skoru:.4f}")

#         # Veritabanından film detaylarını al
#         film_detay = Film.query.filter_by(title=öneri).first()
#         if film_detay:
#             önerilen_filmler.append(film_detay)

#     # Fragman URL'si (geçici)
#     trailer_url = "https://www.youtube.com/embed/dummy_trailer_id"

#     return render_template(
#         'film_detay.html',
#         film=film,
#         trailer_url=trailer_url,
#         önerilen_filmler=önerilen_filmler
#     )



# @app.route('/kontrol_filmler')
# def kontrol_filmler():
#     filmler = Film.query.all()
#     for film in filmler:
#         print(f"Film ID: {film.id}, Başlık: {film.title}")
#     return "Filmler kontrol edildi. Lütfen terminali kontrol edin."


# # Content-based modelini yükle
# recommender = ContentBasedRecommender('islenmisveri.csv')

# @app.route('/oneriler', methods=['GET'])
# def oneriler():
#     if 'user_id' not in session:
#         flash('Lütfen giriş yapınız.', 'danger')
#         return redirect(url_for('giris'))

#     # Kullanıcının izleme geçmişini al
#     kullanici_id = session['user_id']
#     izleme_gecmisi = IzlemeGecmisi.query.filter_by(kullanici_id=kullanici_id).all()
#     izlenen_filmler = [Film.query.get(gecmis.film_id).title for gecmis in izleme_gecmisi]

#     # Kullanıcıya özel öneriler
#     öneriler = recommender.kullanici_tabanli_oner(izlenen_filmler)

#     # Sonuçları döndür
#     return render_template('oneriler.html', öneriler=öneriler, izlenen_filmler=izlenen_filmler)

# İletişim rotası
#@app.route('/iletisim', methods=['GET', 'POST'])
#def iletisim():
#    if request.method == 'POST':
#        isim = request.form.get('isim')
#        email = request.form.get('email')
 #       hizmet_turu = request.form.get('hizmet_turu')
#        mesaj = request.form.get('mesaj')
        # Verileri işleyin veya saklayın
 #       flash('Mesajınız başarıyla gönderildi.', 'success')
#        return redirect(url_for('iletisim'))
#    return render_template('iletisim.html')

