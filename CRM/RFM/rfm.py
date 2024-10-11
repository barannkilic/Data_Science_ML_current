###############################################################
# RFM ile Müşteri Segmentasyonu (Customer Segmentation with RFM)
###############################################################

# 1. İş Problemi (Business Problem)
# 2. Veriyi Anlama (Data Understanding)
# 3. Veri Hazırlama (Data Preparation)
# 4. RFM Metriklerinin Hesaplanması (Calculating RFM Metrics)
# 5. RFM Skorlarının Hesaplanması (Calculating RFM Scores)
# 6. RFM Segmentlerinin Oluşturulması ve Analiz Edilmesi (Creating & Analysing RFM Segments)
# 7. Tüm Sürecin Fonksiyonlaştırılması



###############################################################
# 1. İş Problemi (Business Problem)
###############################################################
# Bir e-ticaret sirketinin musterilerini segmentlere gore ayırıp bu segmentlere gore
# pazarlama stratejileri belilrnmek isteniyor

# Veri Seti Hikayesi
# https://archive.ics.uci.edu/ml/datasets/Online+Retail+II

# Online Retail II isimli veri seti İngiltere merkezli online bir satış mağazasının
# 01/12/2009 - 09/12/2011 tarihleri arasındaki satışlarını içeriyor.

# Değişkenler
#
# InvoiceNo: Fatura numarası. Her işleme yani faturaya ait eşsiz numara. C ile başlıyorsa iptal edilen işlem.
# StockCode: Ürün kodu. Her bir ürün için eşsiz numara.
# Description: Ürün ismi
# Quantity: Faturadaki Ürün adedi. Faturalardaki ürünlerden kaçar tane satıldığını ifade etmektedir.
# InvoiceDate: Fatura tarihi ve zamanı.
# UnitPrice: Ürün fiyatı (Sterlin cinsinden)
# CustomerID: Eşsiz müşteri numarası
# Country: Ülke ismi. Müşterinin yaşadığı ülke.












###############################################################
# 2. Veriyi Anlama (Data Understanding)
###############################################################
import datetime as dt
import pandas as pd

pd.set_option("display.max_columns", None)
# pd.set_option("display.max_rows", None) # butun satırları gor terich etme
pd.set_option("display.width", 700)
pd.set_option("display.float_format", lambda x: '%.3f' % x) # virgulden sonra kac basamak olsun

data_ = pd.read_excel(r"C:\Users\ibrah\Desktop\miuulBootcamp\pythonProjects\crmAnalytics\datasets\online_retail_II.xlsx", sheet_name="Year 2009-2010")
data = data_.copy() # dosya boyutu fazla oldugu icin her seferınde bekleme yasanmaması adına buradan kopyalanıyor
data.head()
data.info()
data.shape
data.isnull().any()
data.isnull().sum()

## essiz urun sayısı?
print(f"Toplam essiz urun sayısı: {data['Description'].nunique()}")

## urunlerden kacar tane satılmstır? Hangı urunden kacar tane var
data["Description"].value_counts().head()

## en cok siparis edilen urun ..... kere belirli faturada geçmiş
data["Description"].value_counts().max()


## en cok satılan urun?
data.groupby("Description").agg({"Quantity": "sum"}).head() # quantity - olamaz bunu veri on isleme adımında ortadan kaldıracagız
# buyukten kucuge sıralayalım
data.groupby("Description").agg({"Quantity": "sum"}).sort_values("Quantity", ascending=False).head()


# toplam kac tane essiz fatura kesilmis?
print(f"Toplam kesilen essiz fatura sayısı: {data['Invoice'].nunique()}")


# fatura basına urunden toplam ne kadar kazanılmıs?
data["TotalPrice"] = data["Quantity"] * data["Price"]
data.head()

# fatura basınna toplam harcanan para?
data.groupby("Invoice").agg({"TotalPrice": "sum"}).head()











###############################################################
# 3. Veri Hazırlama (Data Preparation)
###############################################################
print(f"Veri setimizin boyutu: {data.shape}")

