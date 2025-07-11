from django.contrib.auth.models import User
from django.db import models
from datetime import date

class Post(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    content = models.TextField(verbose_name='post content', null=False)
    total_likes = models.IntegerField(verbose_name='likes count', default=0)
    image = models.ImageField(upload_to='posts_img/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-created_at']

class Comment(models.Model):
    text = models.TextField(null=False, blank=False, verbose_name='comment text')
    post = models.ForeignKey('Post', on_delete=models.CASCADE, verbose_name='comment')
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.author} - {self.text}'

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['-created_at']


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(blank=True, null=True, upload_to='profile_pic/')

    def __str__(self):
        return f'{self.user}'


    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'



class UserInformation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=150, null=True, blank=True, verbose_name="name")
    last_name = models.CharField(max_length=150, null=True, blank=True, verbose_name="surname")
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="date of birth")
    about_user = models.TextField(null=True, blank=True, verbose_name="about user")
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name="phone")
    inst = models.CharField(max_length=255, null=True, blank=True, verbose_name="Instagram link")
    hobbies = models.TextField(null=True, blank=True, verbose_name="hobbies")
    web_site = models.URLField(max_length=255, null=True, blank=True, verbose_name="web-site")
    geo = models.CharField(max_length=100, null=True, blank=True, verbose_name="geoposition")


    @property
    def years(self):
        today = date.today()
        user_age = date.today().year - self.date_of_birth.year
        if (today.month < self.date_of_birth.month) or (today.month == self.date_of_birth.month and today.day < self.date_of_birth.day ):
            user_age -= 1
        return user_age
git 
    PROFESSION_CHOICES = [
        ('F1', 'Formula 1 pilot'),
        ('LOG', 'Логист'),
        ('IT_DEV', 'Разработчик ПО'),
        ('IT_QA', 'Инженер по тестированию (QA)'),
        ('IT_PM', 'Менеджер проектов (IT)'),
        ('IT_DS', 'Специалист по данным (Data Scientist)'),
        ('IT_UXUI', 'UX/UI Дизайнер'),
        ('IT_ADM', 'Системный администратор'),
        ('EDU_TCHR', 'Учитель/Преподаватель'),
        ('EDU_LEC', 'Лектор ВУЗа'),
        ('MED_DOC', 'Врач'),
        ('MED_NUR', 'Медсестра/Медбрат'),
        ('ENG_CIV', 'Инженер-строитель'),
        ('ENG_MECH', 'Инженер-механик'),
        ('ENG_ELEC', 'Инженер-электрик'),
        ('FIN_ACC', 'Бухгалтер'),
        ('FIN_ANL', 'Финансовый аналитик'),
        ('MKT_MNG', 'Маркетолог'),
        ('SAL_MNG', 'Менеджер по продажам'),
        ('ART_DES', 'Дизайнер (графический/промышленный)'),
        ('ART_PHO', 'Фотограф'),
        ('JUR_LAW', 'Юрист/Адвокат'),
        ('SCI_RES', 'Научный сотрудник'),
        ('SVC_CUS', 'Специалист по обслуживанию клиентов'),
        ('CON_AGR', 'Консультант по агрономии'),
        ('TRA_DRV', 'Водитель/Курьер'),
        ('TRA_PIL', 'Пилот'),
        ('ADM_SEC', 'Секретарь/Ассистент'),
        ('OTH_GEN', 'Другое'),
    ]
    profession = models.CharField(
        max_length=10,
        choices=PROFESSION_CHOICES,
        null=True,
        blank=True,
        verbose_name="profession"
    )

    class Meta:
        verbose_name = "User information"
        verbose_name_plural = "Users information"

    def __str__(self):
        return f"Profile {self.user.username}"




# Create your models here.
