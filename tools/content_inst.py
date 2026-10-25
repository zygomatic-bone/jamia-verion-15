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

# shared texts (each appears once in the original on several pages; shown here under the institution(s) it describes)
COLLEGE_BUILDING = ('The college is housed in a spacious building with well furnished and ventilated class rooms, well equipped laboratories and library with good collection of books. '
                    'Magazines and News papers are also subscribed for the benefit of the students. The computer lab is provided with internet facility. A spacious auditorium is also under construction. '
                    'We aim to provide canteen facility for our students. A nationalized bank (Canara Bank) is also located in the same building.')
COLLEGE_DATED = dated('The remarks that the auditorium is “under construction” and that a canteen is an aim describe the time the original text was written (undated); they are not a present-day statement.')
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
SHARED_SPORTS = lambda who: note(f'The original {who} “Sports” page repeated the Banikuppa Residential School’s co-curricular and sports text unchanged; it is now on the shared <a href="../Sports.html">Co-Curricular Activities &amp; Sports</a> page.')

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
{dated('<strong>As printed on the original page (undated).</strong> The page says the ITI “is in its 16th year of operation”; counting from the 1996 start, that places the text around 2012. Trade list, fees and staffing are those of that time.')}
<p>See the <a href="Message.html">vision, mission and message</a>, <a href="Admissions.html">trades and admissions</a>, <a href="Workshops.html">workshop photographs</a> and the <a href="Contact.html">location and contact</a> page.</p>'''
ITI_MESSAGE = f'''{split(
 '<h2>Our Vision</h2><p>To be a pioneer institution for technician development in vocational training.</p><h2>Our Mission</h2><p>To be a world class training institution, thus creating employment opportunities.</p>'
 + quote('Natural abilities are like natural plants, they need pruning by study.',
         'The Jame ul uloom ITI, which is in its 16th year of operation, has made tremendous progress in imparting quality education in the field of vocational training. At present there are six units running successfully with well qualified, dedicated and experienced teaching staff.',
         'The institute is equipped with the best infrastructural facilities, classrooms, laboratories and a library as per the guidelines issued by DGE&amp;T, New Delhi.',
         'After working in a world class multinational company with hands-on experience, selecting this institution is in the right direction; to join this esteemed institution is the correct decision and I am sure your hopes and ambitions will be fulfilled to your utmost satisfaction.',
         'I wish you the very best in your endeavors.')
 + '<p class="source-note">The message is unsigned on the original page, which shows the Principal’s photograph beside it; the ITI home page names Dr. Shamiulla as Principal.</p>',
 single('../', 'iti_prin', caption='Principal, ITI'))}'''
ITI_ADM = f'''<p class="source-note">Trade table as printed on the original ITI Admissions page. Figures are those of the time of writing (about 2012) and are not a current admissions notice.</p>
{table(['Name of trade under NCVT', 'Duration of training', 'Eligibility qualification', 'No. of units', 'Seating capacity per unit', 'Shifts running (I/II/III)', 'Total seating capacity'],
       [['FITTER', '2 Years', 'SSLC', '1+1', '21', '1+1', '42'], ['MRAC', '2 Years', 'SSLC', '1+1', '21', '1+1', '42'], ['MMV', '2 Years', 'SSLC', '1+1', '21', '1+1', '42']])}
