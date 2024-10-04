################################
# PANDAS SERIES
#################################
import pandas as pd
from fontTools.unicodedata import block
from matplotlib.lines import lineStyles
from unicodedata import numeric

s = pd.Series([10, 12, 34, 55, 4, 5])
s
type(s)

s.index # index bilgisi
s.dtype # elamanların veri tipi
s.size # eleman sayısı
s.ndim # boyut bilgisi
s.values # degerlere erisim

type(s.values) # index bilgisi ile ilgilenilmediginden ndarray döndürür

s.head(3) # ilk 3 gozlem gelir
s.tail(3) # sondan 3 gozlem gelir




#############################
# VERI OKUMA (READING DATA) :Dış kaynaklı verileri okuma
#########################
import pandas as pd

# df = pd.read_csv("path")  PD'YE TIKLA DIGER FONKSYONLARI GOR

# pandas cheatsheet






#########################
# VERIYE HIZLI BAKIS (QUICK LOOK AT DATA)
############################
import pandas as pd
import seaborn as sns

df = sns.load_dataset("titanic") # bir gemi yolculugu yolcuların hayatta kalma durumlarını ınceleyen bir veri seti
df.head()

# survived degiskeni ilgili degiskenin hayatta kalma durumudur. "BAGIMLI DEGISKEN"DIR

df.tail()
df.shape # boyut bilgisi
df.info()

# int kesikli, float sureklii,
# object-category: kategorik degiskendir

df.columns # degisken isimleri
df.index

df.describe() # ozet istatistikler
df.describe().T # okunabilirlik acısından transpozu al

df.isnull().values.any() # herhangi bir degerde bosluk var mı????

df.isnull().values.any()
df.isnull().sum()  # her degıskende yer alan eksık degerlerın toplam adedı

## kac farklı sınıf var
df["sex"].head()
df["sex"].value_counts()

df["class"].value_counts()






########################################
# Pandas'ta secim islemleri   (Selection in Pandas)
###################################

import pandas as pd
import seaborn as sns

df = sns.load_dataset("titanic")
df.head()

df.index
df[0:13]

# indexlerde silme
df.drop(0, axis=0).head() # satirlardan (axis) 0.sütun silindi

delete_index = [1, 3, 5, 7]
df.drop(delete_index, axis=0) # satirlardan listede bulunan indexler silindi

# bu islem kalici degil, kalici olmasi icin atama yapmak gerek
# df.drop(delete_index, axis=0, inplace=True)   "inplace": kalıcı olması icin

####### Degiskeni Indexe cevirmek (Variable to index)

df["age"].head()
df.age.head()

df.index = df["age"] # age degiskeni indexe atandı
df.index

df.drop("age", axis=1, inplace=True) # "age" degiskenini silelim
df.head()


########### İndex To Variable
# YOL 1
df["age"] = df.index
df.head()

# YOL 2
df.drop("age", axis=1, inplace=True)
df.head()

df = df.reset_index().head()   # indexte yer alan degeri silicek sütun olarak atayacak
df.head()







###############################3
# Degiskenler Uzerinde Islemler
##############################
import pandas as pd
import seaborn as sns
df = sns.load_dataset("titanic")
df.head()


### cıktı da yer alan "..." dan kurtulmak
pd.set_option("display.max_columns", None)  # gosterilecek olan max kolon sayısı olmasın
df.head()



# harhangı bır degiskenın varlıgını sorgulamak
"age" in df
"sex" in df

# ozellıkle bir degisken secmek
df["age"].head()
df.age.head()

df["age"].head()
type(df["age"].head())   # tipi pandas series olur ve islem yapılamaz

type(df[["age"]].head()) # "[[]]" iki koseli parantez kullanılırsa "dataframe" olarak kalıcaktır

df[["age"]].head()


### dataframe'de bırden fazla degisken secmek
# yol 1
df[["age", "alive"]].head()

# yol 2
column_names = ["age", "adult_male", "alive"]
df[column_names].head()

### Dataframe'e yeni degisken eklemek

df["age2"] = df["age"] ** 2
df.head()

df.age.head()


df["age3"] = df["age"] / df["age2"]
df.head()

df.age.head()


### Degisken silmek

df.drop("age3" , axis = 1).head() # kalici degil

# birden fazla silmek
column_names = ["age", "adult_male", "alive"]
df.drop(column_names, axis=1).head()


df.head()


### belirli ifadeyi barındıran degiskeni silmek
df.head()

df.loc[:, df.columns.str.contains("age")].head()  # tum satirlari secip sütunlarda str islemi yapıp age iceren sütunları verir
df.loc[:, ~df.columns.str.contains("age")].head()  # age icermeyen sütunları goster





###################################
# loc & iloc: secim islemleri icin kullanılan ozel yapılardır
################################

import pandas as pd
import seaborn as sns
pd.set_option("display.max_columns", None)
df = sns.load_dataset("titanic")
df.head()

## iloc (integer based selection): numpy, listelerden alısık oldugumuz index bilgisi vererek secim islemi
df.iloc[0:3] # 0'da 3'e kadar olanlar "3 DAHİL DEGİL" !!!!!!!!!!!!!!
df.iloc[0, 0]



## loc (label based selection): mutlak olarak indexler'de yer alan label'lara gore secim yapar
df.loc[0:3] # 0'dan 3'e kadar "3 DAHİL" !!!!!!!!!!!!!!


