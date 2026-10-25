"""Phase 9: restored institution sections (sibling folders of the main portal).

SIBLINGS: folder -> {name, logo (image key or None), nav [(label, file)], pages {file: (title, html)}}
REDIRECTS: legacy path (from the site root) -> current path. Pages whose original text was copied unchanged from another institution
are consolidated here: the old URL redirects to the single page that holds the text.
REMOVE: Phase 8 files that carried invented text and are replaced by a redirect.
"""
from html import escape
from rc_helpers import (fig, gallery, single, split, p, quote, dated, note, table, people, vision, scan, logo, phone, doc_list)

ADDR = 'S.J.P. Road, City Market, Bangalore – 560002'
ADMIN = f'<a href="tel:0822272086">0822272086</a>, <a href="tel:0822221165">0822221165</a>'
EMAIL = '<a href="mailto:jamiaululoom@gmail.com">jamiaululoom@gmail.com</a>'
ALL = ('All Institutions', '../Institutions.html')

def facts(*rows):
    return '<dl class="facts">' + ''.join(f'<dt>{k}</dt><dd>{v}</dd>' for k, v in rows) + '</dl>'

def careers_page():
    return facts(('Address', ADDR), ('Telephone', '<a href="tel:0822221151">0822221151</a>, <a href="tel:0822239495">0822239495</a>'), ('Email', EMAIL))

def W(inner):   # wrapper used by every page body
    return inner

# shared texts (each is shown under the institution(s) it describes)
COLLEGE_BUILDING = ('The college is housed in a spacious building with well furnished and ventilated class rooms, well equipped laboratories and library with good collection of books. '
                    'Magazines and News papers are also subscribed for the benefit of the students. The computer lab is provided with internet facility. A spacious auditorium is also under construction. '
                    'We aim to provide canteen facility for our students. A nationalized bank (Canara Bank) is also located in the same building.')
COLLEGE_DATED = dated('The remarks that the auditorium is “under construction” and that a canteen is an aim date from when this text was written; they may no longer apply.')
CLASS_DICTUM = ('believes in the following dictum delivering the lessons “I HEAR, I FORGET, I SEE, I RECALL, I DO, I UNDERSTAND.” All teachers endeavor to prepare their lessons and deliver them in such a way that the child becomes a participant in the learning process. '
                'The lessons are complimented by practical sessions and access of information on the internet. A total holistic approach is adopted to remove the burden of learning and make the process of learning a joyful experience without hang-ups and hiccups. '
                'The lessons are delivered in the class room by using state of the art audio visual equipment such as overhead projectors and LCD projectors.')
ADMISSION_PROCEDURE = '''<h2>Admission procedure</h2>
<ol>
<li>The qualified candidates seeking admission are required to fill up the prescribed application form in their own hand writing and submit the same to the office during working hours within the last date prescribed.</li>
<li>The applications should be accompanied by attested or Xerox copies of the following:
<ol><li>Statement of marks obtained in the qualifying examination.</li><li>Transfer certificate from the institution last attended.</li><li>Latest caste certificate in case of the students belonging to SC/ST/BC/BT.</li><li>Migration certificate if applicable.</li><li>Six passport size and two stamp size photos.</li><li>Original certificates must be submitted at the time of admission for proper verification and other formalities with the P.U Board.</li><li>All admissions are provisional until they are approved by the P.U.C board.</li><li>Producing fake documents or furnishing wrong information will attract criminal prosecution.</li></ol></li>
</ol>'''
SSLC_PARA = ('By the grace of Allah, the excellent result at the SSLC examination has held our heads high in esteem. VIPS with an Islamic outlook have always appreciated the functioning of our Institutions, particularly the wearing of the “hejab” by lady teachers and girl students with an Islamic type of attire in all the classes from nursery to high school. '
             'Very attractive and fabulous awards are given to the outstanding students after the results of SSLC public examination. This is to encourage and appreciate the excellence among the students. A high standard in education, hard work of the members of the staff and excellent result at the SSLC Public Examination cause the heavy rush of the girls for admission. '
             'The secretary of Jame-ul-uloom has given the slogan “SUSTAINED EFFORTS” to the Members of the staff. They continue to march ahead in the academic achievement and they do not look back.')
COMPUTER_EDU = ('The school is conscious about the fact that computer education and information technology is the mainstay of the 21st millennium, a powerful tool for not only communication but also access of information and computer knowledge is useful in all aspects of human endeavor, '
                'hence the school has introduced computer education right from 1st standard to 10th standard to give an edge to our student.')
STAFF_LINE = 'Well qualified, dedicated, attentive, zealous and well behaved.'
SHARED_SPORTS = lambda who: note(f'Co-curricular activities and sports are described on the shared <a href="../Sports.html">Co-Curricular Activities &amp; Sports</a> page.')

SIBLINGS = {}
REDIRECTS = {}
REDIRECTS.update({f'{d}/Message.html': 'Message.html#head-mistress-2013' for d in ('EngNurSchoolDEL', 'EngPrimarySchoolDEL', 'EngGirlsHighSchool', 'EngBoysHighSchool')})
REMOVE = []

# =====================================================================================================================
# ITI
# =====================================================================================================================
iti_nav = [('Overview', 'home.html'), ('Message', 'Message.html'), ('Admissions', 'Admissions.html'), ('Staff', 'Staff.html'), ('Management', 'Management.html'),
           ('Workshops', 'Workshops.html'), ('Library & Computer Lab', 'Library&CompLab.html'), ('Sports', 'Sports.html'), ('Contact', 'Contact.html'), ALL]
ITI_STAFF = [
 ('1', 'SHAMIULLA', 'PRINCIPAL', 'NTC, NAC &amp; DIPLOMA IN FOREMANSHIP (PRODUCTION ENGINEERING)', 'ADMIN FITTER', '10-11-1997', 'REGULAR', 'POT TRAINED'),
 ('2', 'GIRISHA T', 'JTO', 'NTC &amp; NAC', 'MMV', '27-11-2002', 'REGULAR', 'POT TRAINED'),
 ('3', 'MUSHEER PASHA', 'JTO', 'NTC (PERCEIVING DME)', 'MMV', '14-10-2005', 'REGULAR', 'No'),
 ('4', 'MOHAMMED SHAYUB', 'JTO', 'NTC &amp; NAC (PERCEIVING DME)', 'MRAC', '14-10-2008', 'REGULAR', 'No'),
 ('5', 'MOHAMMED IMDAD', 'JTO', 'NTC &amp; NAC', 'FITTER', '25-06-2011', 'REGULAR', 'No'),
 ('6', 'SHAKEEL AHMED', 'JTO', 'NTC, NAC &amp; (DEE)', 'MRAC', '14-02-2012', 'REGULAR', 'No'),
 ('7', 'SYED FAIZULLA', 'JTO', 'NTC &amp; NAC (PERCEIVING DME)', 'W/S CALCULATION &amp; ENGG DRG', '11-04-2012', 'REGULAR', 'NO'),
 ('8', 'ZAID AHMED', 'LAB ATTENDER', 'NTC (PERCEIVING DME)', 'LAB ATTENDER', '20-08-2007', 'REGULAR', '—'),
 ('9', 'ABDUL KAREEM D.A', 'Accountant', 'BSC', 'ACCOUNTS', '02/04/2012', 'REGULAR', '—'),
 ('10', 'SUSHMA B', 'CLERK', 'BBM', 'CLERK', '02/04/2012', 'REGULAR', '—')]
