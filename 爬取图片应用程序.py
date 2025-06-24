import time
import requests
import parsel
import random
import os
from PIL import Image
import io

# 创建IMG目录
if not os.path.exists('IMG'):
    os.makedirs('IMG')

page_num = 0  # 记录页数
counter = 1  # 记录帖子序号
expected_counter = 1  # 用于保持序号连贯性
for page in range(0, 11457351, 50):
    page_num += 1
    print(f'------------------正在爬取第{page_num}页数据------------------')
    x = random.uniform(1, 3)
    time.sleep(x)
    url = f'https://tieba.baidu.com/f?ie=utf-8&kw=ps%E5%90%A7&pn={page}'  # 使用pn参数翻页
    x = page / 50 + 1
    print('现在是第' + str(x) + '页')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) Like Gecko'
    }
    # 发送网络请求
    try:
        response = requests.get(url=url, headers=headers)
        response.raise_for_status()  # 检查请求是否成功
        html_data = response.text
    except requests.RequestException as e:
        print(f"请求页面失败: {e}")
        continue

    # 数据解析
    selector = parsel.Selector(html_data)
    title_url = selector.xpath('//div[@class="threadlist_lz clearfix"]/div/a/@href').getall()
    for li in title_url:
        # 拼接帖子链接
        all_url = 'https://tieba.baidu.com' + li
        print('当前帖子链接为：', all_url)

        # 请求帖子内容
        x = random.uniform(1, 3)
        time.sleep(x)
        try:
            response_2 = requests.get(url=all_url, headers=headers)
            response_2.raise_for_status()
            response_2_selector = parsel.Selector(response_2.text)
        except requests.RequestException as e:
            print(f"请求帖子失败: {e}")
            continue

        # 解析图片地址
        result_list = response_2_selector.xpath('//cc/div/img[@class="BDE_Image"]/@src').getall()
        if not result_list:
            continue  # 如果没有图片，跳过

        # 获取 x.1.jpg 的长宽作为参考
        reference_dimensions = None
        a_counter = 1
        saved_images = False  # 标记是否保存了图片
        for result in result_list:
            x = random.uniform(1, 3)
            time.sleep(x)
            try:
                img_response = requests.get(url=result, headers=headers)
                img_response.raise_for_status()
                img_data = img_response.content
                # 使用 PIL 获取图片尺寸
                img = Image.open(io.BytesIO(img_data))
                img_dimensions = img.size  # 获取 (宽度, 高度)
            except (requests.RequestException, Image.UnidentifiedImageError) as e:
                print(f"请求或解析图片失败: {e}")
                continue

            # 如果是 x.1.jpg，记录其尺寸
            if a_counter == 1:
                reference_dimensions = img_dimensions
                # 保存 x.1.jpg
                file_name = f'IMG/{expected_counter}.{a_counter}.jpg'
                with open(file_name, mode='wb') as f:
                    f.write(img_data)
                print("保存完成：", f"{expected_counter}.{a_counter}")
                saved_images = True
                a_counter += 1
            else:
                # 只保存与 x.1.jpg 长宽相同的图片
                if img_dimensions == reference_dimensions:
                    file_name = f'IMG/{expected_counter}.{a_counter}.jpg'
                    with open(file_name, mode='wb') as f:
                        f.write(img_data)
                    print("保存完成：", f"{expected_counter}.{a_counter}")
                    saved_images = True
                    a_counter += 1
                else:
                    print(f"跳过图片 {result}，尺寸 {img_dimensions} 与参考尺寸 {reference_dimensions} 不符")


        # 如果保存了图片，递增 expected_counter
        if saved_images:
            expected_counter += 1
        counter += 1