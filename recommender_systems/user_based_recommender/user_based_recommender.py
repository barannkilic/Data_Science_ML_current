############################################
# User-Based Collaborative Filtering
#############################################

# Adım 1: Veri Setinin Hazırlanması
# Adım 2: Öneri Yapılacak Kullanıcının İzlediği Filmlerin Belirlenmesi
# Adım 3: Aynı Filmleri İzleyen Diğer Kullanıcıların Verisine ve Id'lerine Erişmek
# Adım 4: Öneri Yapılacak Kullanıcı ile En Benzer Davranışlı Kullanıcıların Belirlenmesi
# Adım 5: Weighted Average Recommendation Score'un Hesaplanması
# Adım 6: Çalışmanın Fonksiyonlaştırılması







#############################################
# Adım 1: Veri Setinin Hazırlanması
#############################################
import pandas as pd

from recommender_systems.arl.arl import recommendation_list

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)
pd.set_option('display.expand_frame_repr', False)

# kullanıcı ve film veri setini olusturalım
def create_user_movie_data():
    import pandas as pd
    movie = pd.read_csv(r"C:\Users\ibrah\Desktop\miuulBootcamp\pythonProjects\recommender_systems\datasets\movie_lens_dataset\movie.csv")
    rating = pd.read_csv(r"C:\Users\ibrah\Desktop\miuulBootcamp\pythonProjects\recommender_systems\datasets\movie_lens_dataset\rating.csv")
    data = movie.merge(rating, how="left", on="movieId") # veri setini birlestir
    comment_counts = pd.DataFrame(data["title"].value_counts())
    rare_movies = comment_counts[comment_counts["count"] <= 10000].index
    common_movies = data[~data["title"].isin(rare_movies)]
    user_movie_data = common_movies.pivot_table(index=["userId"], columns=["title"], values="rating")
    return user_movie_data

user_movie_data = create_user_movie_data()

# Random User alalım:
import pandas as pd
random_user = int(pd.Series(user_movie_data.index).sample(1, random_state=45).values)
random_user









#############################################
# Adım 2: Öneri Yapılacak Kullanıcının İzlediği Filmlerin Belirlenmesi
#############################################
random_user
user_movie_data #hangi kullanıcı ne izlemis
# veri seti kullanıcıya gore indirgendi- veri setinde yer alan tum filmler var
random_user_data = user_movie_data[user_movie_data.index == random_user]

# kullanıcının izlemedigi NaN olan filmleri cıkardık- kullanıcının izledigi filmleri bulalım
movies_watched = random_user_data.columns[random_user_data.notna().any()].tolist()

# Dogrulama yapalım. Veri setinden kullanıcıya ait veri seti eslemesi yapalım
user_movie_data.loc[user_movie_data.index == random_user, user_movie_data.columns == "Abyss, The (1989)"]




len(movies_watched) # kullanıcı bu kadar film izlemis puanlamıs









#############################################
# Adım 3: Aynı Filmleri İzleyen Diğer Kullanıcıların Verisine ve Id'lerine Erişmek
#############################################

# genel veri setini artık izlenen filmler ile indirgeyelim
movies_watched_data = user_movie_data[movies_watched]
movies_watched_data


### kullanıcı ile 1 tane aynı ve 20 tane aynı film izleyenler aynı degil. Bundan dolayı threshold belirle
# her bir kullanıcı kactane film izledi
user_movie_count = movies_watched_data.T.notnull().sum() # kullanıcı filmleri izlemisse true doner bunlar toplanır

# user_Id'yi degisken yap
user_movie_count = user_movie_count.reset_index()

# degisken isimlendirmesi yap
user_movie_count.columns = ["userId", "movie_count"]
user_movie_count

# izleme sayısına gore filtreleme yap
user_movie_count[user_movie_count["movie_count"] > 20]
user_movie_count[user_movie_count["movie_count"] > 20].sort_values("movie_count", ascending=False) # buyukten kucuge sırala

# belilrnen threshold'a gore 'userId' bilgisi ver
user_movie_count[user_movie_count["movie_count"] > 20]["userId"]

# kullanıcının izledigi filmlerin %60'ini izleyen kullanıcıları referans al
percent = len(movies_watched) * 60 / 100
# kullanıcı ile aynı filmleri ve en az %60'ın izleyen kullanıcılar
user_same_movies = user_movie_count[user_movie_count["movie_count"] > percent]["userId"]
user_same_movies













#############################################
# Adım 4: Öneri Yapılacak Kullanıcı ile En Benzer Davranışlı Kullanıcıların Belirlenmesi
#############################################

# Bunun için 3 adım gerçekleştireceğiz:
# 1. Sinan ve diğer kullanıcıların verilerini bir araya getireceğiz.
# 2. Korelasyon df'ini oluşturacağız.
# 3. En benzer bullanıcıları (Top Users) bulacağız

# Sinan ve diğer kullanıcıların verilerini bir araya getireceğiz.
final_data = pd.concat([movies_watched_data[movies_watched_data.index.isin(user_same_movies)],
                      random_user_data[movies_watched]])
### INCELEEE #####
final_data = movies_watched_data[movies_watched_data.index.isin(user_same_movies)]

# veri setinin transpozu, korelasyonu, pivotu, sırala, duplicate kayıtları cıkar
corr_data = final_data.T.corr().unstack().sort_values().drop_duplicates()
# veri setini dataframe yap
corr_data = pd.DataFrame(corr_data, columns=["corr"])
# index isimlerini guncelle
corr_data.index.names = ['user_id_1', 'user_id_2']
# indexleri sutuna ata
corr_data = corr_data.reset_index()
corr_data

