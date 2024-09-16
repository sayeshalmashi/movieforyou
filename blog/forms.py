from django import forms
from blog.models import Comment , Rating


class CommentForm(forms.ModelForm):
  class Meta:
    model=Comment
    fields=['movie','name','email','subject','message']
    
class RatingForm(forms.ModelForm):
  class Meta:
    model=Rating
    fields=['rating']
    widgets= {
      'rating':forms.RadioSelect(choices=[(i,str(i))
                                          for i in range(1,6)]),
    }