ITI_HOME = f'''{logo('../', 'logo_iti')}
{split(
  p('JAMIA MASJID &amp; MUSLIM CHARITABLE FUND TRUST (JM&amp;MCF) is one of the reputed trusts, established in the year 1939 with a mission to support the nation by educating people and to create a good society. The trust, with a core mission to establish a world class university, has started schools and colleges in and around Bangalore. One among the campuses is in Shikshanagar; the Board of Trustees were keen to develop the technically skilled manpower, which can fetch better employment and provide an opportunity for a trained technician to start his own industrial unit after completion of Technical Training courses.',
    'The Board of Trustees took the decision to start I.T.I courses in the trades of Fitter and Mechanic Refrigeration &amp; Air Conditioning from 2nd September 1996. There was a good response both from trainees and industry for trained manpower. This encouraged the Trust to start one more I.T.I course, in the trade of Mechanic Motor Vehicle, from the year 2002. Soon after, within a short span of time, the good response and the hard work of management and staff made the institute grow faster; now the institute has full sanctioned strength and the campus has spread over 2 acres and 12 guntas of land. The institute is situated in a greenery campus with serene atmosphere under the guidance of an excellent team of faculty members headed by a qualified and experienced Principal. The institute has excellent training infrastructure including labs and workshops with state-of-the-art trainer kits, machineries, seminar and lecture halls and a well stocked library.'),
  single('../', 'iti_campus', caption='ITI campus'))}
{facts(('Location', 'On the 27th km off the Bangalore–Mysore Highway (near Wonder La Amusement Park), Shikshanagar'), ('Bus routes', 'From Bangalore City: Nos. 226 (A to H) at Wonder-la Gate; 2 km from Bidadi Railway Station and 1 km from Hejjala Railway Station'), ('Principal', 'Dr. Shamiulla'))}
{quote('Natural abilities are like natural plants, they need pruning by study.', sign='Dr. Shamiulla', role='Principal')}
{dated('<strong>About 2012.</strong> The ITI is described as “in its 16th year of operation”, which places this text around 2012. The trade list, fees and staffing are those of that time.')}
<p>See the <a href="Message.html">vision, mission and message</a>, <a href="Admissions.html">trades and admissions</a>, <a href="Workshops.html">workshop photographs</a> and the <a href="Contact.html">location and contact</a> page.</p>'''
ITI_MESSAGE = f'''{split(
 '<h2>Our Vision</h2><p>To be a pioneer institution for technician development in vocational training.</p><h2>Our Mission</h2><p>To be a world class training institution, thus creating employment opportunities.</p>'
 + quote('Natural abilities are like natural plants, they need pruning by study.',
         'The Jame ul uloom ITI, which is in its 16th year of operation, has made tremendous progress in imparting quality education in the field of vocational training. At present there are six units running successfully with well qualified, dedicated and experienced teaching staff.',
         'The institute is equipped with the best infrastructural facilities, classrooms, laboratories and a library as per the guidelines issued by DGE&amp;T, New Delhi.',
         'After working in a world class multinational company with hands-on experience, selecting this institution is in the right direction; to join this esteemed institution is the correct decision and I am sure your hopes and ambitions will be fulfilled to your utmost satisfaction.',
         'I wish you the very best in your endeavors.')
 + '',
 single('../', 'iti_prin', caption='Principal, ITI'))}'''
ITI_ADM = f'''<p class="source-note">Trade table of about 2012. The figures are those of that time and are not a current admissions notice.</p>
{table(['Name of trade under NCVT', 'Duration of training', 'Eligibility qualification', 'No. of units', 'Seating capacity per unit', 'Shifts running (I/II/III)', 'Total seating capacity'],
       [['FITTER', '2 Years', 'SSLC', '1+1', '21', '1+1', '42'], ['MRAC', '2 Years', 'SSLC', '1+1', '21', '1+1', '42'], ['MMV', '2 Years', 'SSLC', '1+1', '21', '1+1', '42']])}
<p>Selection options: (a) by percentage of marks in the qualifying exam, (b) written test, (c) interview, (d) any other.</p>
<h2>Schemes running in the institute (CTS and MES etc. under NCVT)</h2>
{table(['Name of the scheme', 'Total capacity', 'Duration'], [['Craftsmen Training Scheme', '63+63', '2 Years'], ['Modular Employable', '—', '—'], ['Other Schemes', '—', '—']])}
<p>MRAC = Mechanic Refrigeration &amp; Air Conditioning; MMV = Mechanic Motor Vehicle. Contact details are on the <a href="Contact.html">Contact</a> page.</p>'''
ITI_STAFF_HTML = f'''{dated('<strong>Staff statement of about 2012.</strong> Names, designations, qualifications and joining dates are those of that time and may have changed.')}

{table(['Sl. No.', 'Name', 'Designation', 'Qualification (Class X onwards)', 'Trade', 'Date of joining', 'Regular / Adhoc / Contract', 'CTI trained (Yes/No)'], [list(r) for r in ITI_STAFF])}'''
ITI_MGMT = f'''<p class="source-note">Jamia Masjid &amp; Muslim Charitable Fund Trust. Registration: V of 1939, III of 1904, dated 09-05-1940.</p>
{people([('Alhaj Maqbool Ahmed', 'President'), ('Alhaj A. Syed Murtuza Hussain @ Gufran', 'Vice President'), ('Alhaj Mohammed Ateeq Ahmed', 'Secretary'), ('Alhaj Noorul Ameen @ Anwar', 'Joint Secretary'), ('Mohammed Athiulla', 'Treasurer'), ('Syed Abdul Gafoor', 'Internal Auditor')])}
<p>The Trust’s Governing Body and Trustees are on the <a href="../Team.html">Governing Body</a> and <a href="../Trustees.html">Trustees</a> pages.</p>'''
ITI_WORK = f'''<p>Photographs of the ITI workshops.</p>
<h2 id="fitter">Fitter workshop</h2>
{gallery('../', ['iti_fit1', 'iti_fit2', 'iti_fit3', 'iti_fit4'])}
<h2 id="mmv">Mechanic Motor Vehicle (MMV) laboratory</h2>
{gallery('../', ['iti_mmv'], cls='rc-wide')}
<h2 id="mrac">Mechanic Refrigeration &amp; Air Conditioning (MRAC) laboratory</h2>

<h2>ITI workshop</h2>
{gallery('../', ['iti_work'], cls='rc-wide')}
<h2 id="classroom">Classroom</h2>
{gallery('../', ['iti_cls'])}
'''
ITI_LIB = f'''<h2>Library</h2>
{p('Brief information on journals and books.', 'A well-furnished library with about 250 books is provided for staff and trainees for reference.', 'The library promotes the reading habit among trainees and helps them in their studies. Teaching aids like charts and models are also available in the library.')}
<h2>Computer Lab</h2>
{p('Brief information on hardware and software.', 'At present the institute has 6 systems with P3 configuration; steps have already been initiated to procure 15 systems with the latest configuration.')}
{dated('These numbers are of about 2012 and are not current.')}'''
ITI_SPORTS = f'''
{gallery('../', ['iti_play1', 'iti_play2', 'iti_play3'])}
<h2 id="prize-distribution">Prize distribution: the full photographs</h2>
{p('Three complete photographs of the same prize distribution. The two wide pictures above are narrow strips of two of them.')}
{gallery('../', ['iti_dsc1', 'iti_dsc2', 'iti_dsc3'])}
'''
ITI_CONTACT = f'''{facts(('Campus', 'On the 27th km off the Bangalore–Mysore Highway (near Wonder La Amusement Park), Shikshanagar'), ('Bus routes', 'Nos. 226 (A to H) at Wonder-la Gate; 2 km from Bidadi Railway Station; 1 km from Hejjala Railway Station'), ('Trust office', f'{ADDR} · {ADMIN}'), ('Email', EMAIL))}
'''
SIBLINGS['ITI'] = dict(name='Industrial Training Institute (ITI)', nav=iti_nav, pages={
    'home.html': ('Welcome to Jame-ul-Uloom Industrial Training Institute (ITI)', ITI_HOME),
    'Message.html': ('Vision, Mission & Message — ITI', ITI_MESSAGE),
    'Admissions.html': ('Admissions — ITI', ITI_ADM),
    'Staff.html': ('Staff — ITI', ITI_STAFF_HTML),
    'Management.html': ('Management — ITI', ITI_MGMT),
    'Workshops.html': ('Workshops — ITI', ITI_WORK),
    'Library&CompLab.html': ('Library & Computer Lab — ITI', ITI_LIB),
    'Sports.html': ('Sports — ITI', ITI_SPORTS),
    'Contact.html': ('Location & Contact — ITI', ITI_CONTACT)})
