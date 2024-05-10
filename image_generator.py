from http import HTTPStatus
from urllib.parse import urlparse, unquote
from pathlib import PurePosixPath

import dashscope
import requests
import os
from dashscope import ImageSynthesis

dashscope.api_key = "sk-0778e34d54d14e88a932ccc17b67c80c"

baseurl = "http://127.0.0.1:5000/"


def generate_images(prompt, n=1, size='1024*1024'):
    rsp = ImageSynthesis.call(model=ImageSynthesis.Models.wanx_v1,
                              prompt=prompt,
                              n=n,
                              size=size)
    if rsp.status_code == HTTPStatus.OK:
        # 保存文件到临时目录
        temp_dir = './temp'
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        urls = []
        print(rsp)
        for result in rsp.output.results:
            file_name = PurePosixPath(unquote(urlparse(result.url).path)).parts[-1]
            file_path = os.path.join(temp_dir, file_name)
            with open(file_path, 'wb+') as f:
                f.write(requests.get(result.url).content)
            # 返回文件的URL
            urls.append(baseurl + file_name)
        return urls, None
    else:
        # 返回错误信息
        return None, 'Failed, status_code: %s, code: %s, message: %s' % (rsp.status_code, rsp.code, rsp.message)