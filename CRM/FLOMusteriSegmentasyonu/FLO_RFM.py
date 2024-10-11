
###############################################################
# RFM ile Müşteri Segmentasyonu (Customer Segmentation with RFM)
###############################################################

###############################################################
# İş Problemi (Business Problem)
###############################################################
# FLO müşterilerini segmentlere ayırıp bu segmentlere göre pazarlama stratejileri belirlemek istiyor.
# Buna yönelik olarak müşterilerin davranışları tanımlanacak ve bu davranış öbeklenmelerine göre gruplar oluşturulacak..

###############################################################
# Veri Seti Hikayesi
###############################################################

# Veri seti son alışverişlerini 2020 - 2021 yıllarında OmniChannel(hem online hem offline alışveriş yapan) olarak yapan müşterilerin geçmiş alışveriş davranışlarından
# elde edilen bilgilerden oluşmaktadır.

# master_id: Eşsiz müşteri numarası
# order_channel : Alışveriş yapılan platforma ait hangi kanalın kullanıldığı (Android, ios, Desktop, Mobile, Offline)
# last_order_channel : En son alışverişin yapıldığı kanal
# first_order_date : Müşterinin yaptığı ilk alışveriş tarihi
# last_order_date : Müşterinin yaptığı son alışveriş tarihi
# last_order_date_online : Muşterinin online platformda yaptığı son alışveriş tarihi
# last_order_date_offline : Muşterinin offline platformda yaptığı son alışveriş tarihi
# order_num_total_ever_online : Müşterinin online platformda yaptığı toplam alışveriş sayısı
# order_num_total_ever_offline : Müşterinin offline'da yaptığı toplam alışveriş sayısı
# customer_value_total_ever_offline : Müşterinin offline alışverişlerinde ödediği toplam ücret
# customer_value_total_ever_online : Müşterinin online alışverişlerinde ödediği toplam ücret
# interested_in_categories_12 : Müşterinin son 12 ayda alışveriş yaptığı kategorilerin listesi

###############################################################
# GÖREVLER
###############################################################

# GÖREV 1: Veriyi Anlama (Data Understanding) ve Hazırlama
           # 1. flo_data_20K.csv verisini okuyunuz.
           # 2. Veri setinde
                     # a. İlk 10 gözlem,
                     # b. Değişken isimleri,
                     # c. Betimsel istatistik,
                     # d. Boş değer,
                     # e. Değişken tipleri, incelemesi yapınız.
           # 3. Omnichannel müşterilerin hem online'dan hemde offline platformlardan alışveriş yaptığını ifade etmektedir. Herbir müşterinin toplam
           # alışveriş sayısı ve harcaması için yeni değişkenler oluşturun.
           # 4. Değişken tiplerini inceleyiniz. Tarih ifade eden değişkenlerin tipini date'e çeviriniz.
           # 5. Alışveriş kanallarındaki müşteri sayısının, ortalama alınan ürün sayısının ve ortalama harcamaların dağılımına bakınız.
           # 6. En fazla kazancı getiren ilk 10 müşteriyi sıralayınız.
           # 7. En fazla siparişi veren ilk 10 müşteriyi sıralayınız.
           # 8. Veri ön hazırlık sürecini fonksiyonlaştırınız.

# GÖREV 2: RFM Metriklerinin Hesaplanması

# GÖREV 3: RF ve RFM Skorlarının Hesaplanması

# GÖREV 4: RF Skorlarının Segment Olarak Tanımlanması

# GÖREV 5: Aksiyon zamanı!
           # 1. Segmentlerin recency, frequnecy ve monetary ortalamalarını inceleyiniz.
           # 2. RFM analizi yardımı ile 2 case için ilgili profildeki müşterileri bulun ve müşteri id'lerini csv ye kaydediniz.
                   # a. FLO bünyesine yeni bir kadın ayakkabı markası dahil ediyor. Dahil ettiği markanın ürün fiyatları genel müşteri tercihlerinin üstünde. Bu nedenle markanın
                   # tanıtımı ve ürün satışları için ilgilenecek profildeki müşterilerle özel olarak iletişime geçeilmek isteniliyor. Sadık müşterilerinden(champions,loyal_customers),
                   # ortalama 250 TL üzeri ve kadın kategorisinden alışveriş yapan kişiler özel olarak iletişim kuralacak müşteriler. Bu müşterilerin id numaralarını csv dosyasına
                   # yeni_marka_hedef_müşteri_id.cvs olarak kaydediniz.
                   # b. Erkek ve Çoçuk ürünlerinde %40'a yakın indirim planlanmaktadır. Bu indirimle ilgili kategorilerle ilgilenen geçmişte iyi müşteri olan ama uzun süredir
                   # alışveriş yapmayan kaybedilmemesi gereken müşteriler, uykuda olanlar ve yeni gelen müşteriler özel olarak hedef alınmak isteniliyor. Uygun profildeki müşterilerin id'lerini csv dosyasına indirim_hedef_müşteri_ids.csv
                   # olarak kaydediniz.


