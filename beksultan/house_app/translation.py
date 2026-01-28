from .models import Property,PropertyDocument,Review
from modeltranslation.translator import TranslationOptions,register

@register(Property)
class PropertyTranslationOptions(TranslationOptions):
    fields = ('title','description','property_type','region','city','district'
              ,'address','condition')


@register(PropertyDocument)
class DocumentTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(Review)
class DocumentTranslationOptions(TranslationOptions):
    fields = ('comment',)

