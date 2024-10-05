########################################
# VERI YAPILARI (DATA SCRUCTURES)
########################################
# - Sayılar (NUmbers): int, float, complex
# - Karakter Dizileri (Strings): str
# - Boolean (TRUE-FALSE): bool
# - Liste (List)
# - Sözlük (Dictionary)
# - Demet (Tuple)
# - Set






##########################################
# Sayılar (NUmbers): int, float, complex
##########################################

a = 5 # int
b = 10.5 # float

a * 3
b / 7
a ** 2

##### Tipleri Degistirmek #####
type(b)
int(b) # b nin tipi int oluyor

type(a)
float(a) # a nın tipi float oluyor

##########################################
# Karakter Dizileri (Strings): str
##########################################

print("John")
"John"

name = "John"
name

#### Cok Satırlı Karakter Dizileri #####

""""sknldsakda
dkasldnkalsdnasd
sşdmankdnsmdaödas"""

name
name[0]
name[3]

##### Karakter Dizilerinde Slice İslemleri ########

name
name[0:2] # 0. elemandan 2.elamana kadar git. 2. eleman haric (0. ve 1. indexi alır yanı 1. ve 2. elaman)

##### String İcerisinde Karakter Sorgulamak ####
long_str = "asndklandssafsğf "
"veri" in long_str

"asn" in long_str










##########################################
# String (Karakter Dizileri) Metodları
##########################################

dir(str)
dir(int)

#### len ######

name = "John"
len(name)
len("barankilic")
len("miuul")
# NOT: Eger class icerisindeyse "metod" degilse "fonksiyon"

#### upper() & lower() donusumleri ######
"miuul".upper()
"MIULL".lower()

###### replace: karakter degistirir ######
hi = "hello ai era"
hi.replace("l", "p")

#### split: bolme metodu #####
"hello ai era".split()
" ofofo ".split()
"ofofo".split("o")

##### capitalize: ilk harfi buyur ####3
"foo".capitalize()
dir("foo")
"foo".startswith("f")










##########################################
# Liste (List)
##########################################
# - Değiştirilebilir
# - Sıralıdır. Index islemleri yapılabilir
# - Kapsayıcıdır

notes = [50, 60, 80, 50]
notes
type(notes)
notes[2]
notes[0:2]

names = ["a", "b", "c", "d"]
names
type(names)

not_name = [1, 2, 3, "a", "b", True, [1, 2, 3]] # Kapsayıcı
not_name

not_name[0]   # Sıralıdır
not_name[3]
not_name[5]
not_name[6]
not_name[6][1]

type(not_name[6])
type(not_name[6][1])

not_name[0]
not_name[0] = 99
not_name[0]

##### Liste Metodları (List Methods) #####

dir(notes)
notes
len(notes)
len(not_name)

##### append: eleman ekler #####
notes.append(40)
notes

##### pop: indexe gore eleman siler #####
notes
notes.pop(0)
notes

#### insert: indexe gore eleman ekler ######
notes.insert(1, 200)
notes










##########################################
# Sözlük (Dictionary)
##########################################
# - key_value ciftlerinden olusurlar
# - Degistirilebilir
# - Sırasız (3.7 sonrasında sıralıdır)
# - Kapsayıcı

dictionary = {"isim": "baran",
              "soyisim": "kilic",
              "yas": 24}
dictionary

dictionary["isim"]

dictionary_2 = {"isim": ["baran", "emre", "efe"],
              "soyisim": ["kilic", "oglakci", "guzel"],
              "yas": [24, 21, 21]}
dictionary_2
dictionary_2["isim"] # listeye erisim
dictionary_2["yas"][1] # sozluk icinde yer alan listenin elemanina erisim

#### key sorgulama #####

"isim" in dictionary_2

##### key'e gore value'ya erismek ######
dictionary_2["isim"]
dictionary_2.get("isim")

#### Value Degistirmek ######
dictionary_2["isim"]
dictionary_2["isim"] = ["yusuf", "muhammed", "ebubekir"]
dictionary_2["isim"]

dictionary_2

#### Tum key'lere erismek #####
dictionary_2.keys()

##### Tum Value'lere erismek #####
dictionary_2.values()

##### Tum key-value ciftlerine erismek ######
dictionary_2.items()

##### Key-Value Degerlerini Guncellemek #######
dictionary_2.update({"yas": [23, 20, 20]})
dictionary_2

####### Yenı Key-Value Eklemek ####
dictionary_2.update({"cinsiyet": ["erkek", "erkek", "erkek"]})
dictionary_2

dictionary_2.keys()
dictionary_2.values()








##########################################
# Demet (Tuple)
##########################################
# - Degistirilemez
# - Sıralıdır (Elemanlara erisilir)
# - Kapsayıcıdır (Birden farklı veri yapıları icerir)

t = ("john", "mark", 1, 2)
type(t)
t
t[0]
t[3]
t[0:3] # slice islemi

# t[0] = 23 # Degistirilemez
# Not: Degistirilebilmesi icin once listeye cevrilir
t = list(t)
t[0] = 99
t = tuple(t)
t










##########################################
# Set (Kume islemleri gerektiginde kullanılır)
##########################################
# - Degistirilebilir
# - Sırasız + Eşsizdir
# - Kapsayıcıdır

###### difference(): Ikı kumenın farkı #######
set1 = set([1, 3, 5])
set2 = set([1, 2, 3])

# set1 de olup set2 de olmayan
set1.difference(set2)
set1 - set2

# set2 de olup set1 de olmayan
set2.difference(set1)
set2 - set1

##### symmetric_diffrence(): Iki kumede de birbirlerine gore olmayanlar #######
set1.symmetric_difference(set2)
set2.symmetric_difference(set1)

##### intersection(): Iki kumenin kesisimi #######
set1 = set([1, 3, 5])
set2 = set([1, 2, 3])

set1.intersection(set2)
set2.intersection(set1)
set1 & set2

##### union(): iki kumenin birlesimi ######
set1.union(set2)
set2.union(set1)

###### isdisjoint(): Iki kumenin kesisimi bos mu? ######
set1.isdisjoint(set2)
set2.isdisjoint(set1)

###### issubset(): Bir kume diger kumenin alt kumesi mi? #########
set1.issubset(set2)

###### issuperset(): Bir kume diger kumeyi kapsıyor mu? #########
set2.issuperset(set1)







# NOT: Liste, tuple, set ve dictioanry veri yapilari aynı
# zamanda Python Collections (Arrays) olarak da geçmektedir.