# GÖREV 6: Tüm süreci fonksiyonlaştırınız.

###############################################################
# GÖREV 1: Veriyi  Hazırlama ve Anlama (Data Understanding)
###############################################################
import pandas as pd
import datetime as dt

from pythonProgramminForDs.functions_conditions_loops_comprehensions.funcitons_conditions_lopps_comprehensions import \
    index

pd.set_option('display.max_columns', None)
#pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.2f' % x)
pd.set_option('display.width',1000)

# 2. Veri setinde
        # a. İlk 10 gözlem,
        # b. Değişken isimleri,
        # c. Boyut,
        # d. Betimsel istatistik,
        # e. Boş değer,
        # f. Değişken tipleri, incelemesi yapınız.
df_ = pd.read_csv(r"C:\Users\ibrah\Desktop\miuulBootcamp\pythonProjects\crmAnalytics\FLOMusteriSegmentasyonu\flo_data_20k.csv")
data = df_.copy()
data.head(10)

data.columns

data.shape
data.describe().T
data.isnull().sum()
data.info()


# 3. Omnichannel müşterilerin hem online'dan hemde offline platformlardan alışveriş yaptığını ifade etmektedir.
# Herbir müşterinin toplam alışveriş sayısı ve harcaması için yeni değişkenler oluşturunuz.
data["order_num_total"] = data["order_num_total_ever_online"] + data["order_num_total_ever_offline"]
data["order_num_total"][:10]

data["customer_value_total"] = data["customer_value_total_ever_online"] + data["customer_value_total_ever_offline"]
data["customer_value_total"][:10]

# 4. Değişken tiplerini inceleyiniz. Tarih ifade eden değişkenlerin tipini date'e çeviriniz.
data.info()
date_in_columns = data.columns[data.columns.str.contains("date")]
data[date_in_columns] = data[date_in_columns].apply(pd.to_datetime)
data.info()

# df["last_order_date"] = df["last_order_date"].apply(pd.to_datetime)



# 5. Alışveriş kanallarındaki müşteri sayısının, toplam alınan ürün sayısı ve toplam harcamaların dağılımına bakınız. 
data.groupby("order_channel").agg({"master_id": "count",
                                   "order_num_total": "sum",
                                   "customer_value_total": "sum"})


# 6. En fazla kazancı getiren ilk 10 müşteriyi sıralayınız.
data.sort_values("customer_value_total", ascending=False)[:10]



# 7. En fazla siparişi veren ilk 10 müşteriyi sıralayınız.
data.sort_values("order_num_total", ascending=False)[:10]



# 8. Veri ön hazırlık sürecini fonksiyonlaştırınız.
def data_preparation(dataframe):
    data["order_num_total"] = data["order_num_total_ever_online"] + data["order_num_total_ever_offline"]
    data["customer_value_total"] = data["customer_value_total_ever_online"] + data["customer_value_total_ever_offline"]
    date_in_columns = data.columns[data.columns.str.contains("date")]
    data[date_in_columns] = data[date_in_columns].apply(pd.to_datetime)
    return dataframe

###############################################################
# GÖREV 2: RFM Metriklerinin Hesaplanması
###############################################################

# Veri setindeki en son alışverişin yapıldığı tarihten 2 gün sonrasını analiz tarihi
data["last_order_date"].max()
today_date = dt.datetime(2021, 6, 1)
today_date

# customer_id, recency, frequnecy ve monetary değerlerinin yer aldığı yeni bir rfm dataframe
rfm = pd.DataFrame()
rfm["customer_id"] = data["master_id"]

rfm["recency"] = (today_date - data["last_order_date"]).dt.days
rfm.head()

rfm["frequency"] = data["order_num_total"]
rfm.head()

rfm["monetary"] = data["customer_value_total"]
rfm.head()

###############################################################
# GÖREV 3: RF ve RFM Skorlarının Hesaplanması (Calculating RF and RFM Scores)
###############################################################

