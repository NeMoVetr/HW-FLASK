import logging

from django.http import HttpResponse

# Create your views here.

logger = logging.getLogger(__name__)


def index(request):
    html = """
    <h1>Это главная страница моего сайта</h1>
    <p>Привет мир!</p>
    """

    logger.info("Страницу 'Главаня' кто-то посетил (-_-)")
    return HttpResponse(html)


def about(request):
    html = """
    <h1>Это страница расскажет вам обо мне</h1>
    <p>Здесь что-то написано обо мне и очень интересно излаженно ))))</p>
    """

    logger.info("Страницу 'О себе' кто-то посетил (-_-)")

    return HttpResponse(html)
