

##################################################
# Pandas Alıştırmalar
##################################################

import numpy as np
import seaborn as sns
import pandas as pd
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

#########################################
# Görev 1: Seaborn kütüphanesi içerisinden Titanic veri setini tanımlayınız.
#########################################
data = sns.load_dataset("titanic")
data.head()
#########################################
# Görev 2: Yukarıda tanımlanan Titanic veri setindeki kadın ve erkek yolcuların sayısını bulunuz.
#########################################
data["sex"].value_counts()



#########################################
# Görev 3: Her bir sutuna ait unique değerlerin sayısını bulunuz.
#########################################

data.nunique()

#########################################
# Görev 4: pclass değişkeninin unique değerleri bulunuz.
#########################################

data["pclass"].unique()


#########################################
# Görev 5:  pclass ve parch değişkenlerinin unique değerlerinin sayısını bulunuz.
#########################################
data[["pclass", "parch"]].nunique()


#########################################
# Görev 6: embarked değişkeninin tipini kontrol ediniz. Tipini category olarak değiştiriniz. Tekrar tipini kontrol ediniz.
#########################################
data["embarked"].dtype
data["embarked"] = data["embarked"].astype("category")
data["embarked"].dtype

#########################################
# Görev 7: embarked değeri C olanların tüm bilgelerini gösteriniz.
#########################################
data[data["embarked"] == "C"]



#########################################
# Görev 8: embarked değeri S olmayanların tüm bilgelerini gösteriniz.
#########################################
data[data["embarked"] != "S"]


#########################################
# Görev 9: Yaşı 30 dan küçük ve kadın olan yolcuların tüm bilgilerini gösteriniz.
#########################################
data[(data["age"] < 30) & (data["sex"] == "female")].head()


#########################################
# Görev 10: Fare'i 500'den büyük veya yaşı 70 den büyük yolcuların bilgilerini gösteriniz.
#########################################
data[(data["fare"] > 500) | (data["age"] > 70)].head()


#########################################
# Görev 11: Her bir değişkendeki boş değerlerin toplamını bulunuz.
#########################################
data.isnull().sum()



#########################################
# Görev 12: who değişkenini dataframe'den düşürün.
#########################################
data.drop("who", axis=1).head()


#########################################
# Görev 13: deck değikenindeki boş değerleri deck değişkenin en çok tekrar eden değeri (mode) ile doldurunuz.
#########################################
data["deck"].fillna(data["deck"].mode()[0], inplace=True)




#########################################
# Görev 14: age değikenindeki boş değerleri age değişkenin medyanı ile doldurun.
#########################################

data["age"].fillna(data["age"].median(), inplace=True)

#########################################
# Görev 15: survived değişkeninin Pclass ve Cinsiyet değişkenleri kırılımınında sum, count, mean değerlerini bulunuz.
#########################################
data.groupby(["pclass", "sex"]).agg({"survived": ["sum", "mean", "count"]})

#########################################
# Görev 16:  30 yaşın altında olanlar 1, 30'a eşit ve üstünde olanlara 0 vericek bir fonksiyon yazınız.
# Yazdığınız fonksiyonu kullanarak titanik veri setinde age_flag adında bir değişken oluşturunuz oluşturunuz. (apply ve lambda yapılarını kullanınız)
#########################################

# YOL 1:
def age_30(age):
    if age < 30:
        return 1
    else:
        return 0
data["age"]
data["age_flag"] = data["age"].apply(lambda x: 1 if x < 30 else 0)
data["age_flag"].head()

#########################################
# Görev 17: Seaborn kütüphanesi içerisinden Tips veri setini tanımlayınız.
#########################################
import seaborn as sns
df = sns.load_dataset("tips")
df.head()

#########################################
# Görev 18: Time değişkeninin kategorilerine (Dinner, Lunch) göre total_bill  değerlerinin toplamını, min, max ve ortalamasını bulunuz.
#########################################
df.groupby("time").agg({"total_bill": ["min", "max", "mean"]})


#########################################
# Görev 19: Günlere ve time göre total_bill değerlerinin toplamını, min, max ve ortalamasını bulunuz.
#########################################
df.groupby(["day", "time"]).agg({"total_bill": ["min", "max", "mean"]})


#########################################
# Görev 20:Lunch zamanına ve kadın müşterilere(kosulları altında) ait total_bill ve tip  değerlerinin day'e göre toplamını, min, max ve ortalamasını bulunuz.
#########################################
df[(df["time"] == "Lunch") & (df["sex"] == "Female")].groupby("day").agg({"total_bill": ["sum", "min", "max", "mean"],
                                                                          "tip": ["sum", "min", "max", "mean"]})


#########################################
# Görev 21: size'i 3'ten küçük, total_bill'i 10'dan büyük olan siparişlerin ortalaması nedir?
#########################################
df.loc[(df["size"] < 3) & (df["total_bill"] > 10), "total_bill"].mean()


#########################################
# Görev 22: total_bill_tip_sum adında yeni bir değişken oluşturun. Her bir müşterinin ödediği totalbill ve tip in toplamını versin.
#########################################

df["total_bill_tip_sum"] = df["total_bill"] + df["tip"]
df.head()

#########################################
# Görev 23: total_bill_tip_sum değişkenine göre büyükten küçüğe sıralayınız ve ilk 30 kişiyi yeni bir dataframe'e atayınız.
#########################################


new_df = df.sort_values("total_bill_tip_sum", ascending=False) # ascending: artan demek False olurse artma azal demek
new_df.head()