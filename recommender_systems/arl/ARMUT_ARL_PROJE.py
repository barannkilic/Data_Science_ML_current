from platform import freedesktop_os_release

#########################
# İş Problemi
#########################

# Türkiye’nin en büyük online hizmet platformu olan Armut, hizmet verenler ile hizmet almak isteyenleri buluşturmaktadır.
# Bilgisayarın veya akıllı telefonunun üzerinden birkaç dokunuşla temizlik, tadilat, nakliyat gibi hizmetlere kolayca
# ulaşılmasını sağlamaktadır.
# Hizmet alan kullanıcıları ve bu kullanıcıların almış oldukları servis ve kategorileri içeren veri setini kullanarak
# Association Rule Learning ile ürün tavsiye sistemi oluşturulmak istenmektedir.


#########################
# Veri Seti
#########################
#Veri seti müşterilerin aldıkları servislerden ve bu servislerin kategorilerinden oluşmaktadır.
# Alınan her hizmetin tarih ve saat bilgisini içermektedir.

# UserId: Müşteri numarası
# ServiceId: Her kategoriye ait anonimleştirilmiş servislerdir. (Örnek : Temizlik kategorisi altında koltuk yıkama servisi)
# Bir ServiceId farklı kategoriler altında bulanabilir ve farklı kategoriler altında farklı servisleri ifade eder.
# (Örnek: CategoryId’si 7 ServiceId’si 4 olan hizmet petek temizliği iken CategoryId’si 2 ServiceId’si 4 olan hizmet mobilya montaj)
# CategoryId: Anonimleştirilmiş kategorilerdir. (Örnek : Temizlik, nakliyat, tadilat kategorisi)
# CreateDate: Hizmetin satın alındığı tarih

import pandas as pd
from matplotlib.pyplot import xlabel

from recommender_systems.arl.arl import frequent_itemsets, recommendation_list, sorted_rules

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 1000)
from mlxtend.frequent_patterns import apriori, association_rules


#########################
# GÖREV 1: Veriyi Hazırlama
#########################

# Adım 1: armut_data.csv dosyasınız okutunuz.
data_ = pd.read_csv(r"C:\Users\ibrah\Desktop\miuulBootcamp\pythonProjects\recommender_systems\proje\armut_data.csv")
data = data_.copy()
data
data.shape
data.isnull().sum() # eksik deger kontrolu

# Adım 2: ServisID her bir CategoryID özelinde farklı bir hizmeti temsil etmektedir.
# ServiceID ve CategoryID'yi "_" ile birleştirerek hizmetleri temsil edecek yeni bir değişken oluşturunuz.
data["hizmet"] = data["ServiceId"].astype(str) + "_" + data["CategoryId"].astype(str)
data
# 2.yol
# [str(row[1]) + "_" + str(row[2]) for row in data.values]

# Adım 3: Veri seti hizmetlerin alındığı tarih ve saatten oluşmaktadır, herhangi bir sepet tanımı (fatura vb. ) bulunmamaktadır.
# Association Rule Learning uygulayabilmek için bir sepet (fatura vb.) tanımı oluşturulması gerekmektedir.
# Burada sepet tanımı her bir müşterinin aylık aldığı hizmetlerdir. Örneğin; 7256 id'li müşteri 2017'in 8.ayında aldığı 9_4, 46_4 hizmetleri bir sepeti;
# 2017’in 10.ayında aldığı  9_4, 38_4  hizmetleri başka bir sepeti ifade etmektedir. Sepetleri unique bir ID ile tanımlanması gerekmektedir.
# Bunun için öncelikle sadece yıl ve ay içeren yeni bir date değişkeni oluşturunuz. UserID ve yeni oluşturduğunuz date değişkenini "_"
# ile birleştirirek ID adında yeni bir değişkene atayınız.

# mevcut tarih degiskeninin tipi degisiyor
data["CreateDate"] = pd.to_datetime(data["CreateDate"])
data.info()
# tarih degiskeni yıl-ay olarak guncelleniyor
data["NewDate"] = data["CreateDate"].dt.strftime("%Y-%m")
data
data.info()
# sepet_id olusuyor
data["SepetId"] = data["UserId"].astype(str) + "_" + data["NewDate"].astype(str)
data


#########################
# GÖREV 2: Birliktelik Kuralları Üretiniz
#########################

# Adım 1: Aşağıdaki gibi sepet hizmet pivot table’i oluşturunuz.

# Hizmet         0_8  10_9  11_11  12_7  13_11  14_7  15_1  16_8  17_5  18_4..
# SepetID
# 0_2017-08        0     0      0     0      0     0     0     0     0     0..
# 0_2017-09        0     0      0     0      0     0     0     0     0     0..
# 0_2018-01        0     0      0     0      0     0     0     0     0     0..
# 0_2018-04        0     0      0     0      0     1     0     0     0     0..
# 10000_2017-08    0     0      0     0      0     0     0     0     0     0..

invoice_product_data = data.groupby(["SepetId", "hizmet"])["hizmet"].count().unstack().fillna(0).applymap(lambda x: 1 if x > 0 else 0)


# Adım 2: Birliktelik kurallarını oluşturunuz.
# olası tum urun bırlıkteliklerinin olasılıkları
frequent_itemsets = apriori(invoice_product_data,
                            min_support=0.01,
                            use_colnames=True)
# birliktelik kuralları
rules = association_rules(frequent_itemsets,
                          metric="support",
                          min_threshold=0.01)
rules.head()



#Adım 3: arl_recommender fonksiyonunu kullanarak en son 2_0 hizmetini alan bir kullanıcıya hizmet önerisinde bulununuz.

def arl_recommender(rules_data, product_id, recommendation_count = 1):
    sorted_rules = rules_data.sort_values("lift", ascending=False)
    recommendation_list = []
    for i, product in enumerate(sorted_rules["antecedents"]):
        for j in list(product): # her gozlem set oldugu icin icinde gezmek adına 'list' yapılıyor
            if j == product_id:
                recommendation_list.append(list(sorted_rules.iloc[i]["consequents"])[0])
    return recommendation_list[0: recommendation_count] # onerı istenilen aralık

arl_recommender(rules, "2_0", 1)

