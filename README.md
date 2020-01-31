# Debis Module

[![PyPI version](https://badge.fury.io/py/debis.svg)](https://badge.fury.io/py/debis)

Dokuz Eylül Üniversitesi'nin [DEBİS](http://debis.deu.edu.tr) sitesinden öğrenci ve ders bilgileri çekmek amacıyla hazırlanmış bir modül.

## Installation

> pip install debis

## Demo

1. *user.py* dosyasını açın ve debis kullanıcı adı ve şifrenizi bu dosya içinde domain uzantısı kullanmadan belirtin.

örnek *user.py* kullanımı:

    username = 'ridvan.altun'
    password = 'benimgüzelsifrem'

2. *demo.py* dosyasını açıp [33](https://github.com/ridvanaltun/debis-module/blob/master/demo.py#L33). satırı kendinize uydurun.

3. Son olarak demo'yu çalıştırın.

> python demo.py

4. Örnek çıktı:

![alt text](https://github.com/ridvanaltun/debis-module/blob/master/images/example.png?raw=true "Çıktı")

## Usage

### Kütüphaneyi Projeye Eklemek:

```python
from  debis import person

# logic..
```

### Ön Ayarlar:

Kütüphaneyi kullanmaya başlamadan önce yapabileceğimiz ön ayarlar.

#### Request Hatalarını Kapat

Bu kütüphaneyi ilk defa kullanacak kullanıcılar için bu kısmın kullanılması tavsiye edilmez, oluşan hataları görmek için bu kısmı atlamanız tavsiye edilir.

```python
# request (istek) esnasında oluşan hataları bildir, default: True
Student.show_timer_errors = False
```

### Öğrenci Nesnesi Oluşturmak:

İki farklı şekilde öğrenci nesnesi oluşturmak mümkün:

- başlayıp kısa sürede biten işlemler için (normal bir şekilde)
- uzun süren işlemler için

Uzun süren işlemler için ayrı bir yöntem geliştirilmesinin nedeni Debis sitesinin belirli bir süre kadar işlem yapmayınca 'connection timeout' ile otomatik olarak oturumu sonlandırmasıdır ki bu yöntem sadece nadir senaryolarda kullanılıyor, kafanız karışmasın.

#### Normal Bir Şekilde Öğrenci Nesnesi Oluşturmak

```python
try:

ogrenci1 = person.Student('username', 'password')

### more codes..

except:
    print('Hata.')
```

#### Uzun Süren (~10dk) İşlemler İçin Öğrenci Nesnesi Oluşturmak

```python
try:

# timer çalışma esnasında oluşan hataları gösterme, default: True
person.Student.show_request_errors = False

ogrenci1 = person.Student('username', 'password', alive = True)

# connection timeout olmasın diye bir thread baslatiliyor
ogrenci1.timer.start()

### more codes..

except:
    print('Hata.')

finally:
    ogrenci1.timer.stop()
```

### Öğrenci Hakkında Bilgi Edinmek:

```python
print('\n#### OGRENCININ BUGUNE KADAR ALDIGI DONEMLER\n')

# öğrenciye ait dönemlerin adları bir liste içinde yazdırılıyor
print(ogrenci1.all_period_name)

print('\n#### OGRENCININ BUGUNE KADAR ALDIGI DERSLER\n')

# öğrenciye ait derslerin adları matris şeklinde yazdırılıyor
print(ogrenci1.all_lesson_name)

# for each kullanarak daha güzel bir sekilde goruntulemek mumkun
for x in ogrenci1.all_lesson_name:
    print(x)

print('\n#### DERS KODLARI\n')

# öğrenciye ait derslerin kodları matris şeklinde yazdırılıyor
print(ogrenci1.all_lesson_code)

# for each kullanarak daha güzel bir sekilde goruntulemek mumkun
for x in ogrenci1.all_lesson_code:
    print(x)

print('\n#### OGRENCI BILGILERI\n')

# tüm ögrenci bilgilerini topluca yazdırıyoruz
for x in ogrenci1:
    print(x)

# ogrenci hakkındaki bilgilere tek tek erisebiliyoruz
print(ogrenci1.name)
print(ogrenci1.no)
print(ogrenci1.grade)
print(ogrenci1.fakulty)
print(ogrenci1.department)
print(ogrenci1.grading)
```

### Ders Nesnesi Oluşturmak:

Ders oluşturmanın birçok yöntemi vardır.

```python
# dönem adı ve ders adı vererek ders nesnesi oluşturabiliriz
ders1 = ogrenci1.get_lesson('2017-2018-Güz', lesson_name='Türk Dili I')

# ders adı yerine ders kodu belirtebiliriz
ders1 = ogrenci1.get_lesson('2017-2018-Güz', lesson_code='TDL-1001')

# ders adı girerken buyuk kucuk harf uyumu gözetilmez
ders1 = ogrenci1.get_lesson('2018-2019-Güz', lesson_name='GÖRSEL PROGRAMLAMA 2')

# ders adını tam girmek zorunda değiliz
ders1 = ogrenci1.get_lesson('2018-2019-Güz', lesson_name='görsel')

# ders nesnesini oluştururken dönem adı belirtmedik, default olarak son dönem alındı
ders1 = ogrenci1.get_lesson(lesson_name='görsel')

# ders nesnesini sadece öğrenci nesnesinin içinde oluşturduk
ogrenci1.get_lesson(lesson_name='görsel')
```

### Ders Hakkında Bilgi Edinmek:

```python
print('\n#### DERS NESNE LISTESI\n')

# ogrenci nesnesi üstünden ders nesnelerini liste şeklinde yazdırabiliyoruz
print(ogrenci1.lessons)

# ogrenci icindeki ders nesnesinden veri cektik
print(ogrenci1.lessons[0].credit)

# olusturulan nesne ile ogrenciye ait nesnenin bir link oldugunun gösterimi
print(id(ogrenci1.lessons[0]))
print(id(ders1))

print('\n#### DERS BILGILERI\n')

# ders hakkında bilgileri toplu bir sekilde yazdiriyoruz
for x in ders1:
   print(x)

# ders hakkındaki bilgilere tek tek erisebiliyoruz
print(ders1.code)
print(ders1.name)
print(ders1.fakulty)
print(ders1.department)
print(ders1.branch)
print(ders1.credit)
print(ders1.attendance_required)
print(ders1.repeat_count)
print(ders1.attendance_status)
print(ders1.teaching_assistant)
print(ders1.teaching_assistant_email)
print(ders1.status)

print('\n#### DERS NOT BILGISI\n')

# ilgili dersin notlarına topluca erisiyoruz
print(ders1.notes)

# vize notuna ulasıyoruz
print(ders1.notes['vize_not'])
```

## Contributing

If you find any problem while using this library create an [issue](https://github.com/ridvanaltun/debis-module/issues/new). 😋

## License

This project is licensed under the [MIT License](https://github.com/ridvanaltun/debis-module/LICENSE).