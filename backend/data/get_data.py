def get_data_task():
    from bs4 import BeautifulSoup
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.action_chains import ActionChains
    import time
    import json
    import pandas as pd

    %load_ext autoreload
    %autoreload 2

    chrome_driver_path = "D:\Administrator\software-tool\Google\chromedriver-win64\chromedriver.exe"
    url = "https://www.zhipin.com/shanghai/?ka=header-home"

    # 创建 Service 对象并指定 ChromeDriver 路径
    service = Service(executable_path=chrome_driver_path)
    # 启动 Chrome 浏览器
    driver = webdriver.Chrome(service=service)
    # 打开访问的页面
    driver.get(url)
    # 等待页面加载
    time.sleep(3) 

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    job_menu_wrapper = soup.find('div', class_='job-menu-wrapper')
    menu_sub = job_menu_wrapper.find('div', class_='menu-sub', recursive=True)  # 找到第一个符合条件的 <div class="menu-sub">
    if menu_sub:
        menu_article = menu_sub.find('p', class_='menu-article', string='互联网/AI')  # 检查 <p> 的文本是否为“互联网/AI”

    direct = list() # 所有方向名称
    subdir_link = dict() # 子方向网页专属url
    subdir_dirno = dict() # 子方向所属方向编号

    # 获取所有方向名称
    categories = menu_sub.find_all('h4')  # 找到所有的<h4>标签
    for category in categories:
        direct.append(category.text.strip())

    # 获取包含方向-子方向的元素
    list_dir_subdir = menu_sub.find_all('li')
    # 每个li元素对饮一个方向
    for dirno, li in enumerate(list_dir_subdir):
        links = li.find_all('a')
        for link in links:
            text = link.text.strip()  # 链接文本内容
            subdir_link[text] = link['href']
            subdir_dirno[text] = dirno + 1 # 从1开始的编号

    # 输出
    df_dir = pd.DataFrame(direct, columns=['dir']).reset_index().rename(columns={'index':'dirno'})
    df_dir['dirno'] = df_dir['dirno']+1 # 将就数据库的自动编号从1开始
    df_dir.to_csv(' 方向.csv',encoding = 'GB18030',index = False)
    df_subdir = pd.DataFrame({'dirno':subdir_dirno,'subdir_link':subdir_link})
    df_subdir.index.name = 'subdir'
    df_subdir.reset_index(inplace=True)
    df_subdir.to_csv(' 子方向.csv',encoding = 'GB18030',index = False)

    # 获取cookie
    def get_cookie(url, cookie_file_name):
        driver = webdriver.Chrome(service=service)
        driver.get(url)
        time.sleep(15)
        dictCookies = driver.get_cookies()
        jsonCookies = json.dumps(dictCookies)
        with open(cookie_file_name, 'w') as fp:
            fp.write(jsonCookies)
            print('cookie保存成功！')
    base_url = "https://www.zhipin.com"
    get_cookie(base_url, 'cookie/boss.json')

    # 先获取源代码再进行解析（为防止访问浏览器的中途出错）
    subdir_source = []
    from selenium import webdriver
    import time
    import json
    from bs4 import BeautifulSoup

    base_url = "https://www.zhipin.com"
    inschool_url = "e_108/"
    job_card_list = []
    for subdirno,sublink in enumerate(subdir_link):
        boss = webdriver.Chrome(service=service)
        url = base_url + sublink + inschool_url
        boss.get(url)
        time.sleep(10)
        # 注入cookie
        with open(r"cookie/boss.json",'r') as fp:
            jsonCookies = fp.read()
        # 将JSON格式的Cookie转换为字典
        cookies = json.loads(jsonCookies)
        for cookie in cookies:
            boss.add_cookie(cookie)
        # 进入网页获取源码
        boss.get(url)
        time.sleep(6)
        boss_text = boss.page_source
        subdir_source.append(boss_text)
        boss.quit()
        # 写入文件保存
        file_path = f'subdir_page/subdir_page_{subdirno}.html'
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(boss_text)

        
    job_card_list = []
    nlink = len(subdir_link)
    # 从文件读取网页
    for i in range(nlink):
        file_path = f'subdir_page/subdir_page_{i}.html'
        # 读取文件
        with open(file_path, "r", encoding="utf-8") as file:
            html_content = file.read()
            # 提取job-card-left元素
            soup = BeautifulSoup(html_content, 'html.parser')
            job_card_left_elements = soup.find_all(class_='job-card-left')
            # 遍历30个job-card-left元素，获取<a>的href链接
            for element in job_card_left_elements:
                href = element['href']
                full_link = 'https://www.zhipin.com' + href
                job_card_list.append({'job_subdirno':subdirno,'job_card_link':full_link})

    df_job_card_list = pd.DataFrame(job_card_list)
    df_job_card_list.to_csv('job_card_list_origin.csv',encoding = 'GB18030',index = False)
    df = pd.read_csv('job_card_list_origin.csv',encoding = 'GB18030')

    # 网页爬取
    source = []
    # 先获取源代码再进行解析（为防止访问浏览器的中途出错）
    # source = []
    for i,item in enumerate(df_job_card_list.values):
        subdirno, url = item
        
        boss = webdriver.Chrome(service=service)
        boss.get(url)
        time.sleep(10)
        # 注入cookie
        with open(r"cookie/boss.json",'r') as fp:
            jsonCookies = fp.read()
        # 将JSON格式的Cookie转换为字典
        cookies = json.loads(jsonCookies)
        for cookie in cookies:
            boss.add_cookie(cookie)
        # 进入网页获取源码
        boss.get(url)
        time.sleep(5)
        boss_text = boss.page_source
        source.append(boss_text)
        boss.quit()
        # 写入文件保存
        file_path = f'page/page_{i}.html'
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(boss_text)

    # 从网页中提取信息
    title = [] 
    # 职位名称。形如：‘Java实习生’
    # '#main > div.job-banner > div > div > div.info-primary > div.name > h1'

    salary = [] 
    # 薪水。形如：'150-240元/天'
    # '#main > div.job-banner > div > div > div.info-primary > div.name > span'

    JD = [] 
    # 职位描述。形如：'工作职责•	参与项目需求分析和设计，能够主动思考需求中的不足。•	……'
    # '#main > div.job-box > div > div.job-detail > div:nth-child(1) > div.job-sec-text'

    key_words = [] 
    # 关键词。形如："['Java', 'Docker', 'SpringCloud', 'MySQL', 'Kafka', 'CI/CD', 'Spring']"
    # '#main > div.job-box > div > div.job-detail > div:nth-child(1) > ul > li'

    duty_time = [] 
    # 到岗时间要求。形如：'4天/周 6个月'
    # '#main > div.job-banner > div > div > div.info-primary > p > span.text-desc.text-experiece'

    address = [] 
    # 形如：'上海徐汇区港汇恒隆广场二座3509'
    # '#main > div.job-box > div > div.job-detail > div.job-detail-section.job-detail-company > div.detail-section-item.company-address > div > div.job-location-map.js-open-map' - 'data-content'

    location = [] 
    # 形如：'121.3997,31.1143'
    # '#main > div.job-box > div > div.job-detail > div.job-detail-section.job-detail-company > div.detail-section-item.company-address > div > div.job-location-map.js-open-map' - 'data-lat'

    # 由位置衍生出的特征 API获取
    ## 方案数
    trans_plan_count = []
    ## 距离
    distance = []
    ## 交通费用
    cost = []
    ## 通勤时间
    duration = []
    index = []

    from location_to_cost import LocationToCost
    api_key = "作者的key" 
    school = '同济大学(嘉定校区)'
    city = '上海'
    ltc = LocationToCost(school, city, api_key)


    ## 从文件读取网页
    # for i in range(napge):
    #     file_path = f'page/page_{i}.html'
    #     # 读取文件
    #     with open(file_path, "r", encoding="utf-8") as file:
    #         html_content = file.read()

    ## 爬取后，网页还保存在变量区
    for ind, html_content in enumerate(source):
        soup = BeautifulSoup(html_content, 'html.parser')

        # 职位名称
        title_element = soup.select_one('#main > div.job-banner > div > div > div.info-primary > div.name > h1')
        if title_element:
            title.append(title_element.get_text(strip=True))  # 提取纯文本
        else:
            title.append("内容缺失")
        print(ind, title[-1])  # 打印最后一个添加的职位名称

        # 编号 
        index.append(ind)

        # 薪水
        salary_element = soup.select_one('#main > div.job-banner > div > div > div.info-primary > div.name > span')
        if salary_element:
            salary.append(salary_element.get_text(strip=True))  # 提取纯文本
        else:
            salary.append("内容缺失")

        # 职位描述
        JD_element = soup.select_one('#main > div.job-box > div > div.job-detail > div:nth-child(1) > div.job-sec-text')
        if JD_element:
            JD.append(JD_element.get_text(strip=True))  # 提取纯文本
        else:
            JD.append("内容缺失")

        # 关键词 (需要进行统计)
        key_words_elements = soup.select('#main > div.job-box > div > div.job-detail > div:nth-child(1) > ul > li')
        if key_words_elements:
            keywords = [li.text.strip() for li in key_words_elements]    
            key_words.append(str(keywords))  # 提取关键词列表
        else:
            key_words.append("内容缺失")  

        # 到岗时间要求
        duty_time_element = soup.select_one('#main > div.job-banner > div > div > div.info-primary > p > span.text-desc.text-experiece')
        if duty_time_element:
            duty_time.append(duty_time_element.get_text(strip=True))  # 提取纯文本
        else:
            duty_time.append("内容缺失")

        # 地址和经纬度
        add_loc_element = soup.select_one('#main > div.job-box > div > div.job-detail > div.job-detail-section.job-detail-company > div.detail-section-item.company-address > div > div.job-location-map.js-open-map')
        
        try:
            if add_loc_element and 'data-content' in add_loc_element.attrs and 'data-lat' in add_loc_element.attrs:
                address.append(add_loc_element['data-content'])
                location_element = add_loc_element['data-lat']
                location.append(location_element)

                # 地理衍生特征
                message = ltc.get_school_to_company_message(location_element)
                if message:
                    trans_plan_count.append(message.get('count', 0))
                    distance.append(message.get('distance', 0))
                    cost.append(message.get('cost', 0))
                    duration.append(message.get('duration', 0))
                else:
                    print(f"地理衍生特征获取失败，location_element={location_element}")
                    trans_plan_count.append(0)
                    distance.append(0)
                    cost.append(0)
                    duration.append(0)
            else:
                print("无法提取地址或经纬度")
                address.append("内容缺失")
                location.append("内容缺失")
                trans_plan_count.append(0)
                distance.append(0)
                cost.append(0)
                duration.append(0)
        except Exception as e:
            print(f"处理地理信息时出错：{e}")
            address.append("内容缺失")
            location.append("内容缺失")
            trans_plan_count.append(0)
            distance.append(0)
            cost.append(0)
            duration.append(0)

    import pandas as pd

    # 假设您已经提取了所有数据并存储在对应的列表中
    data = {
        'index': index,
        'title': title,
        'salary': salary,
        'JD': JD,
        'key_words': key_words,
        'duty_time': duty_time,
        'address': address,
        'location': location,
        'trans_plan_count': trans_plan_count,
        'distance': distance,
        'cost': cost,
        'duration': duration
    }


    df = pd.DataFrame(data)
    df_job_card_list = pd.read_csv('job_card_list_origin.csv',encoding = 'GB18030')
    df_final = pd.concat([df_job_card_list,df], axis=1)

    # 数据清洗
    import numpy as np
    df_final_cleaned = df_final.replace('内容缺失', np.nan)
    df_final_cleaned[['trans_plan_count', 'distance', 'cost', 'duration']] = df_final_cleaned[['trans_plan_count', 'distance', 'cost', 'duration']].replace(0, np.nan)
    df_final_cleaned = df_final_cleaned.dropna()

    # 对`salary`和`duty`字段从文本构造数据字段
    import re 
    def salary_match_min(x):
        return re.match(r"(\d+)-(\d+)元/天", x).group(1)
    def salary_match_max(x):
        return re.match(r"(\d+)-(\d+)元/天", x).group(2)

    df_final_cleaned['salary_min'] = df_final_cleaned['salary'].apply(salary_match_min).astype(int)
    df_final_cleaned['salary_max'] = df_final_cleaned['salary'].apply(salary_match_max).astype(int)
    df_final_cleaned['salary_avg'] = (df_final_cleaned['salary_min'] + df_final_cleaned['salary_max']) // 2
    df_final_cleaned.head(1)

    def duty_time_match_days(x):
        return re.match(r"(\d+)天/周 (\d+)个月", x).group(1)
    def duty_time_match_months(x):
        return re.match(r"(\d+)天/周 (\d+)个月", x).group(2)

    df_final_cleaned['internship_days'] = df_final_cleaned['duty_time'].apply(duty_time_match_days).astype(int)
    df_final_cleaned['internship_months'] = df_final_cleaned['duty_time'].apply(duty_time_match_months).astype(int)
    df_final_cleaned.head(1)

    # 添加方向编号
    df_subdir = pd.read_csv('子方向.csv',encoding = 'GB18030')
    df_subdir = df_subdir.reset_index()
    df_subdir = df_subdir[['index','dirno']]
    df_add_subno =  df_final_cleaned.merge(df_subdir, left_on='job_subdirno', right_on='index', how='left')
    # 输出最终结果
    df_add_subno.to_csv('job_message.csv', index=False, encoding='GB18030')


if __name__ == "__main__":
    interval = 2*24*60*60
    while True:
        get_data_task()
        time.sleep(interval)  # 等待指定的时间后继续执行