### Satirlarda 0'dan 3'e kadar gidelim, sütunlardan da degisken secelim

# iloc:
df.iloc[0:3, "age"] # hata vericek
df.iloc[0:3, 0:3]

df.loc[0:3, "age"]

### NOT: SATIR VEYA SÜTUNLARDAKI DEGERLERIN BIZZAT KENDILERINE ERISMEK ISTIYORSAK loc kullanıyoruz


column_names = ["age", "embarked", "alive"]
df.loc[0:3, column_names]









#################################33
# Kosullu Secim (Conditional Selection)
################################
import pandas as pd
import seaborn as sns
pd.set_option("display.max_columns", None)
df = sns.load_dataset("titanic")
df.head()

### veri setinde yas>50 olanlara eriselim
df[df["age"] > 50].head()

# yas>50 kac kisi var
df[df["age"] > 50].age.count()
df[df["age"] > 50]["age"].count()


### yas>50 olan kisilerin "class" degiskenindeki degerleri
df.loc[df["age"] > 50, "class"].head()   # degisken aradıgımız icin "loc" geldi

# yas bilgisi de gelsin
df.loc[df["age"] > 50, ["age", "class"]].head()


### yas > 50 olan erkekler
df.loc[(df["age"] > 50) & (df["sex"] == "male"), ["age", "class", "sex"]].head() # aynı anda 2 kosul varsa "()" icerisine almalısın

##### NOT:iterrows()
### yas > 50 olan erkekler ve yolculuk icin cherbourg limanından binmis olsun

df.loc[(df["age"] > 50)
       & (df["sex"] == "male")
       & (df["embark_town"] == "Cherbourg"),
       ["age", "sex", "embark_town"]].head()


### yas > 50 olan erkekler  ve yolculuk icin "chebourg" ya da "southampton limanlari

df.loc[(df["age"] > 50)
       & (df["sex"] == "male")
       & (df["embark_town"] == "Cherbourg") | (df["embark_town"] == "Southampton"),
       ["age", "sex", "embark_town"]].head()


## NOT: Bir degiskenin sınıfları ve sınıf sayıları
df["embark_town"].unique()
df["embark_town"].nunique()


## degiskene ait frekanslar
df["embark_town"].value_counts()

df_new = df.loc[(df["age"] > 50)
       & (df["sex"] == "male")
       & (df["embark_town"] == "Cherbourg") | (df["embark_town"] == "Southampton"),
       ["age", "sex", "embark_town"]]

df_new["embark_town"].value_counts()  # yaptıgımız kosullu islem sonucunda "embark_town"da iki sınıf kaldı










##########################################
# Toplulastirma & Gruplama:   (Aggregation & Grouping)
###################################

# - count()
# - first()
# - last()
# - mean()
# - median()
# - min()
# - max()
# - std()
# - var()
# - sum()
# - pivot table

import pandas as pd
import seaborn as sns
pd.set_option("display.max_columns", None)
df = sns.load_dataset("titanic")
df.head()


## yas ortalaması
df["age"].mean()



## kadınların ve erkeklerin yas ortalaması
# yol 1
df.groupby("sex")["age"].mean()
# yol 2
df.groupby("sex").agg("age").mean()



## kadınların ve erkeklerin yas ortalaması ve toplamı
df.groupby("sex").agg({"age": "mean"})   # cinsiyet kırılımında yasların ortalaması

df.groupby("sex").agg({"age": ["mean", "sum"]}) # cinsiyet kırılımında yasların ortalaması ve toplamı

df.groupby("sex").agg({"age": ["mean", "sum", "min", "max"]}) # cinsiyet kırılımında yasların ortalaması, toplamı, min ve max yaslar



## gemiye binis limanı ile ilgili frekans bilgisi de ver

df.groupby("sex").agg({"age": ["mean", "sum"],
                       "embark_town": "count"})


## cinisyet kırılımında yas ve hayatta kalma bilgileri
df.groupby("sex").agg({"age": ["mean", "sum"],
                       "survived": "mean"})

## farklı kategorilere gore kırılım yapıp degerlendırme yap

df.groupby(["sex", "embark_town"]).agg({"age": ["mean", "sum"],
                                        "survived": "mean"})  # cinsiyete ve limana gore kırılım gerceklesir

df.groupby(["sex", "embark_town", "class"]).agg({"age": ["mean", "sum"],
                                                 "survived": "mean"}) # cinsiyete, limana ve sınıfa gore kırılım yapıldı

df.groupby(["sex", "embark_town", "class"]).agg({"age": ["mean", "sum"],
                                                 "survived": "mean",
                                                 "sex": "count"}) # cinsiyetei limana ve sınıfa gore kırılım ve kisi frekans bilgisi










####################################
# Pivot Table: kırılımlar acısından degerlendırmek ve ıstenılen ozet ıstatıstıgı gormeye yarar
################################
import pandas as pd
import seaborn as sns
pd.set_option("display.max_columns", None)
df = sns.load_dataset("titanic")
df.head()


### yas ve gemiye binme lokasyonu acısından pivot tablo olustur bunların kesisiminde yas bilgisi ya da survived

df.pivot_table("survived", "sex", "embarked")  ## hayatta kalmanın ortalaması, satirda "sex" sütunda "embarked" olacak



