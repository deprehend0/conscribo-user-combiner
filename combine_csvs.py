

courses = []
course_lvl = []
members = []
member_course_level = []
person_contact_info = []
users = []
levels = []


with open('./data/wp_ula_course.csv', 'r') as file:
    courses = file.readlines()

# with open('./data/wp_ula_courselevel.csv', 'r', encoding='utf8') as file:
with open('./data/wp_ula_courselevel.csv', 'r') as file:
    course_lvl = file.readlines()

with open('./data/wp_ula_member.csv', 'r') as file:
    members = file.readlines()

with open('./data/wp_ula_membercourselevel.csv', 'r') as file:
    member_course_level = file.readlines()

with open('./data/wp_ula_personcontactinfo.csv', 'r') as file:
    person_contact_info = file.readlines()

with open('./data/wp_users.csv', 'r') as file:
    users= file.readlines()

with open('./data/wp_ula_level.csv', 'r') as file:
    levels = file.readlines()

courses_dict = []
course_lvl_dict = []
members_dict = []
member_course_dict = []
contact_info_dict = []
user_dicts = []
level_dicts = []

tables = [courses, course_lvl, member_course_level, members, person_contact_info, users, levels]
table_dicts = [courses_dict, course_lvl_dict, member_course_dict, members_dict, contact_info_dict, user_dicts, level_dicts]

c_header = courses[0][1:-2].split('";"')
clvl_header = course_lvl[0][1:-2].split('";"')
m_header = members[0][1:-2].split('";"')
mc_header = member_course_level[0][1:-2].split('";"')
ci_header = person_contact_info[0][1:-2].split('";"')
u_header= users[0][1:-2].split('";"')
l_header= levels[0][1:-2].split('";"')

headers = [c_header, clvl_header, mc_header, m_header, ci_header, u_header, l_header]
print(headers)
# print('c-header: {}'.format(c_header))
# print('clvl-header: {}'.format(clvl_header))
# print('m-header: {}'.format(m_header))
# print('mc-header: {}'.format(mc_header))
# print('ci-header: {}'.format(ci_header))
# print('u-header: {}'.format(u_header))
# print('l-header: {}'.format(l_header))

for i in range(len(tables)):
    table = tables[i]
    table_dict = table_dicts[i]
    keys = headers[i]
    for record in table:
        if record is not table[0]:
            record_fields = record[1:-2].replace('NULL', '"NULL"').replace(';;;', ';"Onbekend";"Onbekend";').replace(';;', ';"Onbekend";').split('";"')
            dict = {}
            for k in range(len(keys)):
                dict[keys[k]] = record_fields[k]

            table_dict.append(dict)

# print(table_dicts)

courses_dict = table_dicts[0]
course_lvl_dict = table_dicts[1]
members_dict = table_dicts[3]
member_course_dict = table_dicts[2]
contact_info_dict = table_dicts[4]


'''
Ik wil een tabel die er als volgt uit ziet:
Firstname | Lastnam | email |  dob | gender | memberContactInfo (postcode, city, straat, nr + toevoeging, telnr) | Cursussen | bankBIC | dateMemberStart | dateMemberEnd | Student | Institution | collegeKaart | is Honorary
'''


def getContactInfoCSV(id):
    person = []
    for record in contact_info_dict:
        if record.get('personContactInfoId') == id:
            person = record

    houseNumberExtension = person.get('houseNumberExtension') if person.get('houseNumberExtension') != 'Onbekend' else ''

    return '{}";"{}";"{}";"{}";"{}";"{}'.format(person.get('postalCode'), person.get('streetName'), person.get('houseNumber'),
                                           houseNumberExtension, person.get('city'), person.get('telephoneNumber'))


def getCourseCSV(id):
    courses = []
    for course in member_course_dict:
        if course.get('memberId') == id:
            courses.append(course)

    course_levels = []
    level_ids = []
    for course in courses:
        clvl_id = course.get('courseLevelId')
        for course_level in course_lvl_dict:
            if course_level.get('courseLevelId') == clvl_id:
                level_ids.append(course_level.get('levelId'))

    lvl_titles = []

    for level in level_dicts:
        if level.get('levelId') in level_ids:
            lvl_titles.append(level.get('title'))

    return ','.join(lvl_titles)


def getEmail(id):
    user = {}
    for record in user_dicts:
        if record.get('ID') == id:
            user = record

    return user.get('user_email')


def reformatDate(date):
    if date != 'NULL':
        dateparts = date.split('-')
        return '{}-{}-{}'.format(dateparts[2], dateparts[1], dateparts[0])
    else:
        return 'NULL'


# header = '"Voornaam";"Achternaam";"Email";"Geboortedatum";"Geslacht";"Postcode";"Stad";"Straatnaam";"Huisnummer + toevoeging";"Telefoon";"Cursussen";bankBIC";"Start lidmaatschap";"Einde lidmaatschap";"Is student";"Instituut";"Collegekaart nummer";"Is erelid"\n'
header = '"Aanhef";"Voornaam";"Achternaam";"Geboortedatum";"Postcode";"Straatnaam";"Huisnr";"Huisnr toev.";"Plaatsnaam";"Telefoonnummer";"E-mailadres";"Bankrekeningnummer";"BIC nummer";"Salsa";"Stijldansen";"Dansend";"Student";"Erelid";"Opmerkingen";"Nieuwsbrief";"Smoelenboek";"Akkoord privacyverklaring";"Start lidmaatschap";"Eind Lidmaatschap"\n'
csv_string = ''
for member in members_dict:
    if member.get('dateMemberEnd') == 'NULL':
        email = getEmail(member.get('wpUserId'))
        if not isinstance(email, str):
            email = ''
        contact_info = getContactInfoCSV(member.get('memberContactInfoId'))
        courses = getCourseCSV(member.get('memberId'))
        aanhef = ''
        isStudent = 'Nee'
        if member.get('student') == '1':
            isStudent = 'Ja'
        if member.get('gender') == '1':
            aanhef = 'Dhr.'
        elif member.get('gender') == '0':
            aanhef = 'Mevr.'
        if member.get('isHonoraryMember') == '0':
            honorary = 'Nee'
        elif member.get('isHonoraryMember') == '1':
            honorary = 'Ja'

        csv_string += '"{}";"{}";"{}";"{}";"{}";"{}";"{}";"{}";"{}";"{}";"{}";"{}";"{}";"{}";"{}";"{}";"{}";"{}";"{}"\n'.format(
                                                                                                       aanhef,
                                                                                                       member.get('firstName'),
                                                                                                       member.get('lastName'),
                                                                                                       reformatDate(member.get('dateOfBirth')),
                                                                                                       contact_info,
                                                                                                       email,
                                                                                                       member.get('bankAccountNumber'),
                                                                                                       member.get('bankBIC'),
                                                                                                       '',
                                                                                                       '',
                                                                                                       '',
                                                                                                       isStudent,
                                                                                                       honorary,
                                                                                                       '',
                                                                                                       'Ja',
                                                                                                       'Ja',
                                                                                                       'Ja',
                                                                                                       reformatDate(member.get('dateMemberStart')),
                                                                                                       reformatDate(member.get('dateMemberEnd')))



# print(csv_string)
csv_string = header + csv_string
with open('./data/members_may_nonutf.csv', 'w+', encoding='utf8') as file:
    file.write(csv_string)
