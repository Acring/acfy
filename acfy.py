#!python3
# coding=utf-8
"""
             acfy
命令行翻译脚本 使用有道翻译API

运行环境:python3.5 Linux/Windows

不指定语言的查询
例 acfy i am your father
指定语言查询
例 acfy -l zh "你好 朋友" ja

Options:
    -l      指定语言的查询
    -h      显示帮助文档

注意在指定语言查询时，长句子要用单引号或双引号引起来
语言转换表
    zh          中文
    ja          日文
    en          英文
    ko          韩语
    fr          法语
    ru          俄语
    pt          葡萄牙
    es          西班牙
"""
import requests
import hashlib
import random
import sys
import getopt

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


# 生成md5签名
def to_sign(q, salt):
    """
    签名要进行UTF-8编码(否则中文无法翻译)
    :param q: 翻译文本
    :param salt: 随机数
    :return: sign: md5签名
    """
    sign = app_key + q + salt + secret_key
    m = hashlib.md5()
    m.update(sign.encode('utf-8'))
    sign = m.hexdigest()
    return sign


# 生成api_url
def get_api_url(sign, salt, q="Hello World", from_lan="auto", to_lan="auto"):
    api_url = "{}?q={}&sign={}&from={}&to={}&appKey={}&salt={}".format(https_url, q, sign, from_lan, to_lan, app_key, salt)
    return api_url


# 解析返回的json字段生成翻译
def resolve_res(trans_json):
    """
    把API返回的json字段解析成文字
    :param trans_json: json
    :return: string
    """
    if type(trans_json) != dict:
        print("返回字段格式不正确:",type(trans_json))
        return ""
    if trans_json["errorCode"] != '0':  # 查询正确与否
        print("查询失败,errorCode:{},可查询官方文档:{}".format(trans_json["errorCode"], api_docs))
        return ""

    result = "==============acfy翻译结果==============\n"  # 翻译结果

    if 'l' in trans_json:  # 转换关系
        lan2lan = trans_json['l'].split('2')
        result += "{}转{}".format(language[lan2lan[0]], language[lan2lan[1]]) + '\n'

    if 'query' in trans_json:  # 查询词句
        print(trans_json['query'])
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


def resolve_opts(argv):
    """
    解析命令行参数
    :param argv: 命令行参数
    1.不指定语言的查询(中英互译) 如'hello'
    2.指定语言的查询 如'-l zh 你好 ja'
    :return: query:dict 如{'form':'zh', 'to': 'ja', 'q': '你好'}
    """
    query = {'form': 'auto', 'to': 'auto', 'q': ''}
    short_opts = 'hl'
    lan = ['zh', 'ja', 'en', 'ko', 'fr', 'ru', 'pt', 'es']
    opts, argvs = getopt.getopt(argv[1:], short_opts)
    for o, a in opts:
        if o == '-h':  # 显示帮助文档
            print(__doc__)
            sys.exit(0)
        if o == '-l':  # 指定语言的翻译
            if argvs[0] in lan and argvs[2] in lan:
                query['form'] = argvs[0]
                query['q'] = argvs[1]
                query['to'] = argvs[2]
                break
            else:
                print("指定语言不正确")
                sys.exit(1)
    else:  # 不指定语言的查询
        q = " ".join(argvs)
        query['q'] = q
    return query


def main():
    argv = sys.argv

    query = resolve_opts(argv)

    if query['q'] == '':
        print("翻译文本为空,请重新输入")
        return 1
    salt = str(random.randint(12345, 56789))  # 生成随机数
    sign = to_sign(query['q'], salt)  # 生成签名
    api_url = get_api_url(q=query['q'], sign=sign, salt=salt, from_lan=query['form'], to_lan=query['to'],)
    translation_json = requests.get(api_url)
    if not translation_json.ok:
        print("网络错误:{}".format(translation_json))
        return 2
    result = resolve_res(trans_json=translation_json.json())
    print(result)
    return 0

if __name__ == '__main__':
    sys.exit(main())
