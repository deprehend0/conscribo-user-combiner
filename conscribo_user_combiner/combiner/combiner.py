import datetime

def get_dob(date_string):
    if date_string:
        date = date_string
        day, month, year = date.split(' ')[0].replace('/', '-').split('-')
        if len(day) < 2:
            day = '0{}'.format(day)
        if len(month) < 2:
            month = '0{}'.format(month)
        if len(year) < 4:
            year = int('20{}'.format(year))
        elif len(year) == 4:
            year = int(year)
        if year > datetime.datetime.now().year:
            year -= 100
        return '{}-{}-{}'.format(day, month, year)


def get_date(date_string):
    if date_string:
        date = date_string.split(' ')[0]
        month, day, year = date.replace('/', '-').split('-')
        return '{}-{}-{}'.format(day, month, year)


def getAchternaam(record):
    if record.get('Tussenvoegsel') != 'Onbekend':
        return '{} {}'.format(record.get('Tussenvoegsel').strip(), record.get('Achternaam').strip())
    else:
        return record.get('Achternaam')


def find_relation_number(sign_up, old):
    relation_number = ''
    sign_up = "{} {}, {}".format(sign_up.get('Voornaam').strip(), getAchternaam(sign_up),
                                 get_dob(sign_up.get('Geboortedatum')))
    for record in old:
        existing_user = "{} {}, {}".format(record.get('Voornaam'),
                                           record.get('Naam'),
                                           record.get('Geboortedatum'))

        if sign_up.lower() == existing_user.lower():
            relation_number = record.get('Relatienummer')

    if relation_number == '':
        print(sign_up.lower())

    return relation_number


def find_start_date(sign_up, old):
    start_date = None
    sign_up = "{} {}, {}".format(sign_up.get('Voornaam').strip(), getAchternaam(sign_up),
                                 get_dob(sign_up.get('Geboortedatum')))

    for record in old:
        existing_user = "{} {}, {}".format(record.get('Voornaam'),
                                           record.get('Naam'),
                                           record.get('Geboortedatum'))

        if sign_up.lower() == existing_user.lower():
            start_date = record.get('Start Lidmaatschap')

    return start_date


def add_relation_numbers(old, new):
    related_dicts = new
    for i, record in enumerate(new):
        relation_number = find_relation_number(record, old)
        start_date = find_start_date(record, old)
        related_dicts[i]['relationNumber'] = relation_number
        related_dicts[i]['start_date'] = start_date

    return related_dicts


def getStudent(instelling):
    studie_instelling = instelling.lower()
    if ' uu ' in studie_instelling or ' hu ' in studie_instelling:
        return 'UU/HU'
    elif ' ander' in studie_instelling:
        return 'Andere instelling'
    else:
        return 'Geen student'


def getSmoelenboek(smoelenboek):
    if smoelenboek == 'Ja':
        return smoelenboek
    else:
        return 'Nee'


def create_existing_non_dancing_user_line(record):
    return '"{}";"{}";"{}";"{}";"{}";"{}";"{}";"{}";"{}";"{}";{};' \
           '"{}";"{}";"{}";"{}";"{}";"{}";"{}";"{}";"{}";"{}";"{}";"{}"\n'.format(record.get('Relatienummer'),
                                                                                  record.get('Aanhef'),
                                                                                  record.get('Voornaam'),
                                                                                  record.get('Naam'),
                                                                                  record.get('Geboortedatum'),
                                                                                  record.get('Postcode'),
                                                                                  record.get('Plaatsnaam'),
                                                                                  record.get('Straatnaam'),
                                                                                  record.get('Huisnr'),
                                                                                  record.get('Huisnr toev.'),
                                                                                  record.get('Telefoonnummer'),
                                                                                  record.get('E-mailadres'),
                                                                                  record.get('Bankrekeningnummer'),
                                                                                  record.get('BIC nummer'),
                                                                                  record.get('Student'),
                                                                                  'Nee',
                                                                                  '',
                                                                                  '',
                                                                                  '',
                                                                                  record.get('Nieuwsbrief'),
                                                                                  record.get('Smoelenboek'),
                                                                                  record.get('Akkoord privacyverklaring'),
                                                                                  record.get('Start Lidmaatschap'))


def create_existing_user_line(record):
    return '"{}";"{}";"{}";"{}";"{}";"{}";"{}";"{}";"{}";"{}";{};' \
           '"{}";"{}";"{}";"{}";"{}";"{}";"{}";"{}";"{}";"{}";"{}";"{}"\n'.format(record.get('relationNumber'),
                                                                                  record.get('Aanhef'),
                                                                                  record.get('Voornaam'),
                                                                                  getAchternaam(record),
                                                                                  get_dob(record.get('Geboortedatum')),
                                                                                  record.get('Postcode'),
                                                                                  record.get('Woonplaats'),
                                                                                  record.get('Straatnaam'),
                                                                                  record.get('Huisnr'),
                                                                                  record.get('Toevoeging'),
                                                                                  record.get('Telefoonnummer'),
                                                                                  record.get('E-mailadres'),
                                                                                  record.get('IBAN'),
                                                                                  record.get('BIC'),
                                                                                  getStudent(record.get('Student')),
                                                                                  record.get('Dansend'),
                                                                                  record.get('Salsa'),
                                                                                  record.get('Stijldansen'),
                                                                                  record.get('Partners'),
                                                                                  record.get('Nieuwsbrief'),
                                                                                  getSmoelenboek(record.get('Smoelenboek')),
                                                                                  record.get('Privacy'),
                                                                                  record.get('start_date'))