<p>Selection options printed beneath the table: (a) by percentage of marks in the qualifying exam, (b) written test, (c) interview, (d) any other. The original does not say which applies.</p>
<h2>Schemes running in the institute (CTS and MES etc. under NCVT)</h2>
{table(['Name of the scheme', 'Total capacity', 'Duration'], [['Craftsmen Training Scheme', '63+63', '2 Years'], ['Modular Employable', '—', '—'], ['Other Schemes', '—', '—']])}
<p>MRAC = Mechanic Refrigeration &amp; Air Conditioning; MMV = Mechanic Motor Vehicle. Contact details are on the <a href="Contact.html">Contact</a> page.</p>'''
ITI_STAFF_HTML = f'''{dated('<strong>Staff statement of about 2012, as published on the original site.</strong> Names, designations, qualifications and joining dates are reproduced exactly as printed. Publication of this historical list has been approved by the website owner; the details may be out of date and have not been checked against any current record.')}
<p class="source-note">Heading as printed: “Jamia Masjid &amp; Muslim Charitable Fund Trust, N R Road, Bangalore 560002. Registration: V of 1939, III of 1904, dated 09-05-1940.” (The Trust’s other pages give the address as S.J.P. Road.)</p>
{table(['Sl. No.', 'Name', 'Designation', 'Qualification (Class X onwards)', 'Trade', 'Date of joining', 'Regular / Adhoc / Contract', 'CTI trained (Yes/No)'], [list(r) for r in ITI_STAFF])}
<h2 id="verify">Points that still need verification</h2>
<ul>
<li>The heading prints “N R Road”; every other page of the original gives S.J.P. Road. The Trust’s registration is printed as “V of 1939, III of 1904, dated 09-05-1940”; other pages give 1939 or 1936 (see <a href="../AboutUs.html">About Us</a>).</li>
<li>Rows 9 and 10 print their dates with slashes (02/04/2012) where the other rows use hyphens (dd-mm-yyyy); the original does not say whether 02/04/2012 is 2 April or 4 February.</li>
<li>The column headed “CTI trained (Yes/No)” contains “POT TRAINED” for rows 1 and 2, and “No” or “NO” for others; the original does not explain it. Rows 8 to 10 are blank in that column.</li>
<li>The abbreviations in the Designation, Qualification and Trade columns (JTO, NTC, NAC, DME, DEE, MMV, MRAC and the rest) are printed without explanation and are not expanded here.</li>
<li>The list is a statement of about 2012. Whether these persons are still employed, and in what roles, is not known.</li>
</ul>'''
ITI_MGMT = f'''<p class="source-note">As printed on the original “ITI Management” page, under the heading “Jamia Masjid &amp; Muslim Charitable Fund Trust, N R Road, Bangalore 560002, Registration: V of 1939, III of 1904, dated 09-05-1940”.</p>
{people([('Alhaj Maqbool Ahmed', 'President'), ('Alhaj A. Syed Murtuza Hussain @ Gufran', 'Vice President'), ('Alhaj Mohammed Ateeq Ahmed', 'Secretary'), ('Alhaj Noorul Ameen @ Anwar', 'Joint Secretary'), ('Mohammed Athiulla', 'Treasurer'), ('Syed Abdul Gafoor', 'Internal Auditor')])}
<p>The Trust’s Governing Body and Trustees are on the <a href="../Team.html">Governing Body</a> and <a href="../Trustees.html">Trustees</a> pages.</p>'''
ITI_WORK = f'''<p>The original ITI site had a page for each workshop. Photographs are shown whole, as on the original pages.</p>
<h2 id="fitter">Fitter workshop</h2>
{gallery('../', ['iti_fit1', 'iti_fit2', 'iti_fit3', 'iti_fit4'])}
<h2 id="mmv">Mechanic Motor Vehicle (MMV) laboratory</h2>
{gallery('../', ['iti_mmv'], cls='rc-wide')}
<h2 id="mrac">Mechanic Refrigeration &amp; Air Conditioning (MRAC) laboratory</h2>
<p>The original MRAC page held no text or photograph.</p>
<h2>ITI workshop</h2>
{gallery('../', ['iti_work'], cls='rc-wide')}
<h2 id="classroom">Classroom</h2>
{gallery('../', ['iti_cls'])}
{note('This photograph was in the ITI image folder of the original site (as “Classroom.jpg”), but no original ITI page displayed it. Which room or building it shows was not stated.')}'''
ITI_LIB = f'''<h2>Library</h2>
{p('Brief information on journals and books.', 'A well-furnished library with about 250 books is provided for staff and trainees for reference.', 'The library promotes the reading habit among trainees and helps them in their studies. Teaching aids like charts and models are also available in the library.')}
<h2>Computer Lab</h2>
{p('Brief information on hardware and software.', 'At present the institute has 6 systems with P3 configuration; steps have already been initiated to procure 15 systems with the latest configuration.')}
{dated('Numbers are as printed on the original page (about 2012) and are not current.')}'''
ITI_SPORTS = f'''<p>The original ITI “Sports” page held photographs only; they are shown here with the descriptions that can be seen in them. No dates or names were printed.</p>
{gallery('../', ['iti_play1', 'iti_play2', 'iti_play3'])}
<h2 id="prize-distribution">Prize distribution: the full photographs</h2>
{p('The ITI image folder of the original site also held three complete photographs of the same prize distribution. The two wide pictures above are narrow strips of two of them (the people, the blazers and the table of trophies match). Copies of the same three files also sat in the Shobae Alimiyath and Shobae Hifz image folders.')}
{gallery('../', ['iti_dsc1', 'iti_dsc2', 'iti_dsc3'])}
{note('No original page displayed these three files, and no date, place or names were printed with them. The captions describe only what can be seen. The camera’s time stamp is visible on two of them (12:33 PM and 3:57 PM) and is not a date.')}'''
ITI_CONTACT = f'''{facts(('Campus', 'On the 27th km off the Bangalore–Mysore Highway (near Wonder La Amusement Park), Shikshanagar'), ('Bus routes', 'Nos. 226 (A to H) at Wonder-la Gate; 2 km from Bidadi Railway Station; 1 km from Hejjala Railway Station'), ('Trust office', f'{ADDR} · {ADMIN}'), ('Email', EMAIL))}
<p class="source-note">The original ITI Contact and Careers pages held no text. The Trust office numbers are those of the central <a href="../Contact.html">contact directory</a>.</p>'''
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
{split(p(PU_HISTORY, PU_HISTORY2, PU_HISTORY3) + dated('<strong>Dated text.</strong> The page is undated: “strength of 150 girls” and the other figures are those of the time it was written. Years are quoted as printed.')
        + '<p class="rc-sign">Dr. Bazigah Heal (M.Sc, PhD)<small>Principal</small></p>',
       single('../', 'pu_school', caption='Pre University College', detail='Group photographs from a college function (original “School Photo”).'))}
{facts(('Address', ADDR), ('Administrative Office', ADMIN), ('P.U. Block', '<a href="tel:0826705591">0826705591</a>, <a href="tel:0826705486">0826705486</a>'), ('Email', EMAIL))}
<p>Aims, mission and vision are on the shared <a href="../Colleges.html">Colleges</a> page.</p>'''
PU_MSG = f'''{split('<p>The original PU College “Message” page shows the Principal’s photograph beside the college’s aims and mission. Those statements are identical on the PU, Degree and BCA college pages and are shown once on the <a href="../Colleges.html">Colleges: Aims, Mission &amp; Vision</a> page.</p><p class="rc-sign">Dr. Bazigah Heal (M.Sc, PhD)<small>Principal, as signed on the college overview page</small></p>', single('../', 'pu_prin', caption='Principal, Pre University College for Girls'))}'''
PU_ADM = f'''<h2>Combinations offered</h2>
<ul><li><strong>Part 1 – Languages:</strong> A – English (compulsory); B – Urdu / Hindi / Kannada.</li><li><strong>Part 2 – Optional:</strong> A – Physics, Chemistry, Maths, Biology; B – Economics, Business Studies, Accountancy, Computer Science.</li></ul>
<h2>Fee structure</h2>
<p>Despite being an unaided institution the fee structure in comparison to other colleges is very nominal.</p>
{table(['Combination', 'Fee as printed'], [['PCMB', '8280/- per year'], ['EBs ACs (Economics, Business Studies, Accountancy, Computer Science)', '7335/- per year']])}
{dated('<strong>Dated fees.</strong> The amounts are those printed on the original page (undated) and are not current: please ask the college office for this year’s fees.')}
<p>The fee should be paid within the stipulated date; fee once paid will not be refunded.</p>
<h2>Eligibility for admissions</h2>
<p>Admission to the Karnataka two years pre-university course shall be open to the candidates who have passed (a) the Karnataka secondary school leaving certificate examination, or any other examination recognized by the board as equivalent to the Karnataka SSLC. (b) Students who have scored good marks in the qualifying examination are encouraged to opt for the PCMB combination.</p>
{ADMISSION_PROCEDURE}'''
PU_STAFF = f'''{split(p('To strengthen the teaching and learning process, well qualified, talented and experienced teaching faculty is appointed. The college is headed by a highly qualified and experienced principal with good leadership qualities and with a vision to meet the challenges of the present competitive atmosphere.') + '<p class="source-note">The names of the staff are printed on the photograph.</p>',
       single('../', 'pu_staff', caption='PUC staff members with Principal'))}
<h2 id="names">Names printed with the photograph</h2>
<p class="rc-quote-plain">“Sitting L to R; R.Zuberunnisa, Zohra Banu, Dr. Bazigah Heal (Principal) Fahmeedunnisa, Mamta L. Almel., Standing L to R: Nousheen Fathima, Thaseen Banu, Sunitha, Naheeda Kousar, Ayesha Bi.,”</p>
{note('Typed from the caption that is part of the photograph, exactly as printed, including its punctuation (one comma after “(Principal)” is missing in the print). The photograph carries no date, the caption gives no qualifications or subjects, and the spellings could not be checked against any other record: please verify them with the college.')}'''
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
# DEGREE COLLEGE (B.Com) and BCA — same principal; photographs and the staff list are shared between the two original folders
# =====================================================================================================================
deg_nav = [('Overview', 'home.html'), ('Principal', 'Message.html'), ('Admissions', 'Admissions.html'), ('Staff', 'Staff.html'), ('Facilities', 'Facilities.html'), ('Rules', '../CollegeRegulations.html'), ('Contact', 'Contact.html'), ('Careers', 'Careers.html'), ALL]
DEG_HOME = f'''{logo('../', 'logo_bcom')}
{split(p('The original Degree College for Girls home page reproduces, word for word, the history of the Pre University College (the PU College’s years, its “150 girls” and its II PUC rolling cup). That text describes the PU College and is shown on the <a href="../PUGirlsCollege/home.html">Pre University College page</a>. No separate history of the B.Com programme was published.',
         'The page is signed by the Principal of the Degree and BCA colleges:') + '<p class="rc-sign">Miss Farzana Fathima (M.C.A)<small>Principal, Degree College</small></p>',
       single('../', 'deg_prin', caption='Principal, Degree and BCA colleges'))}
{facts(('Programme', 'Bachelor of Commerce (B.Com) for women'), ('Address', ADDR), ('Administrative Office', ADMIN), ('Degree College', '<a href="tel:0826709915">0826709915</a>'), ('Email', EMAIL))}
<p>Aims, mission and vision are on the shared <a href="../Colleges.html">Colleges</a> page.</p>'''
DEG_MSG = f'''{split('<p>The original Degree College “Message” page shows the Principal’s photograph beside the aims and mission that are common to the PU, Degree and BCA colleges (see <a href="../Colleges.html">Colleges: Aims, Mission &amp; Vision</a>).</p><p class="rc-sign">Miss Farzana Fathima (M.C.A)<small>Principal, Degree College</small></p>', single('../', 'deg_prin', caption='Principal, Degree and BCA colleges'))}'''
DEG_ADM = f'''<h2>Combinations offered</h2>
<p>Bachelor of Commerce (B.Com).</p>
<h2>Fee structure</h2>
<p>Despite being an unaided institution the fee structure in comparison to other colleges is very nominal. The fee should be paid within the stipulated date; fee once paid will not be refunded. The original page prints the headings “Fee structure” and “Eligibility for admissions” but gives no amount or eligibility under them.</p>
{ADMISSION_PROCEDURE}
{note('The procedure above is the Pre-University procedure (it refers to the P.U Board and the P.U.C board) repeated on the original Degree College and BCA admissions pages. Please ask the college office for the university’s own requirements.')}'''
DEG_STAFF = f'''{split(p('To strengthen the teaching and learning process, well qualified, talented and experienced teaching faculty is appointed. The college is headed by a highly qualified and experienced principal with good leadership qualities and with a vision to meet the challenges of the present competitive atmosphere.') + '<p class="source-note">The same photograph and names caption are used on the original Degree College and BCA pages; the names are printed on the photograph.</p>',
       single('../', 'deg_staff', caption='Faculty of the Degree and BCA colleges'))}
{single('../', 'deg_staff_names', caption='Names printed with the faculty photograph', extra_cls='rc-big')}
<h2 id="names">Names printed with the photograph</h2>
<p class="rc-quote-plain">“Sitting L to R: Nibeditha Patel, Hashmath Sadia, Farzana Fathima (Principal) Shahnaz Begum, Nazia Munir<br>Standing L to R: Mubashirunnisa, Sunitha, Tahseen Begum, Tahseen Begum”</p>
{note('Typed from the printed caption image, exactly as printed (one comma after “(Principal)” is missing in the print). The name “Tahseen Begum” is printed twice in the standing row; the original does not say whether these are two persons or a repeated entry, so it is not changed. The photograph is undated and the caption gives no qualifications: please verify with the college.')}'''
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
{dated('The page is undated and gives no start year, fee or intake for the BCA programme.')}
{facts(('Address', ADDR), ('B.C.A. Office', '<a href="tel:0826709915">0826709915</a>'), ('Head Office', ADMIN), ('Email', EMAIL))}
<p>Aims, mission and vision are on the shared <a href="../Colleges.html">Colleges</a> page.</p>'''
BCA_ADM = f'''{note('The original BCA Admissions page is a copy of the B.Com page: it lists “Combinations Offered: Bachelor of Commerce (B.Com)” and gives no BCA-specific combination, fee or eligibility. It is reproduced as printed; please ask the college office (<a href="tel:0826709915">0826709915</a>) for BCA requirements.')}
<h2>Combinations offered (as printed)</h2>
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
{note('The second classroom photograph was in the BCA image folder of the original site (as “Classroom1.jpg”); the original BCA Classroom page displayed only the first.')}
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
{dated('“About 11 years ago” is relative to the date the original page was written (undated). The centre’s own founding year is given as 1999.')}
{facts(('Telephone', '<a href="tel:0822221158">0822221158</a> · JUU Computer Section: <a href="tel:0822221161">0822221161</a>'), ('Address', ADDR))}'''
NCP_ADM = f'''<h2>Fee structure</h2>
{p('As per the scheme, admission fee of Rs. 1000/- and a monthly fee of Rs. 500/- is to be collected from the students. As Majlis-e-Millia is a social organisation in the service of community, it is collecting a monthly fee of Rs. 250/- only.',
   'A corpus fund is maintained from the fee collection, which is utilised for augmenting computers, UPS and meeting other maintenance expenses.',
   'Despite being an unaided institution the fee structure in comparison to other colleges is very nominal. The fee should be paid within the stipulated date; fee once paid will not be refunded.')}
{dated('<strong>Dated fees.</strong> The amounts are as printed on the original page (undated), not current fees.')}
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
{dated('As printed on the original “Message” page (undated): these are the arrangements of that time.')}'''
NCP_LIB = f'''{p('The Centre has built up a library. The books are mainly on the subjects of computer science for the benefit of reference of students. Presently it has over 500 books of reputed authors.')}
{dated('“Over 500 books” is as printed on the original page (undated).')}'''
NCP_FAC = f'''<h2>Classroom</h2>
{gallery('../', ['ncpul_cls'])}
<h2>Computer laboratory</h2>
{gallery('../', ['ncpul_lab1', 'ncpul_lab2'], cls='rc-wide')}
<p>Masjid photographs on the original NCPUL pages are on the <a href="../Masjid.html">Jamia Masjid</a> page.</p>'''
SIBLINGS['NCPUL'] = dict(name='MMI-NCPUL Computer Centre', nav=ncp_nav, pages={
    'home.html': ('MMI-NCPUL Computer Centre', NCP_HOME),
    'Admissions.html': ('Admissions & Course — MMI-NCPUL Computer Centre', NCP_ADM),
    'Support.html': ('Financial Assistance — MMI-NCPUL Computer Centre', NCP_SUP),
    'Library.html': ('Library — MMI-NCPUL Computer Centre', NCP_LIB),
    'Facilities.html': ('Facilities — MMI-NCPUL Computer Centre', NCP_FAC),
    'Staff.html': ('Staff — MMI-NCPUL Computer Centre', f'''{single('../', 'ncpul_staff', caption='Staff members')}<p class="source-note">The original page carried this photograph only; no names were printed.</p>'''),
    'Awards.html': ('Awards — MMI-NCPUL Computer Centre', f'''{single('../', 'ncpul_aw', big=True, caption='Certificate presentation')}<p class="source-note">The original page carried this photograph and a scanned certificate of a named student. The certificate is not reproduced here because it carries a private person’s name, photograph and result; it can be added back if she and her family agree. The certificate shows the diploma was awarded jointly by DOEACC Centre, Chandigarh and the National Council for Promotion of Urdu Language, for “One Year Diploma in Computer Applications and Multilingual D.T.P.” taken at the Majlis-e-Millia Islamia centre, Bangalore.</p>''')})
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
{dated('<strong>Dates differ between pages.</strong> This page gives 1984 for the start of the nursery; the Founder Secretary’s essay gives 1986 and the Admissions Diary 1983-84. “Around 500” pupils is the figure of the time of writing (undated).')}
{gallery('../', ['act_nur2', 'act_nur3'])}'''
NUR_STAFF = f'''<p>{STAFF_LINE}</p><p class="source-note">One line, as printed on the original Nursery and Primary school staff pages. The original page also carried a photograph of the staff, which is already part of the Banikuppa gallery; it is not reproduced here because its caption does not identify the school.</p>'''
NUR_FAC = f'''<h2>Classrooms</h2>
{p('Jame-ul-uloom Boys Residential School believes in the following dictum delivering the lessons “I HEAR, I FORGET, I SEE, I RECALL, I DO, I UNDERSTAND.” All teachers endeavor to prepare their lessons and deliver them in such a way that the child becomes a participant in the learning process. The lessons are complimented by practical sessions and access of information on the internet. A total holistic approach is adopted to remove the burden of learning and make the process of learning a joyful experience without hang-ups and hiccups. The lessons are delivered in the class room by using state of the art audio visual equipment such as overhead projectors and LCD projectors.')}
{note('This paragraph is headed “Jame-ul-uloom Boys Residential school” on the original Nursery and Primary school pages: it was copied from the Banikuppa school’s Classroom page and describes that school. It is also on the <a href="../ResidentialSchoolBanikuppa/classroom.html">Banikuppa Classroom page</a>. The institutions’ smart classrooms are described on the <a href="../Classroom.html">Smart Classrooms</a> page.')}
<h2>Library</h2>
<p>The original Nursery School Library page carried the school computer-education paragraph below (identical on the High Schools’ Library pages):</p>
{p(COMPUTER_EDU)}
{SHARED_SPORTS('Nursery School')}'''
NUR_CONTACT = f'''{facts(('Address', ADDR), ('Head Mistress', '<a href="tel:0822221156">0822221156</a>'), ('Administrative Office', ADMIN), ('Email', EMAIL))}
<p class="source-note">The original Nursery School Contact and Careers pages held no text; these are the Trust’s central numbers from the <a href="../Contact.html">contact directory</a>.</p>'''
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
{dated('Strength (1000), number of teachers (thirty) and results are as printed on the original page (undated) and are not current figures.')}
<p class="rc-sign">Naveeda Naaz (M.A, B.Sc, B.Ed)<small>Head Mistress, as signed on the original page</small></p>'''
PRI_FAC = f'''<h2>Library</h2>
<p>The original Higher Primary School Library page (headed “English Higher Primary School”) carried the computer-education paragraph below:</p>
{p(COMPUTER_EDU)}
<h2>Classrooms</h2>
<p>The original Classroom page repeated the Banikuppa school’s classroom paragraph; it is on the <a href="../ResidentialSchoolBanikuppa/classroom.html">Banikuppa Classroom page</a>. The smart classrooms are described on <a href="../Classroom.html">Smart Classrooms</a>.</p>
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
{dated('<strong>Dated figures.</strong> Strengths and results are those of the time the page was written (the last result quoted is for 1999-2000) and are not current. The Admissions Diary 2013–14 (<a href="../AdmissionsDiary.html">here</a>) quotes later SSLC results.')}
<p class="rc-sign">Naveeda Naaz (M.A, B.Sc, B.Ed)<small>Head Mistress, as signed on the original page</small></p>
{note('The original Girls and Boys High School home pages also carried a quotation and a sentence about the ITI being “in its 16th year”. That text belongs to the Industrial Training Institute and is on its <a href="../ITI/Message.html">Message page</a>.')}'''
GH_STAFF = f'''<p>{STAFF_LINE}</p>
{gallery('../', ['school_staff', 'school_staff2'], captions={'school_staff': 'Staff of the English High Schools', 'school_staff2': 'Staff of the English Girls High School'})}
<p class="source-note">Names are not printed with the photographs.</p>'''
GH_FAC = f'''<h2>Classrooms</h2>
{p('Jame-ul-uloom Boys Residential School believes in the following dictum delivering the lessons “I HEAR, I FORGET, I SEE, I RECALL, I DO, I UNDERSTAND.” All teachers endeavor to prepare their lessons and deliver them in such a way that the child becomes a participant in the learning process. The lessons are complimented by practical sessions and access of information on the internet. A total holistic approach is adopted to remove the burden of learning and make the process of learning a joyful experience without hang-ups and hiccups. The lessons are delivered in the class room by using state of the art audio visual equipment such as overhead projectors and LCD projectors.')}
{note('Headed “Boys Residential School” on the original High School Classroom pages: the paragraph was copied from the Banikuppa school’s page. See the <a href="../ResidentialSchoolBanikuppa/classroom.html">Banikuppa Classroom page</a>.')}
{gallery('../', ['girls_cls'])}
<h2>Computer laboratory</h2>
{p(COMPUTER_EDU)}
{gallery('../', ['girls_comp'])}
<h2>Library</h2>
<p>The original High School Library page carried the same computer-education paragraph as above.</p>
{note('The original English Girls High School “Science Labs” page carried a paragraph about boarding, lodging and the Warden-in-chief. That describes the Banikuppa residential campus and is not shown here; see the <a href="../ResidentialSchoolBanikuppa/hostel.html">Banikuppa Hostel page</a>.')}
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
<p class="rc-sign">Naveeda Naaz (M.A, B.Sc, B.Ed)<small>Head Mistress, as signed on the original page</small></p>
{note('The original Boys High School home page repeated the Girls High School paragraph about SSLC results and the “heavy rush of the girls for admission”. It describes the girls’ school and is on the <a href="../EngGirlsHighSchool/home.html">English Girls High School page</a>.')}'''
BH_FAC = f'''<h2>Classrooms</h2>
{p('The original Classroom page repeated the Banikuppa school’s classroom paragraph; see the <a href="../ResidentialSchoolBanikuppa/classroom.html">Banikuppa Classroom page</a>.')}
{gallery('../', ['boys_cls', 'boys_cls2'])}
{note('The second photograph was in the Boys High School image folder of the original site (as “Classroom1.jpg”); the original Classroom page displayed only the first.')}
<h2>Computer laboratory</h2>
{p(COMPUTER_EDU)}
<h2>Science laboratories</h2>
<p>The original Boys High School Laboratories page described three photographs of the Banikuppa campus laboratories: Chemistry (students conducting experiments under the guidance of subject teachers), Physics (students exhibiting an experiment to a guest from U.S.A.) and Biology (students conducting practicals using natural specimens). They are on the <a href="../ResidentialSchoolBanikuppa/laboratories.html">Banikuppa Science Laboratories page</a>.</p>
<h2>Library</h2>
<p>The original High School Library page carried the computer-education paragraph above.</p>
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
hifz_nav = [('Overview', 'home.html'), ('Proposed building', 'Proposed.html'), ('Contact', 'Contact.html'), ('Full original text', '../Services.html#english'), ALL]
HIFZ_HOME = f'''{logo('../', 'logo_hifz')}
<p>The original Shoba-e-Hifz pages carried no text of their own: their “About Us” pages were the same scanned pages (English and Urdu) as the Darul Quran Arabic College, and their “Proposed” page the architect’s drawing. What the Trust’s pages say about the Hifz section is gathered here, as printed.</p>
{quote('In the year of 1986 there were two halls towards the western side of the Mosque which is earmarked for the Welfare of the Community; one more privileged achievement to exhibit our educational &amp; character building milestone was to start Hifz section for the guest of Hazarat Mohammed sal-allaha-o-Alaihi-o-salamm with boarding &amp; lodging to impart not only Religious education but also general education so as to pass 10th &amp; P.U Exams.', sign='Original English “About Us” page (scan)', role='J.U Darul Quran Arabic College, Bangalore')}
{quote('In the Hifze Quran department boys and girls both are becoming Hafiz and Hafiza.', sign='Original “About Us” page 1', role='A Revolutionary movement')}
{quote('About a dozen teachers including Hufaz and Moulvies are employed for the purpose.', sign='Original home page', role='Jame-ul-uloom, Jamia Masjid')}
{dated('The first quotation gives 1986 for the start of the Hifz section as written on that page; the years given on other pages of the original site differ. No admission conditions, fees, staff or timings were published for Shoba-e-Hifz.')}
<p>The scanned English and Urdu pages are on the <a href="../Services.html">Services</a> page; the <a href="../ShobaeAlimiyathDel/home.html">Shoba-e-Alimiyath</a> and <a href="Proposed.html">proposed building</a> pages complete the original set.</p>'''
HIFZ_PROPOSED = f'''<p>The original “Proposed” page showed the architect’s drawing below, titled “Proposed J.U Darul Quran &amp; Arabic College, Bangalore”: front elevation and ground-floor plan.</p>
{single('../', 'dq_plan', big=True, caption='Proposed building: front elevation and ground-floor plan')}
{dated('A proposal drawing from the original site; it is not a photograph of a completed building. No date was printed.')}'''
SIBLINGS['ShobaehifzDel'] = dict(name='Shoba-e-Hifz', nav=hifz_nav, pages={
    'home.html': ('Shoba-e-Hifz', HIFZ_HOME), 'Proposed.html': ('Proposed Building — Shoba-e-Hifz', HIFZ_PROPOSED),
    'Contact.html': ('Contact — Shoba-e-Hifz', facts(('Address', ADDR), ('Jamia Masjid', '<a href="tel:0822239495">0822239495</a>'), ('Administrative Office', ADMIN), ('Email', EMAIL)) + '<p class="source-note">The original page held no text; these are the Trust’s central details.</p>')})
