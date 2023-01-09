# This is the form that you are going to use for the user to enter a coupon code.

from django import forms

class CouponApplyForm(forms.Form):
    code = forms.CharField()