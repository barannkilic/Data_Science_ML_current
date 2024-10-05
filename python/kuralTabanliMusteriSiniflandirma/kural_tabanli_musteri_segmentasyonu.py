## GOREV 1
# Soru 1: persone.csv dosyasını okutunuz ve veri seti ile ilgili genel bilgileri elde ediniz.
import numpy as np
import pandas as pd

from functions_conditions_loops_comprehensions.funcitons_conditions_lopps_comprehensions import index

data = pd.read_csv(r"C:\Users\ibrah\Desktop\miuulBootcamp\pythonProjects\data_analysis_with_python\KuralTabanl─▒S─▒n─▒fland─▒rmaProje\persona.csv")

print(f"########### HEAD #############\n{data.head()}")
print(f"########### SHAPE #############\n{data.shape}")
print(f"########### INFO #############")
print(data.info())


# Soru 2: Kac unique SOURCE vardır? Frekansları nelerdir?
print(f"SOURCE degiskeninin {data['SOURCE'].nunique()} adet essiz sınıfı vardır. Ve frakansları sunlardir:\n {data['SOURCE'].value_counts()}")


# SORU 3: Kac unique PRICE vardır?
print(f"PRICE degiskeninin essiz sınıf sayıları {data['PRICE'].nunique()}")


# SORU 4: Hangi PRICE'dan kacar tane satıss gerceklesmistir?
print(f"PRICE'lardan gerceklesen satıs adetleri: {data['PRICE'].value_counts()}")

# SORU 5: Hangi ulkeden kacar tane satıs gercekelsmıstır?
# Yol 1
print(f"Ulkelere gore gerceklesen satıslar: {data['COUNTRY'].value_counts()}")

# YOL 2: Groupby ile cozum
data.groupby("COUNTRY")["PRICE"].count()  # alfabetık sıralar

# Yol 3: Pivot_table ile cozum
data.pivot_table(values="PRICE", index="COUNTRY", aggfunc="count") # alfabetik sıralar


# Soru 6: Ulkelere gore satıslardan toplam ne kadar kazanılmıs?
# Yol 1: Groupby
data.groupby("COUNTRY")["PRICE"].sum()
data.groupby("COUNTRY").agg({"PRICE": "sum"})

# Yol 2: Pivot_table
data.pivot_table(values="PRICE", index="COUNTRY", aggfunc="sum")

# Soru 7: SOURCE turlerıne gore satıs sayıları nedir?
# Yol 1
data.groupby("SOURCE")["PRICE"].count()

# Yol 2
data["SOURCE"].value_counts()


# Soru 8: Ulkelere gore PRICE ortalamaları?
# Yol 1
data.groupby("COUNTRY")["PRICE"].mean()

# Yol 2
data.groupby("COUNTRY").agg({"PRICE": "mean"})

# Yol 3
data.pivot_table(values="PRICE", index="COUNTRY", aggfunc="mean")


# Soru 8: SOURCE'lara gore PRICE ortalamaları?
data.groupby("SOURCE")["PRICE"].mean()

# Yol 2
data.groupby("SOURCE").agg({"PRICE": "mean"})

# Yol 3
data.pivot_table(values="PRICE", index="SOURCE", aggfunc="mean")


# Soru 10: COUNTRY-SOURCE kırılımında PRICE ortalamaları nedir?
data.groupby(["COUNTRY", "SOURCE"]).agg({"PRICE": "mean"})


## GOREV 2
# COUNTRY, SOURCE, SEX, AGE kırılımında ortalama kazanclar nedir?

data.groupby(["COUNTRY", "SOURCE", "SEX", "AGE"]).agg({"PRICE": "mean"}).head()


## GOREV 3
# Cıktıyı PRICE'a gore sıralayınız.
# Oncekı sorudakı cıktıyı daha ıyı gorebılmek ıcın sort_values metodunu azalan olacak sekılde sıralayınız. Cıktıyı agg_df olarak kaydet.

agg_data = data.groupby(["COUNTRY", "SOURCE", "SEX", "AGE"]).agg({"PRICE": "mean"}).sort_values("PRICE", ascending=False)
agg_data.head()



## GOREV 4
#Ucuncu sorunun cıktısında yer alan PRICE dısındakı tum degiskenler isimleridir.
# ipucu: reset_index()
# agg_df.reset_index(inplace=True)

agg_data = agg_data.reset_index()
agg_data.head()


## GOREV 5: AGE degiskenini kategorik degiskene ceviriniz ve agg_df'e ekleyiniz.
# Age sayısal değişkenini kategorik değişkene çeviriniz.
# Aralıkları ikna edici olacağını düşündüğünüz şekilde oluşturunuz.
# Örneğin: '0_18', '19_23', '24_30', '31_40', '41_70'

bins = [0, 18, 23, 30, 40, data["AGE"].max()] # sınıf aralıkları
bins
labels = ["0_18", "19_23", "24_30", "31_40", "41_" + str(data["AGE"].max())]
labels
agg_data["age_categorical"] = pd.cut(agg_data["AGE"], bins, labels=labels)
agg_data.head()

## GOREV 6:
# Yeni level based musterileri tanımlayınız ve veri setine degisken olarak ekleyiniz.
# customers_level_based adında degisken olsun.
# ListComprehensions ile customers_level_based degerleri olusturulduktan sonra bu degerlerin tekıllesitirilmesi gerekmektedir. Ornegin birden fazla su ıfadeden olabilir:
# "USA_ANDROID_MALE_0_18". Bunların groupby'a alıp PRICE ortalamlarını almak gerekmektedir.

agg_data["customers_level_based"] = agg_data[['COUNTRY', 'SOURCE', 'SEX', 'age_categorical']].agg(lambda
                                 x: '_'.join(x).upper(), axis=1)
agg_data.head()

agg_data = agg_data.groupby("customers_level_based").agg({"PRICE": "mean"}).head()

## cıktıyı duzenlemek ıcın
agg_data = agg_data.reset_index()
agg_data.head()

agg_data["customers_level_based"].value_counts()

agg_data.head()



## GOREV 7: Yenı musterılerı segmentlere ayırınız.
# PRICE'a gore segmentlere ayırınız.
# Segmentleri "SEGMENT" isimlendirmesi ile agg_df'e ekleyiniz.
# segmetnleri betimleyiniz

agg_data["SEGMENT"] = pd.qcut(agg_data["PRICE"], 4, labels=["D", "C", "B", "A"])
agg_data.head()

agg_data.groupby("SEGMENT")["PRICE"].mean()


## GOREV 8: Yeni gelen musterileri sınfılandırınız. Ne kadar gelir getirebileceiğini tahmin ediniz.
# 33 Yasında ANDROID kullanan bir Turk Kadını hangi segmente aittir ve ortalama ne kadar gelir kazandırması beklenir

new_user = "BRA_ANDROID_FEMALE_31_40"
agg_data[agg_data["customers_level_based"] == new_user]



print("simge")