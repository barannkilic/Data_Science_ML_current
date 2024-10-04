##############################################
# NUMPY (Numerical Python)
###########################################

####### Neden Numpy?
# 1- Hız: Cunku sabit tipte veri tutar
# 2- Fonksiyonel ve vektorel duzeyde Yuksek seviyeden islem yapar

import numpy as np
# Bu iki listeyi carpmak isteyelim native yolla
a = [1, 2, 3, 4]
b = [2, 3, 4, 5]
ab = []

for i in range(0, len(a)): # dan a'nı uzunlugu kadar gez
    ab.append(a[i] * b[i])   # a'nın ve b'nin i indexlerini carp ab listesine ekle
ab

# numpy ile
a = np.array([1, 2, 3, 4])
b = np.array([2, 3, 4, 5])
a * b # nunpy oldugu icin daha hızlı ve high-level yoldan yapildi







######## Creating Numpy Arrays
np.array([1, 2, 3, 4, 5])
type(np.array([1, 2, 3, 4, 5]))


np.zeros(10, dtype=int) # 10 tane 0 iceren array olustur

np.random.randint(0, 10, 5) # sinirini gir, kac tane secim istiyorsun.. 0 ile 10 arasında 5 int deger olustur

np.random.normal(10, 4, (3, 4)) # ortalamayi, standart sapması, boyut bilgisini








####### Attributes of Numpy Arrays (Numpy Array Ozellikleri)
 # ndim: boyut sayisi (satir sayisi)
 # shape: boyut bilgisi
 # size: toplam eleman sayisi
 # dtype: array veri tipi
import numpy as np
a = np.random.randint(0, 10, size=5)  # 0 ile 10 arasında 5 tane int deger olustur

a.ndim # 1 boyutlu (boyut sayısı)
a.shape # 5 sütun  (boyut bılgısı (1, 5))
a.size # 5 eleman
a.dtype # elemanin tip bilgisi








########## Reshaping (Yeniden Sekillendirme, Boyut degisimi)
import numpy as np

np.random.randint(1, 10, size=9) # tek boyutlu
np.random.randint(1, 10, size=9).reshape(3, 3) # 3 boyutlu oldu


# atama islemi ile kalici hale geldi
ar = np.random.randint(1, 10, size=9)
ar.reshape(3, 3)





######### Index Secimi (Index Selection)
import numpy as np
a = np.random.randint(0, 10, size=10)
a[0]
a[0:5]  # sliceing ile 0-5 indedxleri arasında olan elemanlar seciliyor
a

a[0] = 999 # 0.index değişiyor
a

# 2 boyutlu arrayda secim islemi
m = np.random.randint(0, 10, size=(3,5))
m
m[0,0] # 0.satir ve 0.sütunda var olan eleman
m[1, 1]

m
m[2, 3]
m[2, 3] = 987
m

m[2, 3] = 2.9
m   # array int degerler icerdigi icin float deger kabul etmez. Array'ler tek tiptir

# cok boyurlularda slice islemi
m[:, 0]  # butun satirlari ve 0. sütunu sec
m[1, :]  # 1. satiri sec tum sütunları sec
m[0:2, 0:3]  # 0'dan 2'ye kadar satır, 0'dan 3'e kadar sütun

a = np.array([1, 2, 3, 4, 5, 6, 7])
a
a[-1] # sonuncu eleman
a[-2] # cıktısı 6'dir. Sondan önceki
a[-3:-1] # cıktısı [5,6] dir. -1. elaman dahil edilmez. -3 ve -2. elaman alınır










########## Fancy Index
import numpy as np
v = np.arange(0, 30, 3) # iki sinir arasi belirlenen artıs. 0'dan 30'a kadar 3'er artır
v

v1 = np.arange(10, 20, 2) # 10'dan 20'ye kadar ikiser artır
v1

v
v[1] # 1. indexi bul

v
catch = [1, 2, 3] # bulunacak olan index'ler
v[catch]  # catch'de yer alan elemanlara karsılık gelen index'ler








################ Numpy'da Kosullu Islemler (Conditions on Numpy)
import numpy as np
v = np.array([1, 2, 3, 4, 5])
v

# Amac: Arrayda 3'den kucuk olan degerlere eriselim

### Klasik Dongu ile ###

three_small = []
for i in v:
    if i < 3:
        three_small.append(i)
        print(f"{i}, 3'den kucuk, listeye eklendi")
    else:
        print(f"{i}, 3'den kucuk degil")

####  Numpy Ile
v
v < 3 # v array'ın da 3'den kucuk olanlar

v[v < 3] # v array'ın da 3'den kucuk olanları sec
v[v > 3] # 3'den buyuk olanlar
v[v != 3] # 3'e esit olmayanlar
v[v <= 3]









######### Matematiksel Islemler (Mathematical Operations)
import numpy as np
v = np.array([1, 2, 3, 4, 5])
v

v / 5
v * 5 / 10
v ** 2
v - 2
v + 2

# Methodlar ile Matematiksel Islemler
v
np.subtract(v, 1)  # CIKARMA ISLEMI
np.add(v, 1)   # TOPLAMA ISLEMI
np.mean(v)   # ORTALAMA
np.sum(v)  # ELEMAN TOPLAMI
np.min(v)  # MİN DEGER
np.max(v)  # MAX DEGER
np.var(v)  # VARYANS

## Numpy Ile Ikı bilinmeyenli denklem çözme

# 5*x0 + x1 = 12
# x0 + 3*x1 = 10

a = np.array([[5, 1], [1, 3]]) # ilk eleman x0 katsayıları, ikinci eleman x1 katsayilari
b = np.array([12, 10])

np.linalg.solve(a, b) # sonucunda x0 ve x1'in cozumlerını verir
print(f" x0'in cozumu: {np.linalg.solve(a, b)[0]}, x1'in cozumu: {np.linalg.solve(a, b)[1]}")










