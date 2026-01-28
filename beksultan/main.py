import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from house_app.models import City, District, Property, PropertyImage, PropertyDocument, Review
from django.contrib.auth.hashers import make_password
from decimal import Decimal
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Заполняет БД тестовыми данными'

    def handle(self, *args, **kwargs):
        self.stdout.write('Начинаем заполнение базы данных...')

        # Очистка старых данных
        Review.objects.all().delete()
        PropertyDocument.objects.all().delete()
        PropertyImage.objects.all().delete()
        Property.objects.all().delete()
        District.objects.all().delete()
        City.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

        # Создаем пользователей
        users = self.create_users()

        # Создаем города и районы
        cities_with_districts = self.create_cities_and_districts()

        # Создаем объявления
        properties = self.create_properties(users, cities_with_districts)

        # Создаем отзывы
        self.create_reviews(users, properties)

        self.stdout.write(self.style.SUCCESS('База данных успешно заполнена!'))

    def create_users(self):
        self.stdout.write('Создаем пользователей...')
        users_data = [
            {
                'username': 'admin_user',
                'user_name': 'Администратор',
                'first_name': 'Азамат',
                'last_name': 'Бекмуратов',
                'email': 'admin@house.kg',
                'phone_number': '+996555123456',
                'telegram': '@azamat_admin',
                'role': 'admin'
            },
            {
                'username': 'seller_nurlan',
                'user_name': 'Нурлан',
                'first_name': 'Нурлан',
                'last_name': 'Сулайманов',
                'email': 'nurlan@mail.kg',
                'phone_number': '+996700234567',
                'telegram': '@nurlan_realty',
                'role': 'seller'
            },
            {
                'username': 'seller_aichurok',
                'user_name': 'Айчурок',
                'first_name': 'Айчурок',
                'last_name': 'Токтогулова',
                'email': 'aichurok@mail.kg',
                'phone_number': '+996770345678',
                'telegram': '@aichurok_kg',
                'role': 'seller'
            },
            {
                'username': 'seller_erkin',
                'user_name': 'Эркин',
                'first_name': 'Эркин',
                'last_name': 'Асанов',
                'email': 'erkin@mail.kg',
                'phone_number': '+996550456789',
                'telegram': '@erkin_estate',
                'role': 'seller'
            },
            {
                'username': 'buyer_meerim',
                'user_name': 'Мээрим',
                'first_name': 'Мээрим',
                'last_name': 'Жумабаева',
                'email': 'meerim@mail.kg',
                'phone_number': '+996777567890',
                'telegram': '@meerim_j',
                'role': 'beyer'
            },
            {
                'username': 'buyer_bektur',
                'user_name': 'Бектур',
                'first_name': 'Бектур',
                'last_name': 'Кадыров',
                'email': 'bektur@mail.kg',
                'phone_number': '+996555678901',
                'telegram': '@bektur_kadirov',
                'role': 'beyer'
            }
        ]

        users = []
        for data in users_data:
            user_data = {
                'username': data['username'],
                'user_name': data['user_name'],
                'first_name': data['first_name'],
                'last_name': data['last_name'],
                'email': data['email'],
                'phone_number': data['phone_number'],
                'role': data['role'],
                'password': make_password('password123')
            }

            # Добавляем telegram если поле есть в модели
            if hasattr(User, 'telegram'):
                user_data['telegram'] = data.get('telegram')

            user = User.objects.create(**user_data)
            users.append(user)
            self.stdout.write(f'  Создан: {user.username} ({data.get("telegram", "нет тг")})')

        return users

    def create_cities_and_districts(self):
        self.stdout.write('Создаем города и районы...')
        cities_data = [
            {
                'city_name': 'Бишкек',
                'districts': ['Ленинский', 'Свердловский', 'Октябрьский', 'Первомайский']
            },
            {
                'city_name': 'Ош',
                'districts': ['Центр', 'Новый город', 'Аэропорт', 'Кызыл-Кыя']
            },
            {
                'city_name': 'Джалал-Абад',
                'districts': ['Центр', 'Новостройка', 'Аэропорт']
            },
            {
                'city_name': 'Каракол',
                'districts': ['Центр', 'Микрорайон', 'Курорт']
            },
            {
                'city_name': 'Токмок',
                'districts': ['Центр', 'Новый район']
            }
        ]

        cities_with_districts = []
        for city_data in cities_data:
            city = City.objects.create(city_name=city_data['city_name'])
            districts = []
            for district_name in city_data['districts']:
                district = District.objects.create(city=city, name=district_name)
                districts.append(district)
            cities_with_districts.append({'city': city, 'districts': districts})
            self.stdout.write(f'  Создан город: {city.city_name} с {len(districts)} районами')

        return cities_with_districts

    def create_properties(self, users, cities_with_districts):
        self.stdout.write('Создаем объявления недвижимости...')
        sellers = [u for u in users if u.role == 'seller']

        properties_data = [
            {
                'title': '3-комнатная квартира в центре Бишкека',
                'title_en': '3-room apartment in the center of Bishkek',
                'description': 'Продается отличная 3-комнатная квартира в Ленинском районе. Квартира после евроремонта, встроенная мебель, техника. Развитая инфраструктура, рядом школы, детские сады, торговые центры.',
                'description_en': 'Excellent 3-room apartment for sale in Leninsky district. The apartment has been renovated, built-in furniture, appliances. Developed infrastructure, near schools, kindergartens, shopping centers.',
                'property_type': 'apartment',
                'region': 'Чуйская область',
                'rooms': 3,
                'floor': 5,
                'total_floors': 9,
                'area': 85.5,
                'price': Decimal('95000.00'),
                'condition': 'new',
                'city_index': 0,
                'district_index': 0
            },
            {
                'title': 'Частный дом с участком в Токмоке',
                'title_en': 'Private house with land in Tokmok',
                'description': 'Продается добротный кирпичный дом в городе Токмок. 4 комнаты, все удобства, газовое отопление. Земельный участок 8 соток, плодовый сад, гараж.',
                'description_en': 'Solid brick house for sale in Tokmok. 4 rooms, all amenities, gas heating. Land plot 8 acres, fruit garden, garage.',
                'property_type': 'house',
                'region': 'Чуйская область',
                'rooms': 4,
                'floor': 1,
                'total_floors': 1,
                'area': 120.0,
                'price': Decimal('75000.00'),
                'condition': 'good',
                'city_index': 4,
                'district_index': 0
            },
            {
                'title': '2-комнатная квартира в новостройке Ош',
                'title_en': '2-room apartment in new building Osh',
                'description': 'Квартира в новом доме в районе Нового города. Сдача дома в этом году. Свободная планировка, можно сделать ремонт под себя. Панорамные окна, высокие потолки.',
                'description_en': 'Apartment in a new house in New City district. House delivery this year. Free layout, you can do repairs for yourself. Panoramic windows, high ceilings.',
                'property_type': 'apartment',
                'region': 'Ошская область',
                'rooms': 2,
                'floor': 12,
                'total_floors': 16,
                'area': 68.0,
                'price': Decimal('52000.00'),
                'condition': 'new',
                'city_index': 1,
                'district_index': 1
            },
            {
                'title': 'Коммерческое помещение в центре Джалал-Абада',
                'title_en': 'Commercial premises in the center of Jalal-Abad',
                'description': 'Продается готовый бизнес - магазин продуктов в проходном месте. Площадь 45 кв.м, есть склад. Стабильная клиентская база, хорошая проходимость.',
                'description_en': 'Ready business for sale - grocery store in a busy location. Area 45 sq.m, there is a warehouse. Stable customer base, good traffic.',
                'property_type': 'commercial',
                'region': 'Джалал-Абадская область',
                'rooms': 1,
                'floor': 1,
                'total_floors': 2,
                'area': 45.0,
                'price': Decimal('38000.00'),
                'condition': 'good',
                'city_index': 2,
                'district_index': 0
            },
            {
                'title': 'Земельный участок в Караколе',
                'title_en': 'Land plot in Karakol',
                'description': 'Продается земельный участок 10 соток в курортной зоне Каракола. Ровный участок, все коммуникации рядом. Идеально под строительство гостевого дома или дачи.',
                'description_en': 'Land plot of 10 acres for sale in the resort area of Karakol. Flat plot, all communications nearby. Ideal for building a guest house or cottage.',
                'property_type': 'land',
                'region': 'Иссык-Кульская область',
                'rooms': 0,
                'floor': 0,
                'total_floors': 0,
                'area': 1000.0,
                'price': Decimal('28000.00'),
                'condition': 'new',
                'city_index': 3,
                'district_index': 2
            },
            {
                'title': 'Студия в Бишкеке, Асанбай',
                'title_en': 'Studio in Bishkek, Asanbay',
                'description': 'Уютная квартира-студия в микрорайоне Асанбай. Свежий ремонт, вся мебель и техника остается. Идеально для молодой семьи или под сдачу.',
                'description_en': 'Cozy studio apartment in Asanbay microdistrict. Fresh renovation, all furniture and appliances remain. Ideal for a young family or for rent.',
                'property_type': 'apartment',
                'region': 'Чуйская область',
                'rooms': 1,
                'floor': 3,
                'total_floors': 5,
                'area': 32.0,
                'price': Decimal('35000.00'),
                'condition': 'new',
                'city_index': 0,
                'district_index': 2
            }
        ]

        properties = []
        for i, data in enumerate(properties_data):
            city_district = cities_with_districts[data['city_index']]
            city = city_district['city']
            district = city_district['districts'][data['district_index']]
            seller = sellers[i % len(sellers)]

            property_obj = Property.objects.create(
                title=data['title'],
                title_en=data['title_en'],
                description=data['description'],
                description_en=data['description_en'],
                property_type=data['property_type'],
                region=data['region'],
                city=city,
                district=district,
                address=f'ул. Примерная, {random.randint(1, 150)}',
                area=data['area'],
                price=data['price'],
                rooms=data['rooms'],
                floor=data['floor'],
                total_floors=data['total_floors'],
                condition=data['condition'],
                seller=seller
            )
            properties.append(property_obj)
            self.stdout.write(f'  Создано: {property_obj.title}')

        return properties

    def create_reviews(self, users, properties):
        self.stdout.write('Создаем отзывы...')
        buyers = [u for u in users if u.role == 'beyer']

        reviews_data = [
            {'rating': 5, 'comment': 'Отличный продавец, все показал, ответил на все вопросы. Рекомендую!',
             'comment_en': 'Excellent seller, showed everything, answered all questions. Recommend!'},
            {'rating': 4, 'comment': 'Хорошая квартира, соответствует описанию. Небольшой торг возможен.',
             'comment_en': 'Good apartment, matches description. Small bargaining possible.'},
            {'rating': 5, 'comment': 'Очень довольны покупкой! Продавец честный, все документы в порядке.',
             'comment_en': 'Very satisfied with the purchase! Honest seller, all documents in order.'},
            {'rating': 3, 'comment': 'Дом хороший, но цена завышена. Долго торговались.',
             'comment_en': 'The house is good, but the price is too high. Long bargaining.'},
            {'rating': 5, 'comment': 'Профессиональный подход, быстро оформили все документы. Спасибо!',
             'comment_en': 'Professional approach, quickly processed all documents. Thanks!'},
            {'rating': 4, 'comment': 'Неплохой вариант за свою цену. Продавец идет на контакт.',
             'comment_en': 'Good option for the price. Seller is responsive.'}
        ]

        for i, review_data in enumerate(reviews_data):
            property_obj = properties[i % len(properties)]
            buyer = buyers[i % len(buyers)]

            Review.objects.create(
                author=buyer,
                seller=property_obj.seller,
                rating=review_data['rating'],
                comment=review_data['comment'],
                comment_en=review_data['comment_en']
            )
            self.stdout.write(f'  Создан отзыв от {buyer.username} для {property_obj.seller.username}')


# Запуск скрипта
if __name__ == '__main__':
    command = Command()
    command.handle()