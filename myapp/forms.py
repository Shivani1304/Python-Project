from django import forms
from myapp.models import Order, Review, Member
from django.contrib.auth.forms import UserCreationForm

class SearchForm(forms.Form):
    CATEGORY_CHOICES = [
        ('S', 'Scinece&Tech'),
        ('F', 'Fiction'),
        ('B', 'Biography'),
        ('T', 'Travel'),
        ('O', 'Other')
    ]
    your_name = forms.CharField(max_length=100, required=False)
    select_a_category = forms.ChoiceField(widget=forms.RadioSelect,choices = CATEGORY_CHOICES,required=False)
    maximum_price = forms.IntegerField(min_value=0)

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['books', 'member', 'order_type']
        widgets = {'books': forms.CheckboxSelectMultiple(), 'order_type': forms.RadioSelect}
        labels = {'member': u'Member name', }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['reviewer', 'book', 'rating', 'comments' ]
        widgets = {'book': forms.RadioSelect, }
        labels = {'reviewer': u'Please enter a valid email','rating': u'An integer between 1 (worst) and 5 (best)',}

class MemberForm(UserCreationForm):

    username = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(max_length=200, required=True)

    class Meta:
        model= Member
        fields= ['username', 'first_name','last_name', 'email','password1','password2','status','address','city','province','borrowed_books']
        widgets = {'status':forms.RadioSelect,}
        labels = {'status':u'Please select your status',}