# Aradıgımız kullanıcı ozelinde istenilen benzerlikte eslesmeleri bul
top_users = corr_data[(corr_data["user_id_1"] == random_user) & (corr_data["corr"] >= 0.35)][
    ["user_id_2", "corr"]].reset_index(drop=True)
# buyukten kucuge sırala
top_users = top_users.sort_values(by='corr', ascending=False)
# degisken adını degistir
top_users.rename(columns={"user_id_2": "userId"}, inplace=True)


# Kullanıcı ile en benzer kullanıcılar bulundu ancak bu kullanıcıların hangi filme kac puan verdigi bilinmiyor
rating = pd.read_csv(r"C:\Users\ibrah\Desktop\miuulBootcamp\pythonProjects\recommender_systems\datasets\movie_lens_dataset\rating.csv")
# top_users ile rating birlestir
top_users_ratings = top_users.merge(rating[["userId", "movieId", "rating"]], how='inner')
# kullanıcının kendisiyle benzerligini gormemek icin listeden cıkar
top_users_ratings = top_users_ratings[top_users_ratings["userId"] != random_user]
# kullanıcı ile en yuksek korelasyona sahip kullancilar ve bunların izledikleri film ve verdikleri puan var
top_users_ratings












#############################################
# Adım 5: Weighted Average Recommendation Score'un Hesaplanması
#############################################
# onermeyi yapacagımız bir score hesaplanmalı
top_users_ratings["weighted_rating"] = top_users_ratings["corr"] * top_users_ratings["rating"]
top_users_ratings

# film bazında score'un ortalamalarina bakalım
top_users_ratings.groupby("movieId").agg({"weighted_rating": "mean"})
recommendation_data = top_users_ratings.groupby("movieId").agg({"weighted_rating": "mean"})
# indexi sutuna ata
recommendation_data = recommendation_data.reset_index()
recommendation_data

# belirli bir kosul bazında verisetini inceleyelim
recommendation_data[recommendation_data["weighted_rating"] > 2]
# tavsıye edilecek filmler
movies_to_be_recommend = recommendation_data[recommendation_data["weighted_rating"] > 2].sort_values("weighted_rating", ascending=False)
movies_to_be_recommend

# Tavsıye edilecek movieId belli bunlara ait 'title'i ogrenelim
movie = pd.read_csv(r"C:\Users\ibrah\Desktop\miuulBootcamp\pythonProjects\recommender_systems\datasets\movie_lens_dataset\movie.csv")
movie
movies_to_be_recommend.merge(movie[["movieId", "title"]])









#############################################
# Adım 6: Çalışmanın Fonksiyonlaştırılması
#############################################

def create_user_movie_df():
    import pandas as pd
    movie = pd.read_csv('datasets/movie_lens_dataset/movie.csv')
    rating = pd.read_csv('datasets/movie_lens_dataset/rating.csv')
    df = movie.merge(rating, how="left", on="movieId")
    comment_counts = pd.DataFrame(df["title"].value_counts())
    rare_movies = comment_counts[comment_counts["title"] <= 1000].index
    common_movies = df[~df["title"].isin(rare_movies)]
    user_movie_df = common_movies.pivot_table(index=["userId"], columns=["title"], values="rating")
    return user_movie_df

user_movie_df = create_user_movie_df()

# perc = len(movies_watched) * 60 / 100
# users_same_movies = user_movie_count[user_movie_count["movie_count"] > perc]["userId"]


def user_based_recommender(random_user, user_movie_df, ratio=60, cor_th=0.65, score=3.5):
    import pandas as pd
    random_user_df = user_movie_df[user_movie_df.index == random_user]
    movies_watched = random_user_df.columns[random_user_df.notna().any()].tolist()
    movies_watched_df = user_movie_df[movies_watched]
    user_movie_count = movies_watched_df.T.notnull().sum()
    user_movie_count = user_movie_count.reset_index()
    user_movie_count.columns = ["userId", "movie_count"]
    perc = len(movies_watched) * ratio / 100
    users_same_movies = user_movie_count[user_movie_count["movie_count"] > perc]["userId"]

    final_df = pd.concat([movies_watched_df[movies_watched_df.index.isin(users_same_movies)],
                          random_user_df[movies_watched]])

    corr_df = final_df.T.corr().unstack().sort_values().drop_duplicates()
    corr_df = pd.DataFrame(corr_df, columns=["corr"])
    corr_df.index.names = ['user_id_1', 'user_id_2']
    corr_df = corr_df.reset_index()

    top_users = corr_df[(corr_df["user_id_1"] == random_user) & (corr_df["corr"] >= cor_th)][
        ["user_id_2", "corr"]].reset_index(drop=True)

    top_users = top_users.sort_values(by='corr', ascending=False)
    top_users.rename(columns={"user_id_2": "userId"}, inplace=True)
    rating = pd.read_csv('datasets/movie_lens_dataset/rating.csv')
    top_users_ratings = top_users.merge(rating[["userId", "movieId", "rating"]], how='inner')
    top_users_ratings['weighted_rating'] = top_users_ratings['corr'] * top_users_ratings['rating']

    recommendation_df = top_users_ratings.groupby('movieId').agg({"weighted_rating": "mean"})
    recommendation_df = recommendation_df.reset_index()

    movies_to_be_recommend = recommendation_df[recommendation_df["weighted_rating"] > score].sort_values("weighted_rating", ascending=False)
    movie = pd.read_csv('datasets/movie_lens_dataset/movie.csv')
    return movies_to_be_recommend.merge(movie[["movieId", "title"]])



random_user = int(pd.Series(user_movie_df.index).sample(1).values)
user_based_recommender(random_user, user_movie_df, cor_th=0.70, score=4)


