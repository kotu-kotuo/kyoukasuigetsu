# Selenium4
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import schedule
import time
from dotenv import load_dotenv
import os
import traceback

# ドライバの自動インストール
service = ChromeService(executable_path=ChromeDriverManager().install())
# ドライバの起動
driver = webdriver.Chrome(service=service)
# 要素検索時のデフォルト待機時間(最大)
driver.implicitly_wait(1)
# 明示的な待機時間(最大)
wait = WebDriverWait(driver, 10)
# 環境変数
load_dotenv()


# ログイン用メールアドレス
email = os.environ['EMAIL']
# ログイン用パスワード
password = os.environ['PASSWORD']
# メッセージ
message = os.environ['MESSAGE']

# スケジュールタスク
def task():
  print("スタート")
  try:
    driver.get("https://crowdworks.jp/login?ref=toppage_hedder")
    sleep(3)
    if driver.find_element(By.ID, "username"):
      driver.find_element(By.ID, "username").send_keys(email)
      print("ユーザーネーム入力")
    if driver.find_element(By.ID, "password"):
      driver.find_element(By.ID, "password").send_keys(password)
      print("メールアドレス入力")
    if driver.find_elements(By.CLASS_NAME, "button-login"):
      wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "button-login"))).click()
      print("ログイン完了")
    sleep(3)
    driver.get("https://crowdworks.jp/contracts/36515262")
    print("ページ遷移")
    sleep(3)
    if driver.find_elements(By.XPATH, "/html/body/div[1]/div[2]/div/div[1]/div[2]/div/div[2]/a"):
      wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/div/div[1]/div[2]/div/div[2]/a"))).click()
    else:
      print("ボタンが押せませんでした")
      raise Exception
    print("ボタンクリック")
    sleep(3)
    unixtime = str(int(time.time()))
    if driver.find_element(By.XPATH, "/html/body/div[14]/div[2]/form/div/p[2]/textarea"):
      driver.find_element(By.XPATH, "/html/body/div[14]/div[2]/form/div/p[2]/textarea").send_keys(message + unixtime)
    else:
      print("入力できませんでした")
      raise Exception
    print("入力完了")
    sleep(3)
    if driver.find_elements(By.XPATH, "/html/body/div[14]/div[2]/form/div/p[5]/input[2]"):
      wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[14]/div[2]/form/div/p[5]/input[2]"))).click()
      print(message + unixtime)
    else:
      print("送信できませんでした")
      raise Exception
  except Exception:
    print("例外処理" + traceback.format_exc())

# スケジュール設定
schedule.every(30).to(599).seconds.do(task)

#スケジュール実行
while True:
    schedule.run_pending()
    sleep(1)

# ブラウザの終了
# driver.quit()