# pivot_table'in on tanımlı argumanı "mean"dir.

df.pivot_table("survived", "sex", "embarked", aggfunc="std")



## embarked ile bazı degiskenleri de boyut olarak ekleyelim
df.pivot_table("survived", "sex", ["embarked", "class"], aggfunc="std") # sütunlar 2 seviyeli satir 1 seviyeli


df.pivot_table("survived", ["sex", "who"], ["embarked", "class"], aggfunc="std")  # sütunlar ve satirlar 2 seviyeli



### hem cinsiyet  hem lokasyon hem de yaslara gore kırılım ve hayatta kalma oranları (yaslar sayısal, gruplandır)

# yaslar kategorik olsun. "cut": hangı kategorilere ayrılacagı bılınıyorsa (0-10 cocuk de vb.)  "qcut": bilinmiyorsa ceyrekler kullanılır
df["new_age"] = pd.cut(df["age"], [0, 10, 18, 25, 40, 90])
df.head()

df.pivot_table("survived", ["sex"], ["new_age"]) # default olaram "mean" veriyor

df.pivot_table("survived", "sex", ["new_age", "class"]) # kategorik deger iceren sınıf ekleniyor



## NOT: CIKTILAR YANYANA OLSUNN
pd.set_option("display.width", 500)











##############################################
# Apply: Satir ya da sutunlarda otomatik olarak fonksiyon calıstırmayı saglar
# & Lambda: Bir fonksiyon tanımlama sekli, Kullan at fonksiyon
##################################
import pandas as pd
import seaborn as sns
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 500)
df = sns.load_dataset("titanic")
df.head()


df["age2"] = df["age"] * 2
df["age3"] = df["age"] * 5
df.head()

### PROBLEM: Degiskenlere fonksiyon uygulamak istiyorum ama cok degisken var
(df["age"] / 10).head()
(df["age2"] / 10).head()
(df["age3"] / 10).head()
 # bu fonksiyon bu sekilde uzun oluyor

for column in df.columns:
    if "age" in column:
        print(column)


## bu sekilde yapalım
for column in df.columns: # sutunlarda gez
    if "age" in column:  # eger "age" iceriyorsa
        print((df[column] / 10).head())  # bu islemi yap

# list comprehensions ile
[print((df["age"] / 10).head) for column in df.columns if "age" in column]

## ama kaydetmedik simdi kaydedelim
for column in df.columns:
    if "age" in column:
        df[column] = df[column] / 10  # su an kaydedildi

df.head()



###### APPLY & LAMBDA İLE UYGULANACAK
df[["age", "age2", "age3"]].apply(lambda x: x / 10).head()

# programatik hal
df.loc[:, df.columns.str.contains("age")].apply(lambda x: x / 10).head()  # x'ler degiskenleri temsil ediyor

# daha karısık. fonksıyon uygulanan dataframe'leri standartlastırsın
df.loc[:, df.columns.str.contains("age")].apply(lambda x: (x - x.mean()) / x.std()).head() # icerisinde "age" olanları sececek ve onları standartlastıracak




## fonksıyonu dısarda tanımlayıp kullanalım
def standart_scaler(column_name):
    return (column_name - column_name.mean()) / column_name.std()

df.loc[:, df.columns.str.contains("age")].apply(standart_scaler).head() # dısarıda olusturulan bır fonksıyon ıle yapıyoruz


# YAPILAN ISLEMI KAYDEDELIM
df.loc[:, ["age", "age2", "age3"]] = df.loc[:, df.columns.str.contains("age")].apply(standart_scaler)

df.loc[:, df.columns.str.contains("age")] = df.loc[:, df.columns.str.contains("age")].apply(standart_scaler) # sol ve sag tarafta istenilen yer secildi ve sag tarafta uygulandı


## CIKTIMIZI GORELİM_____YOL 1
df.loc[:, df.columns.str.contains("age")].head()

## YOL 2
df.head()















##########################################
# Birlestirme (Join) Islemleri
#######################################
# concat: hızlı yaygın metod
# merge yontemı


import pandas as pd
import numpy as np
m = np.random.randint(1, 30, size=(5, 3))  # 1-30 arasında (5,3)'luk numpy array'i olusur

df1 = pd.DataFrame(m, columns=["var1", "var2", "var3"])
df2 = df1 + 99

#### CONCAT ILE
## 2 dataframe'i "index" bazında birlestir
pd.concat([df1, df2])  # indexler 0 1 2 3 4 - 0 1 2 3 4 olarak tekrar eder.
pd.concat([df1, df2], ignore_index=True) # indexler ardısık artar


## 2 dataframe'i "sutun" bazında birlestir
pd.concat([df1, df2], axis=1) # ısımlerı ardısık yapmıyor
pd.concat([df1, df2], axis=1, ignore_index=True)



##### MERGE ILE BIRLESTIRME YONTEMI
df1 = pd.DataFrame({"employees": ["john", "dennis", "mark", "maria"],
                    "group": ["accounting", "engineering", "engineering", "hr"]})

df2 = pd.DataFrame({"employees": ["john", "dennis", "mark", "maria"],
                    "start_date": [2010, 2009, 2014, 2019]})

df1
df2

