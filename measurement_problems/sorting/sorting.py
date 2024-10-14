###################################################
# Sorting Products
###################################################

###################################################
# Uygulama: Kurs Sıralama
###################################################
import pandas as pd
import math
import scipy.stats as st
from sklearn.preprocessing import MinMaxScaler

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

data = pd.read_csv(r"C:\Users\ibrah\Desktop\miuulBootcamp\pythonProjects\measurement_problems\datasets\product_sorting.csv")
print(data.shape)
data.head(10)






####################
# Sorting by Rating
####################

data.sort_values("rating", ascending=False).head(20) # Rating'lere gore buyukten kucuge sırala



####################
# Sorting by Comment Count or Purchase Count
####################

data.sort_values("purchase_count", ascending=False).head(20)
data.sort_values("commment_count", ascending=False).head(20)




####################
# Sorting by Rating, Comment and Purchase
####################
# purchase ve comment'i rating seklınde; 1_5 arasında degerlere cevirelim
data["purchase_count_scaled"] = MinMaxScaler(feature_range=(1, 5)).fit(data[["purchase_count"]]).transform(data[["purchase_count"]]) # skala 1-5 arası verdi, fit etti, dönüstürdü

data.describe().T

data["comment_count_scaled"] = MinMaxScaler(feature_range=(1, 5)). \
    fit(data[["commment_count"]]). \
    transform(data[["commment_count"]])

# 3 farklı degiskene gore ağırlıklandırma: SIMDI UC FARKLI DEGISKENE GORE 'SKORLAR' OLUSTU
(data["comment_count_scaled"] * 32 / 100 +
 data["purchase_count_scaled"] * 26 / 100 +
 data["rating"] * 42 / 100)


def weighted_sorting_score(dataframe, w1=32, w2=26, w3=42):
    return (dataframe["comment_count_scaled"] * w1 / 100 +
            dataframe["purchase_count_scaled"] * w2 / 100 +
            dataframe["rating"] * w3 / 100)


data["weighted_sorting_score"] = weighted_sorting_score(data)

data.sort_values("weighted_sorting_score", ascending=False).head(20)

# veri bilimi ile ilgili kursları 'weighted_sorting_score'a gore sırala
data[data["course_name"].str.contains("Veri Bilimi")].sort_values("weighted_sorting_score", ascending=False).head(20)














####################
# Bayesian Average Rating Score
####################

# Sorting Products with 5 Star Rated
# Sorting Products According to Distribution of 5 Star Rating

# puanların dagılımını kullanarak agırlıklı olasılıksal bir ortalama hesabı yapacagız
def bayesian_average_rating(n, confidence=0.95):
    if sum(n) == 0:
        return 0
    K = len(n)
    z = st.norm.ppf(1 - (1 - confidence) / 2)
    N = sum(n)
    first_part = 0.0
    second_part = 0.0
    for k, n_k in enumerate(n):
        first_part += (k + 1) * (n[k] + 1) / (N + K)
        second_part += (k + 1) * (k + 1) * (n[k] + 1) / (N + K)
    score = first_part - z * math.sqrt((second_part - first_part * first_part) / (N + K + 1))
    return score


data.head()

# veride apply ile gez: degiskenlerde tek tek islem yap(sutunlarda)
data["bar_score"] = data.apply(lambda x: bayesian_average_rating(x[["1_point",
                                                                "2_point",
                                                                "3_point",
                                                                "4_point",
                                                                "5_point"]]), axis=1)
# kendı yaptıgımız
data.sort_values("weighted_sorting_score", ascending=False).head(20)

# bayesci yaklasıma gore sıralama: sadece 'rating'lere bakılarak sıralama yapıldı
data.sort_values("bar_score", ascending=False).head(20)
data[data["course_name"].str.contains("Veri Bilimi")].sort_values("bar_score", ascending=False).head(20)

# kurs isimlerinden 5 ve 1. indexlere gore kursları getirelim
data[data["course_name"].index.isin([5, 1])].sort_values("bar_score", ascending=False)











