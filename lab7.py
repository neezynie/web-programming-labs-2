from flask import Blueprint, render_template, request, redirect, session, current_app, jsonify
from datetime import datetime

lab7 = Blueprint('lab7', __name__)

films = [
    {
        "title": "1+1",
        "title_ru": "1+1",
        "year": 2011,
        "description": "Пострадавв результате несчастного случая, богатый аристократ Филипп нанимает в помощники человека, который менее всего подходит для этой работы, – молодого жителя предместья Дрисса, только что освободившегося из тюрьмы. Несмотря на то, что Филипп прикован к инвалидному креслу, Дриссу удается привнести в размеренную жизнь аристократа дух приключений."
    },
    {
        "title": "The Green Mile",
        "title_ru": "Зеленая миля",
        "year": 1999,
        "description": "Пол Эджкомб — начальник блока смертников в тюрьме «Холодная гора», каждый из узников которого однажды проходит «зеленую милю» по пути к месту казни. Пол повидал много заключённых и надзирателей за время работы. Однако гигант Джон Коффи, обвинённый в страшном преступлении, стал одним из самых необычных обитателей блока."
    },
    {
        "title": "Fight Club",
        "title_ru": "Бойцовский клуб ",
        "year": 1999,
        "description": "Сотрудник страховой компании страдает хронической бессонницей и отчаянно пытается вырваться из мучительно скучной жизни. Однажды в очередной командировке он встречает некоего Тайлера Дёрдена — харизматического торговца мылом с извращенной философией. Тайлер уверен, что самосовершенствование — удел слабых, а единственное, ради чего стоит жить, — саморазрушение.Проходит немного времени, и вот уже новые друзья лупят друг друга почем зря на стоянке перед баром, и очищающий мордобой доставляет им высшее блаженство. Приобщая других мужчин к простым радостям физической жестокости, они основывают тайный Бойцовский клуб, который начинает пользоваться невероятной популярностью."
    },
]

@lab7.route('/lab7/')
def main():
    return render_template("lab7/index.html")

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_all_films():
    return jsonify(films)

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_films(id):
    if id < 0 or id >= len(films):
        return jsonify({"error": "Film not found"}), 404
    
    return jsonify(films[id])

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    if id < 0 or id >= len(films):
        return jsonify({"error": "Film not found"}), 404
    del films[id]
    return "", 204

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    if id < 0 or id >= len(films):
        return jsonify({"error": "Film not found"}), 404
    
    film = request.get_json()
    
    errors = {}
    if 'title_ru' not in film or not film['title_ru']:
        if 'title' not in film or not film['title']:
            errors['title'] = 'Название на оригинальном языке должно быть непустым, если русское название пустое'
    if 'title' not in film or not film['title']:
        if 'title_ru' not in film or not film['title_ru']:
            errors['title'] = 'Название на оригинальном языке должно быть непустым, если русское название пустое'
    if 'year' not in film:
        errors['year'] = 'Год должен быть указан'
    else:
        try:
            year = int(film['year'])  
            if not (1895 <= year <= datetime.now().year):
                errors['year'] = f'Год должен быть от 1895 до {datetime.now().year}'
        except ValueError:
            errors['year'] = 'Год должен быть числом'
    if 'description' not in film or not film['description']:
        errors['description'] = 'Описание должно быть непустым'
    if 'description' in film and len(film['description']) > 2000:
        errors['description'] = 'Описание должно быть не более 2000 символов'
    
    if errors:
        return jsonify(errors), 400
    
    if not film['title']:
        film['title'] = film['title_ru']
    
    films[id] = film
    return jsonify(films[id])

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    new_film = request.get_json()
    
    errors = {}
    if 'title_ru' not in new_film or not new_film['title_ru']:
        if 'title' not in new_film or not new_film['title']:
            errors['title'] = 'Название на оригинальном языке должно быть непустым, если русское название пустое'
    if 'title' not in new_film or not new_film['title']:
        if 'title_ru' not in new_film or not new_film['title_ru']:
            errors['title'] = 'Название на оригинальном языке должно быть непустым, если русское название пустое'
    if 'year' not in new_film:
        errors['year'] = 'Год должен быть указан'
    else:
        try:
            year = int(new_film['year'])  
            if not (1895 <= year <= datetime.now().year):
                errors['year'] = f'Год должен быть от 1895 до {datetime.now().year}'
        except ValueError:
            errors['year'] = 'Год должен быть числом'
    if 'description' not in new_film or not new_film['description']:
        errors['description'] = 'Описание должно быть непустым'
    if 'description' in new_film and len(new_film['description']) > 2000:
        errors['description'] = 'Описание должно быть не более 2000 символов'
    
    if errors:
        return jsonify(errors), 400
    
    if not new_film['title']:
        new_film['title'] = new_film['title_ru']
    
    films.append(new_film)
    
    new_film_index = len(films) - 1
    
    return jsonify({"id": new_film_index}), 201