REDIRECTS.update({'ITI/ITIStaff.html': 'ITI/Staff.html', 'ITI/ITITeam.html': 'ITI/Management.html', 'ITI/Team.html': 'Team.html', 'ITI/Trustees.html': 'Trustees.html',
                  'ITI/FittersLab.html': 'ITI/Workshops.html#fitter', 'ITI/MMVLab.html': 'ITI/Workshops.html#mmv', 'ITI/MRACLab.html': 'ITI/Workshops.html#mrac',
                  'ITI/Annualday.html': 'Activities.html', 'ITI/Careers.html': 'ITI/Contact.html'})

# =====================================================================================================================
# PU COLLEGE
# =====================================================================================================================
PU_HISTORY = ('“Jame-ul-uloom” means center of knowledge. Jame-ul-uloom Institutions are managed by the Jamia Masjid and Muslim Charitable Fund trust. The goal of the management is to establish a trust to provide a nurturing ground for the student’s holistic development, so that she can make effective contribution to the society in today’s dynamic environment. '
              'The movement began with the establishment of Jame-ul-uloom primary school during the year 1982-83 with a major strength. It was followed by the establishment of high school in the year 1990-91. As the primary and high school witnessed steady growth, the management of the trust decided to establish a pre university college during the year 1995-96 with commerce combination; during the next academic year a science section with PCMB combination was also introduced.')
PU_HISTORY2 = ('Since its inception the college is under steady progress with number of admissions increasing yearly. The improvement in the 2nd PU board examination pass percentage is also witness to the steady progress of the institute.')
PU_HISTORY3 = ('Finances amounting to several lakhs were required to equip the laboratory, library, college furniture etc. But experience has proved more than once that the Secretary, Jame-ul-uloom accepts such challenges and pushes forward and he has always been successful in his endeavor. The college has strength of 150 girls and it is running very smoothly and successfully. The parents are quite happy with the affairs. '
               'Again to encourage and appreciate the outstanding girls a fabulous rolling cup is instituted in the name of late Janab Abdul Azeez and awarded to the highest marks scoring girls at the II PUC examination.')
pu_nav = [('Overview', 'home.html'), ('Principal', 'Message.html'), ('Admissions', 'Admissions.html'), ('Staff', 'Staff.html'), ('Facilities', 'Facilities.html'), ('Rules', '../CollegeRegulations.html'), ('Contact', 'Contact.html'), ALL]
PU_HOME = f'''{logo('../', 'logo_pu')}
{split(p(PU_HISTORY, PU_HISTORY2, PU_HISTORY3) + dated('<strong>Dated text.</strong> “Strength of 150 girls” and the other figures are those of the time this text was written.')
        + '<p class="rc-sign">Dr. Bazigah Heal (M.Sc, PhD)<small>Principal</small></p>',
       single('../', 'pu_school', caption='Pre University College', detail='Group photographs from a college function.'))}
{facts(('Address', ADDR), ('Administrative Office', ADMIN), ('P.U. Block', '<a href="tel:0826705591">0826705591</a>, <a href="tel:0826705486">0826705486</a>'), ('Email', EMAIL))}
<p>Aims, mission and vision are on the shared <a href="../Colleges.html">Colleges</a> page.</p>'''
PU_MSG = f'''{split('<p>The college’s aims and mission, shared by the PU, Degree and BCA colleges, are on the <a href="../Colleges.html">Colleges: Aims, Mission &amp; Vision</a> page.</p><p class="rc-sign">Dr. Bazigah Heal (M.Sc, PhD)<small>Principal</small></p>', single('../', 'pu_prin', caption='Principal, Pre University College for Girls'))}'''
PU_ADM = f'''<h2>Combinations offered</h2>
<ul><li><strong>Part 1 – Languages:</strong> A – English (compulsory); B – Urdu / Hindi / Kannada.</li><li><strong>Part 2 – Optional:</strong> A – Physics, Chemistry, Maths, Biology; B – Economics, Business Studies, Accountancy, Computer Science.</li></ul>
<h2>Fee structure</h2>
<p>Despite being an unaided institution the fee structure in comparison to other colleges is very nominal.</p>
{table(['Combination', 'Fee'], [['PCMB', '8280/- per year'], ['EBs ACs (Economics, Business Studies, Accountancy, Computer Science)', '7335/- per year']])}
{dated('<strong>Dated fees.</strong> These amounts are not current: please ask the college office for this year’s fees.')}
<p>The fee should be paid within the stipulated date; fee once paid will not be refunded.</p>
<h2>Eligibility for admissions</h2>
<p>Admission to the Karnataka two years pre-university course shall be open to the candidates who have passed (a) the Karnataka secondary school leaving certificate examination, or any other examination recognized by the board as equivalent to the Karnataka SSLC. (b) Students who have scored good marks in the qualifying examination are encouraged to opt for the PCMB combination.</p>
{ADMISSION_PROCEDURE}'''
PU_STAFF = f'''{split(p('To strengthen the teaching and learning process, well qualified, talented and experienced teaching faculty is appointed. The college is headed by a highly qualified and experienced principal with good leadership qualities and with a vision to meet the challenges of the present competitive atmosphere.') + '',
       single('../', 'pu_staff', caption='PUC staff members with Principal'))}
<h2 id="names">Names of the faculty</h2>
<p class="rc-quote-plain">“Sitting L to R; R.Zuberunnisa, Zohra Banu, Dr. Bazigah Heal (Principal) Fahmeedunnisa, Mamta L. Almel., Standing L to R: Nousheen Fathima, Thaseen Banu, Sunitha, Naheeda Kousar, Ayesha Bi.,”</p>
'''
PU_FAC = f'''<h2>The college building</h2>
{p(COLLEGE_BUILDING)}
{COLLEGE_DATED}
<h2>Classrooms</h2>
{p('Jame-ul-uloom PU College ' + CLASS_DICTUM)}
{gallery('../', ['cls1', 'cls2', 'cls3'])}
<h2>Science laboratories</h2>
{gallery('../', ['pu_lab1', 'pu_lab2'], cls='rc-wide')}
<h2>Computer laboratory</h2>
{gallery('../', ['col_comp2'])}
<h2>Library</h2>
{gallery('../', ['col_lib2'])}
{SHARED_SPORTS('PU College')}'''
SIBLINGS['PUGirlsCollege'] = dict(name='Pre University College for Girls', nav=pu_nav, pages={
    'home.html': ('Pre University College for Girls', PU_HOME),
    'Message.html': ('Principal — Pre University College for Girls', PU_MSG),
    'Admissions.html': ('Admissions — Pre University College for Girls', PU_ADM),
    'Staff.html': ('Faculty — Pre University College for Girls', PU_STAFF),
    'Facilities.html': ('Facilities — Pre University College for Girls', PU_FAC),
    'Contact.html': ('Contact — Pre University College for Girls', facts(('Address', ADDR), ('Administrative Office', ADMIN), ('P.U. Block', '<a href="tel:0826705591">0826705591</a>, <a href="tel:0826705486">0826705486</a>'), ('Email', EMAIL))),
    'Careers.html': ('Careers — Pre University College for Girls', careers_page())})