REDIRECTS.update({'ShobaehifzDel/AboutusEnglish.html': 'Services.html#english', 'ShobaehifzDel/AboutusUrdu.html': 'Services.html#urdu', 'ShobaehifzDel/Admissions.html': 'ShobaehifzDel/home.html',
                  'ShobaehifzDel/Staff.html': 'ShobaehifzDel/home.html', 'InsShobaehifz.html': 'ShobaehifzDel/home.html'})

alim_nav = [('Overview', 'home.html'), ('Proposed building', 'Proposed.html'), ('Contact', 'Contact.html'), ('Full original text', '../Services.html#english'), ALL]
ALIM_HOME = f'''{logo('../', 'logo_alim')}
<p>The original Shoba-e-Alimiyath pages carried no text of their own: their “About Us” pages were the scanned English and Urdu pages of the <strong>J.U Darul Quran Arabic College, Bangalore</strong>, and their “Proposed” page the architect’s drawing. No syllabus, admission conditions, fees or staff were published. What the page says about the Arabic College is gathered here, as printed:</p>
{quote('Now we pray with Almighty to all those who are actively involved in bringing up J.U Arabic College at Bannikuppe. This institution comes up very fast so as to serve the community in a big way.',
       'The management could succeed in getting 61 acres of land, which is 25kms away from the City Mosque at Bannikuppa, so that, a part of it can be rescued for Arabic Studies, in which the construction has already begun … to accommodate lecture hall. It accommodates Lecture Hall, Mosque, Library, Guest house &amp; a Kitchen, Computer center, Tailoring and calligraphy center.',
       sign='Original English “About Us” page (scan)', role='J.U Darul Quran Arabic College, Bangalore')}
{dated('Construction progress, land area and distance are as printed on the undated original page and differ from other pages of the site (for example 52 hectares / 27 km in the Founder Secretary’s essay). They should be confirmed by the Trust before being relied on.')}
<p>The complete scanned pages, with their typed English text, are on the <a href="../Services.html">Services</a> page. The <a href="Proposed.html">proposed building drawing</a> is on its own page. A printed flyer for the college (original file “home.jpg”) is not reproduced because it shows a bank account number; the Trust office can supply it.</p>'''
SIBLINGS['ShobaeAlimiyathDel'] = dict(name='Shoba-e-Alimiyath · J.U Darul Quran Arabic College', nav=alim_nav, pages={
    'home.html': ('Shoba-e-Alimiyath', ALIM_HOME), 'Proposed.html': ('Proposed Building — Shoba-e-Alimiyath', HIFZ_PROPOSED),
    'Contact.html': ('Contact — Shoba-e-Alimiyath', facts(('Address', ADDR), ('Jamia Masjid', '<a href="tel:0822239495">0822239495</a>'), ('Administrative Office', ADMIN), ('Email', EMAIL)) + '<p class="source-note">The original page held no text; these are the Trust’s central details.</p>')})
REDIRECTS.update({'ShobaeAlimiyathDel/AboutusEnglish.html': 'Services.html#english', 'ShobaeAlimiyathDel/AboutusUrdu.html': 'Services.html#urdu', 'ShobaeAlimiyathDel/Admissions.html': 'ShobaeAlimiyathDel/home.html',
                  'ShobaeAlimiyathDel/Staff.html': 'ShobaeAlimiyathDel/home.html', 'InsShobaeAlimiyath.html': 'ShobaeAlimiyathDel/home.html'})
REMOVE += ['InsShobaeAlimiyath.html']

# Other legacy root URLs
REDIRECTS.update({'Caligraphy.html': 'Calligraphy.html', 'ServicesEng.html': 'Services.html#english', 'ServicesUrdu.html': 'Services.html#urdu', 'Recognition.html': 'Recognitions.html',
                  'Institution.html': 'ITI/home.html', 'ScMasjid.html': 'Masjid.html'})
