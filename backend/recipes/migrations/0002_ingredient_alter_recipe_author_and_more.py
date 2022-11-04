# Generated by Django 4.1.2 on 2022-11-04 11:57

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import recipes.models


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0003_alter_tag_color'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, error_messages={'unique': 'Такой ингридиент уже есть.'}, max_length=250, unique=True, verbose_name='Наименование ингредиента')),
                ('measurement_unit', models.CharField(max_length=200, verbose_name='Единица измерения')),
            ],
            options={
                'verbose_name': 'Ингредиент',
                'verbose_name_plural': 'Ингредиенты',
                'ordering': ('name',),
            },
        ),
        migrations.AlterField(
            model_name='recipe',
            name='author',
            field=models.ForeignKey(on_delete=models.SET(recipes.models.get_sentinel_user), related_name='recipes', to=settings.AUTH_USER_MODEL, verbose_name='Автор рецепта'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.PositiveSmallIntegerField(help_text='Не может быть меньше минуты!', validators=[django.core.validators.MinValueValidator(1, message='Время приготовления не может быть меньше 1 мин.'), django.core.validators.MaxValueValidator(32767, message='Время приготовления не может быть больше 32767 мин.')], verbose_name='Время приготовления, мин.'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='name',
            field=models.CharField(error_messages={'unique': 'Рецепт с таким названием уже создан.'}, max_length=200, unique=True, verbose_name='Название рецепта'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(related_name='recipes', to='tags.tag', verbose_name='Тэги'),
        ),
        migrations.CreateModel(
            name='IngredientInRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1, message='Количество ингредиентов не может быть меньше 1.'), django.core.validators.MaxValueValidator(32767, message='Количество ингредиентов не может быть больше 32767.')], verbose_name='Количество')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='get_recipes', to='recipes.ingredient')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='get_ingredients', to='recipes.recipe')),
            ],
            options={
                'verbose_name': 'Количество ингредиента в рецепте',
                'verbose_name_plural': 'Количество ингредиентов в рецептах',
            },
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(through='recipes.IngredientInRecipe', to='recipes.ingredient'),
        ),
        migrations.AddConstraint(
            model_name='ingredientinrecipe',
            constraint=models.UniqueConstraint(fields=('ingredient', 'recipe'), name='recipe_ingredient_unique'),
        ),
    ]
