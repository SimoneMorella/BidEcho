from django import forms
from .models import Listing, Bidding, Comment

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        exclude = ['owner', 'in_watchlist', 'active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

         # Exclude the 'owner' and 'in_watchlist' fields
        excluded_fields = ['owner', 'in_watchlist', 'active']

        # Add different classes and custom placeholders to each remaining input field
        placeholder_mapping = {
            'title': 'Enter the title',
            'description': 'Enter the description. Max 300 character.',
            'current_bid': 'Enter the current bid',
            'category': 'Select the category',
            'url_image': 'Enter the image URL',
        }

        for field_name, field in self.fields.items():
            if field_name not in excluded_fields:
                field.widget.attrs['class'] = f'custom-class-{field_name}'  # Replace 'custom-class-' as needed
                field.widget.attrs['placeholder'] = placeholder_mapping.get(field_name, '')  # Use custom placeholder text
                # field.label = ''  # Set the label to an empty string

    def save(self, commit=True, user=None):
        # Set the owner field based on the logged-in user
        instance = super().save(commit=False)
        instance.owner = user

        if commit:
            instance.save()

        return instance


class BiddingForm(forms.ModelForm):
    class Meta:
        model = Bidding
        fields = ["offer"]
        widgets = {
            'offer': forms.NumberInput(attrs={'class': 'bidInput'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        widgets = {
            'text': forms.Textarea(attrs={'class': 'comment', 'placeholder':'Insert your comment...'}),
        }
        labels = {
            'text': '',
        }