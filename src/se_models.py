from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from os import urandom

db = SQLAlchemy()

tag = db.Table('tag',
               db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True),
               db.Column('thesis_id', db.Integer, db.ForeignKey('thesis.id'), primary_key=True)
               )

class Staff (db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    official_email = db.Column(db.String(255), unique=True, nullable=False)
    position = db.Column(db.String(255), nullable=False)
    science_degree = db.Column(db.String(255), nullable=True)
    still_working = db.Column(db.Boolean, default=False, nullable=False)

    supervisor = db.relationship("Thesis", backref=db.backref("supervisor"), foreign_keys = 'Thesis.supervisor_id')
    adviser = db.relationship("Thesis", backref=db.backref("reviewer"), foreign_keys = 'Thesis.reviewer_id')

    def __repr__(self):
        return '<Staff %r>' % self.official_email

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(255), unique=True, nullable=True)
    password_hash = db.Column(db.String(255), unique=False, nullable=True)

    first_name = db.Column(db.String(255), nullable=False)
    middle_name = db.Column(db.String(255), nullable=True)
    last_name = db.Column(db.String(255), nullable=True)

    avatar_uri = db.Column(db.String(512), default='empty.jpg', nullable=False)

    vk_id = db.Column(db.String(255), nullable=True)
    fb_id = db.Column(db.String(255), nullable=True)
    google_id = db.Column(db.String(255), nullable=True)

    staff = db.relationship("Staff", backref=db.backref("user", uselist=False))

    def get_name(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"

    def __repr__(self):
        return '<Users %r %r %r>' % (self.last_name, self.first_name, self.middle_name)

# Coursework, diploma
class Worktype (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(255), nullable=False)

    thesis = db.relationship("Thesis", backref=db.backref("type", uselist=False))

    def __repr__(self):
        return '<WorkType %r>' % self.type

# Courses
class Courses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    code = db.Column(db.String(15), nullable=False)

    thesis = db.relationship("Thesis", backref=db.backref('course', uselist=False))

class Thesis (db.Model):
    id = db.Column(db.Integer, primary_key=True)

    type_id = db.Column(db.Integer, db.ForeignKey('worktype.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)

    name_ru = db.Column(db.String(512), nullable=False)
    name_en = db.Column(db.String(512), nullable=True)
    description = db.Column(db.String(4096), nullable=True)

    text_uri = db.Column(db.String(512), nullable=True)
    old_text_uri = db.Column(db.String(512), nullable=True)
    presentation_uri = db.Column(db.String(512), nullable=True)
    supervisor_review_uri = db.Column(db.String(512), nullable=True)
    reviewer_review_uri = db.Column(db.String(512), nullable=True)
    source_uri = db.Column(db.String(512), nullable=True)

    author = db.Column(db.String(512), nullable=False)
    supervisor_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=True)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=True)

    publish_year = db.Column(db.Integer, nullable=False)
    recomended = db.Column(db.Boolean, default=False, nullable=False)

class Tags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)

    tags = db.relationship('Thesis', secondary=tag, lazy='subquery', backref=db.backref('tags', lazy=True))


