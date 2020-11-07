from bs4 import BeautifulSoup
import requests

# адрес страницы конкретного вопроса Хабр Q&A это ничто иное как "https://qna.habr.com/q/{id}"
QNA_QUESTION_URL = 'https://qna.habr.com/q/'

# заголовки для HTTP
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
}


def dowloadPage(url):
    page = requests.get(url, headers=headers)
    if page.status_code == 200:
        print(f'Downloading {url} status code: {page.status_code} (OK)')
    return page


def parseTags(document):
    tags = []
    elements = document.select('ul.tags-list li.tags-list__item')
    for i in elements:
        try:
            tags.append(i.attrs['data-tagname'])
        except:
            continue
    return tags


def parseDate(document):
    try:
        date = document.findAll('time')[0]['datetime']
    except:
        date = 'undefined'
    return date


def parseViewCounts(document):
    try:
        viewCounts = document.find(itemprop="interactionCount").get("content")
    except:
        viewCounts = 'undefined'
    return viewCounts


def parseTitle(document):
    try:
        title = document.select('#question_show > div.question.question_full > h1')[0].text
    except:
        title = 'undefined'
    return title


def parseSignersCount(document):
    try:
        signersCount = document.select('#question_show > div.question.question_full > '
                                       'div.buttons-group.buttons-group_question > a.btn.btn_subscribe > span')[0].text
    except:
        signersCount = 'undefined'
    return signersCount


def parseDifficulty(document):
    try:
        difficulty = document.select('#question_show > div.question.question_full > '
                                     'div.buttons-group.buttons-group_question > span')[0].text
    except:
        difficulty = 'undefined'
    return difficulty


def parseSolutionsCount(document):
    try:
        solutionsCount = document.select('#solutions > header > strong > span')[0].text
    except:
        solutionsCount = 'undefined'
    return solutionsCount


def parseSolutionsCount(document):
    try:
        solutionsCount = document.select('#solutions > header > strong > span')[0].text
    except:
        solutionsCount = 'undefined'
    return solutionsCount


def parseAnswersCount(document):
    try:
        answersCount = document.select('#answers > header > strong > span')[0].text
    except:
        answersCount = 'undefined'
    return answersCount


def parseAskerNickname(document):
    try:
        askerNickname = document.select('#question_show > div.question.question_full > div.question-head > '
                                        'div.user-summary.user-summary_question > div > span')[0].text
    except:
        askerNickname = 'undefined'
    return askerNickname


def parseDescriptionLength(document):
    try:
        descriptionLength = len(document.select('#question_show > div.question.question_full > '
                                                'div.question__body > div')[0].text)
    except:
        descriptionLength = 'undefined'
    return descriptionLength


def parseRespondents(document):
    respondents = []
    elements = document.select('div.answer > div.answer__header > div > div > span')
    for i in elements:
        try:
            respondents.append(i.text.strip().replace('@', '').replace('Автор вопроса', ''))
        except:
            continue
    return respondents


def parseQuestion(questionId, document):
    title = parseTitle(document).strip()

    if (title == 'undefined'):
        return

    tags = parseTags(document)
    difficulty = parseDifficulty(document).strip()
    date = parseDate(document)
    viewsCount = parseViewCounts(document).strip('views')
    signersCount = parseSignersCount(document).strip()
    solutionsCount = parseSolutionsCount(document).strip()
    answersCount = parseAnswersCount(document).strip()
    askerNickname = parseAskerNickname(document).strip().replace('@', '')
    respondents = parseRespondents(document)
    descriptionLength = parseDescriptionLength(document)

    return {
        'questionId': questionId,
        'title': title,
        'tags': tags,
        'difficulty': difficulty,
        'date': date,
        'viewsCount': viewsCount,
        'signersCount': signersCount,
        'solutionsCount': solutionsCount,
        'answersCount': answersCount,
        'askerNickname': askerNickname,
        'respondents': respondents,
        'descriptionLength': descriptionLength
    }


def getParsedQuestion(questionId):
    page = dowloadPage(QNA_QUESTION_URL + str(questionId).zfill(6))
    document = BeautifulSoup(page.text, "html.parser")
    question = parseQuestion(questionId, document)
    return question
