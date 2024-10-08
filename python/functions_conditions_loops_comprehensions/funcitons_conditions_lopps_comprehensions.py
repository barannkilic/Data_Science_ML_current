#######################################
# FONKSIYONLAR (FUNCTIONS):Belirli gorevleri yerine getiren kod parçaları
#######################################
from sys import set_asyncgen_hooks

from dataStructures.dataStructures import dictionary


#########################
# Fonksiyon Tanımlama
#########################

def calculate(x):
    print(x * 2)


calculate(2)

#### Iki argumanlı/parametreli fonksiyon tanımlayalım.

def summer(arg1, arg2 ):
    print(arg1 + arg2)


summer(3, 4)
summer(arg1 = 10, arg2 =12)
summer(arg2 = 12, arg1 = 10)








#############################################
# Docstring: Fonskiyonlara Bilgi notu ekleme
#############################################

def summer(arg1, arg2):
    """
    Sum of two numbers
    Args:
        arg1: int, float
        arg2: int, float

    Returns:
        int, float

    Examples:

    Notes:

    """

    print(arg1 + arg2)


summer(13, 14)







######################################
# Fonksiyonların Statement/Body Bolumleri
######################################

# def funciton_name(paramters/arguments):
#       statements (function body)

def say_hi():
    print("Merhaba")
    print("Hi")
    print("Hello")

say_hi()


def say_hi(string):
    print(string)
    print("Hi")
    print("Hello")

say_hi("Miuul")

def multiplication(a, b):
    conclusion = a * b
    print(conclusion)

multiplication(10, 9)


# girilen degerleri bir liste icinde sakla
list_store = []

def add_element(a, b):
    c = a * b
    list_store.append(c)
    print(list_store)


add_element(2,4)
add_element(5, 8)

############# NOT ##########
# GLOBAL: Genel kod icerisinde
# LOCAL: Bir etki alanı icinde (döngü, fonksiyon vb.)








############################################
# Ön Tanımlı Argumanlar/Parametreler (Default Parameters/Arguments)
#############################################

def divide(a, b):
    print(a / b)


divide(1, 2)


def divide(a, b = 2):
    print(a / b)


divide(3) # burada ikinci arguman tanımlı oldugundan girilmiyor
divide(2, 2) # ön tanımlı argumana biz yenı deger verip kullanabiliriz










#################################################
# Return: Fonksiyon Çıktılarını Girdi Olarak Kullanmak
################################################

def calculate(varm, moisture, charge):
    print((varm + moisture) / charge)

calculate(93, 12, 78) * 10
# Yukarıda return olmadıgı ıcın fonksiyon sonuc getirmiyor


def calculate(varm, moisture, charge):
    return (varm + moisture) / charge

calculate(93, 36, 26) * 10
#Yukarıda sonuc verir. Cunku return oldu


def calculate(varm, moisture, charge):
    varm = varm * 2
    moisture = moisture * 2
    charge = charge * 2
    output = (varm + moisture) / charge

    return varm, moisture, charge, output

calculate(90, 36, 56)

varm, moisture, charge, output = calculate(98, 12, 78)










###############################################
# Fonksiyon İcerisinden Fonksiyon Cagırmak
#############################################

def calculate(varm, moisture, charge):
    return int((varm + moisture) / charge) # sonucun int olması icin

calculate(90, 12, 12) * 10


def standardization(a, p):
    return a * 10 / 100 * p * p

standardization(45, 1)



def all_calculation(varm, moisture, charge, p):
    a = calculate(varm, moisture, charge)
    b = standardization(a, p)
    print(b * 10)

all_calculation(1, 3, 5, 12)


def all_calculation(varm, moisture, charge, a, p):
    print(calculate(varm, moisture, charge))
    b = standardization(a, p)
    print(b * 10)


all_calculation(1, 3, 5, 19, 12)








####################################################
# Lokal & Global Degiskenler (Local & Global Variables)
####################################################

list_store = [1, 2]
type(list_store)

def add_alement(a, b): # girilen iki sayiyi carp ve sonucu global'daki degiskene ata
    c = a * b
    list_store.append(c)
    print(list_store)

add_element(4, 6)
add_alement(6,8)

########################################################################################################################
########################################################################################################################






#################################
# KOSULLAR (CONDITIONS)
#################################

# True-False'u hatırlayalım
1 == 1
1 == 2


# if
if 1 == 1:
    print("something")

