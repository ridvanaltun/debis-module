from debis import *
import user

def main():

	try:

		#Student.show_request_errors = False
		#Student.show_timer_errors = False

		ogrenci1 = Student(user.username, user.password)
		#ogrenci1 = Student(user.username, user.password, alive = True)
		#ogrenci1.timer.start()
		#print('Timer Çalışıyor Mu? : ', ogrenci1.timer.is_running)

		print('\n#### OGRENCININ BUGUNE KADAR ALDIGI DONEMLER\n')
		print(ogrenci1.all_period_name)

		print('\n#### OGRENCININ BUGUNE KADAR ALDIGI DERSLER\n')
		#print(ogrenci1.all_lesson_name)
		for x in ogrenci1.all_lesson_name:
			print(x)

		print('\n#### DERS KODLARI\n')
		#print(ogrenci1.all_lesson_code)
		for x in ogrenci1.all_lesson_code:
			print(x)

		print('\n#### OGRENCI BILGILERI\n')
		for x in ogrenci1:
			print(x)

		ders1 = ogrenci1.get_lesson('2017-2018-Güz', lesson_name='Türk Dili I')
		#ders1 = ogrenci1.get_lesson('2017-2018-Güz', lesson_code='TDL-1001')
		#ders1 = ogrenci1.get_lesson('2018-2019-Güz', lesson_name='GÖRSEL PROGRAMLAMA 2')
		#ders1 = ogrenci1.get_lesson('2018-2019-Güz', lesson_name='görsel')
		#ders1 = ogrenci1.get_lesson(lesson_name='görsel')
		#ogrenci1.get_lesson(lesson_name='görsel')

		print('\n#### DERS NESNE LISTESI\n')
		print(ogrenci1.lessons)
		#print(ogrenci1.lessons[0].credit)
		#print(id(ogrenci1.lessons[0]))
		#print(id(ders1))
		
		print('\n#### DERS BILGILERI\n')
		for x in ders1:
			print(x)

		print('\n#### DERS NOT BILGISI\n')
		print(ders1.notes)

	except:
		print('Hata.')

	finally:
		pass
		#ogrenci1.timer.stop()

if __name__ == '__main__':
	main()