pd.merge(df1, df2) # hangi degiskene gore birlestirecegiini bilmeden yapıyor
pd.merge(df1, df2, on="employees") # birlestirilecek degisken argumanı verildi

## AMAÇ: Her calısanın mudurunun bilgisine erismek
df3 = pd.merge(df1, df2)
df3

df4 = pd.DataFrame({"group": ["accounting", "engineering", "hr"],
                    "manager": ["Caner", "Mustafa", "Berkcan"]})
df4

pd.merge(df3, df4, on="group")













###########################################
# VERİ GORSELLESTİRME: MATPLOTLIB & SEABORN
########################################


########### MATPLOTLIB: Low level veri gorsellestirme aracıdır. Seaborn'a kıyasla daha fazla caba gerektırır

# - kategorik degisken: sutun grafikle gosterilir. Matplotlib'de "barplot", seaborn iceriisnde "countplot"
# - sayısal degisken: histogram - kutu grafik (boxplot), ikiside dagılım gosterır boxplot ekstra aykırı degerlerı  gosterir


## KATEGORIK DEGISKEN GORSELLESTIRME
import pandas as pd
import seaborn as sns
pd.set_option("display.max_columns", None)
df = sns.load_dataset("titanic")
df.head()

import matplotlib.pyplot as plt
# Amac: Cinsiyet, class, embarkee, who' kategoriktir.
df["sex"].value_counts()
df["sex"].value_counts().plot(kind="bar")  # kind: grafigin tipi
plt.show() # tıpkı print gibi ekrana bastırması icin kullanılır

df["class"].value_counts().plot(kind="bar")

df["embarked"].value_counts().plot(kind="bar")

df["alive"].value_counts().plot(kind="bar")
df.info()





### SAYISAL DEGISKEN GORSELLESTIRME
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 500)
df = sns.load_dataset("titanic")
df.head()

# hıstogram
plt.hist(df["age"]) # histogramı sec ardından igili degiskeni ver
plt.show()

# boxplot: genel dagılım dısındakı gozlemlerı yakalar yanı aykırı degerlerı
plt.boxplot(df["fare"])
plt.show()

plt.boxplot(df["parch"])
plt.show()




################################
### MATPLOLIB'IN OZELLIKLERI
############################
import numpy as no
import pandas as pd
import matplotlib.pyplot as plt
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 500)



############
# plot
#########
x = np.array([1, 8])
y = np.array([0, 150])

# degerler arasına cizgi ceker
plt.plot(x, y)
plt.show()

# ilgili noktalara nokta koymak. belirlenen noktalar isaretlendir
plt.plot(x, y, "o")
plt.show()

# daha fazla nokta olursa
x = np.array([2, 4, 6, 8, 10])
y = np.array([1, 3, 5, 7, 9])

plt.plot(x, y)
plt.show()

plt.plot(x, y, "o")
plt.show()



##############
# marker: isaretleyici
#############
y = np.array([13, 28, 11, 100])

plt.plot(y, marker="o")
plt.show()

# baska isaret
plt.plot(y, marker="*")
plt.show()



###############
# line
############
y = np.array([13, 28, 11, 100])

plt.plot(y)
plt.show()

# cigi yerıne baska bır sey
plt.plot(y, linestyle="dashed")
plt.show()

plt.plot(y, linestyle="dotted")
plt.show()

plt.plot(y, linestyle="dashdot", color="y")   # renk ozellıgı eklenıyor
plt.show()

#################
# Multiple Lines: Matplotlib'in katmanlı yapısı sayesınde
##############
x = np.array([23, 18, 31, 10])
y = np.array([13, 28, 11, 100])

plt.plot(x)
plt.plot(y)
plt.show()




###########################
# Labels
#######################
x = np.arange(80, 130, 5) # 80'den 130'a 5'er artır
y = np.arange(240, 340, 10) # 240'dan 340'a 10'ar artır

plt.plot(x,y)
plt.show()

## grafige baslık verelim
plt.title("Bu ana başlık")

## x eksenine isimlendirme
plt.xlabel("X ekseni isimlendirme")

## y eksenine isimlendirme
plt.ylabel("Y ekseni isimlendirme")

## ızgara ekleyelim
plt.grid()
plt.show()



###############################
# Subplots:. Birden fazla gorsel
###########################
# plot 1
x = np.arange(80, 130, 5)
y = np.arange(240, 340, 10)
plt.subplot(1, 2, 1) # 1 satırlık 2 sutunluk grafigın 1.sini olustur.
plt.title("1")
plt.plot(x, y)
plt.show()

# plot 2
x = np.array([8, 8, 9, 9, 10, 15, 11, 15, 12, 15])
y = np.array([24, 20, 26, 27, 29, 30, 30, 98, 26, 10 ])
plt.subplot(1, 2, 2) # 1 satırlık 2 sutunluk grafıgın 2. grafıgı
plt.title("2")
plt.plot(x, y)
plt.show()






######################################
# SEABORN: High level, daha az caba daha cok is
################################
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

df = sns.load_dataset("tips")
df.head()
df.info()

## KATEGORIK DEGISKENLER
df["sex"].value_counts()
sns.countplot(x=df["sex"], data=df) # ilgili degiskeni x eksenine ve verisetini arguman olarak veriyoruz
plt.show()

