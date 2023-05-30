import os
from io import BytesIO

from django.conf import settings
from django.db.models import Sum
from django.http import HttpResponse
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from recipes.models import IngredientRecipe


def shopping_cart_response(request):
    recipes = IngredientRecipe.objects.filter(
        recipe__in=request.user.shopping_cart.all()
    )
    ingredients = recipes.values(
        'ingredient__name', 'ingredient__measurement_unit'
    ).annotate(ingredient_count=Sum('amount'))

    response = HttpResponse(content_type='application/pdf')
    filename = f'{request.user}_shopping_cart.pdf'
    response['Content-Disposition'] = f'attachment; filename={filename}'

    recipe_names = ', '.join(
        set([recipe.recipe.name for recipe in recipes])
    )

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    font_path = os.path.join(settings.STATIC_ROOT, 'fonts/DejaVuSerif.ttf')
    pdfmetrics.registerFont(TTFont('DejaVuSerif', font_path))
    y = 740  # Y-coordinate for the content
    line_height = 20
    pdf.setFont('DejaVuSerif', 14)
    pdf.drawString(100, 800, f'Ингредиенты для рецептов {recipe_names}')
    pdf.drawString(50, 780, 'Ingredient')
    pdf.drawString(200, 780, 'Count')
    pdf.drawString(300, 780, 'Unit')
    for ingredient in ingredients:
        name = ingredient['ingredient__name']
        count = ingredient['ingredient_count']
        measurement_unit = ingredient['ingredient__measurement_unit']
        line = f'{name} -   {count}   {measurement_unit}'
        pdf.drawString(50, y, line)
        y -= line_height
    pdf.drawString(
        50,
        y - line_height,
        'Автор: Бекренёв Руслан; Приложение - FOORGRAM'
    )
    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    response.write(buffer.getvalue())
    return response