if 1 == 2:
    print("something")


number = 10
if number == 10:
    print("number is 10")

def number_chech(x):
    if x == 10:
        print("number is 10")

number_chech(10) # cıktı verir
number_chech(12) # cıktı vermez


# else & elif

def number_chech(x):
    if x == 10:
        print("x is 10")
    else:
        print("x is not 10")

number_chech(10)
number_chech(12)

def number(x):
    if x > 10:
        print("greater than 10")
    elif x == 10:
        print("equal to 10")
    else:
        print("less than 10")

number(10)
number(65)
number(5)








#################################
# DONGULER (LOOPS)
#################################


# FOR LOOP

students = ["baran", "ali", "emre", "yusuf"]
for student in students: # for ile listeyi gez ekrana bastır
    print(student)

for student in students: # for ile listeyi gez ekrana ilk harfleri buyuk olarak bastır
    print(student.capitalize())

for student in students:
    print(student.upper())

for student in students:
    print(len(student))


salaries = [1000, 2000, 3000, 4000, 5000]

for salary in salaries:
    print(salary)

# %20 zam uygula
for salary in salaries:
    print(int(salary * 20 / 100 + salary))

def new_salary(salary, rate):
    return int(salary * rate / 100 + salary)

new_salary(1500, 10)
new_salary(2000, 20)

for salary in salaries:
    print(new_salary(salary, 20))

## Maaslar listesinde gez 3000 ustu farklı 3000 altı farlı zamn yap

for salary in salaries:
    if salary >= 3000:
        print(new_salary(salary, 10))
    else:
        print(new_salary(salary, 20))


##################################################################################
# UYGULAMA - MULAKAT SORUSU
###################################

## Amaç: Asagıdaki sekilde string degistiren fonksiyon yazmak istiyoruz.

# before: "hi my name is john and i am learning python"
# after: "Hi mY NaMe iS JoHn aNd i aM LeArNiNg pYtHoN"

# cift index buyuk tek index kucuk


for i in range(0, 5):
    print(i)

for i in range(len("baran")):
    print(i)

def alternating(text):
    new_text = ""
    for text_index in range(len(text)): # girilen text'in indexilerinde gez
        print(text_index)
        if text_index % 2 == 0: # index cift ise buyut
            print(f"{text_index} index cift")
            new_text += text[text_index].upper()
        else: # index tek ise kucuk
            print(f"{text_index} index text")
            new_text += text[text_index].lower()
    print(new_text)

alternating("baran merhaba")
alternating("hi my name is john and i am learning python")
##############################################################################







###########################
# break & continue & while
###########################

salaries = [1000, 2000, 3000, 4000, 5000]

# break: Aranan kosul yakalandıgında dongunun durmasını saglar
for salary in salaries:
    if salary == 3000:
        break
    print(salary)

# continue: Aranan kosul yakalandıgında gormezden gel pas geç
for salary in salaries:
    if salary == 3000:
        continue
    print(salary)

# while: -dığı sürece (kosul dogru oldugu surece calıs)
number = 1
while number < 5:
    print(number)
    number += 1





################################
# Enumerate: Otomatik Counter/Indexer ile for loop
##############################
# bir liste icinde gezip işlem uygularken aynı zamanda idex bilgisine gore islem uygulamak

# indexi cift olanları bir listeye tek olanlara ayrı bir listeye

students = ["Baran", "Ali", "Yusuf", "Ebubekir"]

for student in students:
    print(student)

for index, student in enumerate(students):
    print(index, student)

for index, student in enumerate(students,1): # index 1'den baslıyor
    print(index, student)

A = []
B = []
for index, student in enumerate(students):
    print(index, student)
    if index % 2 == 0:
        A.append(student)
    else:
        B.append(student)
print(f"Liste A (Cift index):{A},\nListe B (Tek index): {B}")






##################################################################################
# UYGULAMA - MULAKAT SORUSU
###################################

# - divide_students fonksiyonu yazınız
# - Cift indexte yer alan ogrencileri bir listeye alınız
# - Tek indexte yer ala ogrencileri baska bir listeye alınız
# - Fakat bu iki liste tek bir liste olarak return olsun



students = ["John", "Mark", "Venessa", "Mariam"]

def divide_students(students):
    group = [[], []]
    for index, student in enumerate(students):
        print(index, student)
        if index % 2 == 0:   # cift index 0. indexe
            group[0].append(student)
        else:             # tek index 1. indexe
            group[1].append(student)
    return group

