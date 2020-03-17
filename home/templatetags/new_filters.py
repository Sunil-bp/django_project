from django import template

register = template.Library()

@register.filter(name='chat_split')
def chat_split(value):
    time = value.split(",")[0].strip()
    text = value.split(":")[2]
    return [time[1:], text]
