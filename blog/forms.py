from django import forms

from blog.models import Article, Comment

class AddArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('header', 'content')

class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content', )
    
    def __init__(self, *args, **kwargs):
        
        try:
            self.request = kwargs.pop("request")
        except:
            pass
        super().__init__(*args, **kwargs)
        self.fields['content'].widget.attrs = {"placeholder": 'Comment'}