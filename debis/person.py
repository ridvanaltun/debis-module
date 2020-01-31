#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup as bs
import re
import timer

class Student:

	url = 'http://debis.deu.edu.tr/OgrenciIsleri/Ogrenci/OgrenciNotu/index.php'
	check_text = 'FAKÜLTE ADI'
	show_request_errors = True # True -> request esnasında hata varsa bildir, False -> vice verse
	show_timer_errors = True # True -> timer request hatası karşılaşınca bildirir, False -> vice verse
	timeout = 10
	timer_minute = 5

	headers = {
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36')
    	}

	def __init__(self, username, password, alive = False):

		self._username = username
		self._password = password
		self._lessons = []

		login_payload = {
		'username': self._username,
		'emailHost': 'ogr.deu.edu.tr',
		'password': self._password
		}

		with requests.Session() as self.session:

			if alive:
				self.__set_timer()

			page = Student.__send_request(self.session,'post', Student.url, Student.timeout, Student.headers, Student.show_request_errors, data = login_payload)
			page.encoding = 'iso-8859-9'

			if not Student.__page_test(page):
				return

			soup = bs(page.content,'html.parser')
			form = soup.find(attrs={'name':'form_donem'}).find_all('td')

			self.name = form[1].text
			self.no = form[4].text
			self.grade = form[7].text
			self.faculty = form[10].text
			self.department = form[13].text
			self.grading = form[16].text

			self.all_period_name = []
			self.all_period_id = []

			periods = soup.find(attrs={'id':'ogretim_donemi_id'}).find_all('option')
			del periods[0] # 'Dönem Seçiniz' yazısı listeden silindi

			for i, period in enumerate(periods):
				self.all_period_name.append(period.text.replace(' ','-'))
				self.all_period_id.append(period.get('value'))

			#tüm ders adları ve kodları bir liste içinde toplanıyor
			self.all_lesson_name = []
			self.all_lesson_code = []
			self.all_lesson_id = []

			for x in range(len(self.all_period_name)):
				self.all_lesson_name.append([])
				self.all_lesson_code.append([])
				self.all_lesson_id.append([])

				period_payload = {
				'ogretim_donemi_id' : self.all_period_id[x],
				'relative' : '../../../',
				'ogrenci_no' : self.no,
				'liste' : ''
				}

				page = Student.__send_request(self.session,'post', Student.url, Student.timeout, Student.headers, Student.show_request_errors, data = period_payload)
				soup = bs(page.content,'html.parser') 

				lessons = soup.find(attrs={'id':'ders'}).find_all('option')
				del lessons[0] # 'Ders Seçiniz' yazısı listeden silindi

				# ders adı buyutuluyor çünkü belirli bir standarta oturtuyoruz
				for lesson in lessons:
					self.all_lesson_name[x].append(lesson.text[9:].upper().replace('  ',' '))
					self.all_lesson_code[x].append(lesson.text[:8].replace(' ','-'))
					self.all_lesson_id[x].append(lesson.get('value'))

				lessons = []

	def __set_timer(self):

		if Student.timer_minute > 10 or Student.timer_minute < 0:
			print("'timer_minute' parametresi 10'dan büyük, 0'dan küçük olamaz!")
		elif Student.timer_minute == 0:
			pass
		else:
			def foo(session, method, url, timeout, headers):
				Student.__send_request(session, method, url, timeout, headers, Student.show_timer_errors)
			self.timer = timer.RepeatedTimer(Student.timer_minute * 60, foo, self.session, 'get', Student.url, Student.timeout, Student.headers)


	#salt okunur değişken
	@property
	def username(self):
		return self._username

	#salt okunur değişken
	@property
	def password(self):
		return self._password

	#salt okunur değişken
	@property
	def lessons(self):
		return self._lessons

	@staticmethod
	def __page_test(page):

		if 'Girmiş olduğunuz kullanıcı bilgileri hatalıdır.' in page.text:
			print('\nKullanıcı Bilgileriniz Hatalı!')
			return False

		# Eğer site bizi attıysa request sonrası giriş sayfasına gitmişiz demektir.
		# Biz belli bir süre işlem yapmayınca site oturumumuzu otomatik sonlandırıyor.
		elif 'D.E.Ü. Bilişim Servisleri' in page.text:
			print('\nSession Timeout Error: Site bizi attı! İşlem başarısız!')
			print("Geliştirici Notu: 5-10dk gibi uzun süren işlemler için Student nesnesi oluştururken 'alive = True' argümanı kullanın. ")
			return False

		# Olasılığı çok düşük bir durum
		elif Student.check_text not in page.text:
			print('\nGirmeye çalıştığınız sayfa güncellenmiş olabilir.\nGeliştirici Notu: Student.check_text parametresini güncelleyebilirsiniz.')
			return False

		else:
			return True

	@staticmethod
	def __send_request(session, method, url , timeout, headers, errors, data = None):

		err = requests.exceptions

		try:

			if method == 'post' and not data == None:
				page = session.post(url, data = data, timeout = timeout, headers = headers)
			
			if method == 'get' and data == None:
				page = session.get(url, timeout = timeout, headers = headers)

			page.raise_for_status()
			return page

		except err.Timeout as errt: # belki burada tekrar istek atılabilir duruma göre
			if errors == True:
				print('\nrequests.exceptions.Timeout : Belirtilen süre içinde işlem (get veya post) tamamlanamadı.')
				print('Geliştirici Notu: Internet veya site yavaşlığından kaynaklı bir problem olabilir, bu durumda; ex. Student.timeout değişkenine yüksek bir değer atayabilirsiniz.\n\n')
				print('DETAILS :\n\n' + str(errt))
			raise requests.exceptions.Timeout
		except err.HTTPError as errh:
			if errors == True:
				print('\nrequests.exceptions.HTTPError : Ulaşmaya çalıştığımız sayfa hata verdi.\n\n')
				print('DETAILS :\n\n' + str(errh))
			raise requests.exceptions.HTTPError
		except err.ConnectionError as errc:
			if errors == True:
				print("\nrequests.exceptions.ConnectionError : Internet bağlantısı, DNS Server veya bağlanmaya çalıştığımız URL'de bir hata var.")
				print('Geliştirici Notu: Internet veya site yavaşlığından kaynaklı bir problem olabilir, bu durumda; ex. Student.timeout değişkenine yüksek bir değer atayabilirsiniz.\n\n')
				print('DETAILS :\n\n' + str(errc))
			raise requests.exceptions.ConnectionError
		except err.MissingSchema as errm:
			if errors == True:
				print("\nrequests.exceptions.MissingSchema : Kullandığınız URL='{}', 'http://' veya 'https://' ifadesi içermiyor.\n\n".format(Student.url))
				print('DETAILS :\n\n' + str(errm))
			raise requests.exceptions.MissingSchema
		except (err.InvalidURL, err.URLRequired):
			if errors == True:
				print("\nrequests.exceptions.URLRequired : Girdiğiniz '{}' adres geçersizdir.".format(Student.url))
			raise requests.exceptions.URLRequired
		except err.TooManyRedirects:
			if errors == True:
				print('\nrequests.exceptions.TooManyRedirects : Çok fazla yönlendirme var.')
			raise requests.exceptions.TooManyRedirects
		except err.RequestException as errr:
			if errors == True:
				print ('\nrequests.exceptions.RequestException : Bilinmeyen bir request hatası bulundu.\n\n')
				print('DETAILS :\n\n' + str(errr))
			raise requests.exceptions.RequestException
		except KeyboardInterrupt:
			if errors == True:
				print('\nKeyboardInterrupt : İşlemi sonlandırdınız.')
			raise KeyboardInterrupt

	def __iter__(self):
		samples = {
		'self.name':self.name,
		'self.no':self.no,
		'self.grade':self.grade,
		'self.fakulty':self.faculty,
		'self.department':self.department,
		'self.grading':self.grading
		}
		space = ''
		for s in samples:
			for x in range(30 - len(s)):
				space = space + ' '
			yield s + space + ': ' + samples.get(s)
			space = ''
		return

	def get_lesson(self, period_name = None, **kwargs): # lesson_name, lesson_code

		if 'lesson_name' in kwargs and 'lesson_code' in kwargs:
			print("\nHATA : get_lesson() -> Şu iki parametreden sadece birini kullanabilirsiniz: 'lesson_code', 'lesson_name'")
			return
		elif 'lesson_name' not in kwargs and 'lesson_code' not in kwargs and len(kwargs) > 0:
			print("\nHATA : get_lesson() -> İsteğe bağlı olarak 'period_name' parametresi ve zorunlu olarak sadece 'lesson_code' veya 'lesson_name' parametresini kullanabilirsiniz.")
			return
		elif 'lesson_name' not in kwargs and 'lesson_code' not in kwargs:
			print("\nHATA : get_lesson() -> 'lesson_code' veya 'lesson_name' parametresi kullanmanız gerekiyor!")
			return
		else:
			# isteğe bağlı period_name parametresi için dönem seçimi yapılıyor
			if period_name == None:
				selected_period_id = self.all_period_id[0] # son dönemi getiriyor
				index = 0			
			else:
				selected_period_id = self.all_period_id[self.all_period_name.index(period_name)]
				index = self.all_period_name.index(period_name)

		if 'lesson_name' in kwargs:

			# kullanıcı ders adını buyuk-kucuk girebilmesi için çalışan satır
			capital_lesson_name = kwargs['lesson_name'].upper()

			# lesson_name parametresi'ne listede en yakın ders adını al
			selected_lesson = ''
			for lesson in self.all_lesson_name[index]:
				if not lesson.find(capital_lesson_name) == -1: # -1 -> yok
					selected_lesson = lesson
					break

			# eger ders bulunamadıysa kullanıcıyı bilgilendir
			if selected_lesson== '':
				print("'{}' dönemine ait, içinde '{}' içeren bir ders adı bulunamadı.".format(self.all_period_name[index], lesson_name))
				return

			selected_lesson_id = self.all_lesson_id[index][self.all_lesson_name[index].index(selected_lesson)]

		elif 'lesson_code' in kwargs:

			selected_lesson_id = self.all_lesson_id[index][self.all_lesson_code[index].index(kwargs['lesson_code'])]

		lesson_payload = {
		'ders' : selected_lesson_id,
		'ogretim_donemi_id' : selected_period_id,
		'relative' : '../../../',
		'ogrenci_no' : self.no,
		'liste' : ''
		}

		page = Student.__send_request(self.session,'post', Student.url, Student.timeout, Student.headers, Student.show_request_errors, data = lesson_payload)
		soup = bs(page.content,'html.parser')

		lesson_object = Lesson(soup)

		self._lessons.append(lesson_object)

		return lesson_object

