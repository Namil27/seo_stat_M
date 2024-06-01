from bs4 import BeautifulSoup


def parse_top_sites_from_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    # Предполагаем, что таблица с данными имеет определенный класс; необходимо уточнить класс
    table = soup.find('div', {'class': 'zaza'})  # замените 'your-table-class' на актуальный класс таблицы
    rows = table.find_all('div', 'clearFix')  # Пропускаем заголовок таблицы и берем топ 30 строк

    sites_info = []
    for row in rows:
        cols = row.find_all('div')
        site_rank = cols[0].text.strip()
        site_link = cols[1].a['href'].split('//')[1].replace('www.', '')
        site_visitors = cols[2].text.strip()  # Предполагается, что в третьей колонке количество посетителей

        sites_info.append({
            'rank': site_rank,
            'link': site_link,
            'visitors': site_visitors
        })

    return sites_info


sites = [{'rank': '1', 'link': 'mail.ru', 'visitors': '7 077 384'},
         {'rank': '2', 'link': 'otvet.mail.ru', 'visitors': '3 229 271'},
         {'rank': '3', 'link': 'tsargrad.tv', 'visitors': '3 083 439'},
         {'rank': '4', 'link': 'hsdigital.ru', 'visitors': '2 890 070'},
         {'rank': '5', 'link': 'kp.ru', 'visitors': '2 691 791'},
         {'rank': '6', 'link': 'ria.ru', 'visitors': '2 224 323'},
         {'rank': '7', 'link': 'iz.ru', 'visitors': '2 053 740'},
         {'rank': '8', 'link': 'bazr.ru', 'visitors': '2 000 156'},
         {'rank': '9', 'link': 'rutube.ru', 'visitors': '1 998 144'},
         {'rank': '10', 'link': 'lenta.ru', 'visitors': '1 989 603'},
         {'rank': '11', 'link': 'rbc.ru', 'visitors': '1 908 533'},
         {'rank': '12', 'link': 'aif.ru', 'visitors': '1 627 729'},
         {'rank': '13', 'link': 'mediakit.iportal.ru', 'visitors': '1 539 697'},
         {'rank': '14', 'link': 'hh.ru', 'visitors': '1 506 128'},
         {'rank': '15', 'link': 'news.ru', 'visitors': '1 498 509'},
         {'rank': '16', 'link': 'mk.ru', 'visitors': '1 485 616'},
         {'rank': '17', 'link': '2gis.ru', 'visitors': '1 479 579'},
         {'rank': '18', 'link': 'gazeta.ru', 'visitors': '1 412 887'},
         {'rank': '19', 'link': 'progorod43.ru', 'visitors': '1 366 740'},
         {'rank': '20', 'link': 'hibiny.com', 'visitors': '1 262 451'},
         {'rank': '21', 'link': 'news.rambler.ru', 'visitors': '1 207 812'},
         {'rank': '22', 'link': 'hearst-shkulev-media.ru', 'visitors': '1 153 552'},
         {'rank': '23', 'link': 'ura.ru', 'visitors': '1 103 875'},
         {'rank': '24', 'link': 'championat.com', 'visitors': '896 360'},
         {'rank': '25', 'link': 'regnum.ru', 'visitors': '841 124'},
         {'rank': '26', 'link': 'kommersant.ru', 'visitors': '831 931'},
         {'rank': '27', 'link': '7days.ru', 'visitors': '781 697'},
         {'rank': '28', 'link': 'sport24.ru', 'visitors': '775 864'},
         {'rank': '29', 'link': 'sportbox.ru', 'visitors': '769 671'},
         {'rank': '30', 'link': 'smi2.ru', 'visitors': '767 367'}]

sites.extend([
    {'rank': '31', 'link': 'auto.ru', 'visitors': '760 123'},
    {'rank': '32', 'link': 'food.ru', 'visitors': '756 289'},
    {'rank': '33', 'link': 'travel.ru', 'visitors': '752 940'},
    {'rank': '34', 'link': 'health.ru', 'visitors': '749 865'},
    {'rank': '35', 'link': 'tech.ru', 'visitors': '745 003'},
    {'rank': '36', 'link': 'books.ru', 'visitors': '740 410'},
    {'rank': '37', 'link': 'cinema.ru', 'visitors': '735 128'},
    {'rank': '38', 'link': 'homes.ru', 'visitors': '731 245'},
    {'rank': '39', 'link': 'fashion.ru', 'visitors': '728 369'},
    {'rank': '40', 'link': 'music.ru', 'visitors': '725 891'}
])

sites.extend([
    {'rank': '41', 'link': 'garden.ru', 'visitors': '723 410'},
    {'rank': '42', 'link': 'pets.ru', 'visitors': '720 932'},
    {'rank': '43', 'link': 'finance.ru', 'visitors': '718 560'},
    {'rank': '44', 'link': 'science.ru', 'visitors': '716 284'},
    {'rank': '45', 'link': 'art.ru', 'visitors': '713 902'},
    {'rank': '46', 'link': 'nature.ru', 'visitors': '711 621'},
    {'rank': '47', 'link': 'study.ru', 'visitors': '709 338'},
    {'rank': '48', 'link': 'kids.ru', 'visitors': '707 145'},
    {'rank': '49', 'link': 'games.ru', 'visitors': '705 054'},
    {'rank': '50', 'link': 'diy.ru', 'visitors': '702 961'},
    {'rank': '51', 'link': 'law.ru', 'visitors': '700 869'},
    {'rank': '52', 'link': 'realty.ru', 'visitors': '698 776'},
    {'rank': '53', 'link': 'events.ru', 'visitors': '696 683'},
    {'rank': '54', 'link': 'jobs.ru', 'visitors': '694 591'},
    {'rank': '55', 'link': 'dating.ru', 'visitors': '692 498'},
    {'rank': '56', 'link': 'astrology.ru', 'visitors': '690 406'},
    {'rank': '57', 'link': 'photography.ru', 'visitors': '688 313'},
    {'rank': '58', 'link': 'history.ru', 'visitors': '686 221'},
    {'rank': '59', 'link': 'politics.ru', 'visitors': '684 128'},
    {'rank': '60', 'link': 'electronics.ru', 'visitors': '682 036'}
])


# Путь к вашему HTML файлу
# file_path = 'raw_data.html'
# top_sites = parse_top_sites_from_html(file_path)
# for site in top_sites:
#    print(site)
