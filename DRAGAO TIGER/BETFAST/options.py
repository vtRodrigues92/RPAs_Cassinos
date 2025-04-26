

'''def manipula_aba():

    try:
        # Abre uma nova aba e vai para o site do SO
        browser.execute_script("window.open('https://www.esportiva.bet', '_blank')")
        time.sleep(15)

        #Fechando a Aba Ativa
        browser.close()

        # Muda de aba
        browser.switch_to_window(browser.window_handles[0])

    except:
        pass'''


'''# Definindo opções para o browser
    warnings.filterwarnings("ignore", category=DeprecationWarning) 
    chrome_options = webdriver.ChromeOptions() 
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_experimental_option('useAutomationExtension', False)
    #chrome_options.add_argument("--incognito") #abrir chrome no modo anônimo
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    #chrome_options.binary_location = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    #chrome_options.add_argument("window-size=1037,547")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_argument('disable-extensions')
    chrome_options.add_argument('disable-popup-blocking')
    chrome_options.add_argument('disable-infobars')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('log-level=3')'''



'''# Definindo opções para o browser
    warnings.filterwarnings("ignore", category=DeprecationWarning) 
    chrome_options = webdriver.ChromeOptions() 
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_argument("--disable-gpu")
    #chrome_options.add_experimental_option('useAutomationExtension', False)
    #chrome_options.add_argument("--incognito") #abrir chrome no modo anônimo
    #chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    #chrome_options.binary_location = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    #chrome_options.add_argument("window-size=1037,547")
    #chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    #chrome_options.add_argument('disable-extensions')
    #chrome_options.add_argument('disable-popup-blocking')
    #chrome_options.add_argument('disable-infobars')
    #chrome_options.add_argument('--disable-dev-shm-usage')
    #chrome_options.add_argument('log-level=3')'''

