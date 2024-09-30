from django import template

from core.models import DialerCredentials,DataSourceCredentials,Profile
register = template.Library()



@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def format_float(value):
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return value



@register.filter
def count_services(queryset):
    return queryset.count()


@register.filter
def get_dialer_credentials(campaign):

    dialer_cred_count =  len(DialerCredentials.objects.filter(campaign=campaign))
    account = " accounts"
    if dialer_cred_count == 1:
        account = " account"

    return str(dialer_cred_count) + account


@register.filter
def get_source_credentials(campaign):

    source_cred_count =  len(DataSourceCredentials.objects.filter(campaign=campaign))
    account = " accounts"
    if source_cred_count == 1:
        account = " account"

    return str(source_cred_count) + account


@register.simple_tag
def range_filter(value):
    return range(1, value + 1)

@register.filter
def get_slot_name(lead_handling_settings, slot_number):
    return getattr(lead_handling_settings, f'slot{slot_number}_name', None)

@register.filter
def get_slot_percentage(lead_handling_settings, slot_number):
    return getattr(lead_handling_settings, f'slot{slot_number}_percentage', None)


@register.filter
def get_slot_dispo(camp_dispo, slot_number):
    return getattr(camp_dispo, f'slot{slot_number}_dispo', None)


@register.filter
def text_to_list(value):
    if not value:
        return []
    # Remove unwanted characters
    value = value.strip('[]').replace('"', '').replace("'", '')
    # Split by comma and strip whitespace from each item
    return [item.strip() for item in value.split(',') if item.strip()]



@register.filter
def truncate(value, max_length=15):
    """
    Truncates the string to a maximum length and appends "..." if necessary.
    :param value: The string to be truncated.
    :param max_length: The maximum length of the string before truncation.
    :return: The truncated string with "..." if it was truncated.
    """
    if not isinstance(value, str):
        return value
    if len(value) > max_length:
        return value[:max_length] + '...'
    return value




@register.filter
def dialer_username(value):

    if value:
        return value.username
    
    else: 
        return "None"
    
@register.filter
def dialer_password(value):

    if value:
        return value.password
    
    else: 
        return "None"
    

@register.filter
def score(campaign):

    campaign = campaign
    lead_score = campaign.lead_points
    return lead_score


@register.filter
def user_id(user):
    try:
        profile_id = Profile.objects.get(user=user).id
    except:
        profile_id = "N/A"
    return profile_id


@register.filter
def user_fullname(user):
    try:
        profile = Profile.objects.get(user=user)
    except:
        profile = "N/A"
    return profile






