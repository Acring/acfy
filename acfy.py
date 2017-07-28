# python3
# coding=utf-8

import requests
import hashlib
import random
import sys


https_url = "https://openapi.youdao.com/api"  # Api的https地址
app_key = "223abc56842b3d2d"  # 应用ID
secret_key = "zfa16CDguP0VTTYHIsmlUBsG0IDYmzTx"  # 应用密钥
api_docs = "http://ai.youdao.com/docs/api.s#"  # 有道翻译api和说明文档
language = {  # 语言转换表
    "zh-CHS": "中文",
    "ja": "日文",
    "EN": "英文",
    "ko": "韩语",
    "fr": "法语",
    "ru": "俄语",
    "pt": "葡萄牙",
    "es": "西班牙文"
}


# 生成md5sign
def to_sign(q, salt):
    sign = app_key + q + salt + secret_key
    m = hashlib.md5()
    m.update(sign.encode('gb2312'))
    sign = m.hexdigest()
    return sign


# 生成api_url
def get_api_url(sign, salt, q="Hello World", from_lan="auto", to_lan="auto"):
    api_url = "{}?q={}&sign={}&from={}&to={}&appKey={}&salt={}".format(https_url, q, sign, from_lan, to_lan, app_key, salt)
    return api_url


# 解析返回的json字段生成翻译
def resolve_res(trans_json):
    if type(trans_json) != dict:
        print("返回字段格式不正确:",type(trans_json))
        return ""
    if trans_json["errorCode"] != '0':  # 查询正确与否
        print("查询失败,errorCode:{},可查询官方文档:{}".format(trans_json.errorCode, api_docs))
        return ""

    result = "==============翻译结果==============\n"  # 翻译结果
    if 'l' in trans_json:  # 转换关系
        lan2lan = trans_json['l'].split('2')
        result += "{}转{}".format(language[lan2lan[0]], language[lan2lan[1]]) + '\n'

    if 'query' in trans_json:  # 查询词句
        result += trans_json['query'] + '\n'
    if 'translation' in trans_json:  # 翻译结果
        translation = "结果:" + "; ".join(trans_json['translation'])
        result += translation + '\n'
    if 'basic' in trans_json:  # 词义及发音
        basic = ""
        if 'uk-phonetic' in trans_json['basic']:  # 英式发音
            basic += '英[{}]'.format(trans_json['basic']['uk-phonetic'])
        if 'us-phonetic' in trans_json['basic']:  # 美式发音
            basic += '美[{}]'.format(trans_json['basic']['us-phonetic'])

        basic += "\n词义:\n" + "\n".join(trans_json['basic']['explains'])
        result += basic + '\n'
    if 'web' in trans_json:  # 网络释义
        web = "网络释义:\n"
        for web_trans in trans_json['web']:
            web += '{},{}'.format(web_trans['key'], "; ".join(web_trans['value'])) + '\n'
        result += web + '\n'

    return result

if __name__ == '__main__':
    q = " ".join(sys.argv[1:])  # 获取要翻译的文本
    q="hi"  # TEST
    salt = str(random.randint(12345, 56789))  # 生成随机数
    sign = to_sign(q, salt)  # 生成签名
    api_url = get_api_url(q=q, sign=sign, salt=salt)  # TODO 翻译类型
    translation_json = requests.get(api_url)
    result = resolve_res(trans_json=translation_json.json())
    print(result)