import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class ContentBasedRecommender:
    def __init__(self, csv_file):
        # Veri setini yükle
        self.veri = pd.read_csv(csv_file)
        
        # TF-IDF vektörleştirme (overview kullanılarak)
        self.tfidf = TfidfVectorizer(stop_words='english')
        self.veri['overview'] = self.veri['overview'].fillna('')
        self.tfidf_matrix = self.tfidf.fit_transform(self.veri['overview'])

        # Cosine similarity hesaplama (özete göre)
        self.cosine_sim = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)

        # Türler için TF-IDF vektörleştirme ve benzerlik matrisi oluşturma
        self.veri['genres'] = self.veri['genres'].fillna('')
        self.genre_vectorizer = TfidfVectorizer(tokenizer=lambda x: x.split(','), stop_words='english')
        self.genre_matrix = self.genre_vectorizer.fit_transform(self.veri['genres'])
        self.genre_cosine_sim = cosine_similarity(self.genre_matrix, self.genre_matrix)

        print("Model hazır!")

    def film_oner(self, film_adi, k=10):
        # Film indexini bul
        try:
            idx = self.veri[self.veri['title'] == film_adi].index[0]
        except IndexError:
            return []  # Film bulunamazsa boş liste döndür

        # Benzer filmleri al (özete göre benzerlik)
        sim_skorlari = list(enumerate(self.cosine_sim[idx]))
        sim_skorlari = sorted(sim_skorlari, key=lambda x: x[1], reverse=True)

        # İlk k benzer filmi döndür
        benzer_filmler = [self.veri['title'].iloc[i] for i, skor in sim_skorlari[1:k + 1]]
        return benzer_filmler

    def film_oner_ture_gore(self, film_adi, k=10):
        # Film indexini bul
        try:
            idx = self.veri[self.veri['title'] == film_adi].index[0]
        except IndexError:
            return []  # Film bulunamazsa boş liste döndür

        # Benzer filmleri al (türe göre benzerlik)
        sim_skorlari = list(enumerate(self.genre_cosine_sim[idx]))
        sim_skorlari = sorted(sim_skorlari, key=lambda x: x[1], reverse=True)

        # İlk k benzer filmi döndür
        benzer_filmler = [self.veri['title'].iloc[i] for i, skor in sim_skorlari[1:k + 1]]
        return benzer_filmler

    def kullanici_tabanli_oner(self, izleme_gecmisi, k=10):
        # İzleme geçmişindeki filmleri al
        izlenen_filmler = self.veri[self.veri['title'].isin(izleme_gecmisi)]
        
        # İzlenen filmlerin TF-IDF vektörlerini al
        indices = izlenen_filmler.index
        if len(indices) == 0:
            return []  # İzleme geçmişi boşsa boş liste döndür
        
        # Ortalama vektör (np.asarray kullanılarak np.matrix sorunlarını düzeltme)
        user_vector = np.asarray(self.tfidf_matrix[indices].mean(axis=0))  # NumPy array türüne dönüştür
        cosine_sim_user = cosine_similarity(user_vector, self.tfidf_matrix).flatten()

        # Benzer filmleri sırala
        sim_skorlari = list(enumerate(cosine_sim_user))
        sim_skorlari = sorted(sim_skorlari, key=lambda x: x[1], reverse=True)

        # İlk k öneriyi döndür (izlenen filmleri çıkar)
        öneriler = [self.veri['title'].iloc[i] for i, skor in sim_skorlari if self.veri['title'].iloc[i] not in izleme_gecmisi][:k]
        return öneriler
