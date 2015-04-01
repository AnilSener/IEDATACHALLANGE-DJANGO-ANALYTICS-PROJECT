__author__ = 'root'
from django import forms
from django.core.validators import EMPTY_VALUES
from django.utils.encoding import smart_text
import re
from mongoengine.django.auth import User

class LoginForm( forms.Form ):
    # Username is an email
    username = forms.EmailField()
    password = forms.CharField( widget=forms.PasswordInput(render_value=False),
                                max_length=20 )

class USPhoneNumberField( forms.CharField ):
    '''
    Recognizes, cleans, and validates a US phone number.
    Based on https://github.com/django/django-localflavor-us/blob/master/django_localflavor_us/forms.py
    '''
    default_error_messages = {
        'invalid' : ('Not a valid phone number. Be sure to include area code.'),
    }

    PHONE_DIGITS_RE = re.compile(r'^(?:1-?)?(\d{3})[-\.]?(\d{3})[-\.]?(\d{4})$')

    def clean( self, value ):
        super( USPhoneNumberField, self ).clean( value )
        if value in EMPTY_VALUES:
            return ''
        value = re.sub( '(\(|\)|\s+)', '', smart_text(value) )
        mat = USPhoneNumberField.PHONE_DIGITS_RE.search( value )
        if mat:
            return "{}-{}-{}".format( mat.group(1), mat.group(2), mat.group(3) )
        raise forms.ValidationError( self.error_messages['invalid'] )

class RegisterForm( forms.Form ):
    # Username is an email
    username = forms.EmailField( label="email" )
    password1 = forms.CharField( widget=forms.PasswordInput(render_value=False),
                                 max_length=20,
                                 label="password",
                                 required=True )
    password2 = forms.CharField( widget=forms.PasswordInput(render_value=False),
                                 max_length=20,
                                 label="password (again)",
                                 required=True )
    first_name = forms.CharField( label="first name" )
    last_name = forms.CharField( label="last name" )
    phone = USPhoneNumberField()

    def clean( self ):
        cleaned_data = super( RegisterForm, self ).clean()

        pw1 = cleaned_data.get('password1')
        pw2 = cleaned_data.get('password2')
        usr = cleaned_data.get('username')

        # Passwords must match
        if pw1 and pw2:
            if cleaned_data['password1'] != cleaned_data['password2']:
                raise forms.ValidationError("Passwords must match.")
        # Unique usernames
        if usr:
            if User.objects( username=usr ).count() > 0:
                raise forms.ValidationError("That username is already taken.")
        return cleaned_data




from datetimewidget.widgets import DateTimeWidget,DateWidget,TimeWidget
class testFormBootstrap3(forms.Form):
    dateTimeOptions = {'format': 'dd-mm-yyyy HH:ii P','autoclose': True,'showMeridian' : True,'minView':1,'startView':3,'todayHighlight': True,'clearBtn':False}
    date_time = forms.DateTimeField(widget=DateTimeWidget(usel10n=True, bootstrap_version=3,options = dateTimeOptions))
    #date = forms.DateField(widget=DateWidget(usel10n=True, bootstrap_version=3))
    #time = forms.TimeField(widget=TimeWidget(usel10n=True, bootstrap_version=3))
