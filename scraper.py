from selenium import webdriver
import itertools
import time


class WebInterface:

    def __init__(self):

        self.get_driver()

    def get_driver(self):

        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        # options.add_argument("--headless")
        options.add_experimental_option("useAutomationExtension", False)
        options.add_experimental_option("prefs", {"profile.default_content_settings.cookies": 2})
        options.add_argument("--test-type")
        options.add_argument("--start-maximized")
        options.add_argument("--no-first-run")
        options.binary_location = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"

        self.driver = webdriver.Chrome(chrome_options=options)

    def go_to(self, link):

        if link != self.driver.current_url:
            self.driver.get(link)

    def enter_text(self, x_path, value, submit=False):

        input_element = self.driver.find_element_by_xpath(x_path)
        input_element.send_keys(value)
        if submit:
            input_element.submit()

    def xpath_click(self, x_path):

        input_element = self.driver.find_element_by_xpath(x_path)
        input_element.click()

    def text_click(self, text):

        input_element = self.driver.find_element_by_link_text(text)
        input_element.click()

    def get_text_by_x_path(self, xpath):
        return self.driver.find_element_by_xpath(xpath).text


def scrape_recursively(start=1, data='', last_fail=False):

    wb = WebInterface()
    wb.go_to(r'https://www.azlyrics.com/m/migos.html')
    main_handle = wb.driver.current_window_handle

    for a in itertools.count(start=start):

        try:
            song_title = wb.get_text_by_x_path('//*[@id="listAlbum"]/a[{}]'.format(a))
            wb.xpath_click('//*[@id="listAlbum"]/a[{}]'.format(a))
            wb.driver.switch_to.window(wb.driver.window_handles[1])
            lyrics = wb.get_text_by_x_path('/html/body/div[3]/div/div[2]/div[5]')
            wb.driver.close()
            wb.driver.switch_to.window(main_handle)
            print(song_title)
            if not data:
                data = song_title + "|||" + lyrics
            else:
                data = data + "@@@" + song_title + "|||" + lyrics
            last_fail = False
        except Exception as e:
            print(str(e))
            wb.driver.quit()
            if not last_fail:
                data = scrape_recursively(start=a, data=data, last_fail=True)
            return data


if __name__ == "__main__":

    data = scrape_recursively()
    text_file = open("lyric_data.txt", "w", encoding='utf-8')
    text_file.write(data)
    text_file.close()