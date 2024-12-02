#############################
# Model-Based Collaborative Filtering: Matrix Factorization
#############################
## Blank'leri doldurmak icin user'lar ve movie'ler icin varsayılan 'latent feature' agırlıkları
# var olan veri seti uzerinden bulunur ve bu agırlıklar ile var olmayan gozlemler icin tahmin yapılır
from os.path import split
from tabnanny import verbose

# !pip install surprise
import pandas as pd
from surprise import Reader, SVD, Dataset, accuracy
from surprise.model_selection import GridSearchCV, train_test_split, cross_validate

from recommender_systems.user_based_recommender.user_based_recommender import rating

pd.set_option('display.max_columns', None)
pd.set_option("display.width", 500)

# Adım 1: Veri Setinin Hazırlanması
# Adım 2: Modelleme
# Adım 3: Model Tuning
# Adım 4: Final Model ve Tahmin







#############################
# Adım 1: Veri Setinin Hazırlanması
#############################

movie = pd.read_csv(r"C:\Users\ibrah\Desktop\miuulBootcamp\pythonProjects\recommender_systems\datasets\movie_lens_dataset\movie.csv")
movie
rating = pd.read_csv(r"C:\Users\ibrah\Desktop\miuulBootcamp\pythonProjects\recommender_systems\datasets\movie_lens_dataset\rating.csv")
rating
# veri setini birlestir
data = movie.merge(rating, how="left", on="movieId")
data

# Kolay bir takip edilme icin 4 movie ve 4 movieId kullanilacak
movie_ids = [130219, 356, 4422, 541]
movies = ["The Dark Knight (2011)",
          "Cries and Whispers (Viskningar och rop) (1972)",
          "Forrest Gump (1994)",
          "Blade Runner (1982)"]

# ornek veri seti olusturalım
sample_data = data[data.movieId.isin(movie_ids)] # anaset icinde belirlenen movie'leri bul
sample_data
sample_data.shape

# user-movie dataseti olsuturalım
sample_data.pivot_table(index="userId", columns="title", values="rating")
user_movie_data = sample_data.pivot_table(index="userId", columns="title", values="rating")
user_movie_data
user_movie_data.shape

# ilgili 'surprise' kutuphanesi  'rating'in degisim aralıgını istiyor
reader = Reader(rating_scale=(1, 5))
# kullandıgın dataframe'i kutuphaneın anladıgı dile donustur
data = Dataset.load_from_df(sample_data[["userId",
                                         "movieId",
                                         "rating"]], reader)












##############################
# Adım 2: Modelleme: Olusturdugumuz veriseti uzerinden 'train-test' ayrımı yapıp. Bir model kuracagız
##############################
# veriyi 'train-test' olarak bolelim. %75 train, %25 test olacak
train_set, test_set = train_test_split(data, test_size=.25)

# matris_factorization yontemini kullancak oldugumuz fonksiyon
svd_model = SVD()
# train_set uzerinden ogren
svd_model.fit(train_set)
# modeli 'train_set' uzerinde kurduk 'test_set' uzerinde kullanalim ve tahmin sonuclarini gorelim
predictions = svd_model.test(test_set)
predictions
## Prediction(uid=54719.0, iid=356, r_ui=4.0, est=4.0569452844344465, details={'was_impossible': False})
# uid: userId, iid= itemId= movieId, r_ui= kullanıcının verdigi rating, est(estimate)=modelin tahmini

## gercek degerler ile tahminler arasındaki fark 'hata'dir. ortalama ne kadar oldugunu ogrenelim
accuracy.rmse(predictions) # rmse: root mean squared error = 0.93
# ornegın kullanıcı 4 puan verecekken buna (4 + 0.93) veya (4 - 0.93) diyebiliriz

# 1 kullanıcı icin tahminde bulunalım
svd_model.predict(uid=1.0, iid=541, verbose=True) # 'Blade Runner'.. verbose=True --> sonucları goster

