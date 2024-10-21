###########################################
# Item-Based Collaborative Filtering
###########################################

# Veri seti: https://grouplens.org/datasets/movielens/

# Adım 1: Veri Setinin Hazırlanması
# Adım 2: User Movie Df'inin Oluşturulması
# Adım 3: Item-Based Film Önerilerinin Yapılması
# Adım 4: Çalışma Scriptinin Hazırlanması




######################################
# Adım 1: Veri Setinin Hazırlanması
######################################
import pandas as pd

from recommender_systems.matrix_factorization.matrix_factorization import user_movie_df

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 500)

movie = pd.read_csv(r"C:\Users\ibrah\Desktop\miuulBootcamp\pythonProjects\recommender_systems\datasets\movie_lens_dataset\movie.csv")
rating = pd.read_csv(r"C:\Users\ibrah\Desktop\miuulBootcamp\pythonProjects\recommender_systems\datasets\movie_lens_dataset\rating.csv")

data = movie.merge(rating, how="left", on="movieId")
data.head()





######################################
# Adım 2: User Movie Df'inin Oluşturulması
######################################

data.head()
data.shape

# Rating sayısı önemli mesela 10000 rating olan filmle 800 rating alan film aynı degil. Threshold belirleriz.

# Essiz film sayısı:
data["title"].nunique()

# Hangi filme kaçar tane yorum gelmiş cunku her filme odaklanmak olmaz
data["title"].value_counts().head()


## 1000'den az yorum alanlari dısarda bırakalım:
# dusuk puan alanı onermeye gerek yok ve hesaplama maliyeti

## Her film kacar kez var yani her film icin kacar 'rating' var
rating_counts = pd.DataFrame(data["title"].value_counts())

## Belirli sayıdan az olan filmler
rating_counts[rating_counts["count"] < 1000]
# Bu filmleri cekelim bunun icin index bilgisi kullanalım
rare_movies = rating_counts[rating_counts["count"] < 1000].index

# Ana veride 'rare_movies'de yer alan filmler dısında olanları getir
common_movies = data[~data["title"].isin(rare_movies)]

# 'rare_movies'leri cıkardıgımız zaman kalan verimizin boyutunu gorelim
common_movies.shape
# yararlı olacak filmlerimizin sayısını gorelim
common_movies["title"].nunique()

data["title"].nunique()

# simdi User Movie veri setini olusturalım
user_movie_data = common_movies.pivot_table(index="userId", columns="title", values="rating")

user_movie_data.shape
user_movie_data.columns # movie name








######################################
# Adım 3: Item-Based Film Önerilerinin Yapılması
######################################

## Onerilebilecek filmlerin benzer olması gerek
# Bu benzerlik durumunu sütunda yer alan filmlerin korelasyolarına bakıcaz
movie_name = "Matrix, The (1999)"
movie_name = "Ocean's Twelve (2004)"
movie_name = user_movie_data[movie_name] # ilgilenilen film cekiliyor

# Veri setine git 'movie_name' ile korelasyona bak
user_movie_data.corrwith(movie_name).sort_values(ascending=False).head(10)

## Veri setinden rastgele film secilsin ve korelasyona bakılsın
movie_name = pd.Series(user_movie_data.columns).sample(1).values[0] # veri setinden rastgele sutun al ve ilk indexini al film ismi gelsin
movie_name = user_movie_data[movie_name] # veri setinden ilgil filmin sütun bilgisi gelsin
user_movie_data.corrwith(movie_name).sort_values(ascending=False).head(10)

# Filmin isminin bir kısmını hatırladık buna gore olan filmleri bulalım
def check_film(keyword, user_movie_data):
    return [column for column in user_movie_data.columns if keyword in column]

check_film("Ocean's", user_movie_data) # ilgili stringi iceren filmleri veriyor
check_film("Holmes", user_movie_data)










######################################
# Adım 4: Çalışma Scriptinin Hazırlanması
######################################

# veri seti olusuyor
def create_user_movie_data():
    import pandas as pd
    movie = pd.read_csv('datasets/movie_lens_dataset/movie.csv')
    rating = pd.read_csv('datasets/movie_lens_dataset/rating.csv')
    data = movie.merge(rating, how="left", on="movieId")
    comment_counts = pd.DataFrame(data["title"].value_counts())
    rare_movies = comment_counts[comment_counts["title"] <= 1000].index
    common_movies = data[~data["title"].isin(rare_movies)]
    user_movie_data = common_movies.pivot_table(index=["userId"], columns=["title"], values="rating")
    return user_movie_data

user_movie_data = create_user_movie_data()

# secilecek filmin veri setiyle koralasyonuna bakılıyor
def item_based_recommender(movie_name, user_movie_df):
    movie_name = user_movie_df[movie_name]
    return user_movie_df.corrwith(movie_name).sort_values(ascending=False).head(10)

item_based_recommender("Matrix, The (1999)", user_movie_df)

# Burada veri setinden rastgele bir film secilip test ediliyor
movie_name = pd.Series(user_movie_df.columns).sample(1).values[0]
item_based_recommender(movie_name, user_movie_df)





