from django import template



register = template.Library()



@register.filter
def seconds_to_hhmmss(seconds):
    """Custom filter to convert seconds to HH:MM:SS format."""
    if not seconds:
        return '00:00:00'
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

@register.filter
def get_item_and_format(dictionary, key):
    """Custom filter to get item from dictionary by key and format seconds to HH:MM:SS."""
    value = dictionary.get(key, 0)  # Default to 0 if key is not found
    return seconds_to_hhmmss(value)