def create_new_user_line(record):
    return '"{}";"{}";"{}";"{}";"{}";"{}";"{}";"{}";"{}";"{}";' \
           '"{}";"{}";"{}";"{}";"{}";"{}";"{}";"{}";"{}";"{}";"{}";"{}"\n'.format(record.get('Aanhef'),
                                                                                  record.get('Voornaam'),
                                                                                  getAchternaam(record),
                                                                                  get_dob(record.get('Geboortedatum')),
                                                                                  record.get('Postcode'),
                                                                                  record.get('Woonplaats'),
                                                                                  record.get('Straatnaam'),
                                                                                  record.get('Huisnr'),
                                                                                  record.get('Toevoeging'),
                                                                                  record.get('Telefoonnummer'),
                                                                                  record.get('E-mailadres'),
                                                                                  record.get('IBAN'),
                                                                                  record.get('BIC'),
                                                                                  getStudent(record.get('Student')),
                                                                                  record.get('Dansend'),
                                                                                  record.get('Salsa'),
                                                                                  record.get('Stijldansen'),
                                                                                  record.get('Partners'),
                                                                                  record.get('Nieuwsbrief'),
                                                                                  record.get('Smoelenboek'),
                                                                                  record.get('Privacy'),
                                                                                  get_dob(record.get('Timestamp')))


def combine(old_location, new_location, export_location):
    old_users = []
    new_users = []
    export_location = export_location.replace('\n', '')

    with open(old_location.replace('\n', ''), 'r', encoding='latin-1') as old_file:
        old_users = old_file.readlines()

    with open(new_location.replace('\n', ''), 'r', encoding='latin-1') as new_file:
        new_users = new_file.readlines()

    old_header = old_users[0][0:-1].split(';')
    new_header = new_users[0][0:-1].split(';')

    old_dicts = []
    for record in old_users:
        if record is not old_users[0]:
            tmp_dict = {}
            fields = record[0:-1].replace(';;', ';Onbekend;').split(';')
            for k in range(len(old_header)):
                tmp_dict[old_header[k]] = fields[k]
            old_dicts.append(tmp_dict)
    new_dicts = []
    for record in new_users:
        if record is not new_users[0]:
            tmp_dict = {}
            fields = record[0:-1].replace(';;', ';Onbekend;').split(';')
            for k in range(len(new_header)):
                tmp_dict[new_header[k]] = fields[k]
            new_dicts.append(tmp_dict)

    combined_dict = add_relation_numbers(old_dicts, new_dicts)

    '''
    {Relation number |} Salution | Firstname | Insertion | Lastname | Birthday | Postal Code | City | Street |
    Housenumber | Housnumber addition | Telephone | IBAN | BIC | Student | Dancing | Salsa | Ballroom | Partners |
    Newsletter | Photo's | Privacy | Start membership

    {x} shows potential header parts. In our administration we want new users to have a start membership date.
    However, existing users are already members so don't need that. But with the relation number we are able to update
    the right users.
    '''
    existing_user_header = '"Relatienummer";"Aanhef";"Voornaam";"Achternaam";"Geboortedatum";"Postcode";' \
                           '"Woonplaats";"Straatnaam";"Huisnr";"Huisnr toev.";"Telefoonnummer";"E-mailadres";"Bankrekeningnummer";' \
                           '"BIC nummer";"Student";"Dansend";"Salsa";"Stijldansen";"Partners";"Nieuwsbrief";"Smoelenboek";' \
                           '"Akkoord privacyverklaring";"Start lidmaatschap"\n'

    new_user_header = '"Aanhef";"Voornaam";"Achternaam";"Geboortedatum";"Postcode";' \
                      '"Woonplaats";"Straatnaam";"Huisnr";"Huisnr toev.";"Telefoonnummer";"E-mailadres";"Bankrekeningnummer";' \
                      '"BIC nummer";"Student";"Dansend";"Salsa";"Stijldansen";"Partners";"Nieuwsbrief";"Smoelenboek";' \
                      '"Akkoord privacyverklaring";"Start lidmaatschap"\n'

    dancing_existing_users = []

    for record in combined_dict:
        if record.get('relationNumber') != '':
            dancing_existing_users.append(record.get('relationNumber'))
            existing_user_header += create_existing_user_line(record)
        else:
            new_user_header += create_new_user_line(record)

    for record in old_dicts:
        if record.get('Relatienummer') != '' and record.get('Relatienummer') not in dancing_existing_users:
            existing_user_header += create_existing_non_dancing_user_line(record)

    with open(export_location + '/existing_users.csv', 'w+', encoding='latin-1') as existing_user_file:
        existing_user_file.write(existing_user_header.replace('Onbekend', ''))

    with open(export_location + '/new_users.csv', 'w+', encoding='latin-1') as new_user_file:
        new_user_file.write(new_user_header.replace('Onbekend', ''))
