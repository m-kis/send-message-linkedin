import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException

# Remplacez par vos identifiants LinkedIn
email = "contact@m-kis.fr"
password = "xxxxxx"  # N'oubliez pas de remplacer par votre mot de passe

# Liste des URL de profils LinkedIn à contacter
profiles = [
    "https://www.linkedin.com/in/username/",
]

# Configuration du navigateur (Chrome ici) changez le chemin du driver
browser = webdriver.Chrome(service=Service("/Users/cedric/Downloads/chromedriver_mac_arm64/chromedriver"))
def is_logged_in():
    try:
        browser.find_element(By.ID, "ember27")
        return True
    except NoSuchElementException:
        return False

def login_to_linkedin():
    browser.get("https://www.linkedin.com")
    time.sleep(2)

    if is_logged_in():
        print("Déjà connecté")
        return

    browser.get("https://www.linkedin.com/login")
    time.sleep(2)
    browser.find_element(By.ID, "username").send_keys(email)
    browser.find_element(By.ID, "password").send_keys(password)
    browser.find_element(By.CSS_SELECTOR, ".btn__primary--large").click()
    time.sleep(3)

    # Vérifier si la page de vérification à deux facteurs est affichée
    if "checkpoint/challenge" in browser.current_url:
        print("Veuillez saisir le code de vérification à deux facteurs et appuyer sur 'Entrée'")
        input()
        print("Connexion réussie")
    else:
        print("Aucune vérification à deux facteurs requise")
def send_message(profile_url, message):
    browser.get(profile_url)
    time.sleep(2)
     # Switch to the message iframe
    browser.switch_to.frame(browser.find_element(By.XPATH, "//iframe[contains(@class,'msg-form__iframe')]"))

    # Wait for the message box to appear and input the message
    message_box = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".msg-form__contenteditable")))
    message_box.send_keys(message_template)

    # Click on the button to switch to send mode
    send_mode_button = browser.find_element(By.CSS_SELECTOR, "button.msg-form__send-toggle")
    send_mode_button.click()

    # Wait for the Send button to appear and click it
    send_button = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "button.msg-form__send-button")))
    send_button.click()

    # Switch back to the default frame
    browser.switch_to.default_content()

    try:
        name = browser.find_element(By.CSS_SELECTOR, "h1.text-heading-xlarge.inline.t-24.v-align-middle.break-words").text.split()[0]
    except NoSuchElementException:
        print("Name not found")
        return

    personalized_message = message.format(name=name)

    # Cliquez sur le bouton "Message" sur la page de profil
    message_button = browser.find_element(By.CSS_SELECTOR, "button[data-control-name='message']")
    message_button.click()
    time.sleep(2)

    # Cliquez sur le bouton "Joindre un fichier" dans la boîte de dialogue de message
    attach_button = browser.find_element(By.CSS_SELECTOR, "button#attachment-trigger-ember634")
    attach_button.click()
    time.sleep(2)

    # Sélectionnez le fichier à joindre
    file_input = browser.find_element(By.CSS_SELECTOR, "input[type='file']")
    file_input.send_keys("/Users/cedric/Documents/Plaquette_commercial_M-KIS.pdf")

    # Ajoutez le message personnalisé
    message_box = browser.find_element(By.CSS_SELECTOR, ".msg-form__contenteditable")
    message_box.send_keys(personalized_message)

    # Cliquer sur le bouton "Envoyer" s'il est visible
    try:
        # Cliquer sur le bouton d'envoi
        send_button = browser.find_element(By.CSS_SELECTOR, "button.msg-form__send-button")
        send_button.click()

    except NoSuchElementException:
        print("Aucun bouton d'envoi de message visible")

    time.sleep(2)


    print(f"Message envoyé à {name} :\n{personalized_message}\n")
login_to_linkedin()

message_template = """
Bonjour {name},
Your message here
"""

for profile_url in profiles:
    send_message(profile_url, message_template)

browser.quit()
