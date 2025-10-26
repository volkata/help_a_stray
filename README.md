# (pass main_district to create admin:)
from accounts.models import CustomUser
from district.models import District
superuser = CustomUser.objects.create_superuser(
    username='admin',
    password='supersecurepassword',
    main_district=District.objects.first()
)

# (to test give yourself both groups Vet and district admin)


# (signal to create profile with user, custom delete to delete user with profile)


# (3-step cat sighting process, first step only select color, district and gender, second step (template only) filter cats by district, gender, color with option to update or add new, 3rd step add new or update existing)


# (new cats to be verified by district admin group)


# (cat health notes treatment cost to be added by vet admin group)


# (adopt cat view accessible on 100 profile karma)


# (populate districts:)
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

# (populate colors:)
from cat.models import Color
from cat.choices import CAT_COLOR_CHOICES
for code, name in CAT_COLOR_CHOICES:
     Color.objects.get_or_create(code=code, defaults={'name': name})