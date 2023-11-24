from django.core.exceptions import ValidationError


def limit_file_size(value):
    if value.size > 2097152:
        raise ValidationError("حجم عکس بیشتر از 2 مگابایت نمیتواند باشد.")
    if value.height / value.width != 1:
        raise ValidationError("ابعاد عکس باید 1x1 (مربعی) باشد.")