## matplotlib'de nasıl yapılıyor
df["sex"].value_counts().plot(kind="bar")
plt.show()


## SAYISAL DEGISKENLER
sns.boxplot(x=df["total_bill"])
plt.show()

sns.histplot(x=df["total_bill"])
plt.show()


#### PANDAS ILE HISTOGRAM
df["total_bill"].hist()
plt.show()















#######################################################################
# GELİŞMİŞ FONKSİYONEL KEŞİFÇİ VERİ ANALİZİ (ADVANCED FUNCTIONAL EXPLORATORY DATA ANALYSIS)
######################################################################




###################################
# 1. Genel Resim
#################################3
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 500)
df = sns.load_dataset("titanic")
df.head()

## genel bilgi almak icin kullanılan fonksiyonlar
df.head()
df.tail()
df.shape
df.info()
df.columns
df.index
df.describe().T # sayısal degiskenlerin betımsel istatistikleri
df.isnull().values.any() # herhangi bir degiskende eksik deger var mı?
df.isnull().sum() # degiskenlerde yer alan eksik degerlerin toplamı


### Genel resmi veren fonksiyon
def check_df(dataframe, head=5):
    print("###################### Shape ######################")
    print(dataframe.shape)
    print("\n################## Types #######################")
    print(dataframe.dtypes)
    print("\n############### Head ###########################")
    print(dataframe.head(head))
    print("\n############### Tail ###########################")
    print(dataframe.tail(head))
    print("\n############### NA ###########################")
    print(dataframe.isnull().sum())
    print("\n############### Quantiles ###########################")
    print(dataframe.describe([0, 0.05, 0.50, 0.95, 0.99]).T)


check_df(df)


# yeni dataset uzerınde functıon'ı deneyelim
df = sns.load_dataset("tips")
check_df(df)










########################################################################
# 2. Kategorik Degisken Analizi (Analysis of Categorical Variables)
#######################################################################
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 500)
df = sns.load_dataset("titanic")
df.head()

df["embarked"].value_counts() # sınıf sayıları (sınıflara ait frekanslar)
df["embarked"].unique() # unique sınıfları
df["embarked"].nunique() # unique sınıf sayısı


## Amac: kategorik degiskenleri yakalamak
# 1. tip seklinde kontrol et
# 2. tip seklinde bizi atlatmıs ama farklı tipte görünüp gercekte kategorik olan (sinsirella degisken)

categorical_column = [column for column in df.columns if str(df[column].dtypes) in ["category", "object", "bool"]]
categorical_column # icerisinde kategorikler var evet ama "survived" degiskeni de kategorik ama burada yazmıyor

# simdi 2.tip. Yani tipi "int, float" olup essiz degeri belli degerden kucuk olanlari yakala
numeric_but_categorical = [column for column in df.columns if df[column].nunique() < 10 and df[column].dtypes in ["int64", "float64"]]
numeric_but_categorical

## Kardinalitesi Yüksek Degisken: Ölçülemeyecek kadar, acıklanabılırlık tasımayacak kadar sınıfı vardır demek (isim_soyisim)

categorical_but_cardinal = [column for column in df.columns if df[column].nunique() > 20 and str(df[column].dtypes) in ["category", "object"]]
# degiskenin tipi "object" ya da "category" ise ve essiz sınf sayısı 20'den fazla ise bunları yakala
categorical_but_cardinal # cıktısı bos boyle bır degısken yok

# categorical_column'u gunccellemek gerel
categorical_column = categorical_column + numeric_but_categorical
categorical_column # artık "categeory","object" ve sinsirella degiskenler bır arada

### eger kardinal degısken olsaydı bunları categorical_column'lardan cıkarmak gerekirdi. Örneğin:
categorical_column = [column for column in categorical_column if column not in categorical_but_cardinal]
categorical_column

# bu degiskenleri dataset'den alalım
df[categorical_column].head()

# bu degıskenler amacımızla tutarlı mı?
df[categorical_column].nunique()


# sayısal degıskenler ne durumda bakalım o zaman "categorical_column"da olmayanlar sayısaldır
[column for column in df.columns if column not in categorical_column]




### PURPOSE OF THE FUNCTION:
# 1. Kendisine girilen degerlerin frekansına baksın
# 2. Sınıfların %'lik bilgisini döndürsün

def categorical_summary(dataframe, column_name):
    print(pd.DataFrame({column_name: dataframe[column_name].value_counts(),
                        "Ratio": 100 * dataframe[column_name].value_counts() / len(dataframe)}))
    print("########################################\n") # birden fazla degisken gelirse ara cizgi

categorical_summary(df, "survived")
categorical_summary(df, "sex")

# "categorical_column"ların hepsine uygula
for column in categorical_column:
    categorical_summary(df, column)



########################################################################
# 2. Kategorik Degisken Analizi 2 (Analysis of Categorical Variables)
#######################################################################



## "categorical_summary" founction'ı ileri seviyeye tasıyıp grafık cızdılerım

def categorical_summary(dataframe, column_name, plot=False):
    print(pd.DataFrame({column_name: dataframe[column_name].value_counts(),
                        "Ratio": 100 * dataframe[column_name].value_counts() / len(dataframe)}))
    print("########################################\n")

    if plot: # plot=True ise
        sns.countplot(x=dataframe[column_name], data=dataframe)
        plt.show(block=True)

