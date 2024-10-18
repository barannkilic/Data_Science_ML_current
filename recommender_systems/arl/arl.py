############################################
# ASSOCIATION RULE LEARNING (BİRLİKTELİK KURALI ÖĞRENİMİ)
############################################
# Cok sık birlikte satın alınan urunlerin olasılıklarını cıkarıp bunlara gore oneri yapılır


# 1. Veri Ön İşleme
# 2. ARL Veri Yapısını Hazırlama (Invoice-Product Matrix)
# 3. Birliktelik Kurallarının Çıkarılması
# 4. Çalışmanın Scriptini Hazırlama
# 5. Sepet Aşamasındaki Kullanıcılara Ürün Önerisinde Bulunmak









############################################
# 1. Veri Ön İşleme
############################################

# !pip install mlxtend
import pandas as pd
pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
pd.set_option('display.width', 500)
# çıktının tek bir satırda olmasını sağlar.
pd.set_option('display.expand_frame_repr', False)
from mlxtend.frequent_patterns import apriori, association_rules

# https://archive.ics.uci.edu/ml/datasets/Online+Retail+II

data_ = pd.read_excel(r"C:\Users\ibrah\Desktop\miuulBootcamp\pythonProjects\recommender_systems\datasets\online_retail_II.xlsx",
                    sheet_name="Year 2010-2011")
data = data_.copy()
data.head()
# pip install openpyxl
# df_ = pd.read_excel("datasets/online_retail_II.xlsx",
#                     sheet_name="Year 2010-2011", engine="openpyxl")


data.describe().T # -'li degerler var bunlar iade urunler
data.isnull().sum() # bos degerler gorunuyor
data.shape



# EKSİK DEGER - İPTAL FATURALAR - 1'DENA FAZLA ADET VE TUTAR ( betımsel istatistiklerde '-'li deger olmaması icim
def retail_data_prep(dataframe):
    dataframe.dropna(inplace=True) # eksik degerler kalıcı olarak cıkıyor
    dataframe = dataframe[~dataframe["Invoice"].str.contains("C", na=False)] # iptal olan urunler
    dataframe = dataframe[dataframe["Quantity"] > 0] # degerı 1 ve ustu olanlar
    dataframe = dataframe[dataframe["Price"] > 0] # degerı 1 ve ustu olanlar
    return dataframe

data = retail_data_prep(data)
data.describe().T





############################################################################
# UC DEGERLER İCİN ESİK DEGER BELİRLEME
# aykırı deger olduunu 'describe()' fonksıyonunda ceyreklıkle arası olan buyuk farktan anlıyoruz
# aykırı deger: bir verideki genel dagılımın dısında olan degerlerdir
def outlier_thresholds(dataframe, variable):
    quartile1 = dataframe[variable].quantile(0.01) # girilen degiskenin 0.01 hesapla 1.ceyrek olarak tut
    quartile3 = dataframe[variable].quantile(0.99) # girilen degiskenin 0.99 hesapla 3. ceyrek olarak tut
    interquantile_range = quartile3 - quartile1 # kabul edilebilir aralık
    up_limit = quartile3 + 1.5 * interquantile_range # ust limit
    low_limit = quartile1 - 1.5 * interquantile_range # alt limit
    return low_limit, up_limit

def replace_with_thresholds(dataframe, variable):
    low_limit, up_limit = outlier_thresholds(dataframe, variable) # up-low limit belirleme
    dataframe.loc[(dataframe[variable] < low_limit), variable] = low_limit # low limitten dusuk olanları low limit ile degistir
    dataframe.loc[(dataframe[variable] > up_limit), variable] = up_limit # up limitten yuksek olanları up limit ile degistir
#####################################################################




## TEK FONKSİYON HALİNE GETİRME
def actual_retail_data_prep(dataframe):
    dataframe.dropna(inplace=True)
    dataframe = dataframe[~dataframe["Invoice"].str.contains("C", na=False)]
    dataframe = dataframe[dataframe["Quantity"] > 0]
    dataframe = dataframe[dataframe["Price"] > 0]
    replace_with_thresholds(dataframe, "Quantity")
    replace_with_thresholds(dataframe, "Price")
    return dataframe

data = data_.copy()
data.head()
data.isnull().sum()

data = retail_data_prep(data)
data.isnull().sum()
data.describe().T

