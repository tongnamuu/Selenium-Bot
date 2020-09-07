from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time, math
from image import make_result, init, clean


qal_list = (r.rstrip('\n') for r in open('input.txt'))
# qal_list = (
#     r'\dfrac{ 4+4 \sqrt{ 2  }    }{ 2  }',
#     r'\dfrac{ 4+4 \sqrt{ 2  }    }{ 2  }',
#     r'\dfrac{ -243  }{ - \left(  3 \right)   ^{ n  }    }   =  81',
# )
init()

browser = webdriver.Chrome(executable_path=ChromeDriverManager().install())
browser.get("http://127.0.0.1:5000/")

browser.maximize_window()

for idx, qal in enumerate(qal_list):
    # print(f'{idx}: {qal}')
    browser.refresh()
    search = browser.find_element_by_name("expression")
    search.clear()
    time.sleep(1)
    search.send_keys(qal)
    search.send_keys(Keys.ENTER)
    time.sleep(1)
    try:
        WebDriverWait(browser, 10).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'explains')))
    except TimeoutException:
        print(f'fail with {idx}: {qal}')
        clean('./screenshots')
        continue
    child = browser.execute_script("return document.getElementById('solver_result').childElementCount")
    print(child)
    if child == 0:
        print(f'fail with {idx}: {qal}')
        clean('./screenshots')
        continue
    time.sleep(1)
    BROWSER_HEIGHT = browser.execute_script("return window.innerHeight")
    time.sleep(1)
    SCROLL_SIZE = browser.execute_script("return document.body.scrollHeight")
    time.sleep(1)
    while True:
        NEW_SCROLL_SIZE = browser.execute_script("return document.body.scrollHeight")
        time.sleep(0.2)
        if SCROLL_SIZE < NEW_SCROLL_SIZE:
            SCROLL_SIZE = NEW_SCROLL_SIZE
        else:
            break

    N = math.ceil(SCROLL_SIZE / BROWSER_HEIGHT)
    for i in range(N):
        browser.execute_script(f"window.scrollTo(0, {i * BROWSER_HEIGHT})")
        if i >= 100:
            s = f'{i}'
        elif i >= 10:
            s = f'0{i}'
        else:
            s = f'00{i}'
        browser.save_screenshot(f"screenshots/{s}.png")

    make_result(N, f'{idx}')
    clean('./screenshots')
browser.quit()