svd_model.predict(uid=1.0, iid=356, verbose=True)
# kullanıcının gercek degeri yok bulalım
sample_data[sample_data["userId"] == 1]







##############################
# Adım 3: Model Tuning: Modelin tahmin performansını arttırmaya calısmak
##############################
## dıssal parametre = kullanıcı tarafından ayarlanabilen = hiperparametrelerini optimize etmek
## Hiperparametreler:
# 1. epoch sayısı: iterasyon sayısı yani agırlıkların guncellenme sayısı
# 2. factor sayısı: user-movie'lerin feature'ları gizli ozellikler
# 3. learning rate: ogrenme oranı. Her adımda ogrenme oranı ne kadar degisecek.
# Kucuk olursa: model yavas ogrenir Buyuk olursa: model hızlı ogrenir ama optimum cozume ulasmayabilir veya dengeli bir sonuc bulamayabilir
# 4. reg_all: teoremde yer alan 'lambda'

# hiperparametreler icin verilen degerleri sırayla dene. Ve degerleri esle yani: (5_0.002)
parameter_grid = {"n_epochs": [5, 10, 20],
                  "lr_all": [0.002, 0.005, 0.007]} # cok toy bir degisim oldu her pc de calısması icin

gs = GridSearchCV(SVD, # model nesnesi
                  parameter_grid, # uygulanacak olan olası parametre ciftlerini dene
                  measures=['rmse', 'mae'], # mae (mean absolute error):  gerçek değerler ile tahmin edilen değerler arasındaki farkların mutlak değerlerinin ortalamasıdır.
                  cv=3, # 3 katlı capraz dogrulama yap. Veri setini 3'e bol 2 parcasıyla model kur 1 parcasıyla test et. Tum kombınasyon olana kadar devam et. Yanı verisetini 'a-b-c' olarak bol. 'a-b'train 'c' test. / 'a-c'egit 'b' test gibi gibi
                  n_jobs=-1, # islemcileri full performans ile kullan
                  joblib_verbose=True) # islemler gerceklesirken raporlama yap

# islem tamamlansın. Olası en iyi hiperparametre setini ver
gs.fit(data)






param_grid = {'n_epochs': [5, 10, 20],
              'lr_all': [0.002, 0.005, 0.007]}


gs = GridSearchCV(SVD,
                  param_grid,
                  measures=['rmse', 'mae'],
                  cv=3,
                  n_jobs=-1,
                  joblib_verbose=True)

gs.fit(data)

# modelin en iyi skorunu gorelim
gs.best_score["rmse"]
# sonucu veren en iyi parametreler.
gs.best_params["rmse"] # en ıyı sonuc epoch:10 lr_all: 0.002 olacak sekilde elde edilmis











##############################
# Adım 4: Final Model ve Tahmin
##############################
# Model olusturma basamagına tekrar gidip. Daha iyi bparametreleri SVD adımında kullanmamız lazım

# degisiklik yapılabilecek parametreler
dir(svd_model)

# ilk modelin 'epoch' sayısı
svd_model.n_epochs

## 'epoch' sayısını guncellemek icin tekrardan model kurmamız gerekiyor
# en iyi parametre degerlerini hatırlayalım
gs.best_params["rmse"]
svd_model = SVD(**gs.best_params["rmse"]) # n_epochs=10 ve lr_all=0.002 yazmak yerine kısa yol

# veri sayısını artırıp butun veriyi kullanalım. Tum veri seti 'train_set' oldu
data = data.build_full_trainset()
svd_model.fit(data) # model fit ediliyor

# 1. user icin 541 id'li (Blade Runner) filmi icin prediction
svd_model.predict(uid=1.0, iid=541, verbose=True)

sample_data[sample_data["userId"] == 1]
 # sonucta 'Blade Runner' icin 4 rating verilmis tahminimiz 4.17

# 1-5 arasında ki bir skala icin 0.17 sapma tartısmaya acık ne cok iyi ne cok kotu





