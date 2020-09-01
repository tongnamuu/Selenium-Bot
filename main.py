from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time, math
from image import make_result, init, clean

qal_list = (
    r'a \times   \dfrac{ 5+a  }{ 6  }  -2 \times    \dfrac{ 5-a  }{ 2  }   =  -3',
    r'x^{2}=5',
    r'x^{2}+2\sqrt{3}x+5=0',
    r'\left(x+3\right)\left(x-2\right)=0',
    r'\dfrac{ 1  }{  \sqrt{ 3- \sqrt{ 5  }    }    }',
    r'\left(\dfrac{1+i}{1-i}\right)^{2051}-\left(\dfrac{1-i}{1+i}\right)^{2051}',
    r'\dfrac {\sqrt{10} -\sqrt{2} } {\sqrt{10} +\sqrt{2} }', '\dfrac{3-\sqrt{5}}{2}',
    r'-\sqrt[2]{1+\sqrt{2}}\sqrt[2]{1+\sqrt{2}}',
    r'-\sqrt{1-\sqrt{3}}\sqrt{1-\sqrt{3}}',
    r'\sqrt{1-\sqrt{2}}\sqrt{1+\sqrt{2}}',
    r'-\sqrt{1-\sqrt{2}}\sqrt{1+\sqrt{2}}',
    r'-\sqrt{1-\sqrt{2}}* -\sqrt{1+\sqrt{2}}',
    r'3-i+\dfrac{i}{i+1}-3i+\dfrac{2-i}{1-i}',
    r'\sqrt[6]{\left(-e\right)^{6}}',
)

init()

browser = webdriver.Chrome(executable_path=ChromeDriverManager().install())
browser.get("http://127.0.0.1:5000/")

browser.maximize_window()
search = browser.find_element_by_name("expression")

for idx, qal in enumerate(qal_list):
    print(f'{idx}: {qal}')
    browser.execute_script("window.scrollTo(0, 0)")
    search.send_keys(qal)
    search.send_keys(Keys.ENTER)
    time.sleep(0.2)
    wait = WebDriverWait(browser, 10).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, "explains")))
    time.sleep(3)
    BROWSER_HEIGHT = browser.execute_script("return window.innerHeight")
    time.sleep(1)
    SCROLL_SIZE = browser.execute_script("return document.body.scrollHeight")
    time.sleep(1)
    while True:
        NEW_SCROLL_SIZE = browser.execute_script("return document.body.scrollHeight")
        if SCROLL_SIZE < NEW_SCROLL_SIZE:
            print("CHANGED!!!!!!!!!!!!")
            SCROLL_SIZE = NEW_SCROLL_SIZE
        else:
            break

    N = math.ceil(SCROLL_SIZE / BROWSER_HEIGHT)
    for i in range(N - 1):
        browser.execute_script(f"window.scrollTo(0, {i * BROWSER_HEIGHT})")
        browser.save_screenshot(f"screenshots/{i}.png" if i >= 10 else f'screenshots/0{i}.png')

    make_result(N - 1, f'{idx}')
    clean('./screenshots')
    search.clear()
browser.quit()
