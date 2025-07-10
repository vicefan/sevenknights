from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import streamlit as st

st.set_page_config(
    page_title="Sena",
    page_icon="⚔️"
)

# 셀레니움 css
use_button = 'div.ActionPanel_panel__bYC6M.ActionPanel_webpage__1aO9h.false.bg-con--bg-color > div > button'
accept_button = 'div.Alert_buttons__DWiaN > button.Button_button__k4Gkp.primary--bg-color.on-primary--font-color.radius-high--border-radius'
check_uid = 'div.Alert_buttons__DWiaN > button'

# 쿠폰 리스트
with open('coupons.txt', 'r') as file:
    coupons = [line.strip() for line in file if line.strip()]

with st.sidebar:
    st.title("적용되는 쿠폰")
    results = st.empty()
    tmp = ""
    for coupon in coupons:
        tmp += f"{coupon}\n"
    results.text(tmp)

# UID 입력
uid = st.text_input("UID를 입력하세요:", value="")
uid_button = st.button("실행")

gui = st.empty()
test = True

if uid_button:
    # 크롬 드라이버 설정
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")


    service = Service()
    driver = webdriver.Chrome(service=service, options=options)

    for coupon in coupons:
        gui.markdown(f"쿠폰 사용 시도: {coupon}")
        url = f"https://coupon.netmarble.com/tskgb?playerId={uid}&code={coupon}"
        driver.get(url)
        st.code(driver.page_source)


        try:
            EC.element_to_be_clickable((By.XPATH, use_button))
            driver.find_element(By.CSS_SELECTOR, use_button).click()

            EC.element_to_be_clickable((By.XPATH, accept_button))
            driver.find_element(By.CSS_SELECTOR, accept_button).click()
            
            # UID 오류 확인 - 최초 1회
            if test:
                try:
                    time.sleep(0.5)
                    if_checkuid = driver.find_element(By.CSS_SELECTOR, check_uid)
                    gui.markdown(f"UID({uid}) 오류로 중지합니다.")
                    for coupon in coupons:
                        coupons[coupons.index(coupon)] = f"{coupon} ❌"
                    break
                
                except Exception as e:
                    test = False

            gui.markdown(f"쿠폰 {coupon} 사용 성공")
            coupons[coupons.index(coupon)] = f"{coupon} ✔️"

            time.sleep(1)

        except Exception as e:
            gui.markdown(f"쿠폰 {coupon} 사용 실패")
    
    tmp = ""
    for coupon in coupons:
        tmp += f"{coupon}\n"
    results.text(tmp)
    driver.quit()
    gui.markdown("")