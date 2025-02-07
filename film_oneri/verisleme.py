import pandas as pd
import json

# Veri setini yükle
movies = pd.read_csv('tmdb_5000_movies.csv')

# Gerekli sütunları seçelim
selected_columns = ['title', 'genres', 'runtime', 'vote_average', 'popularity', 'overview']  # İlgili sütunlar
movies_filtered = movies[selected_columns]

# Türleri işleme fonksiyonu
def extract_genres(genres_json):
    try:
        genres = json.loads(genres_json)  # JSON formatındaki türleri ayıkla
        return ", ".join([genre['name'] for genre in genres])
    except (TypeError, json.JSONDecodeError):
        return "Bilinmiyor"

# Türleri işleyelim
movies_filtered['genres'] = movies_filtered['genres'].apply(extract_genres)

# Boş değerler için varsayılan değerler atayalım
movies_filtered['runtime'] = movies_filtered['runtime'].fillna(0)  # Süre boşsa 0
movies_filtered['overview'] = movies_filtered['overview'].fillna('Bu film hakkında bilgi bulunmamaktadır.')  # Özet boşsa varsayılan metin
movies_filtered['vote_average'] = movies_filtered['vote_average'].fillna(0)  # Kullanıcı puanı boşsa 0
movies_filtered['popularity'] = movies_filtered['popularity'].fillna(0)  # Popülerlik boşsa 0

# Temizlenmiş veri setini kaydedelim
movies_filtered.to_csv('islenmisveri.csv', index=False)
print("Tüm veri seti işlenip kaydedildi.")
