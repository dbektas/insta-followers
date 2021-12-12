from selenium import webdriver
from time import sleep
import secrets

class InstaBot:
    def __init__(self, username, pw):
        self.driver = webdriver.Chrome()
        self.username = username
        self.driver.get("https://instagram.com")
        sleep(2)
        if self.cookies() == True:
            self.driver.find_element_by_xpath("//button[contains(text(), 'Accept')]")\
                .click()
        sleep(2)
        self.driver.find_element_by_xpath("//input[@name=\"username\"]")\
            .send_keys(username)
        self.driver.find_element_by_xpath("//input[@name=\"password\"]")\
            .send_keys(pw)
        self.driver.find_element_by_xpath('//button[@type="submit"]')\
            .click()
        sleep(10)
        if self.save_login_information() ==  True:
            self.driver.find_element_by_xpath("//button[contains(text(), 'Not now')]")\
                .click()
            sleep(10)
        if self.turn_on_notifications() ==  True:
            self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]")\
                .click()
            sleep(5)

    def get_unfollowers(self):
        self.driver.find_element_by_xpath("//a[contains(@href,'/{}')]".format(self.username))\
            .click()
        sleep(4)
        self.driver.find_element_by_xpath("//a[contains(@href,'/following')]")\
            .click()
        following = self._get_following()
        sleep(4)
        self.driver.find_element_by_xpath("//a[contains(@href,'/followers')]")\
            .click()
        followers = self._get_followers()
        not_following_back = [user for user in following if user not in followers]
        print(not_following_back)

    def _get_following(self): 
        sleep(2)
        scroll_box = self.driver.find_element_by_xpath("/html/body/div[6]/div/div/div[3]")
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
        # close button
        self.driver.find_element_by_xpath("/html/body/div[6]/div/div/div[1]/div/div[2]/button")\
            .click()
        return names
    
    def _get_followers(self):
        sleep(2)
        scroll_box = self.driver.find_element_by_xpath("/html/body/div[6]/div/div/div[2]")
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
        # close button
        self.driver.find_element_by_xpath("/html/body/div[6]/div/div/div[1]/div/div[2]/button")\
            .click()
        return names

    def cookies(self) -> bool:
        try:
            self.driver.find_element_by_xpath("//button[contains(text(), 'Accept')]")
            return True
        except:
            return False
    
    def turn_on_notifications(self) -> bool:
        try:
            self.driver.find_element_by_xpath("//button[contains(text(), 'Turn On')]")
            return True
        except:
            return False
    
    def save_login_information(self) -> bool:
        try:
            self.driver.find_element_by_xpath("//button[contains(text(), 'Save information')]")
            return True
        except:
            return False

my_bot = InstaBot(secrets.username, secrets.password)
my_bot.get_unfollowers()
