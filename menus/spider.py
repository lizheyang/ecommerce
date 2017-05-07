import requests
from bs4 import BeautifulSoup
import random
import os
import time
from menus.models import Menu, MenuStep


class UrlManager(object):
    """
    通过美食杰的搜索页面获取具体菜单页的地址列表
    """
    def __init__(self, new_num):
        self.base_url = 'http://so.meishi.cc/?q=%E5%B1%B1%E8%8D%AF&sort=time&page='
        self.url_nums = new_num
        self.url_to_parser = []

        db_menus = Menu.objects.all()
        self.url_already_parser = [menu.url for menu in db_menus]

    def get_page_content(self, url):
        user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                     'Chrome/57.0.2987.133 Safari/537.36'
        headers = {'User-Agent': user_agent}
        return requests.get(url, headers=headers).text

    def get_urls(self, page_no):
        """
        从第page_num页查询结果获取未获取过的菜谱url，将其更新至self.url_to_parser中
        :param page_num:
        :return:
        """
        try:
            url_to_parser = []
            url = self.base_url + str(page_no)
            menus_page = self.get_page_content(url)
            # with open('a.html', 'r', encoding='utf-8') as f:
            #     menus_page = f.read()

            soup = BeautifulSoup(menus_page, "html5lib")
            menu_divs = soup.find_all(class_="search2015_cpitem")
            for menu_div in menu_divs:
                url_to_parser.append(menu_div.a.get('href'))
            self.url_to_parser.extend(list(set(url_to_parser) - set(self.url_already_parser)))
        except Exception as e:
            print(e)

    def main(self):
        """
        随机选取搜索页面页数,在每次循环后检查url_to_parser的数量，确保一共只取url_nums个url
        :return:
        """
        menus_page = self.get_page_content(self.base_url)
        soup = BeautifulSoup(menus_page, "html5lib")
        #获取总菜谱数量
        menus_total_num = int(soup.find(class_="search2015_path").em.string.strip().replace(',', ''))
        # page_total_num = menus_total_num // 20 + 1
        page_total_num = 40
        print('一共有%s页山药食谱' % page_total_num)

        while len(self.url_to_parser) < self.url_nums:
            page_no = random.randint(1, page_total_num)
            print('获取第%s页的山药食谱' % page_no)
            self.get_urls(page_no)

        self.url_to_parser = self.url_to_parser[:self.url_nums]


class MenuParser(object):
    def __init__(self):
        self.base_dir = r'C:\django\ecommerce\imgs\menus'

    def menu_parser(self, url):
        try:
            user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                         'Chrome/57.0.2987.133 Safari/537.36'
            headers = {'User-Agent': user_agent}
            menu_page = requests.get(url, headers=headers).text
            soup = BeautifulSoup(menu_page, "html5lib")
            # 获取菜谱名
            menu_name = soup.find(id="tongji_title").string
            # 菜谱描述
            menu_description = soup.find(class_="materials").p.get_text()[1:-1]
            # 菜谱用料
            menu_materials = [tag.a.get_text() for tag in soup.find_all('h4')[1:]]
            # 所有步骤
            steps = soup.find_all(class_="content clearfix")
            steps_list = []
            for step in steps:
                tmp_dic ={
                    'step_no': step.em.get_text()[0],
                    'step_detail': step.div.p.get_text(),
                    'step_img_url': step.find(class_="conimg").get("src")
                }
                steps_list.append(tmp_dic)

            # 获取存储文件的文件夹名
            pa = soup.find(id="tongji_title").get('href')
            folder_name = os.path.split(pa)[1].split('.')[0]
            folder_path = os.path.join(self.base_dir, folder_name)
        except Exception as e:
            return False, '文档解析错误%s' % e
        try:
            if os.path.exists(folder_path):
                pass
            else:
                os.mkdir(folder_path)
        except OSError as e:
            return False, '创建文件夹失败'
        old_path = os.getcwd()
        os.chdir(folder_path)
        # with open('text.txt', 'a', encoding='utf-8') as f:
        #     f.write(menu_name + '\n')
        #     f.write(url + '\n')
        #     f.write(folder_name + '\n')
        #     f.write(menu_description + '\n')
        #     f.write('用料：' + ','.join(menu_materials) + '\n')
        #     for step in steps_list:
        #         f.write('Step ' + step['step_no'] + '\n')
        #         f.write(step['step_detail'] + '\n')
        #         with open(step['step_no']+'.jpg', 'wb') as img:
        #             time.sleep(1)
        #             img.write(requests.get(step['step_img_url']).content)
        try:
            menu = Menu()
            menu.name = menu_name
            menu.url = url
            menu.folder_name = folder_name
            menu.description = menu_description
            menu.materials = ','.join(menu_materials)
            menu.save()
            if menu.pk:
                for step in steps_list:
                    with open(step['step_no'] + '.jpg', 'wb') as img:
                        time.sleep(1)
                        img.write(requests.get(step['step_img_url']).content)
                    ms = MenuStep()
                    ms.menu = menu
                    ms.no = int(step['step_no'])
                    ms.detail = step['step_detail']
                    ms.img = 'menus/%s/%s.jpg' % (folder_name, step['step_no'])
                    ms.save()
        except Exception as e:
            return False, '存储失败%s' % e
        os.chdir(old_path)
        return True, '解析并保存菜谱%s成功' % menu_name


def superviser(new_num):
    manager = UrlManager(new_num)
    manager.main()
    # for url in manager.url_to_parser:
    #     print(url)
    parser = MenuParser()
    for url in manager.url_to_parser:
        success, message = parser.menu_parser(url)
        print(message)


if __name__ == '__main__':
    superviser(2)