####################
# Hybrid Sorting: BAR Score + Diğer Faktorler
####################

# Rating Products
# - Average
# - Time-Based Weighted Average
# - User-Based Weighted Average
# - Weighted Rating
# - Bayesian Average Rating Score: Puanları kırpmaktadır. Olasılıksal bir ortalamadır

# Sorting Products
# - Sorting by Rating
# - Sorting by Comment Count or Purchase Count
# - Sorting by Rating, Comment and Purchase
# - Sorting by Bayesian Average Rating Score (Sorting Products with 5 Star Rated): Puanları dagılımı uzerınden yenı bır score olustu
# - Hybrid Sorting: BAR Score + Diğer Faktorler


def hybrid_sorting_score(dataframe, bar_w=60, wss_w=40):
    bar_score = dataframe.apply(lambda x: bayesian_average_rating(x[["1_point",
                                                                     "2_point",
                                                                     "3_point",
                                                                     "4_point",
                                                                     "5_point"]]), axis=1)
    wss_score = weighted_sorting_score(dataframe)# yukarıda purchaese,comment ve rating ile hesaplanacak sekilde tanımlandı

    return bar_score * bar_w/100 + wss_score * wss_w/100


data["hybrid_sorting_score"] = hybrid_sorting_score(data)

data.sort_values("hybrid_sorting_score", ascending=False).head(20)

data[data["course_name"].str.contains("Veri Bilimi")].sort_values("hybrid_sorting_score", ascending=False).head(20)








############################################
# Uygulama: IMDB Movie Scoring & Sorting
############################################

import pandas as pd
import math
import scipy.stats as st
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

data_ = pd.read_csv(r"C:\Users\ibrah\Desktop\miuulBootcamp\pythonProjects\measurement_problems\datasets\movies_metadata.csv",
                 low_memory=False)  # DtypeWarning kapamak icin

data = data_[["title", "vote_average", "vote_count"]] # baslık - oy_ortalaması - oy_sayisi

data.head()
data.shape






########################
# Vote Average'a Göre Sıralama
########################

data.sort_values("vote_average", ascending=False).head(20)

data["vote_count"].describe([0.10, 0.25, 0.50, 0.70, 0.80, 0.90, 0.95, 0.99]).T # betimsel istatistikleri

# oy sayısı 400'den buyuk olanlari sirala
data[data["vote_count"] > 400].sort_values("vote_average", ascending=False).head(20)

from sklearn.preprocessing import MinMaxScaler

data["vote_count_score"] = MinMaxScaler(feature_range=(1, 10)). \
    fit(data[["vote_count"]]). \
    transform(data[["vote_count"]])

########################
# vote_average * vote_count
########################

data["average_count_score"] = data["vote_average"] * data["vote_count_score"]

data.sort_values("average_count_score", ascending=False).head(20)




########################
# IMDB Weighted Rating
########################


# weighted_rating = (v/(v+M) * r) + (M/(v+M) * C)

# r = vote average
# v = vote count
# M = minimum votes required to be listed in the Top 250
# C = the mean vote across the whole report (currently 7.0)

# Film 1:
# r = 8 : ortalama puan
# M = 500 :  gereken oy sayısı
# v = 1000 : filmin aldıgı oy sayısı

# (1000 / (1000+500))*8 = 5.33


# Film 2:
# r = 8
# M = 500
# v = 3000

# (3000 / (3000+500))*8 = 6.85

# (1000 / (1000+500))*9.5

# Film 1:
# r = 8
# M = 500
# v = 1000

# Birinci bölüm:
# (1000 / (1000+500))*8 = 5.33

# İkinci bölüm:
# 500/(1000+500) * 7 = 2.33

# Toplam = 5.33 + 2.33 = 7.66


# Film 2:
# r = 8
# M = 500
# v = 3000

# Birinci bölüm:
# (3000 / (3000+500))*8 = 6.85

# İkinci bölüm:
# 500/(3000+500) * 7 = 1