def init_db():

    # Data
    users = [
        {'email' : 'a.terekhov@spbu.ru', 'first_name' : 'Андрей', 'last_name' : 'Терехов', 'middle_name' : 'Николаевич',
         'avatar_uri' : 'terekhov.jpg'},
        {'email': 'o.granichin@spbu.ru', 'first_name': 'Олег', 'last_name': 'Граничин', 'middle_name': 'Николаевич',
         'avatar_uri': 'granichin.jpg'},
        {'email': 'd.koznov@spbu.ru', 'first_name': 'Дмитрий', 'last_name': 'Кознов', 'middle_name': 'Владимирович',
         'avatar_uri': 'koznov.jpg'},
        {'email': 't.bryksin@spbu.ru', 'first_name': 'Тимофей', 'last_name': 'Брыксин', 'middle_name': 'Александрович',
         'avatar_uri': 'bryksin.jpg'},
        {'email': 'd.bylychev@spbu.ru', 'first_name': 'Дмитрий', 'last_name': 'Булычев', 'middle_name': 'Юрьевич',
         'avatar_uri': 'boulytchev.jpg'},
        {'email': 'y.litvinov@spbu.ru', 'first_name': 'Юрий', 'last_name': 'Литвинов', 'middle_name': 'Викторович',
         'avatar_uri': 'litvinov.jpg'},
        {'email': 'd.lutsiv@spbu.ru', 'first_name': 'Дмитрий', 'last_name': 'Луцив', 'middle_name': 'Вадимович',
         'avatar_uri': 'luciv.jpg'},
        {'email': 'k.romanovsky@spbu.ru', 'first_name': 'Константин', 'last_name': 'Романовский', 'middle_name': 'Юрьевич',
         'avatar_uri': 'empty.jpg'},
        {'email': 'm.serov@spbu.ru', 'first_name': 'Михаил', 'last_name': 'Серов',
         'middle_name': 'Александрович', 'avatar_uri': 'empty.jpg'},
        {'email': 's.s.sysoev@spbu.ru', 'first_name': 'Сергей', 'last_name': 'Сысоев',
         'middle_name': 'Сергеевич', 'avatar_uri': 'empty.jpg'},
        {'email': 'm.baklanovsky@spbu.ru', 'first_name': 'Максим', 'last_name': 'Баклановский',
         'middle_name': 'Викторович', 'avatar_uri': 'baklanovsky.jpg'},
        {'email': 'm.m.zhuravlev@spbu.ru', 'first_name': 'Максим', 'last_name': 'Журавлев',
         'middle_name': 'Михайлович', 'avatar_uri': 'zhuravlev.jpg'},
        {'email': 'i.zelenchuk@spbu.ru', 'first_name': 'Илья', 'last_name': 'Зеленчук',
         'middle_name': 'Валерьевич', 'avatar_uri': 'zelenchuk.jpg'},
        {'email': 'y.kirilenko@spbu.ru', 'first_name': 'Яков', 'last_name': 'Кириленко',
         'middle_name': 'Александрович', 'avatar_uri': 'kirilenko.jpg'},
        {'email': 'st035425@student.spbu.ru', 'first_name': 'Антон', 'last_name': 'Козлов',
         'middle_name': 'Павлович', 'avatar_uri': 'empty.jpg'},
        {'email': 'egor.k.kulikov@gmail.com', 'first_name': 'Егор', 'last_name': 'Куликов',
         'middle_name': 'Константинович', 'avatar_uri': 'kulikov.jpg'},
        {'email': 'd.mordvinov@spbu.ru', 'first_name': 'Дмитрий', 'last_name': 'Мордвинов',
         'middle_name': 'Александрович', 'avatar_uri': 'empty.jpg'},
        {'email': 'm.nemeshev@spbu.ru', 'first_name': 'Марат', 'last_name': 'Немешев',
         'middle_name': 'Халимович', 'avatar_uri': 'empty.jpg'},
        {'email': 'stanislav.sartasov@spbu.ru', 'first_name': 'Станислав', 'last_name': 'Сартасов',
         'middle_name': 'Юрьевич', 'avatar_uri': 'empty.jpg'},
        {'email': 'm.n.smirnov@spbu.ru', 'first_name': 'Михаил', 'last_name': 'Смирнов',
         'middle_name': 'Николаевич', 'avatar_uri': 'smirnov.jpg'},
        {'email': 'st036451@student.spbu.ru', 'first_name': 'Артур', 'last_name': 'Ханов',
         'middle_name': 'Рафаэльевич', 'avatar_uri': 'empty.jpg'},
        {'email': 's.shilov@spbu.ru', 'first_name': 'Сергей', 'last_name': 'Шилов',
         'middle_name': 'Юрьевич', 'avatar_uri': 'empty.jpg'},
        {'email': 'st013464@student.spbu.ru', 'first_name': 'Петр', 'last_name': 'Лозов',
         'middle_name': 'Алексеевич', 'avatar_uri': 'empty.jpg'},
        {'email': 'st013039@student.spbu.ru', 'first_name': 'Евгений', 'last_name': 'Моисеенко',
         'middle_name': 'Александрович', 'avatar_uri': 'empty.jpg'},
        {'email': 's.v.grigoriev@spbu.ru', 'first_name': 'Семен', 'last_name': 'Григорьев',
         'middle_name': 'Вячеславович', 'avatar_uri': 'empty.jpg'},
        {'email': 'pimenov_aa_stub@spbu.ru', 'first_name': 'Александр', 'last_name': 'Пименов',
         'middle_name': 'Александрович', 'avatar_uri': 'empty.jpg'},
    ]
    staff = [
        {'position': 'Заведующий кафедрой, профессор', 'science_degree' : 'д.ф.-м.н.',
         'official_email': 'a.terekhov@spbu.ru', 'still_working' : True},
        {'position': 'Профессор', 'science_degree': 'д.ф.-м.н.',
         'official_email': 'o.granichin@spbu.ru', 'still_working': True},
        {'position': 'Профессор', 'science_degree': 'д.т.н.',
         'official_email': 'd.koznov@spbu.ru', 'still_working': True},
        {'position': 'Доцент', 'science_degree': 'к.т.н.',
         'official_email': 't.bryksin@spbu.ru', 'still_working': True},
        {'position': 'Доцент', 'science_degree': 'к.ф.-м.н.',
         'official_email': 'd.bylychev@spbu.ru', 'still_working': True},
        {'position': 'Доцент', 'science_degree': 'к.т.н.',
         'official_email': 'y.litvinov@spbu.ru', 'still_working': True},
        {'position': 'Доцент', 'science_degree': 'к.ф.-м.н.',
         'official_email': 'd.lutsiv@spbu.ru', 'still_working': True},
        {'position': 'Доцент', 'science_degree' : 'к.ф.-м.н.',
         'official_email' : 'k.romanovsky@spbu.ru', 'still_working': True},
        {'position': 'Доцент', 'official_email': 'm.serov@spbu.ru', 'still_working': True},
        {'position': 'Преподаватель-практик', 'science_degree': 'к.ф.-м.н.',
         'official_email': 's.s.sysoev@spbu.ru', 'still_working': True},
        {'position': 'Старший преподаватель', 'official_email': 'm.baklanovsky@spbu.ru', 'still_working': True},
        {'position': 'Старший преподаватель', 'official_email': 'm.m.zhuravlev@spbu.ru', 'still_working': True},
        {'position': 'Старший преподаватель', 'official_email': 'i.zelenchuk@spbu.ru', 'still_working': True},
        {'position': 'Старший преподаватель', 'official_email': 'y.kirilenko@spbu.ru', 'still_working': True},
        {'position': 'Старший преподаватель', 'official_email': 'st035425@student.spbu.ru', 'still_working': True},
        {'position': 'Старший преподаватель', 'official_email': 'egor.k.kulikov@gmail.com', 'still_working': True},
        {'position': 'Старший преподаватель', 'official_email': 'd.mordvinov@spbu.ru', 'still_working': True},
        {'position': 'Старший преподаватель', 'official_email': 'm.nemeshev@spbu.ru', 'still_working': True},
        {'position': 'Старший преподаватель', 'official_email': 'stanislav.sartasov@spbu.ru', 'still_working': True},
        {'position': 'Старший преподаватель', 'science_degree': 'к.т.н.','official_email': 'm.n.smirnov@spbu.ru',
         'still_working': True},
        {'position': 'Старший преподаватель', 'official_email': 'st036451@student.spbu.ru', 'still_working': True},
        {'position': 'Старший преподаватель', 'official_email': 's.shilov@spbu.ru', 'still_working': True},
        {'position': 'Инженер-исследователь', 'official_email': 'st013464@student.spbu.ru', 'still_working': True},
        {'position': 'Инженер-исследователь', 'official_email': 'st013039@student.spbu.ru', 'still_working': True},
        {'position': 'Доцент', 'official_email': 's.v.grigoriev@spbu.ru', 'science_degree': 'к.ф.-м.н.', 'still_working': False},
        {'position': 'Старший преподаватель', 'official_email': 'pimenov_aa_stub@spbu.ru', 'still_working': False},
    ]
    wtypes = [
        {'type': 'Все работы'},
        {'type' : 'Курсовая работа'},
        {'type' : 'Бакалаврская ВКР'},
        {'type' : 'Магистерская ВКР'},
    ]
    courses = [
        {
            'name' : 'Математическое обеспечение и администрирование информационных систем',
            'code' : '02.03.03'
        },
        {
            'name' : 'Программная инженерия',
            'code' : '09.03.04'
        }
    ]
    tags = [
        {
            'name' : 'Компилятор'
        },
        {
            'name' : 'Android'
        },
        {
            'name' : 'F#'
        },
        {
            'name' : 'РуСи'
        }
    ]

    """
    thesis = [
        {
            'name_ru' : 'Реализация расширенного препроцессора для проекта РуСи',
            'name_en' : 'Implementing an Advanced Preprocessor for a RuC Project',
            'description' : 'Языки программирования – область, которая активно развивается на протяжении всей истории развития IT, начиная с 50-х годов прошлого века. Наряду с ультрасовременными языками, основанными на последних разработках, такими как Swift или Kotlin, продолжается и развитие традиционных языков, существующих с 80-х годов прошлого века. Это в полной мере относится к языку C, простота и эффективность которого сделала его «фактическим стандартом» для программирования встроенных систем и систем реального времени.',
            'text_uri' : 'Anikin_Egor_Georgievich_Bachelor_Thesis_2020_text.pdf',
            'presentation_uri' : 'Anikin_Egor_Georgievich_Bachelor_Thesis_2020_slides.pdf',
            'supervisor_review_uri' : 'Anikin_Egor_Georgievich_Bachelor_Thesis_2020_supervisor_review.pdf',
            'reviewer_review_uri' : 'Anikin_Egor_Georgievich_Bachelor_Thesis_2020_ reviewer_review.pdf',
            'author' : 'Аникин Егор Георгиевич',
            'supervisor_id' : 1,
            'reviewer_id' : 2,
            'publish_year' : 2020,
            'type_id' : 2,
        },
        {
            'name_ru': 'Изолированный запуск поставщиков типов для компилятора F#',
            'name_en': 'Hosting F# type providers out-of-process',
            'description': 'Современное программирование процветает на пространствах с большими данными и сложными задачами по их обработке. Можно наблюдать, что из-за распространенности многоядерных процессоров все чаще требуется писать параллельный код. Точно так же и в облач- ных системах важно уметь распределить выполнение задачи по парал- лельным потокам вычислений.',
            'text_uri': 'Berezhnykh_Aleksey_Vladimirovich_Bachelor_Thesis_2020_text.pdf',
            'presentation_uri': 'Berezhnykh_Aleksey_Vladimirovich_Bachelor_Thesis_2020_slides.pdf',
            'supervisor_review_uri': 'Berezhnykh_Aleksey_Vladimirovich_Bachelor_Thesis_2020_supervisor_review.pdf',
            'reviewer_review_uri': 'Berezhnykh_Aleksey_Vladimirovich_Bachelor_Thesis_2020_ reviewer_review.pdf',
            'source_uri': 'https://github.com/DedSec256/fsharp',
            'author': 'Бережных Алексей Владимирович',
            'supervisor_id': 3,
            'reviewer_id': 4,
            'publish_year': 2020,
            'type_id' : 3
        },
    ]
    """

    thesis = []

    # Init DB
    db.session.commit() # https://stackoverflow.com/questions/24289808/drop-all-freezes-in-flask-with-sqlalchemy
    db.drop_all()
    db.create_all()

    # Create users
    print ("Create users")
    for user in users:
        u = Users(email=user['email'], password_hash = generate_password_hash(urandom(16).hex()), first_name = user['first_name'], last_name = user['last_name'],
                  middle_name = user['middle_name'], avatar_uri = user['avatar_uri'])

        db.session.add(u)
        db.session.commit()

    # Create staff
    print("Create staff")
    for user in staff:
        u = Users.query.filter_by(email=user['official_email']).first()

        if 'science_degree' in user:
            s = Staff(position = user['position'], science_degree = user['science_degree'],
                  official_email = user['official_email'], still_working = user['still_working'],
                  user_id = u.id)
        else:
            s = Staff(position = user['position'], official_email = user['official_email'],
                      still_working = user['still_working'], user_id = u.id)

        db.session.add(s)
        db.session.commit()

    # Create WorkTypes
    print("Create worktypes")
    for w in wtypes:
        wt = Worktype(type = w['type'])
        db.session.add(wt)
        db.session.commit()

    # Create Courses
    print("Create courses")
    for course in courses:
        c = Courses(name = course['name'], code = course['code'])
        db.session.add(c)
        db.session.commit()

    for tag in tags:
        t = Tags(name=tag['name'])
        db.session.add(t)
        db.session.commit()

    # Create Thesis
    print("Create thesis")
    for work in thesis:
        if 'source_uri' in work:
            t = Thesis(name_ru = work['name_ru'], name_en=work['name_en'], description=work['description'],
                   text_uri=work['text_uri'], presentation_uri=work['presentation_uri'],
                   supervisor_review_uri=work['supervisor_review_uri'], reviewer_review_uri=work['reviewer_review_uri'],
                   author=work['author'], supervisor_id=work['supervisor_id'], reviewer_id=work['reviewer_id'],
                   publish_year=work['publish_year'], type_id=work['type_id'], course_id = 1, source_uri=work['source_uri'])
        else:
            t = Thesis(name_ru = work['name_ru'], name_en=work['name_en'], description=work['description'],
                   text_uri=work['text_uri'], presentation_uri=work['presentation_uri'],
                   supervisor_review_uri=work['supervisor_review_uri'], reviewer_review_uri=work['reviewer_review_uri'],
                   author=work['author'], supervisor_id=work['supervisor_id'], reviewer_id=work['reviewer_id'],
                   publish_year=work['publish_year'], type_id=work['type_id'], course_id = 1)

        db.session.add(t)
        db.session.commit()

        # Adds tags
        records = Tags.query.all()
        for tag in records:
            t.tags.append(tag)
            db.session.commit()

    return