#### NOT: Bu islemler ardından:
# 1) eksik degerler
# 2) iptal faturalar (C' iceren fatura numaraları)
# 3) Aykırı degerlerü
# temizlenmis oldu. Bu islemler ile veri on isleme adımı tamamlanmıs olur












############################################
# 2. ARL Veri Yapısını Hazırlama (Invoice-Product Matrix)
############################################

data.head()

## SUTUNLARDA OLASI BUTUN URUNLER SATIRLARDA FATURALAR(SEPET OLARAK)YER ALACAK.
# Faturada urun var mı yok mu?
# Description   NINE DRAWER OFFICE TIDY   SET 2 TEA TOWELS I LOVE LONDON    SPACEBOY BABY GIFT SET
# Invoice
# 536370                              0                                 1                       0
# 536852                              1                                 0                       1
# 536974                              0                                 0                       0
# 537065                              1                                 0                       0
# 537463                              0                                 0                       1

# Veri setini belirli bir ulkeye indirgeyelim
data_fr = data[data["Country"] == "France"]
data_fr

# Faturada yer alan urun adetleri
data_fr.groupby(['Invoice', 'Description']).agg({"Quantity": "sum"}).head(20)

# Faturalar tekillesiyor. Ve ufak bir cıktı alınıyor
data_fr.groupby(['Invoice', 'Description']).agg({"Quantity": "sum"}).unstack().iloc[0:10, 0:10]

# Eksik degelern yerinde 0 yazılacak
data_fr.groupby(['Invoice', 'Description']).agg({"Quantity": "sum"}).unstack().fillna(0).iloc[0:5, 0:5]

# Dolu gozlem bırımlerının yerinde 1 yazılacak ve urun acıklaması yerine 'stock_code' yazılsın
data_fr.groupby(['Invoice', 'StockCode']). \
    agg({"Quantity": "sum"}). \
    unstack(). \
    fillna(0). \
    applymap(lambda x: 1 if x > 0 else 0).iloc[0:10, 0:10]







# 'stock_code' veya 'description' istenilmesi durumuna gore function yazılsın
def create_invoice_product_data(dataframe, id=False):
    if id:
        return dataframe.groupby(["Invoice", "StockCode"])["Quantity"].sum().unstack().fillna(0).applymap(lambda x: 1 if x > 0 else 0)
    else:
        return dataframe.groupby(["Invoice", "Description"])["Quantity"].sum().unstack().fillna(0).applymap(lambda x: 1 if x > 0 else 0)


fr_inv_pro_df = create_invoice_product_data(data_fr) # Argumansız
fr_inv_pro_df

fr_inv_pro_df = create_invoice_product_data(data_fr, id=True) # Argumanlı
fr_inv_pro_df


# StockCode'a ait urun acıklamasını veriyor
def check_id(dataframe, stock_code):
    product_name = dataframe[dataframe["StockCode"] == stock_code][["Description"]].values[0].tolist()
    print(product_name)

check_id(data_fr, 10120)








############################################
# 3. Birliktelik Kurallarının Çıkarılması
############################################
# support(x, y) = freq(x, y)/N   -->  || x ve y'nin birlikte gorulme olasılıgı
# confidence(x, y)= freq(x, y)/freq(x)    --> || x satın alındıgında y'nin satılması olasılıgı
# lift = support(x, y) / (support(x) * support(x))   --> || x satın alındıgında y'nin satın alınma olasılıgı lift kat kadar artar




# Olası tum urun birlikteliklerinin support degerlerini yani olasılıklarını bulmak olucak
frequent_itemsets = apriori(fr_inv_pro_df, # dataframe'i ver
                            min_support=0.01, # threshold ver. Bu degerın altında olanları almaz
                            use_colnames=True) # degisken isimlerini kullanmak istiyorsan

frequent_itemsets.sort_values("support", ascending=False) # "support"a gore azalan bir sekilde sırala

# Birliktelik kurallarını cıkartalım
rules = association_rules(frequent_itemsets,
                          metric="support",
                          min_threshold=0.01)

# Ornek olası kombinasyonları inceleyelim
rules[(rules["support"]>0.05) & (rules["confidence"]>0.1) & (rules["lift"]>5)]

# StockCode'una gore urun adını ogrenelim
check_id(data_fr, 21080)
check_id(data_fr, 21086)

