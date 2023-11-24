from django.db import models
from django_jalali.db import models as jmodels
from django.contrib.auth.models import AbstractUser
from .validators import limit_file_size
from .utils import generate_new_verify_code



class User(AbstractUser):
    GENDER_CHOICES = [
        ('m', 'آقا'),
        ('f', 'خانم'),
        ('o', 'سایر'),
    ]

    date_joined = jmodels.jDateTimeField(auto_now=True, null=True, verbose_name='زمان عضویت')
    last_update = jmodels.jDateTimeField(auto_now=True, null=True, verbose_name='آخرین بروزرسانی')
    last_login = jmodels.jDateTimeField(null=True, blank=True, verbose_name='آخرین ورود')

    valid_phone = models.BooleanField(default=False, verbose_name="تایید تلفن همره")
    valid_email = models.BooleanField(default=False, verbose_name="تایید ایمیل")

    is_manager = models.BooleanField(default=False, verbose_name='مدیر ارشد', help_text='دسترسی کامل دارد')
    created_by = models.ForeignKey('User', null=True, blank=True, on_delete=models.SET_NULL,
                                    verbose_name='ایجاد کننده')
    
    phone = models.CharField(max_length=11, unique=True, null=True, blank=True, verbose_name='موبایل',
                              help_text='شماره تلفن با صفر وارد شود')
    email = models.EmailField(verbose_name='پست الکترونیکی', unique=True, null=True)
    birth_date = jmodels.jDateField(verbose_name='تاریخ تولد', null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='m', verbose_name='جنسیت')
    avatar = models.ImageField(null=True, blank=True, upload_to='accounts/avatars',
                                validators= limit_file_size, verbose_name='عکس پروفایل')
    

    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name_plural = 'کاربران'
        verbose_name = 'کاربر'

    def get_date_joined(self):
        return self.date_joined.strftime("%H:%M - %Y/%m/%d")
    get_date_joined.short_description = 'تاریخ عضویت'
    
    def get_date_joined___date_only(self):
         return self.date_joined.strftime("%Y/%m/%d")
    
    def get_last_update(self):
        return self.last_update.strftime("%H:%M - %Y/%m/%d")
    get_last_update.short_description = 'آخرین بروزرسانی'

    def get_last_login(self):
        if self.last_login:
            return self.last_login.strftime("%H:%M - %Y/%m/%d")
        return "تاکنون وارد سایت نشده است."
    get_last_login.short_description = 'آخرین ورود'

    def get_gender(self):
        if self.gender == 'm':
            return 'آقای'
        elif self.gender == 'f':
            return 'خانم'
        else:
            return 'سایر'
        
    def __str__(self):
        if self.get_full_name():
            return self.get_full_name()
        return self.username
    
    def profile_check(self):
        if self.first_name and self.last_name and self.email and self.gender and self.phone:
            return True
        return False
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__previous_phone = self.phone
        self.__previous_email = self.email

    def save(self, *args, **kwargs):   
        if self.__previous_phone != self.phone:
            self.valid_phone = False
        if self.__previous_email != self.email:
            self.valid_email = False
            
        super().save(*args, **kwargs)
 
    

class VerifyCode(models.Model):
    SUBJECT_CHOICES = [
        ("phone", "تلفن همراه"),
        ("email", "ایمیل"),
        ("login", "ورود به سایت"),
    ]

    STATUS_CHOICES =[
        (0, "نامعتبر"),
        (1, "معتبر"),
        (2, "اعمال شده"),
    ]

    subject = models.CharField(max_length=20, choices=SUBJECT_CHOICES, verbose_name="نوع کد تایید")
    code = models.CharField(max_length=10, blank=True, editable=False, unique=True,
           default=generate_new_verify_code, verbose_name="کد تایید")
    status = models.PositiveSmallIntegerField(default=1, choices=STATUS_CHOICES, verbose_name="وضعیت کد")
    attempts =  models.PositiveSmallIntegerField(default=0, verbose_name="تعداد تلاش")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")

    class Meta:
        verbose_name = 'کد تایید'
        verbose_name_plural = 'کدهای تایید'
    
    def __str__(self):
        return f"{self.subject} - {self.code}"
    
    @property
    def get_status(self):
        return dict(self.STATUS_CHOICES)[self.status]
    
    @property
    def get_subject(self):
        return dict(self.SUBJECT_CHOICES)[self.subject]
