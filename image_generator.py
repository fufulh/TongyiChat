from http import HTTPStatus
from urllib.parse import urlparse, unquote
from pathlib import PurePosixPath
from minio import Minio
from minio.error import S3Error
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
        # 设置MinIO服务器信息，endpoint不要带http/https
        minio_endpoint = '127.0.0.1:9000'
        minio_access_key = 'TXkKGJSBdqZhErSmRi5t'
        minio_secret_key = 'OmaJNEdjmz5aK2vV08tjjZtta6GrjuWbTu4hdsur'
        minio_bucket = 'history'

        # 创建MinIO客户端
        minio_client = Minio(minio_endpoint,
                             access_key=minio_access_key,
                             secret_key=minio_secret_key,
                             secure=False)  # 如果使用https，请将secure设置为True
        # 保存文件到 MinIO 服务器并获取 URL
        urls = []
        for result in rsp.output.results:
            url = result.url
            file_name = os.path.basename(unquote(urlparse(url).path))
            file_path = os.path.join('./temp', file_name)

            # 下载文件到临时目录
            with open(file_path, 'wb') as f:
                f.write(requests.get(url).content)

            # 上传文件到 MinIO 服务器
            try:
                minio_client.fput_object(minio_bucket, file_name, file_path)
                # 获取文件的 URL
                object_url = minio_client.presigned_get_object(minio_bucket, file_name)
                urls.append(object_url)
            except S3Error as e:
                return None, 'Failed to upload file to MinIO: {}'.format(e)

        return urls, None
    else:
        # 返回错误信息
        return None, 'Failed, status_code: %s, code: %s, message: %s' % (rsp.status_code, rsp.code, rsp.message)