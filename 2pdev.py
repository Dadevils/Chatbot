from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import time
import json




class Bot():
    def __init__(self):
        self.runtime = True
        self.firsttime = True
        self.message_counter = 15

        self.settings_parser()

        time.sleep(1)

       




    def WaitForObject(self, type, string, browser):
        return WebDriverWait(browser, 3).until(EC.presence_of_element_located((type,string)))

    def WaitForObjects(self, type, string, browser):
        return WebDriverWait(browser, 3).until(EC.presence_of_all_elements_located((type,string)))



    ### Printing the Logo  ###

    def start(self):
        print("""
  ______             _______                      
 /      \           |       \                     
|  $$$$$$\  ______  | $$$$$$$\  ______  __     __ 
 \$$__| $$ /      \ | $$  | $$ /      \|  \   /  \\
 /      $$|  $$$$$$\| $$  | $$|  $$$$$$\\$$\ /  $$
|  $$$$$$ | $$  | $$| $$  | $$| $$    $$ \$$\  $$ 
| $$_____ | $$__/ $$| $$__/ $$| $$$$$$$$  \$$ $$  
| $$     \| $$    $$| $$    $$ \$$     \   \$$$   
 \$$$$$$$$| $$$$$$$  \$$$$$$$   \$$$$$$$    \$    
          | $$                                    
          | $$                                    
           \$$                                    
           
    """)

        print("\n\n")
        self.manager()

    



    def manager(self):

        input("Type Something to start...")

        ## Three Steps to create, login and loop the message process ##

        self.parallel_browser()
        self.login()
        self.loop()


    def captcha_check(self, browser):
        try:
            self.WaitForObject(By.XPATH, "//div[@id='checkbox']", browser)
            print("Captcha blocking continuation!")
            input("Type something to continue if you finished all login steps...")
        except:
            return

        


    def login(self):

        time.sleep(1)

        ## Logging in Account 1 ##

        e_query1 = self.WaitForObject(By.XPATH, "//input[@name='email']", self.b1)
        e_query1.send_keys(self.emails[0])

        time.sleep(1)

        p_query1 = self.WaitForObject(By.XPATH, "//input[@name='password']", self.b1)
        p_query1.send_keys(self.passwords[0])

        time.sleep(1)

        p_query1.send_keys(Keys.ENTER)


        ## Logging in Account 2 ##

        e_query2 = self.WaitForObject(By.XPATH, "//input[@name='email']", self.b2)
        e_query2.send_keys(self.emails[1])

        time.sleep(1)

        p_query2 = self.WaitForObject(By.XPATH, "//input[@name='password']", self.b2)
        p_query2.send_keys(self.passwords[1])
        
        time.sleep(1)

        p_query2.send_keys(Keys.ENTER)

        time.sleep(1)

        self.captcha_check(self.b1)
        self.captcha_check(self.b2)


       




        


    ### Translating Setting Json into Code ###

    def settings_parser(self):
        with open("settings.json") as settings_json:
            settings_data = json.load(settings_json)
            self.server_id = settings_data["server_id"]
            self.channel_ids = settings_data["channel_ids"]
            self.protocol_ids = settings_data["protocol_ids"]
            self.timeout = settings_data["timeout"]
            self.developer_mode = settings_data["developer_mode"]

            self.emails = settings_data["emails"]
            self.passwords = settings_data["passwords"]



    ### Creating list from file algorithm ###

    def file_to_list(self, filename):
        with open(filename) as protocol:
            plain_text = protocol.read()

            for line in plain_text.split("\n"):
                self.clines.append(line)



    ### Creation of Parallel Browsers ###

    def parallel_browser(self):

        print("Opening Parallel Browsers...")

        self.b1 = webdriver.Chrome("./chromedriver.exe")
        self.b1.get("https://discord.com/login")

        self.b2 = webdriver.Chrome("./chromedriver.exe")
        self.b2.get("https://discord.com/login")

        print("Please login.")

        time.sleep(1)



    def interact(self, browser):

        if self.firsttime:
            self.sending_message(self.clines[self.message_counter], browser)
            self.message_counter += 1

            self.firsttime = False
            return

            
        self.answer(browser)
        time.sleep(int(self.timeout))

        self.sending_message(self.clines[self.message_counter], browser)
        self.message_counter += 1




    def chat(self):

        ## Algorithm for change of talking browser ##

        current_b = self.b1
        sleeping_b = self.b2

        cache_b = current_b

        while self.runtime:
            
            self.interact(current_b)
            current_b = sleeping_b
            sleeping_b = cache_b

            cache_b = current_b
            
        
    
    def find_message2(self, browser, p_text):

        xpath = "//div[text()='" + p_text +"']"

        print("Method 1 did not work, starting Method 2 to find message")

        if self.developer_mode:
            print("XPATH being used: " + xpath)

        message = self.WaitForObject(By.XPATH, xpath, browser)

        if self.developer_mode:
            print("Message ID: " + str(message.get_attribute("id")))


        return message



    def find_message1(self, browser, p_text):
        messages = self.WaitForObjects(By.XPATH, "//div[@class='markup-2BOw-j messageContent-2qWWxC']", browser)

        if not str(messages[-1].get_attribute("innerText")) == p_text:
            
            print("Method 1 Failed!")

            if self.developer_mode:
                print("Failure Analysis:\n")
                print("Previous Text:")
                print(p_text)

                print("\n")

                print("Message's Text")
                print(":" + str(messages[-1].get_attribute("innerText")) + ":")

            raise Exception("Text not found")

        print("Method 1 used \n\n")

        return messages[-1]

    def find_answer_button(self, browser):
        try:
            self.reply_button = self.WaitForObject(By.XPATH, "//div[@data-list-item-id='chat-messages___chat-messages-" + str(self.message_id) + "']/div[@class='buttonContainer-DHceWr']/div[@class='buttons-cl5qTG container-3npvBV isHeader-2dII4U']/div[@class='wrapper-2aW0bm']/div[@aria-label='Reply']", browser)
            if self.developer_mode:
                print("English Version used")
            return
        except:
            print("Reply button could not be found in english version!")

        try:    
            self.reply_button = self.WaitForObject(By.XPATH, "//div[@data-list-item-id='chat-messages___chat-messages-" + str(self.message_id) + "']/div[@class='buttonContainer-1502pf']/div[@aria-label='Nachrichtenaktionen']/div[@class='wrapper-2vIMkT']/div[@aria-label='Antworten']", browser)
            if self.developer_mode:
                print("German Version used")
            return
        except:
            print("Reply button could not be found!")



    ### Clicking the reply button ###

    def answer(self, browser):

        time.sleep(1.5)
        previous_text = self.clines[self.message_counter - 1].replace("\n", "").strip()

        ## Testing two ways to find the previous message ##

        try: 
            message = self.find_message1(browser, previous_text)
            self.message_id = str(message.get_attribute("id")).split("-")[2]
            if self.developer_mode:
                print(self.message_id)
            message.click()

        except:
            try:
                message = self.find_message2(browser, previous_text)
                self.message_id = str(message.get_attribute("id")).split("-")[2]
                if self.developer_mode:
                    print(self.message_id)

                message.click()
            except:
                print("Any attempt to find the message failed - Message will be sent without reply note")
                return

        time.sleep(0.5)
        self.find_answer_button(browser)
        self.reply_button.click()


        for x in range(9):
            try:
                message.click()
                time.sleep(1)
                self.reply_button.click()
                print("Reply-Button found! Tries needed: " + str(x + 1))
                return
            except:
                print(f"Try {x + 1} failed.")
                time.sleep(0.5)

        print("Button could not be found - message will be sent without answer note.")   

        

            




    ### Sending the message ###

    def sending_message(self, phrase, browser):
        self.WaitForObject(By.XPATH, "//div[@class='markup-eYLPri slateTextArea-27tjG0 fontSize16Padding-XoMpjI']", browser).send_keys(phrase)
        time.sleep(1)
        self.WaitForObject(By.XPATH, "//div[@class='markup-eYLPri slateTextArea-27tjG0 fontSize16Padding-XoMpjI']", browser).send_keys(Keys.ENTER)
        #textArea-2CLwUE textAreaSlate-9-y-k2 slateContainer-3x9zil


    
    ### Extended Functions ###

    def loop(self):

        for i in range(len(self.channel_ids)):
            
            """
            def trier():
                for x in range(5):
                    try:
                        print("Searching Channel " + self.channel_ids[i])
                        self.b1.get("https://discord.com/channels/" + self.server_id + "/" + self.channel_ids[i])
                        self.b2.get("https://discord.com/channels/" + self.server_id + "/" + self.channel_ids[i])

                        time.sleep(4)

                        self.WaitForObject(By.XPATH, "//a[@href='/channels/" + str(self.server_id) + "/" + str(self.channel_ids[i]) + "']", self.b1).click()
                        self.WaitForObject(By.XPATH, "//a[@href='/channels/" + str(self.server_id) + "/" + str(self.channel_ids[i]) + "']", self.b2).click()

                        return
                    except:
                        print(f"Try {x+1} failed")
                        time.sleep(2)

            """
 
            
            #trier()
                
            self.b1.get("https://discord.com/channels/" + self.server_id + "/" + self.channel_ids[i])
            self.b2.get("https://discord.com/channels/" + self.server_id + "/" + self.channel_ids[i])

            input()

            
            ## Resetting Conversation Lines ##

            print("Formating Conversation...")

            self.clines = []
            self.message_counter = 0
            self.file_to_list(self.protocol_ids[i])



            print("Starting Chat!")

            try:
                self.chat()
            except IndexError:
                print("End of the conversation \n\n")
                continue
                



#### Scroll down after getting in different channel ####
#### Captcha identification at login ####
#### Neural Network to make prescripted conversations unnecessary ####






instance = Bot()
instance.start()
nothing = input()
