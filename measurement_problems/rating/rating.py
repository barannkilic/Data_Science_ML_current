###################################################
# Rating Products
###################################################

# - Average
# - Time-Based Weighted Average
# - User-Based Weighted Average
# - Weighted Rating


############################################
# Uygulama: Kullanıcı ve Zaman Ağırlıklı Kurs Puanı Hesaplama
############################################

import pandas as pd
import math
import scipy.stats as st
from sklearn.preprocessing import MinMaxScaler

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 500)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

# (50+ Saat) Python A-Z™: Veri Bilimi ve Machine Learning
# Puan: 4.8 (4.764925)
# Toplam Puan: 4611
# Puan Yüzdeleri: 75, 20, 4, 1, <1
# Yaklaşık Sayısal Karşılıkları: 3458, 922, 184, 46, 6

data = pd.read_csv(r"C:\Users\ibrah\Desktop\miuulBootcamp\pythonProjects\measurement_problems\datasets\course_reviews.csv")
data.head()
data.shape

# rating dagılımı
data["Rating"].value_counts() # puanlara gore kategoriler

data["Questions Asked"].value_counts() # soru sorma sayıları

data.groupby("Questions Asked").agg({"Questions Asked": "count", # soru sormaya saysıına gore toplam sorulan soru ve rating ortalamalaı
                                   "Rating": "mean"})


data.head()





####################
# Average
####################

# Ortalama Puan
data["Rating"].mean()



####################
# Time-Based Weighted Average: Son zamanlarda kı trend degısebılır. Gozden bır sey kacmaması adına zamana gore ortalama saglıklı olur
####################
# Puan Zamanlarına Göre Ağırlıklı Ortalama

data.head()
data.info()

data["Timestamp"] = pd.to_datetime(data["Timestamp"]) # degiskenin tipi zamana cevrilmeli

current_date = pd.to_datetime('2021-02-10 0:0:0') # bugunun tarihi

data["days"] = (current_date - data["Timestamp"]).dt.days # analiz yapılan tarih ile yorum yapılan tarih arası fark alınır ve gun cinsinden ifade edilir

# 30 gunden once yapılan yorumların ortalaması
data.loc[data["days"] <= 30, "Rating"].mean()

# son 30-90 gun arasında yapılan yorumların ortalaması
data.loc[(data["days"] > 30) & (data["days"] <= 90), "Rating"].mean()

# son 90-180 gun arası yorumların ortalaması
data.loc[(data["days"] > 90) & (data["days"] <= 180), "Rating"].mean()

# 180 gunden fazla yorumların ortalaması
data.loc[(data["days"] > 180), "Rating"].mean()

### GUN CINSINDEN AGIRLIKLANDIRMA
###### NOT: belirli zaman aralıklarına farklı bır sekılde yaklasalım. Her farklı zaman ıcın farklı bır agırlık verelım
data.loc[data["days"] <= 30, "Rating"].mean() * 28/100 + \
    data.loc[(data["days"] > 30) & (data["days"] <= 90), "Rating"].mean() * 26/100 + \
    data.loc[(data["days"] > 90) & (data["days"] <= 180), "Rating"].mean() * 24/100 + \
    data.loc[(data["days"] > 180), "Rating"].mean() * 22/100



def time_based_weighted_average(dataframe, w1=28, w2=26, w3=24, w4=22):
    return dataframe.loc[data["days"] <= 30, "Rating"].mean() * w1 / 100 + \
           dataframe.loc[(dataframe["days"] > 30) & (dataframe["days"] <= 90), "Rating"].mean() * w2 / 100 + \
           dataframe.loc[(dataframe["days"] > 90) & (dataframe["days"] <= 180), "Rating"].mean() * w3 / 100 + \
           dataframe.loc[(dataframe["days"] > 180), "Rating"].mean() * w4 / 100

time_based_weighted_average(data)

time_based_weighted_average(data, 30, 26, 22, 22)



####################
# User-Based Weighted Average: Herkesin verdigi puan aynı mı olmalı
####################

data.head()

data.groupby("Progress").agg({"Rating": "mean"}) # izleme oranına gore verilen puanlar

data.loc[(data["Progress"] <= 50), "Rating"].mean()  # kursun %50'sinden azını izleyenlerin verdigi puan ortalaması

data.loc[data["Progress"] <= 10, "Rating"].mean() * 22 / 100 + \
    data.loc[(data["Progress"] > 10) & (data["Progress"] <= 45), "Rating"].mean() * 24 / 100 + \
    data.loc[(data["Progress"] > 45) & (data["Progress"] <= 75), "Rating"].mean() * 26 / 100 + \
    data.loc[(data["Progress"] > 75), "Rating"].mean() * 28 / 100



def user_based_weighted_average(dataframe, w1=22, w2=24, w3=26, w4=28):
    return dataframe.loc[dataframe["Progress"] <= 10, "Rating"].mean() * w1 / 100 + \
           dataframe.loc[(dataframe["Progress"] > 10) & (dataframe["Progress"] <= 45), "Rating"].mean() * w2 / 100 + \
           dataframe.loc[(dataframe["Progress"] > 45) & (dataframe["Progress"] <= 75), "Rating"].mean() * w3 / 100 + \
           dataframe.loc[(dataframe["Progress"] > 75), "Rating"].mean() * w4 / 100


user_based_weighted_average(data, 20, 24, 26, 30)


####################
# Weighted Rating
####################

def course_weighted_rating(dataframe, time_w=50, user_w=50):
    return time_based_weighted_average(dataframe) * time_w/100 + user_based_weighted_average(dataframe)*user_w/100
# iceride yer alan 2 fonksiyonun argumanlarını kendi veya ana fonksiyon icinde tanımlayabiliriz

course_weighted_rating(data)

course_weighted_rating(data, time_w=40, user_w=60)