# Toplam = 7.85

######################################################
# weighted_rating = (v/(v+M) * r) + (M/(v+M) * C)

# r = vote average: ortalama puan
# v = vote count: oy sayısı
# M = minimum votes required to be listed in the Top 250: gereken min oy sayısı
# C = the mean vote across the whole report (currently 7.0):  yıgın ortalaması



M = 2500
C = data['vote_average'].mean()

def weighted_rating(r, v, M, C):
    return (v / (v + M) * r) + (M / (v + M) * C)

data.sort_values("average_count_score", ascending=False).head(20)

# Deadpool filmi
weighted_rating(7.40000, 11444.00000, M, C)

# Inception
weighted_rating(8.10000, 14075.00000, M, C)

# Esaretin bedeli
weighted_rating(8.50000, 8358.00000, M, C)

data["weighted_rating"] = weighted_rating(data["vote_average"],
                                        data["vote_count"], M, C)

data.sort_values("weighted_rating", ascending=False).head(10)










####################
# Bayesian Average Rating Score
####################

# 12481                                    The Dark Knight
# 314                             The Shawshank Redemption
# 2843                                          Fight Club
# 15480                                          Inception
# 292                                         Pulp Fiction



def bayesian_average_rating(n, confidence=0.95):
    if sum(n) == 0:
        return 0
    K = len(n)
    z = st.norm.ppf(1 - (1 - confidence) / 2)
    N = sum(n)
    first_part = 0.0
    second_part = 0.0
    for k, n_k in enumerate(n):
        first_part += (k + 1) * (n[k] + 1) / (N + K)
        second_part += (k + 1) * (k + 1) * (n[k] + 1) / (N + K)
    score = first_part - z * math.sqrt((second_part - first_part * first_part) / (N + K + 1))
    return score
# esaretin bedeli
bayesian_average_rating([34733, 4355, 4704, 6561, 13515, 26183, 87368, 273082, 600260, 1295351])
# baba
bayesian_average_rating([37128, 5879, 6268, 8419, 16603, 30016, 78538, 199430, 402518, 837905])

data_ = pd.read_csv(r"C:\Users\ibrah\Desktop\miuulBootcamp\pythonProjects\measurement_problems\datasets\imdb_ratings.csv")
data = data_.iloc[0:, 1:]


data["bar_score"] = data.apply(lambda x: bayesian_average_rating(x[["one", "two", "three", "four", "five",
                                                                "six", "seven", "eight", "nine", "ten"]]), axis=1)
data.sort_values("bar_score", ascending=False).head(20)


# Weighted Average Ratings
# IMDb publishes weighted vote averages rather than raw data averages.
# The simplest way to explain it is that although we accept and consider all votes received by users,
# not all votes have the same impact (or ‘weight’) on the final rating.

# When unusual voting activity is detected,
# an alternate weighting calculation may be applied in order to preserve the reliability of our system.
# To ensure that our rating mechanism remains effective,
# we do not disclose the exact method used to generate the rating.
#
# See also the complete FAQ for IMDb ratings.


# Ağırlıklı Ortalama Puanlar
# IMDb, ham veri ortalamaları yerine ağırlıklı oy ortalamaları yayınlar.
# Bunu açıklamanın en basit yolu, kullanıcıların aldığı tüm oyları kabul etmemize ve dikkate almamıza rağmen,
# Tüm oylar final derecelendirmesi üzerinde aynı etkiye (veya 'ağırlığa') sahip değildir.

# Olağandışı oylama aktivitesi tespit edildiğinde,
# Sistemimizin güvenilirliğini korumak için alternatif bir ağırlıklandırma hesaplaması uygulanabilir.
# Derecelendirme mekanizmamızın etkinliğini sürdürmesini sağlamak,
# Derecelendirmeyi oluşturmak için kullanılan tam yöntemi açıklamıyoruz.
#
# Ayrıca IMDb derecelendirmeleri için tam SSS'ye bakın.