REDIRECTS.update({f'PUGirlsCollege/{n}.html': 'PUGirlsCollege/Facilities.html' + a for n, a in [('Classroom', '#classrooms'), ('Library', '#library'), ('ComputerLab', '#computer-laboratory'), ('ScienceLabs', '#science-laboratories')]})
REDIRECTS.update({'PUGirlsCollege/Regulations.html': 'CollegeRegulations.html', 'PUGirlsCollege/Sports.html': 'Sports.html', 'PUGirlsCollege/Masjid.html': 'Masjid.html',
                  'PUGirlsCollege/Team.html': 'Team.html', 'PUGirlsCollege/Trustees.html': 'Trustees.html'})

# =====================================================================================================================
# DEGREE COLLEGE (B.Com) and BCA — same principal; photographs and the staff list are shared between the two colleges
# =====================================================================================================================
deg_nav = [('Overview', 'home.html'), ('Principal', 'Message.html'), ('Admissions', 'Admissions.html'), ('Staff', 'Staff.html'), ('Facilities', 'Facilities.html'), ('Rules', '../CollegeRegulations.html'), ('Contact', 'Contact.html'), ('Careers', 'Careers.html'), ALL]
DEG_HOME = f'''{logo('../', 'logo_bcom')}
{split(p('The history of the college (the PU College’s years, its “150 girls” and its II PUC rolling cup) is on the <a href="../PUGirlsCollege/home.html">Pre University College page</a>.',
         'The page is signed by the Principal of the Degree and BCA colleges:') + '<p class="rc-sign">Miss Farzana Fathima (M.C.A)<small>Principal, Degree College</small></p>',
       single('../', 'deg_prin', caption='Principal, Degree and BCA colleges'))}
{facts(('Programme', 'Bachelor of Commerce (B.Com) for women'), ('Address', ADDR), ('Administrative Office', ADMIN), ('Degree College', '<a href="tel:0826709915">0826709915</a>'), ('Email', EMAIL))}
<p>Aims, mission and vision are on the shared <a href="../Colleges.html">Colleges</a> page.</p>'''
DEG_MSG = f'''{split('<p>The aims and mission common to the PU, Degree and BCA colleges are on the <a href="../Colleges.html">Colleges: Aims, Mission &amp; Vision</a> page.</p><p class="rc-sign">Miss Farzana Fathima (M.C.A)<small>Principal, Degree College</small></p>', single('../', 'deg_prin', caption='Principal, Degree and BCA colleges'))}'''
DEG_ADM = f'''<h2>Combinations offered</h2>
<p>Bachelor of Commerce (B.Com).</p>
<h2>Fee structure</h2>
<p>Despite being an unaided institution the fee structure in comparison to other colleges is very nominal. The fee should be paid within the stipulated date; fee once paid will not be refunded. For fee structure and eligibility, please ask the college office.</p>
{ADMISSION_PROCEDURE}
{note('The procedure above is the Pre-University procedure (it refers to the P.U Board and the P.U.C board). Please ask the college office for the university’s own requirements.')}'''
DEG_STAFF = f'''{split(p('To strengthen the teaching and learning process, well qualified, talented and experienced teaching faculty is appointed. The college is headed by a highly qualified and experienced principal with good leadership qualities and with a vision to meet the challenges of the present competitive atmosphere.') + '',
       single('../', 'deg_staff', caption='Faculty of the Degree and BCA colleges'))}
{single('../', 'deg_staff_names', caption='Names of the faculty in the photograph', extra_cls='rc-big')}
<h2 id="names">Names of the faculty</h2>
<p class="rc-quote-plain">“Sitting L to R: Nibeditha Patel, Hashmath Sadia, Farzana Fathima (Principal) Shahnaz Begum, Nazia Munir<br>Standing L to R: Mubashirunnisa, Sunitha, Tahseen Begum, Tahseen Begum”</p>
'''
DEG_FAC = f'''<h2>The college building</h2>
{p(COLLEGE_BUILDING)}
{COLLEGE_DATED}
<h2>Classrooms</h2>
{p('Jame-ul-uloom Degree College ' + CLASS_DICTUM)}
{gallery('../', ['deg_cls1', 'deg_cls2'])}
<h2>Computer laboratory</h2>
{gallery('../', ['col_comp'])}
<h2>Library</h2>
{gallery('../', ['col_lib'])}
{SHARED_SPORTS('Degree College')}'''
SIBLINGS['DegreeGirlsCollege'] = dict(name='Degree College for Girls (B.Com)', nav=deg_nav, pages={
    'home.html': ('Degree College for Girls (B.Com)', DEG_HOME),
    'Message.html': ('Principal — Degree College for Girls', DEG_MSG),
    'Admissions.html': ('Admissions — Degree College for Girls (B.Com)', DEG_ADM),
    'Staff.html': ('Faculty — Degree College for Girls', DEG_STAFF),
    'Facilities.html': ('Facilities — Degree College for Girls', DEG_FAC),
    'Contact.html': ('Contact — Degree College for Girls', facts(('Address', ADDR), ('Administrative Office', ADMIN), ('Degree College', '<a href="tel:0826709915">0826709915</a>'), ('Email', EMAIL))),
    'Careers.html': ('Careers — Degree College for Girls', careers_page())})
REDIRECTS.update({f'DegreeGirlsCollege/{n}.html': 'DegreeGirlsCollege/Facilities.html' + a for n, a in [('Classroom', '#classrooms'), ('Library', '#library'), ('ComputerLab', '#computer-laboratory')]})
REDIRECTS.update({'DegreeGirlsCollege/Regulations.html': 'CollegeRegulations.html', 'DegreeGirlsCollege/Sports.html': 'Sports.html', 'DegreeGirlsCollege/Masjid.html': 'Masjid.html',
                  'DegreeGirlsCollege/Team.html': 'Team.html', 'DegreeGirlsCollege/Trustees.html': 'Trustees.html'})
REMOVE += ['DegreeGirlsCollege/Masjid.html']