#  Recency, Frequency ve Monetary metriklerini qcut yardımı ile 1-5 arasında skorlara çevrilmesi ve
# Bu skorları recency_score, frequency_score ve monetary_score olarak kaydedilmesi
rfm["recency_score"] = pd.qcut(rfm["recency"], 5, labels=[5, 4, 3, 2, 1])
rfm["frequency_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
rfm["monetary_score"] = pd.qcut(rfm["monetary"], 5, labels=[1, 2, 3, 4, 5])
rfm.head()

# recency_score ve frequency_score’u tek bir değişken olarak ifade edilmesi ve RF_SCORE olarak kaydedilmesi
rfm["RF_SCORE"] = (rfm["recency_score"].astype(str) + rfm["frequency_score"].astype(str))
rfm.head()

###############################################################
# GÖREV 4: RF Skorlarının Segment Olarak Tanımlanması
###############################################################
seg_map = {
    r'[1-2][1-2]': 'hibernating',
    r'[1-2][3-4]': 'at_Risk',
    r'[1-2]5': 'cant_loose',
    r'3[1-2]': 'about_to_sleep',
    r'33': 'need_attention',
    r'[3-4][4-5]': 'loyal_customers',
    r'41': 'promising',
    r'51': 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]': 'champions'
}
# Oluşturulan RFM skorların daha açıklanabilir olması için segment tanımlama ve  tanımlanan seg_map yardımı ile RF_SCORE'u segmentlere çevirme
rfm["segment"] = rfm["RF_SCORE"].replace(seg_map, regex=True)
rfm.head()

###############################################################
# GÖREV 5: Aksiyon zamanı!
###############################################################

# 1. Segmentlerin recency, frequnecy ve monetary ortalamalarını inceleyiniz.
rfm.groupby("segment").agg({"recency": "mean",
                            "frequency": "mean",
                            "monetary": "mean"})


# 2. RFM analizi yardımı ile 2 case için ilgili profildeki müşterileri bulunuz ve müşteri id'lerini csv ye kaydediniz.

# a. FLO bünyesine yeni bir kadın ayakkabı markası dahil ediyor. Dahil ettiği markanın ürün fiyatları genel müşteri tercihlerinin üstünde. Bu nedenle markanın
# tanıtımı ve ürün satışları için ilgilenecek profildeki müşterilerle özel olarak iletişime geçeilmek isteniliyor. Bu müşterilerin sadık  ve
# kadın kategorisinden alışveriş yapan kişiler olması planlandı. Müşterilerin id numaralarını csv dosyasına yeni_marka_hedef_müşteri_id.cvs
# olarak kaydediniz.

#1.yol
rfm = pd.merge(rfm, df[["master_id", "interested_in_categories_12"]], on="master_id", how="left")

rfm["category"] = rfm["interested_in_categories_12"] #1.yol

#rfm = rfm.rename(columns={"interested_in_categories_12": "category"}) #2.yol

yeni_marka_hedef_musteri_id = rfm.loc[(rfm["monetary"] > 250) & (rfm["category"].str.contains("KADIN")) & ((rfm["segment"] == "champions") | (rfm["segment"] == "loyal_customers")), ["master_id", "monetary", "category", "segment"]]
yeni_marka_hedef_musteri_id.head(10)

yeni_marka_hedef_musteri_id.to_csv("yeni_marka_hedef_müşteri_id.csv")



rfm[rfm["segment"].isin(["champions", "loyal_customers"])][:10] # hedef segmentler ortaya cıkıyor
target_segment_customer_id = rfm[rfm["segment"].isin(["champions", "loyal_customers"])]["customer_id"] # hedef segment de bır sutun gorunuyor

# hedef segmentte bulunan id ile data da bulunan kadın kategorisini kosula sok
cust_ids = data[(data["master_id"].isin(target_segment_customer_id)) & (data["interested_in_categories_12"].str.contains("KADIN"))]["master_id"]
cust_ids.head()
cust_ids.to_csv("yeni_marka_hedef_musteri_id.csv", index=False)

# b. Erkek ve Çoçuk ürünlerinde %40'a yakın indirim planlanmaktadır. Bu indirimle ilgili kategorilerle ilgilenen geçmişte iyi müşterilerden olan ama uzun süredir
# alışveriş yapmayan ve yeni gelen müşteriler özel olarak hedef alınmak isteniliyor. Uygun profildeki müşterilerin id'lerini csv dosyasına indirim_hedef_müşteri_ids.csv
# olarak kaydediniz.

target_segment_customer_id_2 = rfm[rfm["segment"].isin(["cant_loose", "hibernating", "new_customers"])]["customer_id"]
target_segment_customer_id_2

cust_ids_2 = data[(data["master_id"].isin(target_segment_customer_id_2)) & ((data["interested_in_categories_12"].str.contains("ERKEK")) | (data["interested_in_categories_12"].str.contains("COCUK")))]["master_id"]
cust_ids_2

cust_ids_2.to_csv("indirim_hedef_musteri_id.csv", index=False)



