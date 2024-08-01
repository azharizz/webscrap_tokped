from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from selenium import webdriver
import re
from selenium_stealth import stealth
import time
from datetime import datetime, timedelta
from google.cloud import storage
import os
import tempfile
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

def stock_finder(p_stok, stok_total):
    res_stok = p_stok.find_elements(By.CSS_SELECTOR, 'b')[0].text
    res_stok = re.sub(r'\D', '', res_stok)
    if res_stok == '':
        res_stok = 0
    else:
        res_stok = int(res_stok)
    stok_total += res_stok

    return stok_total

def start_scrap(driver, dct_data, df):
    index_stopped=0
    counter = 0
    for link in df['Link']:
        print('counter now', counter)
        if counter < index_stopped:
            counter += 1
            continue
        else:
            counter += 1

        #Try if the web is still not ready
        try_time = 5
        for i in range(try_time):
            try:    
                driver.get(link)
                time.sleep(2.4)

                # Nama Toko data
                h2_nama_toko = driver.find_element(By.XPATH, '//h2[@class="css-1wdzqxj-unf-heading e1qvo2ff2"]')
                break
            except:
                try_time -= 1
        if try_time == 0:
            print(f'Error loading page after 5 try time')
            continue
        
        dct_data['nama_toko'].append(h2_nama_toko.text)


        # Daerah Data
        try:
            h2_daerah = driver.find_element(By.XPATH, '//h2[@class="css-1pd07ge-unf-heading e1qvo2ff2"]')
            nama_daerah = h2_daerah.find_elements(By.CSS_SELECTOR, 'b')[0].text
        except:
            nama_daerah = 'Unknown/Dilayani Tokopedia'

        dct_data['daerah_toko'].append(nama_daerah)

        # Terjual Data
        try:
            p_sold = driver.find_element(By.XPATH, '//p[@data-testid="lblPDPDetailProductSoldCounter"]')
            sold_val = int(re.sub(r'\D', '', p_sold.text)) 
            if 'rb' in p_sold.text:
                sold_val = sold_val * 1000
        except:
            sold_val = 0

        dct_data['jumlah_terjual'].append(sold_val)
        
        # Stok Data
        stok_total = 0
        try:
            div_variant = driver.find_element(By.XPATH, '//div[@class="css-1b2d3hk"]')
            parent_level_div = div_variant.find_elements(By.CSS_SELECTOR, 'div')
            all_level_div = [x for x in parent_level_div if x.get_attribute('class')=='css-hayuji']

            len_level1 = len(all_level_div[0].find_elements(By.CSS_SELECTOR, 'button'))

            stok_total = 0
            for el_level1 in all_level_div[0].find_elements(By.CSS_SELECTOR, 'button'):
                el_level1.click()

                if len(all_level_div) >= 2:
                    for el_level2 in all_level_div[1].find_elements(By.CSS_SELECTOR, 'button'):
                        el_level2.click()
                        p_stok = driver.find_element(By.XPATH, '//p[@class="css-1yy88m3-unf-heading e1qvo2ff8"]')
                        stok_total = stock_finder(p_stok, stok_total)

                else:
                    p_stok = driver.find_element(By.XPATH, '//p[@class="css-1yy88m3-unf-heading e1qvo2ff8"]')
                    stok_total = stock_finder(p_stok, stok_total)
        except:
            p_stok = driver.find_element(By.XPATH, '//p[@class="css-1yy88m3-unf-heading e1qvo2ff8"]')
            stok_total = stock_finder(p_stok, stok_total)
        

        dct_data['stok_tersisa'].append(stok_total)
    

if __name__ == "__main__":
    start = datetime.now()
    options = webdriver.ChromeOptions()
    webdriver_service = Service(ChromeDriverManager().install())
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    # options.add_argument('window-size=1920x1080')
    # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(service=webdriver_service, options=options)
    # driver = uc.Chrome(options=options)

    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )
    

    driver.get('https://www.tokopedia.com')
    df = pd.read_csv('all_clean_scrap_wo_ta.csv')

    df = df[df['category'].isin(['aksesoris_pria'])]

    dct_data = {
        "nama_toko": [],
        "daerah_toko": [],
        "jumlah_terjual": [],
        "stok_tersisa": []
    }

    start_scrap(driver, dct_data, df)

    df['stok_tersisa'] = dct_data['stok_tersisa']
    df['daerah_toko'] = dct_data['daerah_toko']
    df['nama_toko'] = dct_data['nama_toko']
    # Get the current date and time
    now = datetime.now()

    # Subtract one year (approximate by subtracting 365 days)
    one_year_ago = now - timedelta(days=731)

    # Format the date as a string in the desired format
    date_string = one_year_ago.strftime("%Y-%m-%d")

    df['created_at'] = date_string

    # UPLOAD GCP
    # Set up Google Cloud Storage client
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "datahub-project-430801-c216773b2d70.json"
    client = storage.Client()


    # Use tempfile to create a temporary file
    with tempfile.NamedTemporaryFile(suffix='.csv') as tmp:
        local_file_path = tmp.name
        df.to_csv(local_file_path, index=False)

        # Define the GCS bucket and blob (file) name
        bucket_name = 'data_scrap_azhar'
        destination_blob_name = f'result_data/aksesoris_pria_{date_string}.csv'

        # Upload the file to GCS
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(local_file_path)

        print(f'File {local_file_path} uploaded to {destination_blob_name}.')
    
    end = datetime.now()
    elapsed_time = end - start

    print(f"Time elapsed: {elapsed_time}")
    