bca_nav = [('Overview', 'home.html'), ('Principal', 'Message.html'), ('Admissions', 'Admissions.html'), ('Staff', 'Staff.html'), ('Facilities', 'Facilities.html'), ('Rules', '../CollegeRegulations.html'), ('Contact', 'Contact.html'), ('Careers', 'Careers.html'), ALL]
BCA_HOME = f'''{logo('../', 'logo_bca')}
{split(p('Starting of Bachelor of Computer Application is yet another landmark in the annals of the history of Jame-ul-uloom. It involved several lakhs of rupees to provide the required infrastructure, well furnished accommodation, a standard library and latest units of computers for the purpose. These days everyone talks of importance of computer in every walk of life.',
         'If computer is nucleus, information technology revolves round the nucleus. Life minus the computer education is vacuum. Hence the trustees endeavored to start the BCA College in a well-guarded environment, as its very cause is basically for the benefit of the girls. This college is located in a spacious building at an arm’s length from the Jamia Mosque; Jame-ul-uloom institutions never mean commercialization. Hence the fee charged for the BCA will be very reasonable, within the reach of the average income group.')
        + '<p class="rc-sign">Miss Farzana Fathima (M.C.A)<small>Principal, BCA Degree College</small></p>',
       single('../', 'deg_prin', caption='Principal, Degree and BCA colleges'))}

{facts(('Address', ADDR), ('B.C.A. Office', '<a href="tel:0826709915">0826709915</a>'), ('Head Office', ADMIN), ('Email', EMAIL))}
<p>Aims, mission and vision are on the shared <a href="../Colleges.html">Colleges</a> page.</p>'''
BCA_ADM = f'''{note('The combinations listed here are those of the B.Com programme. For BCA combinations, fees and eligibility, please ask the college office (<a href="tel:0826709915">0826709915</a>) for BCA requirements.')}
<h2>Combinations offered</h2>
<p>Bachelor of Commerce (B.Com).</p>
<h2>Fee structure</h2>
<p>Despite being an unaided institution the fee structure in comparison to other colleges is very nominal. The fee should be paid within the stipulated date; fee once paid will not be refunded.</p>
{ADMISSION_PROCEDURE}'''
BCA_FAC = f'''<h2>The college building</h2>
{p(COLLEGE_BUILDING)}
{COLLEGE_DATED}
<h2>Classrooms</h2>
{p('Jame-ul-uloom Degree College ' + CLASS_DICTUM)}
{gallery('../', ['bca_cls', 'bca_cls2'])}

<h2>Computer laboratory</h2>
{gallery('../', ['col_comp'])}
<h2>Library</h2>
{gallery('../', ['col_lib'])}
{SHARED_SPORTS('BCA')}'''
SIBLINGS['BCA'] = dict(name='Degree College for Girls (B.C.A)', nav=bca_nav, pages={
    'home.html': ('Degree College for Girls (B.C.A)', BCA_HOME),
    'Message.html': ('Principal — BCA Degree College', DEG_MSG),
    'Admissions.html': ('Admissions — Degree College for Girls (B.C.A)', BCA_ADM),
    'Staff.html': ('Faculty — Degree College for Girls (B.C.A)', DEG_STAFF),
    'Facilities.html': ('Facilities — Degree College for Girls (B.C.A)', BCA_FAC),
    'Contact.html': ('Contact — Degree College for Girls (B.C.A)', facts(('Address', ADDR), ('Head Office', ADMIN), ('Degree College', '<a href="tel:0826709915">0826709915</a>'), ('Email', EMAIL))),
    'Careers.html': ('Careers — Degree College for Girls (B.C.A)', careers_page())})
REDIRECTS.update({f'BCA/{n}.html': 'BCA/Facilities.html' + a for n, a in [('Classroom', '#classrooms'), ('Library', '#library'), ('ComputerLab', '#computer-laboratory')]})
REDIRECTS.update({'BCA/Regulations.html': 'CollegeRegulations.html', 'BCA/Sports.html': 'Sports.html', 'BCA/Masjid.html': 'Masjid.html', 'BCA/Team.html': 'Team.html', 'BCA/Trustees.html': 'Trustees.html'})

# =====================================================================================================================
# NCPUL
# =====================================================================================================================
ncp_nav = [('Overview', 'home.html'), ('Admissions & Course', 'Admissions.html'), ('Support', 'Support.html'), ('Library', 'Library.html'), ('Facilities', 'Facilities.html'), ('Staff', 'Staff.html'), ('Awards', 'Awards.html'), ('Rules', '../CollegeRegulations.html'), ALL]
NCP_HOME = f'''{logo('../', 'logo_ncpul')}
{p('The National Council for the Promotion of Urdu Language is an autonomous organisation under the Ministry of Human Resource Development, Govt. of India. Initially it promoted the establishment of Urdu calligraphy centres. But with the advent of Urdu software, computers took the place of calligraphy. Considering the limited usage of Urdu software, a composite programme of Urdu &amp; English DTP was introduced about 11 years ago.',
   'NCPUL supports organisations which can establish centres, with hardware and software technical know-how and financial assistance.',
   'Majlis-e-Millia Islamia is a social welfare organisation and is serving the community in the field of education, health and social activities. One among these is the MMI-NCPUL COMPUTER CENTRE. It was established in the year 1999.',
   'This centre was established mainly for the benefit of girls. Such of those who have passed or studied up to 10th standard are eligible for admission.',
   'The MMI-NCPUL COMPUTER CENTRE has been set up with the objective of promoting, developing and propagating the Urdu language and linking the language with Information Technology. However its activities were diversified by inclusion of useful DTP application of English.')}
{dated('“About 11 years ago” is relative to when this text was written; the centre was founded in 1999.')}
{facts(('Telephone', '<a href="tel:0822221158">0822221158</a> · JUU Computer Section: <a href="tel:0822221161">0822221161</a>'), ('Address', ADDR))}'''
NCP_ADM = f'''<h2>Fee structure</h2>
{p('As per the scheme, admission fee of Rs. 1000/- and a monthly fee of Rs. 500/- is to be collected from the students. As Majlis-e-Millia is a social organisation in the service of community, it is collecting a monthly fee of Rs. 250/- only.',
   'A corpus fund is maintained from the fee collection, which is utilised for augmenting computers, UPS and meeting other maintenance expenses.',
   'Despite being an unaided institution the fee structure in comparison to other colleges is very nominal. The fee should be paid within the stipulated date; fee once paid will not be refunded.')}
{dated('<strong>Dated fees.</strong> These amounts are not current fees; please ask the office.')}
<h2>Course</h2>
{p('The total duration of the course is 1000 hrs spreading over a period from July to June. The intake is 60 students per year. It will be in two batches of 30 students. Course duration is three hours daily for each batch. Out of these three hours, one and a half hours for theory and one and a half hours for practicals.',
   'The course has been structured as follows.')}
<div class="rc-twocol"><div><h3>Module I – Information Technology</h3><ul><li>Computer fundamentals</li><li>Computer organisation</li><li>Operating System concept</li><li>Office Automation Tool (MS Office)</li><li>IT application</li></ul>
<h3>Module II – Business System</h3><ul><li>Introduction to Business Data Processing</li><li>Fundamentals of Programming</li><li>MS Access</li><li>Accounting Fundamentals</li><li>Account application: Tally</li></ul>
<h3>Module III – Web Application Development</h3><ul><li>Introduction to internet</li><li>World Wide Web</li><li>Browsers</li><li>FTP</li><li>HTML</li><li>FrontPage</li><li>JavaScript</li><li>Graphic tools (Adobe Photoshop)</li></ul></div>
<div><h3>Module IV – Programming through Visual Basic</h3><ul><li>Integrated Development Environment</li><li>Managing Projects</li><li>Visual Basic programming elements</li><li>Working with Form</li><li>ActiveX controls</li><li>Graphic with Visual Basic</li><li>Multiple Documents Interface</li><li>Error Handling</li><li>Windows API &amp; DLL</li><li>Database programming with Visual Basic</li></ul>
<h3>Module V – Multilingual DTP</h3><ul><li>Urdu and English DTP</li><li>PageMaker</li><li>CorelDraw</li></ul>
<h3>Module VI – Project work</h3><ul><li>The project prepared by the students shall be examined by the external examiner.</li></ul></div></div>
<p>Rules and regulations are on the shared <a href="../CollegeRegulations.html">College Rules</a> page.</p>'''
NCP_SUP = f'''<h2>Financial assistance</h2>
{p('Initially NCPUL provided six computers, one mono printer, one colour printer and a scanner. Majlis-e-Millia Islamia provided necessary appurtenance required for the Centre. Later the systems were upgraded with new Pentium IV computers.',
   'Financial assistance to the extent of Rs. 85,000 is provided by the NCPUL annually towards salaries of the Supervisor and an attender, and salaries of the other two members of faculty are paid through their agent Kathuria Information Technology.')}
{dated('These are the arrangements of the time this text was written.')}'''
NCP_LIB = f'''{p('The Centre has built up a library. The books are mainly on the subjects of computer science for the benefit of reference of students. Presently it has over 500 books of reputed authors.')}
'''
NCP_FAC = f'''<h2>Classroom</h2>
{gallery('../', ['ncpul_cls'])}
<h2>Computer laboratory</h2>
{gallery('../', ['ncpul_lab1', 'ncpul_lab2'], cls='rc-wide')}
<p>Masjid photographs are on the <a href="../Masjid.html">Jamia Masjid</a> page.</p>'''
SIBLINGS['NCPUL'] = dict(name='MMI-NCPUL Computer Centre', nav=ncp_nav, pages={
    'home.html': ('MMI-NCPUL Computer Centre', NCP_HOME),
    'Admissions.html': ('Admissions & Course — MMI-NCPUL Computer Centre', NCP_ADM),
    'Support.html': ('Financial Assistance — MMI-NCPUL Computer Centre', NCP_SUP),
    'Library.html': ('Library — MMI-NCPUL Computer Centre', NCP_LIB),
    'Facilities.html': ('Facilities — MMI-NCPUL Computer Centre', NCP_FAC),
    'Staff.html': ('Staff — MMI-NCPUL Computer Centre', f'''{single('../', 'ncpul_staff', caption='Staff members')}'''),
    'Awards.html': ('Awards — MMI-NCPUL Computer Centre', f'''{single('../', 'ncpul_aw', big=True, caption='Certificate presentation')}''')})
