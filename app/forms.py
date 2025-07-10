from django import forms


class UserUpdateProfileForm(forms.Form):
    username = forms.CharField(label='You name', max_length=120)
    email = forms.EmailField(label='You email address',)
    profile_image = forms.ImageField(label='Profile image', required=False)


class PostCreateForm(forms.Form):
    title = forms.CharField(label='Title of the post', max_length=120)
    text = forms.CharField(label='Post content')
    image = forms.ImageField(required=False)




class UserInformationForm(forms.Form):
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
    phone = forms.CharField(required=False)
    inst = forms.CharField(required=False, label='Instagram link')
    hobbies = forms.CharField(required=False)
    web_site = forms.CharField(required=False)
    geo = forms.CharField(required=False, label='Location')
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    date_of_birth = forms.DateField(required=False,
                                    widget=forms.DateInput(attrs={'type': 'date', 'class': 'datepicker'}))
    profession = forms.ChoiceField(required=False, choices=PROFESSION_CHOICES)
    about_user = forms.CharField(required=False, label='About you')

class CommentCreateForm(forms.Form):
    text = forms.CharField(required=True)