divide_students(students)






####################################################
# Alternating Fonksiyonunun Enumerate ile Yazılması
#####################################################

## Amaç: Asagıdaki sekilde string degistiren fonksiyon yazmak istiyoruz.

# before: "hi my name is john and i am learning python"
# after: "Hi mY NaMe iS JoHn aNd i aM LeArNiNg pYtHoN"

# cift index buyuk tek index kucuk

def alternating_with_enumerate(text):
    new_text = ""
    for index, character in enumerate(text): # enumerate ile index ve karakter ikilisi ile
        print(index, character)
        if index % 2 == 0:
           new_text += character.upper()
        else:
            new_text += character.lower()
    print(new_text)
alternating_with_enumerate("hi my name is john and i am learning python")





############################
# Zip
###############################

# Amaç: 3 farklı listenin elemanlarini indexe gore esleyelim
students = ["John", "Mark", "Venessa", "Mariam"]

departments = ["mathematics", "statistics", "pyhsics", "astronomy"]

ages = [23, 30, 36, 22]

# liste halinde
list(zip(students, departments, ages))

for i in list(zip(students, departments, ages)):
    print(i)




###################################
# lambda, map, filter, reduce
##################################


def summer(a, b):
    return a + b
summer(1, 2)

#########  lambda: fonksiyon tanımlama seklidir. Kullan at fonksiyondur

new_sum = lambda a, b: a + b # a ve b argumanlarından olusur ':' şu işi yapar 'a + b'
new_sum(1, 2)

######### map: dongu yazmaktan kurtarır

salaries = [1000, 2000, 3000, 4000, 5000]

def new_salary(x):
    return x * 20 / 100 + x

new_salary(1000)
for salary in salaries:
    print(new_salary(salary))

list(map(new_salary, salaries)) # liste  olarak cıktı vermesi icin 'list' olarak yazıldı.
# map'in icine uygulamak istedigmiz fonksiyon ve uzerinde gezecegi iteratif nesne yazılır

# İteratif Nesne: Uzerinde gezilebilen nesneler. Ornegin: [1, 2, 3] , ["baran", "ali"]

list(map(lambda x: x * 20 / 100 + x, salaries)) # kullan at fonksiyon ornegi


# del new_sum

list(map(lambda x: x * 20 / 100 + x, salaries))

# maaslarin karelerini alalım
list(map(lambda x: x ** 2, salaries))


####### FILTER: Belirli kosulu saglayanları secelim

list_store = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

list(filter(lambda x: x % 2 == 0, list_store)) # iteratif nesnede gezer ve 2'ye bolumunden kalanları verir


######## REDUCE: indirgemek
from functools import reduce
list_store = [1, 2, 3, 4]

reduce(lambda a, b: a + b, list_store)








#############################################
# COMPREHENSIOIONS
#############################################3

#########################
# LIST COMPREHENSIONS
#########################

#### ESKI YAPI
salaries = [1000, 2000, 3000, 4000, 5000]

def new_salary(x):
    return x * 20 / 100 + x

null_list = []
for salary in salaries:
    null_list.append(new_salary(salary))
null_list

# maaslari gez 3000'den buyukse new_salary ile listeye ekle degilse new_salary ile iki katını listeye ekle
null_list  = []
for salary in salaries:
    if salary > 3000:
        null_list.append(new_salary(salary))
    else:
        null_list.append(new_salary(salary * 2))
null_list

##### LIST COMPREHENSIONS YAPISI

# Amac: Maasler listesindeki her bir maasi 2 ile çarp
[salary * 2 for salary in salaries] # kaydetmek ıstersek bir degiskene atayabiliriz

# Amac: Maası 3000'den az olanlari 2 ile carp
[salary * 2 for salary in salaries if salary < 3000] # maaslari gezer 3000'den az olanlari 2 ile carpar

# Amac: Maası 3000'den az olana %20 zam yap
[salary * 20 / 100 + salary for salary in salaries if salary < 3000]

# Amac: Maası 3000'den az olanı 2 ile carp geriye kalan durumlarda 0 ile carp
[salary * 2 if salary < 3000 else salary * 0 for salary in salaries]

# Amac: Elimizde var olan bir fonksiyonu kullanalım.
# Maası 3000'den az olanı 2 ile carp ve zam uygula, 3000 den fazla olana sadece zam uygula
def new_salary(x):
    return x * 20 / 100 + x

