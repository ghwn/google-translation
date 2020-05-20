import os
import re
import time
import stat
import subprocess
import urllib
import zipfile

import bs4
import selenium.webdriver
import wget


class GoogleTranslator:
    def __init__(self):
        # Set Chrome version
        cmd = "google-chrome --version"
        self.chrome_version = subprocess.check_output(
            cmd.split(' ')).decode("utf-8").strip().split(' ')[-1]

        # Download chromedriver file if it doesn't exist
        base_dir = os.path.abspath(os.path.join(__file__, '..'))
        chromedriver_path = os.path.join(base_dir, "chromedriver")
        if not os.path.exists(chromedriver_path):
            self._download_chromedriver(output_dir=base_dir)

        # Create selenium webdriver
        options = selenium.webdriver.ChromeOptions()
        options.add_argument("headless")
        self.web_driver = selenium.webdriver.Chrome(chromedriver_path, options=options)

    def _download_chromedriver(self, output_dir):
        """Download chromedriver file."""
        # Check for the latest release of Chrome driver
        chrome_major_version = self.chrome_version.split('.')[0]
        latest_release_url = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_%s" \
            % chrome_major_version
        with urllib.request.urlopen(latest_release_url) as response:
            latest_release = response.read().decode("utf-8")

        # Download chromedriver file
        chromedriver_url = "https://chromedriver.storage.googleapis.com/" \
            "%s/chromedriver_linux64.zip" % latest_release
        tmp_path = "/tmp/chromedriver.zip"
        wget.download(url=chromedriver_url, out=tmp_path, bar=None)

        # Extract the chromedriver into the `output_dir`
        zipfile.ZipFile(tmp_path, 'r').extractall(output_dir)
        chromedriver_path = os.path.join(output_dir, "chromedriver")

        # Make the chromedriver executable
        os.chmod(chromedriver_path, mode=stat.S_IEXEC)

    def translate(self, text, src="en", dest="ko"):
        """Translate text."""
        # Set Google translation URL
        base_url = "https://translate.google.com/#view=home&op=translate&sl=%s&tl=%s" % (src, dest)

        # Get HTML source by sending the URL
        url = base_url + "&text=" + urllib.parse.quote(text)
        self.web_driver.get(url)
        time.sleep(0.3)
        soup = bs4.BeautifulSoup(self.web_driver.page_source, "html.parser")

        # Extract translations from the HTML source
        page_element = soup.find("span", "tlid-translation translation")
        translations = [re.sub(r"<.+?>", "", str(content))
                        for content in page_element.contents
                        if not isinstance(content, bs4.element.NavigableString)]
        translation = ' '.join(translations).strip()
        return translation
