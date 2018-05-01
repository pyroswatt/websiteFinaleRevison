from django import forms


class LampeForm(forms.Form):
    temperatureTesteur = forms.CharField(label = 'temperatureTesteur' )
    temperatureUV = forms.CharField(label = 'temperature Lampe')
    stateUv = forms.CharField(label = 'Status lampe UV' )

class SpectrophotometerForm(forms.Form):
    phValue = forms.CharField(label= 'ph Eau')
    nitriteValue = forms.CharField(label='NO2 Eau')
    nitrateValue = forms.CharField(label='NO3 Eau')