# Written with <3 by Julien Romero

import hashlib
from sys import argv
import sys
import itertools
from random import randint
if (sys.version_info > (3, 0)):
    from urllib.request import urlopen
    from urllib.parse import urlencode
else:
    from urllib2 import urlopen
    from urllib import urlencode


NAME = "koch".lower()
# This is the correct location on the moodle
#ENCFILE = "../passwords2020/" + NAME + ".enc"
# If you run the script on your computer: uncomment and fill the following
# line. Do not forget to comment this line again when you submit your code
# on the moodle.
ENCFILE = "/home/p5hngk/Downloads/Crack/koch.enc"



class Crack:
    """Crack The general method used to crack the passwords"""

    def __init__(self, filename, name):
        """__init__
        Initialize the cracking session
        :param filename: The file with the encrypted passwords
        :param name: Your name
        :return: Nothing
        """
        self.name = name.lower()
        self.passwords = get_passwords(filename)

    def check_password(self, password):
        """check_password
        Checks if the password is correct
        !! This method should not be modified !!
        :param password: A string representing the password
        :return: Whether the password is correct or not
        """
        password = str(password)
        cond = False
        if (sys.version_info > (3, 0)):
            cond = hashlib.md5(bytes(password, "utf-8")).hexdigest() in \
                self.passwords
        else:
            cond = hashlib.md5(bytearray(password)).hexdigest() in \
                self.passwords
        if cond:
            args = {"name": self.name,
                    "password": password}
            args = urlencode(args, "utf-8")
            page = urlopen('http://137.194.211.71:5000/' +
                                          'submit?' + args)
            if b'True' in page.read():
                print("You found the password: " + password)
                return True
        return False

    def crack(self):
        """crack
        Cracks the passwords. YOUR CODE GOES BELOW.

        We suggest you use one function per question. Once a password is found,
        it is memorized by the server, thus you can comment the call to the
        corresponding function once you find all the corresponding passwords.
        """
        #self.bruteforce_digits()
        #self.bruteforce_letters()

        # self.dictionary_passwords()
        # self.dictionary_passwords_leet()
        # self.dictionary_words_hyphen()
        # self.dictionary_words_digits()
        self.dictionary_words_diacritics()
        self.dictionary_city_diceware()

        #self.social_google()
        #self.social_jdoe()
        #self.paste()

    def bruteforce_digits(self):
        # Plus le MDP est long, plus les combinaisons à tester sont nombreuses : combinations = characters ^ length 
        
        number = ['0','1','2','3','4','5','6','7','8','9']
        
        for i in range(1,10) :
            print('--- Testing passwords of length {} ---'.format(i))
            for j in itertools.product(number, repeat=i):
                self.check_password(''.join(j))
        
        

    def bruteforce_letters(self):
        # Même problématique que précédement, plus le MDP est long, plus les combinaisons à tester sont nombreuses : combinations = characters ^ length 
        
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        
        for i in range(5,6) :
            print('--- Testing passwords of length {} ---'.format(i))
            for j in itertools.product(letters, repeat=i):
                self.check_password(''.join(j))



    def dictionary_passwords(self):
        
        with open("/home/p5hngk/Downloads/Crack/10k-most-common.txt") as infile:
            for password in infile:
                password = password[:-1] # on retire le saut de ligne
                self.check_password(password)
                
        

    def dictionary_passwords_leet(self):
        def leet(word):
            # try also with 4bcd3f6h1jklmn0pqr57u
            leet_matches = [['a', '@'],
                            ['e', '3'],
                            ['i', '1'],
                            ['l', '1'],
                            ['o', '0']]
                        
            l = []
            for letter in word:
                for match in leet_matches:
                    if match[0] == letter:
                        l.append(match)
            result = list(itertools.product(*l))
            [self.check_password(''.join(r)) for r in result]
            pass
            
        with open("/home/p5hngk/Downloads/Crack/10k-most-common.txt") as infile:
            for password in infile:
                leet(password[:-1]) # on retire le saut de ligne



    def dictionary_words_hyphen(self):
        
        with open("/home/p5hngk/Downloads/Crack/20k.txt") as infile:
            for password in infile:
                password = password[:-1] # on retire le saut de ligne
                
                for i in range(len(password)):
                    password_1 = password[:i] + "-" + password[i:]
                    self.check_password(password_1)
                    for j in range(len(password_1)):
                        password_2 = password_1[:j] + "-" + password_1[j:]
                        self.check_password(password_2)
                        for k in range(len(password_2)):
                            password_3 = password_2[:k] + "-" + password_2[k:]
                            self.check_password(password_3)
        
    

    def dictionary_words_digits(self):
        
        with open("/home/p5hngk/Downloads/Crack/20k.txt") as infile:
            for password in infile:
                password = password[:-1]
                
                number = ['0','1','2','3','4','5','6','7','8','9']
                for i in range(1,3) :
                    for j in itertools.product(number, repeat=i):
                        psw_tested = ''.join(str(password) + str(''.join(j)))
                        self.check_password(psw_tested)
                        
                        
                            
                            

    def dictionary_words_diacritics(self):
        def leet(word):
            # try also with 4bcd3f6h1jklmn0pqr57u
            leet_matches = [['ù', 'u']]
                            #['é', 'e']
                            #['è', 'e']
                            #['à', 'a']
                            #['ç', 'c']
                            #['ù', 'u']
                        
            l = []
            for letter in word:
                for match in leet_matches:
                    if match[0] == letter:
                        l.append(match)
            result = list(itertools.product(*l))
            [self.check_password(''.join(r)) for r in result]
            pass
            
        most_common_fr =[]
        with open("/home/p5hngk/Downloads/Crack/10k-most-common_fr.txt", encoding='utf-8') as infile:
            for psw in infile:
                most_common_fr.append(psw.split("," )[0].lower())
            
            for password in most_common_fr:
                leet(password[:-1]) # on retire le saut de ligne
        

    def dictionary_city_diceware(self):
        
        list_african_capital = []
        with open("/home/p5hngk/Downloads/Crack/capital.txt", encoding='utf-8') as infile:
            for psw in infile:
                list_african_capital.append(psw.split("," )[0].lower())
                
        list_african_capital.append('addisababa')
        list_african_capital.append('capetown')
        list_african_capital.append('santacruzdetenerifeandlaspalmas')
        
        for word1 in list_african_capital :
            for i in range(1,5) :
                for j in itertools.product(list_african_capital, repeat=i):
                    self.check_password('-'.join(j))
    
    

    def social_google(self):
        # On applique ici le principe de tout mettre en minuscule et changer les lettres
        psw_1 = 'prom3th3us'
        self.check_password(psw_1)
        
        psw_2 = 'prom3theus'
        self.check_password(psw_2)
        
        psw_3 = 'pr0m3th3us'
        self.check_password(psw_3)
        
        psw_4 = 'pr0metheus'
        self.check_password(psw_4)
        
        psw_5 = 'pr0m3theus'
        self.check_password(psw_5)
        
        psw_6 = 'pr0meth3us'
        self.check_password(psw_6)
        
        
       
        

    def social_jdoe(self):
        pass

    def paste(self):
        psw = 'Riseagainst1'
        self.check_password(psw)
        pass



def get_passwords(filename):
    """get_passwords
    Get the passwords from a file
    :param filename: The name of the file which stores the passwords
    :return: The set of passwords
    """
    passwords = set()
    with open(filename, "r") as f:
        for line in f:
            passwords.add(line.strip())
    return passwords


# First argument is the password file, the second your name
crack = Crack(ENCFILE, NAME)


if __name__ == "__main__":
    crack.crack()