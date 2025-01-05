import requests
import numpy as np

# api_key = "68f258a413ed2cbf1e8709e7296ae169" # 自己的key
# school = '同济大学(嘉定校区)'
# city = '上海'

class LocationToCost:
    def __init__(self, school, city, api_key):
        self.school = school
        self.city = city
        self.api_key = api_key
        # url = f'https://restapi.amap.com/v3/geocode/geo?address={school}&output=JSON&key={api_key}'
        # response = requests.get(url)
        # if response.status_code == 200:
        #     data = response.json()
        #     print(response.text)
        #     if data['status'] == '1' and 'geocodes' in data:
        #         self.tj_location = data['geocodes'][0]['location']
        #         print(f'{school}的经纬度为',self.tj_location)
        self.tj_location = '121.506269,31.281904'


    def get_school_to_company_message(self, destination):
        """
        输入某个地点的经纬度，根据学校的经纬度获取通行代价。
        """
        url = f"https://restapi.amap.com/v3/direction/transit/integrated?origin={self.tj_location}&destination={destination}&city={self.city}&key={self.api_key}"

        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data['status'] == '1' and 'route' in data:
                count = int(data['count'])  # 公交换乘方案数目
                distance = int(data['route']['distance'])  # 步行距离
                cost_list = []
                duration_list = []

                for transit in data['route'].get('transits', []):
                    cost = transit.get('cost')
                    duration = transit.get('duration')

                    # 尝试转换 cost 和 duration 为浮点数
                    try:
                        if cost is not None:
                            cost_list.append(float(cost))
                        if duration is not None:
                            duration_list.append(float(duration))
                    except (ValueError, TypeError):
                        continue

                # 如果列表为空，设置默认值
                cost = int(np.mean(cost_list)) if cost_list else 0
                duration = int(np.mean(duration_list)) if duration_list else 0

                message = {'count': count, 'distance': distance, 'cost': cost, 'duration': duration}
                return message
            else:
                print("无法获取路径数据：API返回无效内容。")
        else:
            print(f"请求失败：状态码 {response.status_code}。")
        return None