categorical_summary(df, "sex") # grafiksiz
categorical_summary(df, "sex", plot=True) # grafikli
categorical_summary(df, "survived", plot=True)



# fonksyıonu tekrardan loop'a sokalım
for column in categorical_column:
    categorical_summary(df, column, plot=True)

## NOT: TİP DEGİSTİRME, "astype()"















########################################################################
# 2. Sayısal Degisken Analizi (Analysis of Numerical Variables)
#######################################################################
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 500)
df = sns.load_dataset("titanic")
df.head()

df[["age", "fare"]].describe().T # ozet istatistikler

## numeric degiskenleri secme
numeric_column = [column for column in df.columns if df[column].dtypes in ["int64", "float64"]]
numeric_column

## bazı degıskenler sayısal gorunumunde ama sayısal degıl
numeric_column = [column for column in numeric_column if column not in categorical_column]
numeric_column


## "numeric_column" icin analiz fonksiyonu
def numerical_summary(dataframe, column_name):
    quantiles = [0.05, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 0.95, 0.99]
    print(dataframe[column_name].describe(quantiles).T)

numerical_summary(df, "age")

## degıskenlerın fazla olması durumunda sayısal degıskenlerı gezmesı ıcın
for column in numeric_column:
    print(f"\n\n{str(column).upper()}")
    numerical_summary(df, column)


### grafık ekleyelim
def numerical_summary(dataframe, column_name, plot=False):
    quantiles = [0.05, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 0.95, 0.99]
    print(dataframe[column_name].describe(quantiles).T)

    if plot:
        dataframe[column_name].hist()  # ilgili degiskene ait hist grafigi
        plt.xlabel(column_name) # x eksenine degisken adı
        plt.title(str(column_name).upper()) # baslıga degısken adı
        plt.show()

numerical_summary(df, "age")
numerical_summary(df, "age", plot=True)


for column in numeric_column:
    print(f"\n\n{str(column).upper()}")
    numerical_summary(df, column, plot=True)
    plt.show()












##############################################################
# Degiskenlerin Yakalanması ve Otomatik Olarak Ele Alınması
#############################################################
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 500)
df = sns.load_dataset("titanic")
df.head()
df.info()

## PURPOSE: Oyle bir funciton yazalım ki bize:
# - kategorik degisken
# - sayısal degisken
# - kategorik ama kardnial degisken
## listelerini dondursun


def grab_column_names(dataframe, categorical_threshold=10, cardinal_threshold=20): ## degısken sayısal olsa dahı essiz degerı 10'dan kucukse categorical, categorical degiskenin essiz degeri 20'den buyukse cardinal
    """
    Veri setindeki kategorik, numerik ve kategorik fakat kardninal degiskenlerin isimlerini verir.

    Args:
    dataframe: dataframe
        Degisknelerin bulundugu dataset
    categorical_threshold: int, float
        Bir degiskenin kategorik degisken olması icin essiz deger sayısının 10'dan kucuk olması gerekir
    cardinal_threshold: int, flaot
        Bir kategorik degiskenin essiz deger sayısı 20'den  buyukse kardinal degisken olur

    Returns:
    categorical_columns: list
        Kategorik degisken listesi
    numerical_columns: list
        Numerik degisken listesi
    categorical_but_cardinal: list
        Kategorik görünümlü kardinal degisken listesi

    Notes:
        categorical_columns + numerical_columns + categorical_but_cardinal = toplam degisken sayısı
        numerical_but_categorical categorical_columns'un icerisinde
        Return olan 3 lsite toplamı toplam degisken sayısına esittir.
    """

    categorical_columns = [column for column in df.columns if str(df[column].dtypes) in ["category", "object", "bool"]]

    numeric_but_categorical = [column for column in df.columns if df[column].nunique() < 10 and df[column].dtypes in ["int64", "float64", 'int32']]

    # bu problem ıcın gecerlı olmayan, kardinal degiskenler
    categorical_but_cardinal = [column for column in df.columns if df[column].nunique() > 20 and str(df[column].dtypes) in ["category", "object"]]

    categorical_columns = categorical_columns + numeric_but_categorical
    categorical_columns = [column for column in categorical_columns if column not in categorical_but_cardinal] # kardinal varsa burada duzenleme yapılır

    numeric_columns = [column for column in df.columns if df[column].dtypes in ["int64", "float64", 'int32']]
    numeric_columns = [column for column in numeric_columns if column not in categorical_columns]

    print(f"Observations: {dataframe.shape[0]}")  # 0.indexten gelenler gozlemler
    print(f"Variables: {dataframe.shape[1]}")     # 1. indexten gelenler degiskenler
    print(f"categorical_columns: {len(categorical_columns)}")  #boyut
    print(f"numeric_columns: {len(numeric_columns)}") #boyut
    print(f"categorical_but_cardinal: {len(categorical_but_cardinal)}")
    print(f"numeric_but_categorical: {len(numeric_but_categorical)}")

    return categorical_columns, numeric_columns, categorical_but_cardinal


categorical_columns, numeric_columns, categorical_but_cardinal = grab_column_names(df)

categorical_columns
numeric_columns
categorical_but_cardinal


## dıger fonksıyonları getırelım

