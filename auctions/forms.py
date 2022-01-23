from django.forms import ModelForm
from django.forms import widgets
from django.forms.widgets import NumberInput, Select, TextInput, Textarea, URLInput
from .models import *


class CreateListing(ModelForm):
    class Meta:
        model = Listings
        exclude = ["owner", "status", "watch", "created"]
        widgets = {
            'title':TextInput(attrs={
                'class':'form-control'
            }),
            'description':Textarea(attrs={
                'class':'form-control'
            }),
            'initial_price':NumberInput(attrs={
                'class':'form-control',
                'min':'0.01'
            }),
            'photo_URL':URLInput(attrs={
                'class':'form-control'
            }),
            'category':Select(attrs={
                'class':'form-select'
            })
        }
        
class CommentForm(ModelForm):
    class Meta:
        model = Comments
        exclude = ["listing_id", "user_id", "created"]
        widgets = {"comment": Textarea(attrs={
            'class':'form-control',
            'rows':'2',
            'cols':'20',
            'placeholder':'Add Comment'
        })}

class BidForm(ModelForm):
    class Meta:
        model = Bids
        exclude = ["listing_id", "user_id"]
        widgets = {"bid": NumberInput(attrs={
            'class':'bid_input',
            'placeholder':' Enter Bid'
        })}


