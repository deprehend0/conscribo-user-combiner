
def find_relation_number(sign_up, old):
    relation_number = ''
    sign_up = "{} {} {}, {}".format(sign_up.get('Voornaam'), sign_up.get('Tussenvoegsel'), sign_up.get('Achternaam'),
                                    sign_up.get('Geboortedatum'))
    for record in old:
        existing_user = "{} {} {}, {}".format(record.get('Voornaam'), record.get('Tussenvoegsel'), record.get('Achternaam'),
                                              record.get('Geboortedatum'))
        if sign_up == existing_user:
            relation_number = record.get('Relatienummer')

    return relation_number


def add_relation_numbers(old, new):
    related_dicts = new
    for i, record in zip(len(new),new):
        relation_number = find_relation_number(record, old)
        related_dicts[i]['relationNumber'] = relation_number
        if relation_number == '':
            related_dicts[i]['startMembership'] = '01-09-2018'

    return related_dicts


def combine(old_location, new_location):
    old_users = []
    new_users = []

    with open(old_location) as old_file:
        old_users = old_file.readlines()

    with open(new_location) as new_file:
        new_users = new_file.readlines()


    old_header = old_users[0][1:-2].split('";"')
    new_header = new_users[0][1:-2].split('";"')

    old_dicts = []
    for record in old_users:
        if record is not old_users[0]:
            tmp_dict = {}
            fields = record[1:-2].replace(';;', ';"Onbekend";').split('";"')
            for k in range(len(old_header)):
                tmp_dict[old_header[k]] = fields[k]
            old_dicts.append(tmp_dict)

    new_dicts = []
    for record in new_users:
        if record is not new_users[0]:
            tmp_dict = {}
            fields = record[1:-2].replace(';;', ';"Onbekend";').split('";"')
            for k in range(len(new_header)):
                tmp_dict[new_header[k]] = fields[k]
            new_dicts.append(tmp_dict)

    combined_dict = add_relation_numbers(old_dicts, new_dicts)

    '''
    Relation number | Salution | Firstname | Insertion | Lastname | Birthday | Postal Code | City | Street | 
    Housenumber | Housnumber addition | Telephone | IBAN | BIC | Student | Dancing | Salsa | Ballroom | Partners | 
    Newsletter | Photo's | Privacy | Start membership
    '''
    header = '"Relatienummer";"Aanhef";"Voornaam";"Tussenvoegsel";"Achternaam";"Geboortedatum";"Postcode";' \
             '"Woonplaats";"Straatnaam";"Huisnr";"Huisnr toev.";"Telefoonnummer";"Bankrekeningnummer";' \
             '"BIC nummer";"Student";"Dansend";"Salsa";"Stijldansen";"Partners";"Nieuwsbrief";"Smoelenboek";' \
             '"Akkoord privacyverklaring";"Start lidmaatschap"\n'

    csv_string = ''
    for record in combined_dict:
        sign_up = '"{}";"{}";"{}";"{}";"{}";"{}";"{}";"{}";"{}";"{}";"{}";' \
                  '"{}";"{}";"{}";"{}";"{}";"{}";"{}";"{}";"{}";"{}";"{}"'.format(record.get('Relatienummer'),
                                                                                  record.get('Aanhef'),
                                                                                  record.get('Voornaam'),
                                                                                  record.get('Tussenvoegsel'),
                                                                                  record.get('Achternaam'),
                                                                                  record.get('Geboortedatum'),
                                                                                  record.get('Postcode'),
                                                                                  record.get('Woonplaats'),
                                                                                  record.get('Straatnaam'),
                                                                                  record.get('Huisnr'),
                                                                                  record.get('Toevoeging'),
                                                                                  record.get('Telefoonnummer'),
                                                                                  record.get('IBAN'),
                                                                                  record.get('BIC'),
                                                                                  record.get('Student'),
                                                                                  record.get('Dansend'),
                                                                                  record.get('Salsa'),
                                                                                  record.get('Stijldansen'),
                                                                                  record.get('Partners'),
                                                                                  record.get('Nieuwsbrief'),
                                                                                  record.get('Smoelenboek'),
                                                                                  record.get('Privacy'))

        if record.get('startMembership'):
            sign_up += ';"{}"'.format(record.get('startMembership'))

        sign_up += '\n'
        csv_string += sign_up


    return 0;