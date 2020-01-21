#Pour que le code fonctionne il vous faut selenium (pip install -U selenium) 
#il vous faut de plus le driver chromedriver (https://chromedriver.chromium.org/downloads)
from selenium import webdriver 
from time import sleep



class InstaBot:
    def __init__(self, nomcompte, mdp):#on cherche a se connecter à intagram, on clique donc sur les bouttons nécessaires tout en remplissant les champs
        self.driver = webdriver.Chrome()
        self.nomcompte = nomcompte
        self.mdp = mdp
        self.driver.get("https://instagram.com")
        sleep(2)
        self.driver.find_element_by_xpath("//a[contains(text(), 'Connectez-vous')]")\
            .click()
        sleep(2)
        self.driver.find_element_by_xpath("//input[@name=\"username\"]")\
            .send_keys(nomcompte)
        self.driver.find_element_by_xpath("//input[@name=\"password\"]")\
            .send_keys(mdp)
        self.driver.find_element_by_xpath('//button[@type="submit"]')\
            .click()
        sleep(5)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Plus tard')]")\
            .click()
        sleep(2)
    
    

    def get_unfollowers(self): #fonction retournant les personnes que vous suivez mais qui vous ne suivent pas
        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div[2]/div/button')\
            .click()
        self.driver.find_element_by_xpath("//a[contains(@href,'/{}')]".format(self.nomcompte))\
            .click()
        sleep(2)
        self.driver.find_element_by_xpath("//a[contains(@href,'/following')]")\
            .click()
        abonnement = self._get_names()
        self.driver.find_element_by_xpath("//a[contains(@href,'/followers')]")\
            .click()
        followers = self._get_names()
        follow_pas_back = [user for user in abonnement if user not in followers]
        print(follow_pas_back)

    def _get_names(self):#fonction permettant de récupérer une liste des personnes qui vous suivent et des personnes que vous suivez
        sleep(2)
        self.driver.execute_script('''
                                   var fBoite = document.querySelector('div[role="dialog"] .isgrP');
                                   function scrolldoucement(px, tmps, fin) {
                                           fBoite.scrollTop += px
                                           if (fin > px) {
                                                   setTimeout(scrolldoucement, tmps, px, tmps, fin - px)
                                                   }
                                           }
                                   scrolldoucement(20, 40, 4000)
                                   ''')
        #les lignes précédentes (54 à 61) sont codées en js c'est une fonction permettant de scrollé jusqu'en bas de la boite de dialogue
        #instagram contenant vos followers et/ou followés. Mon compte ne contenant que peu de followers/followés les valeurs de la fonction scrolldoucement
        #y sont adaptées. Pour votre compte il faudra surement les modifier.
        sleep(5)
        scroll_box = self.driver.find_element_by_xpath("/html/body/div[4]/div/div[2]/ul/div")
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            sleep(1)
            ht = self.driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                return arguments[0].scrollHeight;
                """, scroll_box)
        links = scroll_box.find_elements_by_tag_name('a')
        names = [name.text for name in links if name.text != '']
        # fermer le la boite de dialogue contenant vos followers/followés
        self.driver.find_element_by_xpath("/html/body/div[4]/div/div[1]/div/div[2]/button")\
            .click()
        return names

#vos informations de compte
nom_de_compte = 'aaaaaa'
mdp='bbbbbb'

my_bot = InstaBot(nom_de_compte, mdp)
my_bot.get_unfollowers()