print(f"Veri setindeki eksik degerlerin sayısı:\n{data.isnull().sum()}")
## eksik degerleri kalıcı olarak silelim
data = data.dropna()
print(f"Veri setindeki eskik degerler silidikten sonra veri seti boyutu: {data.shape}")

## "Invoice"da basında "C" olanlar vardı. Bunlar iade cunku "Quantity"de iade var
data.describe().T

# Yol 1
cancel_invoice = [column for column in data["Invoice"] if "C" in str(column)] # basında "C" olanlar
# Yol 2
data[data["Invoice"].str.contains("C", na=False)] # basında "C" olanlar
# Yol 3
data = data[~data["Invoice"].str.contains("C", na=False)] # basında "C" olmayanlar
# basında "C" olanları sildik ama verisetini bir daha kontrol edelim
[column for column in data["Invoice"] if "C" in str(column)]














###############################################################
# 4. RFM Metriklerinin Hesaplanması (Calculating RFM Metrics)
###############################################################
## Her bır musterı ozelınde metriklerı hesaplayacagız

# Recency: Yenilik, musterinin sicaklıgı, son alışveris zamanı. Matematıksel: (analizin yapıldıgı tarih) - (musterinin son satın alma tarihi)
# Frequency: Sıklık, yapılan alısveris sayısı
# Monetary: Para, alısverislerinde bıraktıgı toplam para

data.head()
data.shape

## metrikleri hesaplamak icin analiz yapılan tarihi belirlememiz gerekiyor bunun icin:
print(f"Veri setindeki en son tarih: {data['InvoiceDate'].max()}")

# bugun ku tarihi son tarihten 2 gun sonra olarak belirleyelim
today_date = dt.datetime(2010, 12, 11)
today_date
type(today_date)   # bu islem bize zaman acısından fark almayı saglar

rfm = data.groupby("Customer ID").agg({'InvoiceDate': lambda InvoiceDate: (today_date - InvoiceDate.max()).days, # bugunki tarihten son islem yapılan tarihi cıkarırız ve sonucu "day" olarak veririz
                                       "Invoice": lambda Invoice: Invoice.nunique(), # essiz fatura sayısı
                                       "TotalPrice": lambda TotalPrice: TotalPrice.sum()}) # yapılan toplam harcama

rfm.head()

## sutun isimlerini degistirelim
rfm.columns
rfm.columns = ["recency", "frequency", "monetary"]
rfm.columns
rfm.head(10)

rfm.describe().T
# monetary: yanı toplam odenen paranın min degeri "0" bunu ucurmak gerek
rfm = rfm[rfm["monetary"] > 0]
rfm.describe().T # evet simdi odenen toplam para(monetarY min degeri degisti

# Veri setimiz hakkında son bilgi
print(f"Evet veri setimizde yer alan musterı sayısı {rfm.shape[0]}")
















###############################################################
# 5. RFM Skorlarının Hesaplanması (Calculating RFM Scores)
###############################################################

# recency_score
rfm["recency_score"] = pd.qcut(rfm["recency"], 5, labels=[5, 4, 3, 2, 1]) # "recency" degerını artan sekılde sıralar, belirli parçalara gore boler ve etiketler. etiketleme ters cunku recency degerı kucukse recency_score buyuk

# monetary_score
rfm["monetary_score"] = pd.qcut(rfm["monetary"], 5, labels=[1, 2, 3, 4, 5]) # monetary degerı buyukse monetary_score'u buyur

