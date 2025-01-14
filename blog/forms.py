from django import forms
from .models import (
    Post,
    Comment,
    Category,
)


class PostForm(forms.ModelForm):

    status = forms.ChoiceField(choices=Post.OPTIONS)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='Select')

    class Meta:
        model = Post
        fields = (
            'title',
            'content',
            'image',
            'category',
            'status',
            # 'author', # view'de otomatik ekleyeceğiz.
        )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',) # tupple olduğu için ,'ü unutma!