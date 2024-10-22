from django.core.management.base import BaseCommand
from search.models import Restaurant, Dish

class Command(BaseCommand):
    help = 'Seed the database with dishes for the restaurant'

    def handle(self, *args, **kwargs):
        # Create the restaurant
        restaurant, created = Restaurant.objects.get_or_create(
            name="Rumah Makan Padang Malah Dicubo"
        )

        # List of dishes to seed
        dishes = [
            {
                'name': 'Nasi Gulai Babat',
                'description': 'Nasi Campur Sayur Dan Sambel + gulai babat',
                'price': 35000,
                'image_url': 'https://i.gojekapi.com/darkroom/gofood-indonesia/v2/images/uploads/36831120-ad5e-41a2-adfc-02325e2d0bfc_Go-Biz_20210308_100624.jpeg?auto=format',
            },
            {
                'name': 'Nasi Rendang',
                'description': 'Campur sayur dan sambel + rendang',
                'price': 35000,
                'image_url': 'https://i.gojekapi.com/darkroom/gofood-indonesia/v2/images/uploads/b9ce84b8-af70-491b-b74b-bf3ab10457f3_08951a15-84c4-46cc-a371-3264829cfe8b_Go-Biz_20200314_114713.jpeg?auto=format',
            },
            {
                'name': 'Nasi Gulai Ikan Gurame',
                'description': 'nasi campur sayur dan sambel + gulai gurame',
                'price': 37000,
                'image_url': 'https://i.gojekapi.com/darkroom/gofood-indonesia/v2/images/uploads/a9aab981-ef67-4684-af67-8aab9358a4aa_Go-Biz_20200611_135004.jpeg?auto=format',
            },
            {
                'name': 'Nasi Ikan Kembung',
                'description': 'nasi campur sayur dan sambel + ikan kembung',
                'price': 33000,
                'image_url': 'https://i.gojekapi.com/darkroom/gofood-indonesia/v2/images/uploads/08230e99-4949-4802-9a4d-4db294e2aad8_a5a5dad1-875e-431c-aa04-a02069dc027d_Go-Biz_20200316_115408.jpeg?auto=format',
            },
            {
                'name': 'Nasi Ikan Salais',
                'description': 'nasi campur sayur dan sambel + ikan salais',
                'price': 42500,
                'image_url': 'https://i.gojekapi.com/darkroom/gofood-indonesia/v2/images/uploads/2c0a4d03-9022-4a24-99eb-16d0acc1e26a_Go-Biz_20200611_115923.jpeg?auto=format',
            },
            {
                'name': 'Nasi Ayam Ijo',
                'description': 'nasi campur sayur dan sambel + ayam ijo',
                'price': 33000,
                'image_url': 'https://i.gojekapi.com/darkroom/gofood-indonesia/v2/images/uploads/fb61a78a-2742-4eed-a535-f8189f0f4849_82517bc3-1f28-48bb-a977-3a8e1868d72d_Go-Biz_20200314_115427.jpeg?auto=format',
            },
            {
                'name': 'Nasi Ayam Pop',
                'description': 'nasi campur sayur dan sambel + ayam pop',
                'price': 33000,
                'image_url': 'https://i.gojekapi.com/darkroom/gofood-indonesia/v2/images/uploads/28b3da0c-91a8-413c-9a3f-9f10bb93be8b_Go-Biz_20200611_113857.jpeg?auto=format',
            },
            {
                'name': 'Nasi Ayam Goreng',
                'description': 'nasi campur sayur dan sambel + ayam goreng',
                'price': 33000,
                'image_url': 'https://i.gojekapi.com/darkroom/gofood-indonesia/v2/images/uploads/1aecef4f-a2f9-429e-84fb-768fb01fb351_Go-Biz_20200723_143628.jpeg?auto=format',
            },
            {
                'name': 'Nasi Udang',
                'description': 'nasi campur sayur dan sambel + udang',
                'price': 38500,
                'image_url': 'https://i.gojekapi.com/darkroom/gofood-indonesia/v2/images/uploads/cbdc8c49-2350-4771-88b3-d01b345e1ace_df320987-c7f5-48d6-bae9-6a9a90dd39b2_Go-Biz_20200316_120251.jpeg?auto=format',
            },
            {
                'name': 'Nasi Kikil',
                'description': 'nasi campur sayur dan sambel + kikil',
                'price': 41000,
                'image_url': 'https://i.gojekapi.com/darkroom/gofood-indonesia/v2/images/uploads/3e647df7-5434-4ebd-a883-0c6ac3cb798d_5adf2614-b9df-47e0-96f6-84c5ffc87ea4_Go-Biz_20200316_121203.jpeg?auto=format',
            },
            {
                'name': 'Brownies Panggang',
                'description': 'Brownies panggang coklat dengan topping almond. masa ketahanan 7 hari.',
                'price': 92000,
                'image_url': 'https://i.gojekapi.com/darkroom/gofood-indonesia/v2/images/uploads/2d91da1c-694a-4fb4-ac39-7b118c0fc686_Go-Biz_20240309_103909.jpeg?auto=format',
            },
            {
                'name': 'Pisang Bolen Coklat Keju',
                'description': 'pisang, cokelat, dan keju, masa ketahanan 4 hari',
                'price': 67500,
                'image_url': 'https://i.gojekapi.com/darkroom/gofood-indonesia/v2/images/uploads/066108d7-6422-4b6f-a75e-4775663406a1_Go-Biz_20240309_102139.jpeg?auto=format',
            },
            {
                'name': 'Banana Roll Pandan',
                'description': 'Pisang gulung yang dibalut oleh bolu pandan dengan perpaduan coklat disetiap sisinya masa ketahanan 4 hari',
                'price': 52500,
                'image_url': 'https://i.gojekapi.com/darkroom/gofood-indonesia/v2/images/uploads/91dca013-ea26-46a7-b638-ae3ca7e5e2ad_Go-Biz_20240309_112442.jpeg?auto=format',
            },
            {
                'name': 'Cheese Roll',
                'description': 'Puff pastry dengan isi keju batang, masa ketahanan 4 hari.',
                'price': 67500,
                'image_url': 'https://i.gojekapi.com/darkroom/gofood-indonesia/v2/images/uploads/e92cf404-4d3d-4dba-8244-592b5dd45eb7_Go-Biz_20240309_111002.jpeg?auto=format',
            },
            {
                'name': 'Banana Crispy',
                'description': 'Puff pastry pisang dengan perpaduan coklat, fla, keju dan susu masa ketahanan 3 hari',
                'price': 65000,
                'image_url': 'https://i.gojekapi.com/darkroom/gofood-indonesia/v2/images/uploads/1a31e440-4a39-4aba-a18e-660e4723c8e3_Go-Biz_20240309_111203.jpeg?auto=format',
            },
            {
                'name': 'Brownies Gulung',
                'description': 'Brownies kukus gulung coklat isi selai. masa ketahanan 4 hari',
                'price': 47500,
                'image_url': 'https://i.gojekapi.com/darkroom/gofood-indonesia/v2/images/uploads/08948ad3-a91a-498f-9a26-58fba4448b07_Go-Biz_20240309_104806.jpeg?auto=format',
            },
            {
                'name': 'Brownies Kukus',
                'description': 'Brownies kukus. masa ketahanan 4 hari',
                'price': 70000,
                'image_url': 'https://i.gojekapi.com/darkroom/gofood-indonesia/v2/images/uploads/5159df13-2317-4ae7-ad61-6e05f253907b_Go-Biz_20240309_105208.jpeg?auto=format',
            },
            {
                'name': 'Cheese Stick',
                'description': 'Puff pastry keju dengan taburan keju masa ketahanan 4 hari',
                'price': 67500,
                'image_url': 'https://i.gojekapi.com/darkroom/gofood-indonesia/v2/images/uploads/4aa78f76-46ea-46c7-bccb-1e9652faaf48_Go-Biz_20240309_110748.jpeg?auto=format',
            },
            {
                'name': 'Choco Pastry',
                'description': 'Puff pastry dengan isi coklat batang masa ketahanan 4 hari',
                'price': 55000,
                'image_url': 'https://i.gojekapi.com/darkroom/gofood-indonesia/v2/images/uploads/a007ff1c-074e-4c31-b1bb-eae27662481b_menu-item-image_1635135248806.jpg?auto=format',
            },
            {
                'name': 'Picnic Roll Beef',
                'description': 'Puff pastry dengan perpaduan daging sapi, keju, dan telur masa ketahanan 2 hari',
                'price': 75000,
                'image_url': 'https://i.gojekapi.com/darkroom/gofood-indonesia/v2/images/uploads/fd37ed2e-e5ff-48a8-b803-c13a32c95525_Go-Biz_20240309_111252.jpeg?auto=format',
            },
        ]

        # Seed each dish into the database
        for dish_data in dishes:
            Dish.objects.get_or_create(
                restaurant=restaurant,
                name=dish_data['name'],
                defaults={
                    'description': dish_data['description'],
                    'price': dish_data['price'],
                    'image_url': dish_data['image_url']
                }
            )

        self.stdout.write(self.style.SUCCESS('Successfully seeded restaurant and dishes!'))