def categorical_summary(dataframe, column_name, plot=False):
    print(pd.DataFrame({column_name: dataframe[column_name].value_counts(),
                        "Ratio": 100 * dataframe[column_name].value_counts() / len(dataframe)}))
    print("########################################\n")

    if plot: # plot=True ise
        sns.countplot(x=dataframe[column_name], data=dataframe)
        plt.show(block=True)

categorical_summary(df, "sex")

for column in categorical_columns:
    categorical_summary(df, column)


#### SAYISAL
def numerical_summary(dataframe, column_name, plot=False):
    quantiles = [0.05, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 0.95, 0.99]
    print(dataframe[column_name].describe(quantiles).T)

    if plot:
        dataframe[column_name].hist()  # ilgili degiskene ait hist grafigi
        plt.xlabel(column_name) # x eksenine degisken adı
        plt.title(str(column_name).upper()) # baslıga degısken adı
        plt.show()

numerical_summary(df, "age")

for column in numeric_columns:
    print(f"\n{str(column).upper()}")
    numerical_summary(df, column, plot=True)






###### BONUS:
# Amac: Dataset'de yer alan bool veri tipteki degiskenleri bul int cevir. categorical_summary farklı sekılde kullan
df = sns.load_dataset("titanic")
df.info()

for column in df.columns:
    if df[column].dtypes == "bool":
        df[column] = df[column].astype(int)

df.info()

# fonksıyonu tekrar calıstır
categorical_columns, numeric_columns, categorical_but_cardinal = grab_column_names(df)
categorical_columns

def categorical_summary(dataframe, column_name, plot=False):
    print(pd.DataFrame({column_name: dataframe[column_name].value_counts(),
                        "Ratio": 100 * dataframe[column_name].value_counts() / len(dataframe)}))
    print("########################################\n")

    if plot: # plot=True ise
        sns.countplot(x=dataframe[column_name], data=dataframe)
        plt.show(block=True)

for column in categorical_columns:
    print(f"\n{str(column).upper()}")
    categorical_summary(df, column, plot=True)

















############################################################################
# Hedef Degisken Analizi (Analysis of Target Variables): elimizdeki "survived" degiskenini kategorik ve numeric degiskenler bakımından analiz etmek
#################################################################
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 500)
df = sns.load_dataset("titanic")

## bool tipte olanalrı int yap
for column in df.columns:
    if df[column].dtypes == "bool":
        df[column] = df[column].astype(int)


def grab_column_names(dataframe, categorical_threshold=10, cardinal_threshold=20): ## degısken sayısal olsa dahı essiz degerı 10'dan kucukse categorical, categorical degiskenin essiz degeri 20'den buyukse cardinal
    """
    Veri setindeki kategorik, numerik ve kategorik fakat kardninal degiskenlerin isimlerini verir.

    Args:
    dataframe: dataframe
        Degisknelerin bulundugu dataset
    categorical_threshold: int, float
        Bir degiskenin kategorik degisken olması icin essiz deger sayısının 10'dan kucuk olması gerekir
    cardinal_threshold: int, flaot
        Bir kategorik degiskenin essiz deger sayısı 20'den  buyukse kardinal degisken olur

    Returns:
    categorical_columns: list
        Kategorik degisken listesi
    numerical_columns: list
        Numerik degisken listesi
    categorical_but_cardinal: list
        Kategorik görünümlü kardinal degisken listesi

    Notes:
        categorical_columns + numerical_columns + categorical_but_cardinal = toplam degisken sayısı
        numerical_but_categorical categorical_columns'un icerisinde
        Return olan 3 lsite toplamı toplam degisken sayısına esittir.
    """

    categorical_columns = [column for column in df.columns if str(df[column].dtypes) in ["category", "object", "bool"]]

    numeric_but_categorical = [column for column in df.columns if df[column].nunique() < 10 and df[column].dtypes in ["int64", "float64", 'int32']]

    # bu problem ıcın gecerlı olmayan, kardinal degiskenler
    categorical_but_cardinal = [column for column in df.columns if df[column].nunique() > 20 and str(df[column].dtypes) in ["category", "object"]]

    categorical_columns = categorical_columns + numeric_but_categorical
    categorical_columns = [column for column in categorical_columns if column not in categorical_but_cardinal] # kardinal varsa burada duzenleme yapılır

    numeric_columns = [column for column in df.columns if df[column].dtypes in ["int64", "float64", 'int32']]
    numeric_columns = [column for column in numeric_columns if column not in categorical_columns]

    print(f"Observations: {dataframe.shape[0]}")  # 0.indexten gelenler gozlemler
    print(f"Variables: {dataframe.shape[1]}")     # 1. indexten gelenler degiskenler
    print(f"categorical_columns: {len(categorical_columns)}")  #boyut
    print(f"numeric_columns: {len(numeric_columns)}") #boyut
    print(f"categorical_but_cardinal: {len(categorical_but_cardinal)}")
    print(f"numeric_but_categorical: {len(numeric_but_categorical)}")

    return categorical_columns, numeric_columns, categorical_but_cardinal

categorical_columns, numeric_columns, categorical_but_cardinal = grab_column_names(df)


df.head()

# "survived" kategorik bundan dolayı mevcut fonksıyonumuzla bır bakalaım
categorical_summary(df, "survived", plot=True)


# insanların hayatta kalma durumunu etkıleyen sey nedır????

