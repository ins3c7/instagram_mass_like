# coding:utf-8
# by ins3c7, feb., 2016

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time, os, random, sys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from subprocess import Popen, PIPE


class CygwinFirefoxProfile(FirefoxProfile):

	@property
	def path(self):

		path = self.profile_dir

		# cygwin requires to manually specify Firefox path a below:
		# PATH=/cygdrive/c/Program\ Files\ \(x86\)/Mozilla\ Firefox/:$PATH
		try:
			proc = Popen(['cygpath','-d',path], stdout=PIPE, stderr=PIPE)
			stdout, stderr = proc.communicate()
			path = stdout.split('\n', 1)[0]

		except OSError:
			print("No cygwin path found")

		return path


class Instagram:

	lista = []
	segundosmax = 4

	perfis = open('perfis.txt', 'r').readlines()
	
	for perfil in perfis[0].split('@'):
		if perfil:
			if perfil not in lista:
				lista.append(perfil)

	print
	print str(len(lista)), 'perfis foram carregados.\n'

	def iniciar(self):
		usuario = 'marombahouse_'
		senha = '********'
		frases = open('frases.txt', 'r').readlines()
		print 'Iniciando...'
		firefoxProfile = CygwinFirefoxProfile()
		# firefoxProfile.set_preference('permissions.default.stylesheet', 2)
		firefoxProfile.set_preference("permissions.default.image", False)
		# firefoxProfile.set_preference("browser.display.show_image_placeholders", False)

		self.bro = webdriver.Firefox(firefoxProfile)
		self.bro.get('https://www.websta.me')
		try:
			self.bro.find_element(By.XPATH, '//button[text()="close"]').click()
		except:
			pass
		os.system('clear')
		try:
			self.bro.find_element(By.XPATH, '//a[@class="btn btn-default btn-lg"]').click()
			# self.bro.find_element_by_link_text('Entrar').click()
		except:
			pass

		raw_input('Clique em Entrar e pressione ENTER para continuar.')

		username = self.bro.find_element_by_xpath("//input[@name='username']")
		username.send_keys(usuario)

		password = self.bro.find_element_by_xpath("//input[@name='password']")
		password.send_keys(senha)

		self.bro.find_element(By.XPATH, '//input[@type="submit"]').click()
		os.system('clear')
		
		print 'Perfis carregados!'
		print
		
		lista_count = 1

		for nome in self.lista:
			try:
				url = 'http://websta.me/n/{}'.format(str(nome))
				print '\n"' + str(nome) + '" PERFIL', str(lista_count), 'DE', str(len(self.lista))
				print
				lista_count += 1
				self.bro.get(url)

				try:
					self.bro.find_element(By.XPATH, '//button[@data-action="follow"]').click()
					time.sleep(5)
				except:
					pass

				try:
					likes_count = 0
					likes = self.bro.find_elements(By.XPATH, '//button[@class="btn btn-default btn-xs likeButton"]')
					for like in likes:
						if likes_count > 4:break
						try:
							like.click()
							likes_count += 1
						except:
							pass
				except:
					pass

				comments = self.bro.find_elements(By.XPATH, '//textarea[@name="comment"]')

				x_coment = 0
				for comment in comments:
					if x_coment > 5:break
					frase = random.choice(frases).rstrip()
					banner = random.choice(['', ''])
					posbanner = random.choice([':)', ':D', ';D'])
					
					if not len(frase):
						frase = random.choice(frases).rstrip()

					try:
						comentario = '{} {} {}'.format(banner, str(frase).lower(), posbanner)
						print '-- Enviando comentário: "' + comentario + '"'
						comment.send_keys(comentario)
						x_coment += 1
					except:
						pass

				submits = self.bro.find_elements(By.XPATH, '//input[@type="submit"]')

				x_submit = 0

				for submit in submits:
					if x_submit > 2:break
					time.sleep(float(str(random.randrange(2,int(self.segundosmax))) +'.'+ str(random.randrange(10))))
					try:
						submit.click()
						# print '+ Enviando comentário', str(x_coment)
						x_submit += 1
					except:
						pass

				# self.bro.find_element_by_link_text('Earlier').click()
			except KeyboardInterrupt:
				exit()
			except:
				pass

		# comments = bro.find_element(By.XPATH, '//textarea[@name="comment"]').send_keys(str(random.choice(frases.rstrip())))

def main():
	insta = Instagram()
	insta.iniciar()

if __name__ == '__main__':
	os.system('clear')
	main()
