populate districts:
from district.models import District
District.objects.bulk_create([
    District(name='Bankya'),
    District(name='Vitosha'),
    District(name='Izgrev'),
    District(name='Krasna polyana'),
    District(name='Slatina'),
    District(name='Poduene'),
    District(name='Nadejda'),
    District(name='Oborishte'),
    District(name='Ovcha Kupel'),
    District(name='Studentski grad'),
    District(name='Poduene'),
    District(name='Sredec'),
    District(name='Vrabnica'),
    District(name='Mladost'),
    District(name='Liulin'),
    District(name='Lozenec'),
    District(name='Drujba'),
    ])

populate colors:
from cat.models import Color
from cat.choices import CAT_COLOR_CHOICES
for code, name in CAT_COLOR_CHOICES:
     Color.objects.get_or_create(code=code, defaults={'name': name})