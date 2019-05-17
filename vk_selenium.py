import re
from selenium import webdriver

VK_URL = "https://vk.com"
VK_FEED_URL = "https://vk.com/feed"


class Vk:
    """
    With selenium pulls post's data from VK using Chrome
    """

    def __init__(self, user_login, user_password):
        self.browser = webdriver.Firefox()
        self.browser.get(VK_URL)

        login = self.browser.find_element_by_css_selector("#index_email")
        login.send_keys(user_login)

        password = self.browser.find_element_by_css_selector("#index_pass")
        password.send_keys(user_password)

        submit = self.browser.find_element_by_css_selector("#index_login_button")
        submit.click()

        assert self.browser.current_url is not VK_FEED_URL, \
            "authorization failed"

    def quit(self):
        self.browser.quit()

    def get_feeds_data(self):
        """
        :return: 3 collections
        """
        self.browser.get(VK_FEED_URL)
        feeds_and_adds = self.browser.find_elements_by_css_selector(
            "div[class^='_post post page_block']")
        ads = self.browser.find_elements_by_css_selector(
            "div[class*='_ads_block_data_w']")
        clear_feeds = [item for item in feeds_and_adds if item not in ads]
        link_collection = []
        txt_collection = []
        im_collection = []

        for feed in clear_feeds:
            feed_id = feed.get_attribute("id")

            if feed.find_elements_by_css_selector("div[class='wall_post_text'"):
                wall_post_text = feed.find_element_by_css_selector(
                    "div[class='wall_post_text'")
                feed_links_part_1 = [link.get_property("textContent") for link in
                                     wall_post_text.find_elements_by_css_selector(
                                         "a[href^='/away.php?']")
                                     if link.get_property("textContent")[-1] != '.']
                feed_links_part_2 = [link.get_attribute("title") for link in
                                     wall_post_text.find_elements_by_css_selector(
                                         "a[href^='/away.php?']")
                                     if link.get_attribute("title") != ""]
                feed_links = feed_links_part_1 + feed_links_part_2
                txt_collection.append({'feed_id': feed_id,
                                       'text': wall_post_text.get_property("textContent")})

                if feed_links:
                    link_collection.append({'feed_id': feed_id, 'links': feed_links})

            if feed.find_elements_by_css_selector(
                    "div[class='page_post_sized_thumbs  clear_fix']"):
                sized_thumbs = feed.find_element_by_css_selector(
                    "div[class='page_post_sized_thumbs  clear_fix']")
                images = [re.search(r"\(\"(.+)\"\)", image.get_attribute("style")).group(1)
                          for image in sized_thumbs.find_elements_by_tag_name("a")]
                im_collection.append({'feed_id': feed_id, 'images': images})

        return [txt_collection, link_collection, im_collection]
