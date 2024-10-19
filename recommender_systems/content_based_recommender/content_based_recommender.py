#############################
# Content Based Recommendation (İçerik Temelli Tavsiye)
#############################

#############################
# Film Overview'larına Göre Tavsiye Geliştirme
#############################

# 1. TF-IDF Matrisinin Oluşturulması: Metinleri matematiksel olarak ölçülebilir hale getir
# 2. Cosine Similarity Matrisinin Oluşturulması: Filmlerin benzerliği
# 3. Benzerliklere Göre Önerilerin Yapılması
# 4. Çalışma Scriptinin Hazırlanması









#################################
# 1. TF-IDF Matrisinin Oluşturulması
#################################

import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)
pd.set_option('display.expand_frame_repr', False)
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity



# https://www.kaggle.com/rounakbanik/the-movies-dataset
data = pd.read_csv(r"C:\Users\ibrah\Desktop\miuulBootcamp\pythonProjects\recommender_systems\datasets\the_movies_dataset\movies_metadata.csv", low_memory=False)  # DtypeWarning kapamak icin
data = data.iloc[0:20000, 0:21]
data.shape

data.columns
# Benzerlik icin odaklanacak oldugumuz degisken
data["overview"].head(10)

# sık kullanılan ve gereksiz etkisi olmayan (in-on-the) gibi kelimeler veriden cikarılacak
# max_features= yeterli bellek bulunmaması durumunda bu arguman ile kısıtlma yapılabilir
tf_idf = TfidfVectorizer(stop_words="english", max_features=5000) # metinin hangi dilde oldugunu belirtiyorum

data[data["overview"].isnull()] # "overview" da eksik ola degerler geldi
data['overview'] = data['overview'].fillna('') # eksik olan degerleri bosluklar ile degistirelim


## fit: fit eder, ilgili islem ne ise onu uygular
## transform: yapılan degisikligi donusturur
tf_idf_matrix = tf_idf.fit_transform(data["overview"])
tf_idf_matrix.shape # satırlar filmler yani "overview"dir. Sutunlarda essiz kelimeler vardır

# data['title'].shape # filmlerin baslıklarına bakarsak, "overview"lar ile aynı sayıdadır

# olusturulan essiz kelimeleri dondurur. Anlamlı anlamsız kelimeler icermektedir
tf_idf.get_feature_names_out()

# tf_idf'in kesisimlerine bakalım. Kelimeler ve filmler eslesmesi
tf_idf_matrix.toarray()








#################################
# 2. Cosine Similarity Matrisinin Oluşturulması
#################################

# bana benzerligini hesaplamak istedigin matrsi ver, istersen tek arguman istersen iki arguman ver
cosine_sim = cosine_similarity(tf_idf_matrix,
                               tf_idf_matrix)


cosine_sim.shape # 20000 nedir: "overview"lardır
cosine_sim[1]  # skorlar geldi. Bunlar 1.indexte yer alan filmin diger her filmle olan benzerlik skoru var









#################################
# 3. Benzerliklere Göre Önerilerin Yapılması
#################################

indices = pd.Series(data.index, index=data['title']) # indexlerde her filmin ismi ve karsılıgında index bilgisi var

indices.index.value_counts() # filmlerden fazla sayıda var. "title"ları tekillestir

indices = indices[~indices.index.duplicated(keep='last')] # en son cekilen filmi alalım
indices.index.value_counts() # coklama kayıtlardan kurtulduk


indices["Cinderella"] # en son gorunen "cindirella" filmini alıyor

indices["Sherlock Holmes"]

# ilgili filmin index bilgisini tutalım
movie_index = indices["Sherlock Holmes"]

# ilgili index ile benzer olan diger indexlere bakalım
cosine_sim[movie_index]

similarity_scores = pd.DataFrame(cosine_sim[movie_index],
                                 columns=["score"])

# ilgil fim ile benzerlik oranı 0 dan buyuk olan filmler
similarity_scores[similarity_scores["score"] > 0]


# en yuksek skora sahip 10 filmin index bilgisi
movie_indices = similarity_scores.sort_values("score", ascending=False)[1:11].index

# ilgili indexlere git ve film isimlerini ver
data['title'].iloc[movie_indices]











#################################
# 4. Çalışma Scriptinin Hazırlanması
#################################

def content_based_recommender(title, cosine_sim, dataframe):
    # index'leri olusturma
    indices = pd.Series(dataframe.index, index=dataframe['title'])
    indices = indices[~indices.index.duplicated(keep='last')]
    # title'ın index'ini yakalama
    movie_index = indices[title]
    # title'a gore benzerlik skorlarını hesapalama
    similarity_scores = pd.DataFrame(cosine_sim[movie_index], columns=["score"])
    # kendisi haric ilk 10 filmi getirme
    movie_indices = similarity_scores.sort_values("score", ascending=False)[1:11].index
    return dataframe['title'].iloc[movie_indices]

content_based_recommender("Sherlock Holmes", cosine_sim, data)

content_based_recommender("The Matrix", cosine_sim, data)

content_based_recommender("The Godfather", cosine_sim, data)

content_based_recommender('The Dark Knight Rises', cosine_sim, data)


def calculate_cosine_sim(dataframe):
    tf_idf = TfidfVectorizer(stop_words='english', max_features=5000)
    dataframe['overview'] = dataframe['overview'].fillna('')
    tf_idf_matrix = tf_idf.fit_transform(dataframe['overview'])
    cosine_sim = cosine_similarity(tf_idf_matrix, tf_idf_matrix)
    return cosine_sim


cosine_sim = calculate_cosine_sim(data)
content_based_recommender('The Dark Knight Rises', cosine_sim, data)
# 1 [90, 12, 23, 45, 67]
# 2 [90, 12, 23, 45, 67]
# 3