[new_salary(salary * 2) if salary < 3000 else new_salary(salary) for salary in salaries]

# Amac: Sınav notlarından 45 altında olanlara %10 puan ekle, 45 ustu olanlara 3 puan ekle
notes = [23, 56, 46, 96, 82]
def note(x):
    return x * 10 / 100 + x

[note(point) if point < 45 else point + 3 for point in notes]


# Amac: Elimizde iki liste var istenmeyenleri kucuk ıstenenı buyut

students = ["Baran", "Ibrahim", "Efe", "Emre", "Yusuf"]
student_no = ["Baran", "Emre"]

# cıktımızda "baran" - "emre" kucuk yazılmalı cunku ıstenmeyen ogrencı listesinde var
[student.lower() if student in student_no else student.upper() for student in students]

# not in ile yaparsak yanı ıcermıyorsa mantııgyla cıktı aynı olur
[student.upper() if student not in student_no else student.lower() for student in students]







#########################
# DICT COMPREHENSIONS
#########################

dictionary = {"a": 1,
              "b": 2,
              "c": 3,
              "d": 4}

dictionary.keys()
dictionary.values()
dictionary.items()

# Amaç: Sozluk icinde yer alan her value'nın karesini al
{key: value ** 2 for (key, value) in dictionary.items()} # key'ler sabit value'ların karesini al

# Amac: key'leri buyuk harf yap, value'ler kalsın
{key.upper(): value for (key, value) in dictionary.items()}




#################################
# UYGULAMA - MULAKAT SORUSU
###################################

## Amac: Cift sayilarin karesi alınarak bir sozluge eklenmek istemektedir
# Key'ler orjinal, Value'ler ise degistirilmis degerler olacak
numbers = range(10)
numbers

#### ESKI YONTEM

new_dict = {}
for n in numbers:
    if n % 2 == 0:
        new_dict[n] = n ** 2    # new_dict[n]: n key'inde karsılık gelen value

new_dict

###### DICT COMPREHENSIONS

{n: n ** 2 for n in numbers if n % 2 == 0}
# iteratif nesnede gez, eger cift ise key'e koy value olarak karesini al

# Amac: Cift olan sayıların karesini value al tek sayilarin küpünü al sozluge ekle
{n: n ** 2 if n % 2 == 0 else n ** 3 for n in numbers}







###################################################
# LIST & DICT Comprehensions Uygulamalari - 1
####################################################

#############################
# Bir Veri Setindeki Degisken İsimlerini Degistirmek
####################

# Amac: Bir dataframe'de yer alan stringleri buyuk harfe cevir

import seaborn as sns
df = sns.load_dataset("car_crashes")
df.columns

#### Native Yontem
for column in df.columns:
    print(column.upper())

A = []
for column in df.columns:
    A.append(column.upper())
A
df.columns = A
df.columns

#### Comprehensions
df = sns.load_dataset("car_crashes")
df.columns = [column.upper() for column in df.columns]
df.columns




#############################
# İsminde "INS" olan degiskenlerin basina "FLAG_" digerlerine "NO_FLAG_" eklemek istiyoruz
####################
df = sns.load_dataset("car_crashes")
df.columns = [column.upper() for column in df.columns]
df.columns

df.columns = ["FLAG_" + column if "INS" in column else "NO_FLAG_" + column for column in df.columns]
df.columns








#################################################
# Amaç: Key'i string, Value'su asagidaki gibi bir liste olan sozluk olusturmak.
# Sadece sayisal degiskenler icin yapmak istiyoruz
###############################################
# ["mean", "min", "max", "var"]



df = sns.load_dataset("car_crashes")
df.columns

# veri setinde sayısal olan degiskenleri sec
num_columns = [column for column in df.columns if df[column].dtype != "O"]
# iteratif nesne de gez, ilgili degiskenin tipi kategorik degilse yani sayısal ise sec
num_columns

sozluk = {}
agg_list = ["mean", "min", "max", "sum"]

for column in num_columns:
    sozluk[column] = agg_list

sozluk


### KISA YOL
{column: agg_list for column in num_columns}
new_dict = {column: agg_list for column in num_columns}
new_dict

df[num_columns].head() # df'de numeric kolonları secer

df[num_columns].agg(new_dict) # sectigi numeric kolonlara sozlukte eslesen fonksiyonları uygular

