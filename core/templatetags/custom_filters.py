from django import template

from core.models import DialerCredentials,DataSourceCredentials,Profile, ClientProfile, AffiliateInvoice
register = template.Library()

from core.models import APPLICATION_SKILLS_CHOICES



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
def count_skills(skills):
    # Check if `skills` is a list; if not, return 0
    if isinstance(skills, list):
        return len(skills)
    return 0

@register.filter
def get_skill_value(skill):
    skills = dict(APPLICATION_SKILLS_CHOICES)
    value = skills[skill]
    return value
    

@register.filter
def get_affiliate_clients_count(affiliate):

    clients_count =  len(ClientProfile.objects.filter(affiliate=affiliate))
    account = " Clients"
    if clients_count == 1:
        account = " Client"

    return str(clients_count) + account

@register.filter
def get_affiliate_client_revenue(client,combined_date):


    year, month = map(int, combined_date.split('-'))


    total_rev = 0
    invoices = AffiliateInvoice.objects.filter(client=client, date__month=month, date__year=year)
    
    # Calculate total revenue
    for invoice in invoices:
        total_rev += invoice.revenue  # Assuming 'amount' is a field on the AffiliateInvoice model
    
    return total_rev


@register.filter
def get_affiliate_client_commission(client,combined_date):


    year, month = map(int, combined_date.split('-'))

    total_comm = 0
    total_rev = 0
    invoices = AffiliateInvoice.objects.filter(client=client, date__month=month, date__year=year)
    
    # Calculate total revenue
    for invoice in invoices:
        total_rev += invoice.revenue  # Assuming 'amount' is a field on the AffiliateInvoice model
    
    affiliate_comm = client.affiliate.commission_percentage

    total_comm = total_rev * (affiliate_comm/100)

    return round(total_comm,2)

@register.filter
def get_affiliate_notes(client,combined_date):


    year, month = map(int, combined_date.split('-'))

    
    invoice = AffiliateInvoice.objects.filter(client=client, date__month=month, date__year=year).last()
    
    if invoice:
        notes = invoice.notes 
    else: 
        notes = "None"

    return notes

@register.filter
def get_affiliate_clients(affiliate):

    clients =  ClientProfile.objects.filter(affiliate=affiliate)


    return clients

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






@register.filter
def get_role_members_count(role):

    count =  len(Profile.objects.filter(role=role))
    account = " Users"
    if count == 1:
        account = " User"
 

    return str(count) + account









@register.filter(name='key_for_value')
def key_for_value(value, my_dict):
    """
    Returns the key corresponding to the given value in a dictionary.
    """
    return next((k for k, v in my_dict.items() if v == value), None)




