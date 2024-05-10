from datetime import datetime
import requests

weather_key = "ec61d48470d3489ca731ecbc82bb0dbb"


# 模拟天气查询工具。返回结果示例：“北京今天是晴天。”

def get_location_geo(location):
    base_url = "https://geoapi.qweather.com/v2/city/lookup"
    params = {
        "location": location,
        "key": weather_key,
        "lang": "zh",  # 设置语言为中文
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    # print(data)

    # 假设我们只需要第一个匹配的位置信息
    if data['code'] == '200' and data['location']:
        return data['location'][0]['id']
    else:
        return None


def get_current_weather(location):
    location_geo = get_location_geo(location)
    base_url = "https://devapi.qweather.com/v7/weather/now"
    params = {
        "location": location_geo,
        "key": weather_key,
        "lang": "zh",  # 设置语言为中文
        "unit": "m"  # 设置单位为公制单位
    }

    response = requests.get(base_url, params=params)
    data = response.json()
    print(data)
    if response.status_code == 200:
        try:
            weather = data['now']['text']
            temperature = data['now']['temp']
            feels_like = data['now']['feelsLike']
            humidity = data['now']['humidity']
            wind_dir = data['now']['windDir']
            wind_scale = data['now']['windScale']
            return f"{location} 当前的天气为{weather}，温度为{temperature}℃，体感温度为{feels_like}℃，湿度为{humidity}%，风向为{wind_dir}，风力为{wind_scale}级。"
        except KeyError as e:
            print(f"返回的数据中缺少必要的键值。完整的返回数据是：")
            print(data)
            return f"无法解析天气信息，缺少键值：{e}"
    else:
        return "无法获取天气信息，错误代码:" + str(response.status_code)


def get_weather_forecast(location):
    location_geo = get_location_geo(location)


# 查询当前时间的工具。返回结果示例：“当前时间：2024-04-15 17:15:18。“
def get_current_time():
    # 获取当前日期和时间
    current_datetime = datetime.now()
    # 格式化当前日期和时间
    formatted_time = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
    # 返回格式化后的当前时间
    return f"当前时间：{formatted_time}。"


if __name__ == '__main__':
    print(get_location_geo("长沙"))