######################################################
## Hedef Degiskeninin Kategorik Degiskenler ile Analizi
###################################################

df.groupby("sex").agg({"survived": "mean"}) # iki kategorik degisken hakkında kısa bilgi

df.groupby("pclass").agg({"survived": "mean"})

def target_summary_with_cat(dataframe, target, categorical_column):
    print(pd.DataFrame({"TARGET_MEAN": dataframe.groupby(categorical_column)[target].mean()}))

target_summary_with_cat(df,"survived", "sex")


## tum kategorık degıskenler ıle hedef degısken analızı
for column in categorical_columns:
    target_summary_with_cat(df, "survived", column)


### verileri "cat_summary"den gecırdıkten sonra kategorık ve hedeflerı "target_summary_with_cat"e koyarsak. Ozet ıstatıstıklerı alırız





######################################################
## Hedef Degiskeninin Sayısal Degiskenler ile Analizi
###################################################

df.groupby("age")["survived"].mean() # olmaz

df.groupby("survived")["age"].mean() # yas ortalamalarını alırız
df.groupby("survived").agg({"age": "mean"}) # CIKTISI DAHA DUZGUN

df.groupby("survived")["fare"].mean()


def target_summary_with_num(dataframe, target, numerical_column):
    print(dataframe.groupby(target).agg({numerical_column: "mean"}))

target_summary_with_num(df,"survived", "age")

for column in numeric_columns:
    target_summary_with_num(df, "survived", column)















##########################################################
## Korelasyon Analizi (Analysis Of Correlation)
#########################################################
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 700)

### VERISETI MEME KANSERI ILE ILGILI BIR VERI SETI. Degıskenler cesitli olcum degerleri
df = pd.read_csv(r"C:\Users\ibrah\Desktop\miuulBootcamp\pythonProgramlama-221120-104515\pythonProgramlama\python_for_data_science\data_analysis_with_python\datasets\breast_cancer.csv")
df = df.iloc[:, 1:-1] # id(0.index) ve son degıksen(-1.index) istenmiyor 1. indexten basla -1. indexe git
df.head()

# Amac: Elimize bir dataset geldiğinde bunun ısı haritası aracılığıyla korelasyonlarına bakmak ve daha sonra birbiriyle yuksek koreleasyonlu degıskenlerın bazılarını dısarıda bırakmak

# numeric degiskenleri elde edelim(korelasyon icin)
num_cols = [column for column in df.columns if df[column].dtype in ["int64", "float64"]]
num_cols

correlation = df[num_cols].corr()
correlation   # cıktısı cok fazla cunku ındexte yer alan ve sutunda yer alan degıskenler aynı (tekrarlama yapıyor)
# yanı ıkı degısken arasında 0.99 luk bir korelasyon bu ıkı degıskenın neredeyse aynı degıskenler oldugu anlamına gelır. Bırısını calısma dısında bırakırız

## ISI HARITASI
sns.set(rc={"figure.figsize": (8, 8)}) # haritanın boyutu (12,12)lik.
sns.heatmap(correlation, cmap="RdBu")
plt.show()
## KOYU MAVILER: Siddetli pozitif korelasyon
# KOYU KIRMIZILAR: Siddetli negatif korelasyon


#####################################################
# Yuksek Korelasyonlu Degiskenlerin Silinmesi
#################################################
correlation_matrix = df.corr().abs() # bizim icin su an pozitif/negatif korelasyon önemli degil. YUKSEK KORELASYON ONEMLI BU YUZDEN "MUTLAK DEGER" ICINE ALIRIZ
correlation_matrix


upper_triangle_matrix = correlation_matrix.where(np.triu(np.ones(correlation_matrix.shape), k=1).astype(np.bool_))
upper_triangle_matrix

## 0.99 koralasyonlu degıskeni bi silelim. Sutunlardaki elemanlardan herhangi birisi  "correlastion_threshold"u 0.90 dan buyukse bu degiskeni sil
drop_list = [column for column in upper_triangle_matrix.columns if any(upper_triangle_matrix[column] > 0.90)] # any: herhangi birisi
drop_list

correlation_matrix[drop_list] # matris de gorelim
df.drop(drop_list, axis=1)  # dataset'den "drop_list" icinde olanları sutundan sil


#### Hadı sımdı Fonksıyon yazalım
def high_correlated_cols(dataframe, plot=False, correlation_threshold=0.90):
    corr = dataframe.corr()
    cor_matrix = corr.abs()
    upper_triangle_matrix = cor_matrix.where(np.triu(np.ones(cor_matrix.shape), k=1).astype(np.bool_))
    drop_list = [column for column in upper_triangle_matrix.columns if any(upper_triangle_matrix[column] > correlation_threshold)]
    if plot:
        import seaborn as sns
        import matplotlib.pyplot as plt
        sns.set(rc={"figure.figsize": (8,8)})
        sns.heatmap(corr, cmap="RdBu")
        plt.show()
    return drop_list

high_correlated_cols(df)
drop_list = high_correlated_cols(df, plot=True)
drop_list

high_correlated_cols(df.drop(drop_list, axis=1), plot=True) # yuksek korelasyonlu silinecek verileri fonksıyona gonderıldı



# Amac: kaggle'da yer alan 600 mb'lık veri setinde dene  "fraud_train_transaction.csv"