# CONFİDENCE'e gore sıralayalım: Sepetteki urun satın alınırsa dıger urunun satın alınma olasılıgı
rules[(rules["support"]>0.05) & (rules["confidence"]>0.1) & (rules["lift"]>5)].\
    sort_values("confidence", ascending=False)










############################################
# 4. Çalışmanın Scriptini Hazırlama
############################################

def outlier_thresholds(dataframe, variable):
    quartile1 = dataframe[variable].quantile(0.01)
    quartile3 = dataframe[variable].quantile(0.99)
    interquantile_range = quartile3 - quartile1
    up_limit = quartile3 + 1.5 * interquantile_range
    low_limit = quartile1 - 1.5 * interquantile_range
    return low_limit, up_limit

def replace_with_thresholds(dataframe, variable):
    low_limit, up_limit = outlier_thresholds(dataframe, variable)
    dataframe.loc[(dataframe[variable] < low_limit), variable] = low_limit
    dataframe.loc[(dataframe[variable] > up_limit), variable] = up_limit

def retail_data_prep(dataframe):
    dataframe.dropna(inplace=True)
    dataframe = dataframe[~dataframe["Invoice"].str.contains("C", na=False)]
    dataframe = dataframe[dataframe["Quantity"] > 0]
    dataframe = dataframe[dataframe["Price"] > 0]
    replace_with_thresholds(dataframe, "Quantity")
    replace_with_thresholds(dataframe, "Price")
    return dataframe


def create_invoice_product_df(dataframe, id=False):
    if id:
        return dataframe.groupby(['Invoice', "StockCode"])['Quantity'].sum().unstack().fillna(0). \
            applymap(lambda x: 1 if x > 0 else 0)
    else:
        return dataframe.groupby(['Invoice', 'Description'])['Quantity'].sum().unstack().fillna(0). \
            applymap(lambda x: 1 if x > 0 else 0)


def check_id(dataframe, stock_code):
    product_name = dataframe[dataframe["StockCode"] == stock_code][["Description"]].values[0].tolist()
    print(product_name)


def create_rules(dataframe, id=True, country="France"):
    dataframe = dataframe[dataframe['Country'] == country]
    dataframe = create_invoice_product_df(dataframe, id)
    frequent_itemsets = apriori(dataframe, min_support=0.01, use_colnames=True)
    rules = association_rules(frequent_itemsets, metric="support", min_threshold=0.01)
    return rules

data = data_.copy()

data = retail_data_prep(data)
rules = create_rules(data)

rules[(rules["support"]>0.05) & (rules["confidence"]>0.1) & (rules["lift"]>5)]. \
    sort_values("confidence", ascending=False)











############################################
# 5. Sepet Aşamasındaki Kullanıcılara Ürün Önerisinde Bulunmak
############################################

# Örnek:
# Kullanıcı örnek ürün id: 22492

product_id = 22492 # urun_id
check_id(data, product_id) # urun acıklaması

# anlık olarak önemli olan "lift" ona gore sıralama
sorted_rules = rules.sort_values("lift", ascending=False)
sorted_rules


recommendation_list = [] # onerı yapılacak urunler listesi

for i, product in enumerate(sorted_rules["antecedents"]): # "antecedents"de product, indexlerde i gezecek
    for j in list(product): # "antecedents"de yer alan set veri yapısı. Islem yapabilmek icin "list" yap
        if j == product_id: # product_id ise tavsıye olarak ekle
            recommendation_list.append(list(sorted_rules.iloc[i]["consequents"])[0]) # i indexine git. "consequents" de yer alan degerı dondur

recommendation_list[0:3] # sepette yer alan product_id'li urune onerilebilecek ilk uc urun

check_id(data, 22326)


# Function haline getirelim
def arl_recommender(rules_data, product_id, rec_count=1):
    sorted_rules = rules_data.sort_values("lift", ascending=False)
    recommendation_list = []
    for i, product in enumerate(sorted_rules["antecedents"]):
        for j in list(product):
            if j == product_id:
                recommendation_list.append(list(sorted_rules.iloc[i]["consequents"])[0])

    return recommendation_list[0:rec_count] # en son elde edilen tavsiye listesinden kac urun onerilsin


arl_recommender(rules, 22492, 1) # 1 tavsıyede bulun
arl_recommender(rules, 22492, 2) # 2 tavsıyede bulun
arl_recommender(rules, 22492, 3) # 3 tavsıyede bulun