REDIRECTS.update({'NCPUL/Message.html': 'NCPUL/Support.html', 'NCPUL/Classroom.html': 'NCPUL/Facilities.html#classroom', 'NCPUL/ComputerLab.html': 'NCPUL/Facilities.html#computer-laboratory',
                  'NCPUL/Regulations.html': 'CollegeRegulations.html', 'NCPUL/Sports.html': 'Activities.html', 'NCPUL/Masjid.html': 'Masjid.html', 'NCPUL/Careers.html': 'Careers.html',
                  'NCPUL/Contact.html': 'NCPUL/home.html', 'NCPUL/Team.html': 'Team.html', 'NCPUL/Trustees.html': 'Trustees.html'})

# =====================================================================================================================
# ENGLISH SCHOOLS
# =====================================================================================================================
nur_nav = [('Overview', 'home.html'), ('Staff', 'Staff.html'), ('Facilities', 'Facilities.html'), ('Contact', 'Contact.html'), ALL]
NUR_HOME = f'''{logo('../', 'logo_ens')}
{split(p('Starting of nursery school was the first step of endeavour in the field of education. It took its birth in the year 1984 with just 2 pupils in a thatched structure. It was an eventful beginning. The architects of the endeavour were the trustees of the Institution and Moulana Riyazur Rahman Rashadi Saheb, the Principal. The Institution continued to expand by leaps and bounds. Now the strength has grown to around 500; special attention is given for punctuality and cleanliness. Moral Education commences from this stage. The pupils start learning Hadiths from this stage.'),
        single('../', 'nur_group', caption='English Nursery School'))}
{dated('<strong>Dates differ between pages.</strong> This page gives 1984 for the start of the nursery; the Founder Secretary’s essay gives 1986 and the Admissions Diary 1983-84. “Around 500” pupils is the figure of the time of writing.')}
{gallery('../', ['act_nur2', 'act_nur3'])}'''
NUR_STAFF = f'''<p>{STAFF_LINE}</p>'''
NUR_FAC = f'''<h2>Classrooms</h2>
{p('Jame-ul-uloom Boys Residential School believes in the following dictum delivering the lessons “I HEAR, I FORGET, I SEE, I RECALL, I DO, I UNDERSTAND.” All teachers endeavor to prepare their lessons and deliver them in such a way that the child becomes a participant in the learning process. The lessons are complimented by practical sessions and access of information on the internet. A total holistic approach is adopted to remove the burden of learning and make the process of learning a joyful experience without hang-ups and hiccups. The lessons are delivered in the class room by using state of the art audio visual equipment such as overhead projectors and LCD projectors.')}
{note('This paragraph describes the Residential School at Banikuppa. It is also on the <a href="../ResidentialSchoolBanikuppa/classroom.html">Banikuppa Classroom page</a>. The institutions’ smart classrooms are described on the <a href="../Classroom.html">Smart Classrooms</a> page.')}
<h2>Library</h2>
<p>Computer education at the school:</p>
{p(COMPUTER_EDU)}
{SHARED_SPORTS('Nursery School')}'''
NUR_CONTACT = f'''{facts(('Address', ADDR), ('Head Mistress', '<a href="tel:0822221156">0822221156</a>'), ('Administrative Office', ADMIN), ('Email', EMAIL))}
'''
SIBLINGS['EngNurSchoolDEL'] = dict(name='English Nursery School', nav=nur_nav, pages={
    'home.html': ('English Nursery School', NUR_HOME),
    'Staff.html': ('Staff — English Nursery School', NUR_STAFF), 'Facilities.html': ('Facilities — English Nursery School', NUR_FAC), 'Contact.html': ('Contact — English Nursery School', NUR_CONTACT)})
REDIRECTS.update({'EngNurSchoolDEL/Classroom.html': 'EngNurSchoolDEL/Facilities.html#classrooms', 'EngNurSchoolDEL/Library.html': 'EngNurSchoolDEL/Facilities.html#library',
                  'EngNurSchoolDEL/Sports.html': 'Sports.html', 'EngNurSchoolDEL/Careers.html': 'EngNurSchoolDEL/Contact.html', 'EngNurSchoolDEL/Team.html': 'Team.html', 'EngNurSchoolDEL/Trustees.html': 'Trustees.html',
                  'InsNursery.html': 'EngNurSchoolDEL/home.html'})

