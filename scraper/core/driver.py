from selenium import webdriver

def get_driver() : 
    options = webdriver.ChromeOptions() 
    
    # mode invisible (important pour production)
    options.add_argument("--headless=new")

    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)

    return driver