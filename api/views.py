from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import MonthDataSerializer
from datetime import datetime
import calendar
import ephem

moon_signs = [
    {'symbol': '♑', 'word': 'capricorn'}, 
    {'symbol': '♒', 'word': 'aquarius'}, 
    {'symbol': '♓', 'word': 'pisces'}, 
    {'symbol': '♈', 'word': 'aries'}, 
    {'symbol': '♉', 'word': 'taurus'}, 
    {'symbol': '♊', 'word': 'gemini'}, 
    {'symbol': '♋', 'word': 'cancer'}, 
    {'symbol': '♌', 'word': 'leo'}, 
    {'symbol': '♍', 'word': 'virgo'}, 
    {'symbol': '♎', 'word': 'libra'}, 
    {'symbol': '♏', 'word': 'scorpio'}, 
    {'symbol': '♐', 'word': 'sagittarius'}, 
    {'symbol': '♑', 'word': 'capricorn'}
]

sign_recomendations = [
    'Focus on pruning and maintaining existing plants.',
    'Plant flowers, herbs, and crops that require unique growing conditions.',
    'Plant leafy vegetables, water-loving plants, and flowers.',
    'Plant leafy greens and root crops.',
    'Plant edible root crops and fruits like potatoes and apples.',
    'Plant herbs, legumes, and flowers.',
    'Focus on watering and nurturing existing plants.',
    'Plant vegetables that require plenty of sunlight.',
    'Plant leafy greens, root vegetables, and herbs.',
    'Plant flowers, decorative plants, and crops that require balance of sunlight and shade.',
    'Plant root crops and crops that require deep watering.',
    'Plant fruit-bearing trees and plants.',
    'Focus on pruning and maintaining existing plants.',
]

phase_recomendations = {
    'New Moon': 'Refrain from sowing and engage in soil preparation or other gardening tasks.',
    'Growing Moon': 'Sow plants that require a lot of energy for growth and development, such as tomatoes, cucumbers or legumes.',
    'Full Moon': 'Sow plants that require a lot of light and have a short growth period, such as lettuce, spinach or radishes.',
    'Waning Moon': 'Sow plants that need rooting and root system development, such as carrots, onions or potatoes.',
}

def get_title(year, month):
    months = [
        '',
        'January',
        'February',
        'March',
        'April',
        'May',
        'June',
        'July',
        'August',
        'September',
        'October',
        'November',
        'December'
    ]

    return f'{year} {months[month]}'

def get_sign_change_day(month):
     res = [22, 21, 20, 21, 21, 22, 22, 24, 24, 24, 24, 23, 22]

     return res[month]



def get_moon_sign(year, month):
    signs = [(round(i / 2.5) + month) % 12 for i in range(get_sign_change_day(month))] + \
        [(round(i / 2.5) + month + 1) % 12 for i in range(get_sign_change_day(month), calendar.monthrange(year, month)[1])]
    return signs

def get_designated_moon_sign(year, month):
    signs = get_moon_sign(year, month)
    designated_signs = [moon_signs[i] for i in signs]
    return designated_signs

def get_moon_phase(year, month):
    phases = [{'symbol': '', 'word': ''}]

    for day in range(calendar.monthrange(year, month)[1] + 2):
            moon = ephem.Moon()
            moon.compute(f'{year}/{month}/{day}')
            phase = round(moon.phase / 100, 2)
            if phases[-1]['word'] == 'Waning Moon' and phase < 0.5:
                phases.append({'symbol': '🌑', 'word': 'New Moon'})
            elif phase < 0.5:
                phases.append({'symbol': '🌒', 'word': 'Growing Moon'})
            elif phases[-1]['word'] == 'Growing Moon' and phase < 1:
                phases.append({'symbol': '🌕', 'word': 'Full Moon'})
            elif phase < 1:
                phases.append({'symbol': '🌘', 'word': 'Waning Moon'})
    phases.pop(0)
    return phases

def get_recomendations(year, month):
    month_range = calendar.monthrange(year, month)[1]
    signs = get_moon_sign(year, month)
    phases = [i['word'] for i in get_moon_phase(year, month)]
    recomendations = [f'{sign_recomendations[signs[i]]} {phase_recomendations[phases[i]]}'
                       if phases[i] != 'New Moon' else phase_recomendations[phases[i]]
                         for i in range(month_range)]
    return recomendations

def get_days(year, month):
    weekday = calendar.weekday(year, month, 1)
    if weekday == 0: weekday = 7
    month_range = calendar.monthrange(year, month)[1]
    divided_days = []

    signs = get_designated_moon_sign(year, month)
    phases = get_moon_phase(year, month)            
    recomendations = get_recomendations(year, month)

    days = [{'number': i + 1, 'sign': signs[i], 'phase': phases[i], 'recomendations': recomendations[i]} for i in range(month_range)]

    for i in range(month_range):
        if i == 0 or i % 7 == 7 - weekday:
            divided_days.append([days[i]])
        else:
            divided_days[-1].append(days[i])
        
    return divided_days


class APIData(APIView):
    """
    {
    "title": "2023 November",
    "days": [
        [
            {
                "number": 1,
                "sign": {
                    "symbol": "♐",
                    "word": "sagittarius"
                },
                "phase": {
                    "symbol": "🌖",
                    "word": "Waning Moon"
                }
            },
    """
    def get(self, request):
        serializer = MonthDataSerializer(data=request.query_params)
        if serializer.is_valid():
            year = serializer.validated_data['y']
            month = serializer.validated_data['m']

            title = get_title(year, month)
            days = get_days(year, month)

            return Response({'title': title, 'days': days})
        return Response(serializer.errors, status=400)