pri_nav = [('Overview', 'home.html'), ('Staff', 'Staff.html'), ('Facilities', 'Facilities.html'), ('Contact', 'Contact.html'), ALL]
PRI_HOME = f'''{logo('../', 'logo_ehps')}
{split(p('Primary school runs in the main block of the school from 1st standard to VII standard; it has three sections in each class and total strength is 1000. Every year we get 100% result at VII standard public examination with a number of 1st classes. The good performance at the examination is a result of the able guidance of the management and hard work of the members of the staff of the Institution. This has attracted many pupils from far off places of the city. Thirty qualified, experienced and dedicated teachers are engaged for the primary section. A rolling cup instituted in the name of Mr C.M. Aleemulla Khan is awarded to the highest marks scoring girl at the VII standard Public Examination. Library and laboratory facilities are provided to the students. Girls participate in the indoor games within campus.'),
        single('../', 'hp_group', caption='English Higher Primary School'))}
{dated('Strength (1000), number of teachers (thirty) and results are of the time of writing and are not current figures.')}
<p class="rc-sign">Naveeda Naaz (M.A, B.Sc, B.Ed)<small>Head Mistress</small></p>'''
PRI_FAC = f'''<h2>Library</h2>
<p>Computer education at the school:</p>
{p(COMPUTER_EDU)}
<h2>Classrooms</h2>
<p>The classroom paragraph is on the <a href="../ResidentialSchoolBanikuppa/classroom.html">Banikuppa Classroom page</a>. The smart classrooms are described on <a href="../Classroom.html">Smart Classrooms</a>.</p>
{SHARED_SPORTS('Higher Primary School')}'''
SIBLINGS['EngPrimarySchoolDEL'] = dict(name='English Higher Primary School', nav=pri_nav, pages={
    'home.html': ('English Higher Primary School', PRI_HOME),
    'Staff.html': ('Staff — English Higher Primary School', NUR_STAFF), 'Facilities.html': ('Facilities — English Higher Primary School', PRI_FAC),
    'Contact.html': ('Contact — English Higher Primary School', NUR_CONTACT)})
REDIRECTS.update({'EngPrimarySchoolDEL/Classroom.html': 'EngPrimarySchoolDEL/Facilities.html#classrooms', 'EngPrimarySchoolDEL/Library.html': 'EngPrimarySchoolDEL/Facilities.html#library',
                  'EngPrimarySchoolDEL/Sports.html': 'Sports.html', 'EngPrimarySchoolDEL/Careers.html': 'EngPrimarySchoolDEL/Contact.html', 'EngPrimarySchoolDEL/Team.html': 'Team.html',
                  'EngPrimarySchoolDEL/Trustees.html': 'Trustees.html', 'InsHPrimarySc.html': 'EngPrimarySchoolDEL/home.html'})

gh_nav = [('Overview', 'home.html'), ('Staff', 'Staff.html'), ('Facilities', 'Facilities.html'), ('Contact', 'Contact.html'), ('Careers', 'Careers.html'), ALL]
GH_HOME = f'''{logo('../', 'logo_eghs')}
{split(p('The starting of a girls high school was necessitated by the good response we got from the parents and pupils at the primary level. A high school for girls was started in 1990-91 with a strength of 13 girls only. The strength is growing every year. At present the strength is around 400. Eight batches took the X standard examination, of which 5 batches gave 100% results. In 1999-2000, 104 pupils appeared. All of them were successful in the examination with 2 students getting distinction, 79 getting I class and the rest II class.', SSLC_PARA),
        single('../', 'girls_group', caption='English Girls High School'))}
{dated('<strong>Dated figures.</strong> Strengths and results are those of the time this text was written (the last result quoted is for 1999-2000) and are not current. The Admissions Diary 2013–14 (<a href="../AdmissionsDiary.html">here</a>) quotes later SSLC results.')}
<p class="rc-sign">Naveeda Naaz (M.A, B.Sc, B.Ed)<small>Head Mistress</small></p>
'''
GH_STAFF = f'''<p>{STAFF_LINE}</p>
{gallery('../', ['school_staff', 'school_staff2'], captions={'school_staff': 'Staff of the English High Schools', 'school_staff2': 'Staff of the English Girls High School'})}
'''
GH_FAC = f'''<h2>Classrooms</h2>
{p('Jame-ul-uloom Boys Residential School believes in the following dictum delivering the lessons “I HEAR, I FORGET, I SEE, I RECALL, I DO, I UNDERSTAND.” All teachers endeavor to prepare their lessons and deliver them in such a way that the child becomes a participant in the learning process. The lessons are complimented by practical sessions and access of information on the internet. A total holistic approach is adopted to remove the burden of learning and make the process of learning a joyful experience without hang-ups and hiccups. The lessons are delivered in the class room by using state of the art audio visual equipment such as overhead projectors and LCD projectors.')}

{gallery('../', ['girls_cls'])}
<h2>Computer laboratory</h2>
{p(COMPUTER_EDU)}
{gallery('../', ['girls_comp'])}
<h2>Library</h2>


{SHARED_SPORTS('High School')}'''
SIBLINGS['EngGirlsHighSchool'] = dict(name='English Girls High School', nav=gh_nav, pages={
    'home.html': ('English Girls High School', GH_HOME),
    'Staff.html': ('Staff — English Girls High School', GH_STAFF), 'Facilities.html': ('Facilities — English Girls High School', GH_FAC),
    'Contact.html': ('Contact — English Girls High School', facts(('Address', ADDR), ('Administrative Office', ADMIN), ('Girls Block', '<a href="tel:0822221156">0822221156</a>'), ('Email', EMAIL))),
    'Careers.html': ('Careers — English Girls High School', careers_page())})
REDIRECTS.update({f'EngGirlsHighSchool/{n}.html': 'EngGirlsHighSchool/Facilities.html' + a for n, a in [('Classroom', '#classrooms'), ('Library', '#library'), ('ComputerLab', '#computer-laboratory'), ('ScienceLabs', '#library')]})
REDIRECTS.update({'EngGirlsHighSchool/Sports.html': 'Sports.html', 'EngGirlsHighSchool/Masjid.html': 'Masjid.html', 'EngGirlsHighSchool/Team.html': 'Team.html', 'EngGirlsHighSchool/Trustees.html': 'Trustees.html'})
REMOVE += ['EngGirlsHighSchool/Masjid.html']

bh_nav = [('Overview', 'home.html'), ('Staff', 'Staff.html'), ('Facilities', 'Facilities.html'), ('Contact', 'Contact.html'), ('Careers', 'Careers.html'), ALL]
BH_HOME = f'''{logo('../', 'logo_ebhs')}
{split(p('While the secretary and the trustees are turning out a tireless service for the girls’ education, they do not leave the boys uncared for. They started a high school for boys separately at Ibrahim Ali Shah complex, S.P. Road. This high school is cut off from the girls’ high school for obvious reasons. The boys do not lag behind the girls in excellence, good behavior and discipline. The school building included a very well maintained auditorium; separate science laboratory and library are provided for the boys.'),
        single('../', 'boys_group', caption='English Boys High School'))}
<p class="rc-sign">Naveeda Naaz (M.A, B.Sc, B.Ed)<small>Head Mistress</small></p>
'''
BH_FAC = f'''<h2>Classrooms</h2>
{p('The classroom paragraph is on the <a href="../ResidentialSchoolBanikuppa/classroom.html">Banikuppa Classroom page</a>.')}
{gallery('../', ['boys_cls', 'boys_cls2'])}

<h2>Computer laboratory</h2>
{p(COMPUTER_EDU)}
<h2>Science laboratories</h2>
<p>Photographs of the Banikuppa campus laboratories: Chemistry (students conducting experiments under the guidance of subject teachers), Physics (students exhibiting an experiment to a guest from U.S.A.) and Biology (students conducting practicals using natural specimens). They are on the <a href="../ResidentialSchoolBanikuppa/laboratories.html">Banikuppa Science Laboratories page</a>.</p>
<h2>Library</h2>

{SHARED_SPORTS('Boys High School')}'''
SIBLINGS['EngBoysHighSchool'] = dict(name='English Boys High School', nav=bh_nav, pages={
    'home.html': ('English Boys High School', BH_HOME),
    'Staff.html': ('Staff — English Boys High School', GH_STAFF), 'Facilities.html': ('Facilities — English Boys High School', BH_FAC),
    'Contact.html': ('Contact — English Boys High School', facts(('Address', ADDR), ('Administrative Office', ADMIN), ('Boys Block', '<a href="tel:0822221726">0822221726</a>'), ('Email', EMAIL))),
    'Careers.html': ('Careers — English Boys High School', careers_page())})