class Lesson:
	def __init__(self, soup):
		
		# pieces[0] -> sol kisim, pieces[1] -> sag kisim
		lesson_data = soup.find(attrs={'name':'form_ders'}).table
		pieces = lesson_data.find_all('table')
		lesson_infos = pieces[0].find_all('td')

		# Öğrencinin Ders Durumu: BAŞARILI, ALIYOR vs
		self.status = lesson_data.find_all('td')[-1].text

		# Öğretim Görevlisi Mail Adresi, Öğretim Görevlisi Adından Çekiliyor
		self.teaching_assistant_email = re.findall(r'[\w\.-]+@[\w\.-]+', lesson_infos[20].text)
		email = self.teaching_assistant_email
		self.teaching_assistant_email = self.teaching_assistant_email[0]

		if not len(email) > 0:
			self.teaching_assistant_email = 'Not Found'

		if len(lesson_infos[20].text.replace('('+email[0]+')','').strip()) < 4: # 4 sembolik
			self.teaching_assistant  = 'Not Found'
		else:
			self.teaching_assistant  = lesson_infos[20].text.replace('('+email[0]+')','').strip()
	
		# Ders Kodu ve Ders Adı Parçalanıyor
		lesson_name_info = lesson_data.td.text.split('-')
	
		self.code = lesson_name_info[0].strip()
		self.name = lesson_name_info[1].strip()
		self.fakulty = lesson_infos[2].text
		self.department = lesson_infos[5].text
		self.branch = lesson_infos[8].text
		self.credit = lesson_infos[11].text
		self.attendance_required = lesson_infos[14].text
		self.repeat_count = lesson_infos[17].text
		self.attendance_status = lesson_infos[23].text.replace('/','').replace('\n','')

		self.notes = {}

		lesson_soup = pieces[1].find_all('td')

		for i,x in enumerate(lesson_soup):

			if 'Vize' in x:

				if '1.Vize' in x or '1. Vize' in x:
					#self.notes['vize_1_tarih'] = lesson_soup[i+1].text
					self.notes['vize_1_avg'] = lesson_soup[i+2].text
					self.notes['vize_1_not'] = lesson_soup[i+4].text
				elif '2.Vize' in x or '2. Vize' in x:
					#self.notes['vize_2_tarih'] = lesson_soup[i+1].text
					self.notes['vize_2_avg'] = lesson_soup[i+2].text
					self.notes['vize_2_not'] = lesson_soup[i+4].text
				else:
					#self.notes['vize_tarih'] = lesson_soup[i+1].text
					self.notes['vize_avg'] = lesson_soup[i+2].text
					self.notes['vize_not'] = lesson_soup[i+4].text

			elif 'Quiz' in x:
				#self.notes['quiz_tarih'] = lesson_soup[i+1].text
				self.notes['quiz_avg'] = lesson_soup[i+2].text
				self.notes['quiz_not'] = lesson_soup[i+4].text

			elif 'Uygulama' in x:
				#self.notes['uygulama_tarih'] = lesson_soup[i+1].text
				self.notes['uygulama_avg'] = lesson_soup[i+2].text
				self.notes['uygulama_not'] = lesson_soup[i+4].text

			elif 'Rapor/Ödev' in x or 'Ödev' in x:
				#self.notes['odev_tarih'] = lesson_soup[i+1].text
				self.notes['odev_avg'] = lesson_soup[i+2].text
				self.notes['odev_not'] = lesson_soup[i+4].text

			elif 'Laboratuvar' in x or 'Lab' in x:
				#self.notes['lab_tarih'] = lesson_soup[i+1].text
				self.notes['lab_avg'] = lesson_soup[i+2].text
				self.notes['lab_not'] = lesson_soup[i+4].text

			elif 'Snfiçi' in x:
				#self.notes['sinif_ici_tarih'] = lesson_soup[i+1].text
				self.notes['sinif_ici_avg'] = lesson_soup[i+2].text
				self.notes['sinif_ici_not'] = lesson_soup[i+4].text

			elif 'Final' in x:
				#self.notes['final_tarih'] = lesson_soup[i+1].text
				self.notes['final_avg'] = lesson_soup[i+2].text
				self.notes['final_not'] = lesson_soup[i+4].text

			elif 'Yarıyıl Sonu Başarı Notu' in x:
				#self.notes['yariyil_basari_tarih'] = lesson_soup[i+1].text
				self.notes['yariyil_basari_avg'] = lesson_soup[i+3].text
				self.notes['yariyil_basari_not'] = lesson_soup[i+4].text

			elif 'Başarı Notu' in x: #ders saydırınca boyle oluyor
				self.notes['basari_avg'] = lesson_soup[i+3].text
				self.notes['basari_not'] = lesson_soup[i+4].text

			elif 'Bütünleme Notu' in x: 
				#self.notes['bütünleme_tarih'] = lesson_soup[i+1].text
				self.notes['bütünleme_avg'] = lesson_soup[i+2].text
				self.notes['bütünleme_not'] = lesson_soup[i+4].text
				
			elif 'Bütünleme Sonu Başarı Notu' in x: 
				#self.notes['bütünleme_sonu_basari_notu_tarih'] = lesson_soup[i+1].text
				self.notes['bütünleme_sonu_basari_not'] = lesson_soup[i+4].text

	def __iter__(self):
		samples = {
		'self.code':self.code,
		'self.name':self.name,
		'self.fakulty':self.fakulty,
		'self.department':self.department,
		'self.branch':self.branch,
		'self.credit':self.credit,
		'self.attendance_required':self.attendance_required,
		'self.repeat_count':self.repeat_count,
		'self.attendance_status':self.attendance_status,
		'self.teaching_assistant':self.teaching_assistant,
		'self.teaching_assistant_email':self.teaching_assistant_email,
		'self.status':self.status
		}
		space = ''
		for s in samples:
			for x in range(30 - len(s)):
				space = space + ' '
			yield s + space + ': ' + samples.get(s)
			space = ''
		return