# frequency_score
rfm["frequency_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])

rfm.head()


# rfm_score'u olusturalım

rfm["RFM_score"] = (rfm["recency_score"].astype(str) + rfm["frequency_score"].astype(str))
rfm.head()

rfm.describe().T


# sampıyon musteri
rfm[rfm["RFM_score"] == "55"]

# az degerli musteri
rfm[rfm["RFM_score"] == "11"]














###############################################################
# 6. RFM Segmentlerinin Oluşturulması ve Analiz Edilmesi (Creating & Analysing RFM Segments)
###############################################################

# regex: REGular EXpretion... ARASTIRMALISIN

# RFM isimlendirmesi
seg_map = {
    r'[1-2][1-2]': 'hibernating',  # 1.elamanında 1 ya da 2, 2. elemanında 1 ya da 2 var ise "hibernating" yaz
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

# segment ekleniyor
rfm["segment"] = rfm["RFM_score"].replace(seg_map, regex=True)
rfm.head()


## segmentlerin bir analizini yapalım
rfm[["segment", "recency", "frequency", "monetary"]].groupby("segment").agg(["mean", "count"]) # rfm'ın hepsıne degil. Liste olarak verdigim degıskenleri al "segment"e gore 'mean' ve 'count' uygula


## Amac: Mudur ıkna olduk dedı. Ama nasıl odaklanıcaz sen bıze "need_attention"a odaklanalım.
# Bir departman bızden bu musterılere erısmek ıcın bılgı ıstıyor o zaman bu sınıflarda yer alan musterılerın ID'lerını veririz

rfm[rfm["segment"] == "need_attention"].head()
rfm[rfm["segment"] == "cant_loose"].head()

# departmanın istedigi sınıfın ID'lerine erismek. Cunku musterı bazında inceliyoruz
rfm[rfm["segment"] == "new_customers"].index  # cunku ID'ler indexte
rfm[rfm["segment"] == "cant_loose"].index



## ISTENILEN MUSTERILERI EXPORT ETMEK ICIN DATAFRAME OLUSTURALIM
new_data = pd.DataFrame()
new_data["new_customer_id"] = rfm[rfm["segment"] == "new_customers"].index
new_data.head()

new_data["new_customer_id"] = new_data["new_customer_id"].astype(int)
new_data.head()

new_data.to_csv("new_customers.csv")
rfm.to_csv("rfm.csv")















###############################################################
# 7. Tüm Sürecin Fonksiyonlaştırılması
###############################################################

def create_rfm(dataframe, csv=False):
    # VERIYI HAZIRLAMA
    dataframe["TotalPrice"] = dataframe["Quantity"] * dataframe["Price"]
    dataframe.dropna(inplace=True)
    dataframe = dataframe[~dataframe["Invoice"].str.contains("C", na=False)]

    # RFM METRIKLERININ HESAPLANMASI
    today_date = dt.datetime(2011, 12, 11)
    rfm = dataframe.groupby('Customer ID').agg({'InvoiceDate': lambda date: (today_date - date.max()).days,
                                                'Invoice': lambda num: num.nunique(),
                                                "TotalPrice": lambda price: price.sum()})
    rfm.columns = ['recency', 'frequency', "monetary"]
    rfm = rfm[(rfm['monetary'] > 0)]

    # RFM SKORLARININ HESAPLANMASI
    rfm["recency_score"] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1])
    rfm["frequency_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
    rfm["monetary_score"] = pd.qcut(rfm['monetary'], 5, labels=[1, 2, 3, 4, 5])

    # cltv_df skorları kategorik değere dönüştürülüp df'e eklendi
    rfm["RFM_SCORE"] = (rfm['recency_score'].astype(str) +
                        rfm['frequency_score'].astype(str))


    # SEGMENTLERIN ISIMLENDIRILMESI
    seg_map = {
        r'[1-2][1-2]': 'hibernating',
        r'[1-2][3-4]': 'at_risk',
        r'[1-2]5': 'cant_loose',
        r'3[1-2]': 'about_to_sleep',
        r'33': 'need_attention',
        r'[3-4][4-5]': 'loyal_customers',
        r'41': 'promising',
        r'51': 'new_customers',
        r'[4-5][2-3]': 'potential_loyalists',
        r'5[4-5]': 'champions'
    }

    rfm['segment'] = rfm['RFM_SCORE'].replace(seg_map, regex=True)
    rfm = rfm[["recency", "frequency", "monetary", "segment"]]
    rfm.index = rfm.index.astype(int)

    if csv:
        rfm.to_csv("rfm.csv")

    return rfm






## veri setini en bastaki haline geri donustur

data = data_.copy()
data.head()

rfm_new = create_rfm(data)
rfm.head()