REDIRECTS.update({f'EngBoysHighSchool/{n}.html': 'EngBoysHighSchool/Facilities.html' + a for n, a in [('Classroom', '#classrooms'), ('Library', '#library'), ('ComputerLab', '#computer-laboratory'), ('Laboratories', '#science-laboratories')]})
REDIRECTS.update({'EngBoysHighSchool/Sports.html': 'Sports.html', 'EngBoysHighSchool/Masjid.html': 'Masjid.html', 'EngBoysHighSchool/Team.html': 'Team.html', 'EngBoysHighSchool/Trustees.html': 'Trustees.html'})
REMOVE += ['EngBoysHighSchool/Masjid.html']

# =====================================================================================================================
# SHOBA-E-HIFZ and SHOBA-E-ALIMIYATH (J.U Darul Quran Arabic College)
# =====================================================================================================================
hifz_nav = [('Overview', 'home.html'), ('Proposed building', 'Proposed.html'), ('Contact', 'Contact.html'), ('Full text', '../Services.html#english'), ALL]
HIFZ_HOME = f'''{logo('../', 'logo_hifz')}
<p>What the Trust’s pages say about the Hifz section.</p>
{quote('In the year of 1986 there were two halls towards the western side of the Mosque which is earmarked for the Welfare of the Community; one more privileged achievement to exhibit our educational &amp; character building milestone was to start Hifz section for the guest of Hazarat Mohammed sal-allaha-o-Alaihi-o-salamm with boarding &amp; lodging to impart not only Religious education but also general education so as to pass 10th &amp; P.U Exams.', sign='Scanned English page', role='J.U Darul Quran Arabic College, Bangalore')}
{quote('In the Hifze Quran department boys and girls both are becoming Hafiz and Hafiza.', sign='Jame-ul-uloom, Jamia Masjid', role='A Revolutionary movement')}
{quote('About a dozen teachers including Hufaz and Moulvies are employed for the purpose.', sign='Jame-ul-uloom, Jamia Masjid')}
{dated('The first quotation gives 1986 for the start of the Hifz section; the years given on other pages of this website differ.')}
<p>The scanned English and Urdu pages are on the <a href="../Services.html">Services</a> page; the <a href="../ShobaeAlimiyathDel/home.html">Shoba-e-Alimiyath</a> and <a href="Proposed.html">proposed building</a> pages complete the set.</p>'''
HIFZ_PROPOSED = f'''<p>The architect’s drawing below, titled “Proposed J.U Darul Quran &amp; Arabic College, Bangalore”: front elevation and ground-floor plan.</p>
{single('../', 'dq_plan', big=True, caption='Proposed building: front elevation and ground-floor plan')}
{dated('A proposal drawing; it is not a photograph of a completed building.')}'''
SIBLINGS['ShobaehifzDel'] = dict(name='Shoba-e-Hifz', nav=hifz_nav, pages={
    'home.html': ('Shoba-e-Hifz', HIFZ_HOME), 'Proposed.html': ('Proposed Building — Shoba-e-Hifz', HIFZ_PROPOSED),
    'Contact.html': ('Contact — Shoba-e-Hifz', facts(('Address', ADDR), ('Jamia Masjid', '<a href="tel:0822239495">0822239495</a>'), ('Administrative Office', ADMIN), ('Email', EMAIL)))})
REDIRECTS.update({'ShobaehifzDel/AboutusEnglish.html': 'Services.html#english', 'ShobaehifzDel/AboutusUrdu.html': 'Services.html#urdu', 'ShobaehifzDel/Admissions.html': 'ShobaehifzDel/home.html',
                  'ShobaehifzDel/Staff.html': 'ShobaehifzDel/home.html', 'InsShobaehifz.html': 'ShobaehifzDel/home.html'})

alim_nav = [('Overview', 'home.html'), ('Proposed building', 'Proposed.html'), ('Contact', 'Contact.html'), ('Full text', '../Services.html#english'), ALL]
ALIM_HOME = f'''{logo('../', 'logo_alim')}
<p>What the Trust’s pages say about the <strong>J.U Darul Quran Arabic College, Bangalore</strong>:</p>
{quote('Now we pray with Almighty to all those who are actively involved in bringing up J.U Arabic College at Bannikuppe. This institution comes up very fast so as to serve the community in a big way.',
       'The management could succeed in getting 61 acres of land, which is 25kms away from the City Mosque at Bannikuppa, so that, a part of it can be rescued for Arabic Studies, in which the construction has already begun … to accommodate lecture hall. It accommodates Lecture Hall, Mosque, Library, Guest house &amp; a Kitchen, Computer center, Tailoring and calligraphy center.',
       sign='Scanned English page', role='J.U Darul Quran Arabic College, Bangalore')}
{dated('Construction progress, land area and distance are as stated on an undated page and differ from other pages of this website (for example 52 hectares / 27 km in the Founder Secretary’s essay).')}
<p>The complete scanned pages, with their typed English text, are on the <a href="../Services.html">Services</a> page. The <a href="Proposed.html">proposed building drawing</a> is on its own page.</p>'''
SIBLINGS['ShobaeAlimiyathDel'] = dict(name='Shoba-e-Alimiyath · J.U Darul Quran Arabic College', nav=alim_nav, pages={
    'home.html': ('Shoba-e-Alimiyath', ALIM_HOME), 'Proposed.html': ('Proposed Building — Shoba-e-Alimiyath', HIFZ_PROPOSED),
    'Contact.html': ('Contact — Shoba-e-Alimiyath', facts(('Address', ADDR), ('Jamia Masjid', '<a href="tel:0822239495">0822239495</a>'), ('Administrative Office', ADMIN), ('Email', EMAIL)))})
REDIRECTS.update({'ShobaeAlimiyathDel/AboutusEnglish.html': 'Services.html#english', 'ShobaeAlimiyathDel/AboutusUrdu.html': 'Services.html#urdu', 'ShobaeAlimiyathDel/Admissions.html': 'ShobaeAlimiyathDel/home.html',
                  'ShobaeAlimiyathDel/Staff.html': 'ShobaeAlimiyathDel/home.html', 'InsShobaeAlimiyath.html': 'ShobaeAlimiyathDel/home.html'})
REMOVE += ['InsShobaeAlimiyath.html']

# Other legacy root URLs
REDIRECTS.update({'Caligraphy.html': 'Calligraphy.html', 'ServicesEng.html': 'Services.html#english', 'ServicesUrdu.html': 'Services.html#urdu', 'Recognition.html': 'Recognitions.html',
                  'Institution.html': 'ITI/home.html', 'ScMasjid.html': 'Masjid.html'})
