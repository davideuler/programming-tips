import requests
from bs4 import BeautifulSoup
import chardet
import codecs


def extract_title(soup):
    """
    从 BSoup 对象中提取标题
    """
    title_tag = soup.find('title')
    if title_tag is not None:
        return title_tag.text.strip()
    else:
        return None

def extract_meta(soup):
    """
    从 BSoup 对象中提取元数据，例如关键词、描述
    """
    meta_dict = {'keywords': '', 'description': ''}
    for meta in soup.find_all('meta'):
        meta_name = meta.get('name', '').lower()
        meta_content = meta.get('content', '').strip()

        if meta_name == 'keywords':
            meta_dict['keywords'] = meta_content
        elif meta_name == 'description':
            meta_dict['description'] = meta_content
    
    return meta_dict

def extract_links(soup):
    """
    从 BSoup 对象中提取所有链接
    """
    links = []
    for link in soup.find_all('a', href=True):
        links.append(link['href'])

    return links

def extract_text(soup):
    """
    从 BSoup 对象中提取所有文本
    """
    text = ''
    for tag in soup.find_all():
        if tag.name in ['script', 'style', 'head', 'title', 'meta', '[document]']:
            # 不提取某些标签中的文本
            continue   
        elif tag.name == 'a':
            # 将链接文本作为文本的一部分，以便上下文可读性
            text += tag.text.strip() + ' (' + tag['href'] + ') '
        else:
            text += tag.text.strip() + ' '

    return text

# 示例
url = 'https://www.baidu.com'
response = requests.get(url)

encoding = chardet.detect(response.content)['encoding']
print("encoding: %s" % encoding)
source_code = codecs.decode(response.content, encoding, errors='ignore')

soup = BeautifulSoup(source_code, 'html.parser')

title = extract_title(soup)
meta = extract_meta(soup)
links = extract_links(soup)
text = extract_text(soup)

print('标题：', title)
print('关键词：', meta['keywords'])
print('描述：', meta['description'])
print('链接：', links)
print('文本：', text)
