from django import forms
from .models import User, Patient, UserAddress


class RegistrationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required fields, plus a repeated password.
    Attributes:
        password1 (CharField): User Password
        password2 (CharField): Password Confirmation
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', )

    def clean(self):
        """Checks if the variables are valid.
        """
        # run the standard clean method first
        cleaned_data = super(RegistrationForm, self).clean()
        username = cleaned_data.get("username").lower()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        # check if the username exists already
        if User.objects.filter(username=username).count():
            self.add_error('username', 'This username is taken.')
        # check if passwords are entered and match
        if password1 and password2 and password1 != password2:
            msg = "Passwords do not match!"
            self.add_error('password1', msg)
            self.add_error('password2', msg)
        # always return the cleaned data
        return cleaned_data

    def save(self, commit=True):
        """Changes username and email to lowercase for case insensitivity. Saves User entry to DB.
        Args:
            commit (bool, optional): If false, will just save model to memory.
        Returns:
            User: created user
        """
        user = super(RegistrationForm, self).save(commit=False)
        # Save the provided password in hashed format
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class PatientForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, 2017)))

    class Meta:
        model = Patient
        fields = ('date_of_birth', 'gender', 'weight', 'phone_number')
        help_texts = {'phone_number': "10 digit number, no dashes or parenthesis"}

    def save(self, user, commit=True):
        patient = super(PatientForm, self).save(commit=False)
        patient.user = user
        if commit:
            patient.save()
        return patient


class UserAddressForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        fields = ('address1', 'address2', 'city', 'state', 'zipcode')

    def save(self, user, commit=True):
        address = super(UserAddressForm, self).save(commit=False)
        address.user = user
        if commit:
            address.save()
        return address
