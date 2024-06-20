from django import forms
from django.forms import inlineformset_factory
from .models import Post, Category, PostImage

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'video_url', 'category']

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'video_url', 'category']

PostImageFormSet = inlineformset_factory(
    Post, PostImage, fields=['image'], extra=3, can_delete=True
)

class PostSearchForm(forms.Form):
    q = forms.CharField(label='Search', required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                      required=False, empty_label="All Categories")

