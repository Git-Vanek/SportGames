from bottle import post, request, template
from datetime import date, datetime
import json
import re

# ���������� ��������� ��� �������� ���� � ������� "��.��.����"
regexfordate = re.compile(r'\d{2}.\d{2}.\d{4}$')
# ���������� ��������� ��� �������� �������� � ������� �� 2 �� 20 ��������, ��������� �����, �����,
#  ������ ������������� � �����
regexfornickname = re.compile('[a-zA-Z1-9_\-]{2,20}')

# ������� ��� �������� ������������ ����
def isValidDate(date):
    try:  
        if re.fullmatch(regexfordate, date):
            # ���������, ��� ���� �� ����� ������� � �� ������ 25 ���
            if(datetime.strptime(date, '%d.%m.%Y') <= datetime.now() 
               and (datetime.now().year - datetime.strptime(date, '%d.%m.%Y').year < 25)):
                return True
        return False
    except:
        return False
    
# ������� ��� �������� ������������ ��������
def isValidNick(nick):
    if re.fullmatch(regexfornickname, nick):
        return True
    return False
         

# ��������� ��� ������� addarticle, �����������, ��� ��� ������������ POST-������� �� ����� "/articles"
@post('/articles', method='post')
# ������� ��� ���������� ������
def addarticle():
    #�������� ����������, � ������� ����������� ������ ����� �����
    title = request.forms.get('TITLE')
    description = request.forms.get('DESCRIPTION')
    username = request.forms.get('USERNAME')
    link = request.forms.get('LINK')
    current_date = request.forms.get('DATE')
    # ���������, ��� ����� ��������� �� ����� 8 ��������
    if(len(title) < 8):
        return f"Incorrect title! The title of the article must be at least 8 characters long!" 
    # ���������, ��� ����� �������� �� ����� 50 � �� ����� 350 ��������
    elif(len(description) < 20 or len(description) > 350):
        return f"Incorrect description! The description of the article must be between 20 and 350 characters!" 
    # ���������, ��� ������� ���������
    elif(not isValidNick(username)):
        return f"Incorrect nickname! The nickname must be from 2 to 20 characters (without special characters)!" 
    # ���������, ��� ����� ������ �� ����� 10 ��������
    elif(len(link) < 10):
        return f"Incorrect link! An existing link must be entered!" 
    # ���������, ��� ���� ���������
    elif(not isValidDate(current_date)):
        return f"Incorrect date! The date must be in the format \"dd.MM.yyyy\" and should not be outdated!" 
    

    try:
        # ��������� ���� "articles.json" ��� ������
        with open("static\\articles.json", "r") as read_json:
            # ��������� ������ �� ����� � ������ articles
            articles = json.load(read_json)
    except FileNotFoundError:
            # ���� ���� �� ������, ������� ����� ������ articles    
            articles = []
    except:
        articles = []

    # ��������� ����� ������ � ������ articles
    articles.append({title:{'author': username, 'text': description, 'link': link, 'date': current_date}})
    # ���������, ��� ������ articles �� ������
    if(articles != []):
        # ��������� ������ articles �� ���� � �������� �������
        articles.sort(key=lambda x: x[list(x.keys())[0]]['date'], reverse=True)
    # ��������� ���� "articles.json" ��� ������.
    with open("static\\articles.json", 'w') as outfile:
        # ���������� ������ �� ������ articles � ����
        json.dump(articles, outfile, indent = 3)
    
    # ���������� ������ articles.tpl � ������� ��� ����������� �� ��������
    return template('articles.tpl',title='Articles',
        message='Your articles page.',
        year=datetime.now().year,
        data=articles)
