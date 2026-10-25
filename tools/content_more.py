"""Phase 9: replacements for existing Phase 8 root pages and the shared college pages."""
from html import escape
import recovery_assets as RA
from rc_helpers import (fig, gallery, single, split, p, quote, dated, note, sources, table, people, vision, doc_list, scan, logo, phone)

# ---- J.U Darul Quran Arabic College: the original English “About Us” page, typed from the scan and checked against it ----------------
DQ_ENGLISH = '''<div class="rc-text"><blockquote>
<h3>J.U Darul Quran Arabic College, Bangalore</h3>
<p>In general Mosque committee are formed to look after mosque activity whereas Jamia Masjid has added one more activity i.e. Charitable activity which means to take care of Muslims Educational needs so as to make every Muslim’s future very bright, particularly those who are unable to get educated due to poverty. Jamia Masjid &amp; Muslim Charitable Fund trust has been established to take care of educational needs of those Muslims who are unable to pursue their education due to poverty.</p>
<h3>Establishment of Jame-ul-uloom</h3>
<p>In the year 1982 Jame-ul-uloom Institution was started with just 2 students in its nursery class. Later due to hard efforts of trust &amp; Moulana Riyaz-ur-Rehman saheb khateeb-o-Imam Jamia Masjid through his public sermons, people with traditional ideologies also were motivated towards education &amp; they started admitting their children in Jame-ul-uloom Institution. Let us pray with Almighty Allah to reward Moulana for his devotion &amp; efforts put in for the Improvement of this Institution.</p>
<p>In the year of 1986 there were two halls towards the western side of the Mosque which is earmarked for the Welfare of the Community one more privileged achievement to exhibit our educational &amp; character building milestone was to start Hifz section for the guest of Hazarat Mohammed sal-allaha-o-Alaihi-o-salamm with boarding &amp; lodging to impart not only Religious education but also general education so as to pass 10th &amp; P.U Exams.</p>
<p>Since a long time the members of Management has a quenching thirst &amp; Compulsion to start a healthy residential Campus, away from this busy city environment so as to impart a good &amp; quality education &amp; to accommodate increasing number of students. With the wishes of Almighty Allah, the management could succeed in getting 61 acres of land, which is 25kms away from the City Mosque at Bannikuppa, so that, a part of it can be rescued for Arabic Studies, in which the construction has already begun which is as per file photo to accommodate lecture hall. It accommodates Lecture Hall, Mosque, Library, Guest house &amp; a Kitchen, Computer center, Tailoring and calligraphy center.</p>
<h3>J.U Movement</h3>
<p>In the early 20’s J.U as a small plant with 2 students has grown up to a big tree of 3500 students where in from slate to computer, from Khaida to Tafseer-e-Quran, from Nursery to college. Hifz section on adult education Programs were conducted for both boys and girls between 7.30 a.m in the morning till 10.30 in the late evening. With these features we cannot call this institution as a school or college but a movement not only for Muslims in Karnataka but for the entire Country.</p>
<h3>J.U Arabic College Bangalore</h3>
<p>Jamia Masjid &amp; Muslim Fund Charitable Fund Trust need no introduction. It is one of the central institution for the whole of Karnataka State. What ever the Infrastructure that has been developed &amp; visible today is due to the good wishes of great Philanthropists, donors, who are committed for the well being of Community.</p>
<p>Now we pray with Almighty to all those who are actively involved in bringing up J.U Arabic College at Bannikuppe. This institution comes up very fast so as to serve the community in a big way.</p>
<h3>Appeal</h3>
<p>If possible we request our community people to come and inspect the construction work individually to their satisfaction.</p>
<h3>Note</h3>
<p>Donors are hereby informed that a hall measuring 25x30 will cost Rs: 7 Lakhs; this can be donated in the names of their relatives who have passed away so that the Allah will reward them. <em>Jazak-Allah</em></p>
</blockquote></div>'''

DQ_CAVEAT = dated('<strong>Dated appeal.</strong> This is the text of an undated printed page. The appeal, the donor note (“a hall measuring 25x30 will cost Rs: 7 Lakhs”) and the remark that construction “has already begun” describe the time it was written and are <strong>not</strong> a current request or statement of progress. This website does not invite donations and publishes no bank details; please contact the Trust office (<a href="Contact.html">Contact</a>) for anything of that kind. Years and land figures are quoted as printed and differ from other pages of the original site.')

services = f'''<p class="eyebrow">About Us</p><h1>Services</h1><p class="lede">The services of the Jamia Masjid &amp; Muslim Charitable Fund Trust, as described on the original English and Urdu “Services” pages.</p>
<ul class="card-grid portal-cards">
  <li class="card"><h3>Educational Services</h3><p>Fourteen institutions spanning nursery, primary, high school, Pre-University, B.Com, BCA, ITI vocational trades, and computer training.</p><a class="go" href="Institutions.html">View institutions →</a></li>
  <li class="card"><h3>Moral &amp; Religious Instruction</h3><p>A daily Arabic period from L.K.G. to PUC, a weekly Thursday <em>ijtima</em> for girl students, Shoba-e-Hifz, Shoba-e-Alimiyath and adult education arranged outside school hours.</p><a class="go" href="ShobaeAlimiyathDel/home.html">Shoba-e-Alimiyath →</a></li>
  <li class="card"><h3>Vocational Training</h3><p>Tailoring School for Women, the Calligraphy Centre, the MMI-NCPUL Computer Centre and the Industrial Training Institute (ITI) at Shikshanagar.</p><a class="go" href="Tailoring.html">Tailoring School →</a></li>
  <li class="card"><h3>Charitable Activity</h3><p>Care for the educational needs of Muslims unable to study because of poverty, as the Trust describes it.</p><a class="go" href="#english">Read the original page →</a></li>
</ul>
<div class="rc-prose">
<h2 id="english">Services (English)</h2>
<p class="source-note">The original “Services (English)” page is a scanned page headed “J.U Darul Quran Arabic College, Bangalore”. Its text is typed out below and checked against the scan, spelling as printed except for the obvious typing slips listed in the audit.</p>
{split(DQ_ENGLISH, single('', 'dq_en', big=False, caption='Original “Services (English)” page (scan)'))}
{DQ_CAVEAT}
<h2 id="urdu">Services (Urdu)</h2>
{split('<p>The original “Services (Urdu)” scan is the Urdu version of the page above, headed “J.U Darul Quran Arabic College, Bangalore”. It is shown as a scan only; it has not been transcribed or translated because no Urdu text recognition was available and its wording must not be guessed.</p><p>The original site’s “Services (Urdu)” link also reached a copy of the activity-calendar page, which is on the <a href="Activities.html">Activities</a> page here.</p>', single('', 'dq_ur', caption='Original “Services (Urdu)” page (scan)'), flip=True)}
<p>See also the proposed building drawing on the <a href="ShobaeAlimiyathDel/Proposed.html">Shoba-e-Alimiyath</a> pages.</p>
</div>'''

recognitions_intro = '''<div class="prose"><p>This page gathers the recognitions documented on the original site. Below are the scanned letters of appreciation. The Admissions Diary also describes an awards function held on 13 December 2012 at Town Hall for meritorious students of the Group of Institutions, with the Governor of Karnataka as Chief Guest; it is recorded in the <a href="AdmissionsDiary.html#school-awards">Admissions Diary</a> as printed.</p></div>
<p>See also the <a href="ResidentialSchoolBanikuppa/sports.html">Banikuppa Residential School awards and competitions</a> and <a href="ResidentialSchoolBanikuppa/gallery.html">campus photograph archive</a>.</p>'''

recognitions_intro += single('', 'award_trophy', caption='Trophy picture used as the “Recognitions” menu image on the original site', detail='The engraving reads “Udyog Rattan Award”; the recipient’s line and the year are too small to read, and the original text does not mention the award, so nothing more is said about it here.')

def sciencelabs(photo_section_html):
    return f'''<p class="eyebrow">Facilities</p><h1>Science Laboratories</h1><p class="lede">Science laboratories of the Pre University College for Girls, and laboratory photographs from the Banikuppa campus.</p>
<div class="rc-prose">
<h2>PU College for Girls</h2>
{p('The college is housed in a spacious building with well furnished and ventilated class rooms, well equipped laboratories and library with good collection of books. Magazines and News papers are also subscribed for the benefit of the students. The computer lab is provided with internet facility. A spacious auditorium is also under construction. We aim to provide canteen facility for our students. A nationalized bank (Canara Bank) is also located in the same building.')}
{dated('Paragraph as printed on the original PU College pages; the remarks about the auditorium and canteen are dated.')}
{gallery('', ['pu_lab1', 'pu_lab2'], cls='rc-wide')}
</div>
{photo_section_html}
<p>The English Boys High School’s original Laboratories page describes these Banikuppa photographs as students conducting experiments under the guidance of subject teachers (chemistry), exhibiting an experiment to a guest from U.S.A. (physics) and conducting practicals using natural specimens (biology). More on the <a href="ResidentialSchoolBanikuppa/laboratories.html">Banikuppa Science Laboratories page</a>.</p>'''

transport_cards = '''<p class="eyebrow">Facilities</p><h1>Transport &amp; Campus Facilities</h1><p class="lede">School buses, and campus facilities across the Jame-ul-Uloom Group of Institutions.</p>
<ul class="card-grid portal-cards">
  <li class="card"><h3>City Market Central Campus</h3><p>Located at S.J.P. Road, City Market, in the heart of Bangalore, on the campus of Jamia Masjid.</p><a class="go" href="Contact.html">Central contact directory →</a></li>
  <li class="card"><h3>Science Laboratories</h3><p>Physics, Chemistry and Biology laboratories: the PU College’s, and the Banikuppa campus’s.</p><a class="go" href="ScienceLabs.html">Science Labs →</a></li>
  <li class="card"><h3>Banikuppa Residential Campus</h3><p>On the Bangalore–Mysore highway; the distance from the city is given differently on different pages of the original site. See the campus’s own facilities pages.</p><a class="go" href="ResidentialSchoolBanikuppa/facilities.html">Banikuppa facilities →</a></li>
</ul>'''

def transport(photo_section_html):
    return (transport_cards + f'''<div class="rc-prose"><h2 id="buses">School buses</h2>
<p>Photographs of the school buses, from the original “Transport” page (which held photographs only). The Admissions Diary 2013–14 lists the rules for students travelling by bus or van; see <a href="AdmissionsDiary.html#discipline">School Discipline</a>.</p>
{gallery('', ['veh1', 'veh2', 'veh3'])}</div>''' + photo_section_html)

tailoring = f'''<p class="eyebrow">Institutions</p><h1>Jame-ul-Uloom Tailoring School for Women</h1><p class="lede">The Tailoring Department of Jame-ul-Uloom, Jamia Masjid — girls learning the art of tailoring.</p>
<div class="rc-prose">
{logo('', 'logo_tail')}
{split(p('The “Tailoring Dept.” of Jame-ul-uloom Jamia Masjid: girls learning the art of tailoring.',
         'The Founder Secretary’s essay lists a tailoring institute among the institutions established in the mosque after the nursery (<a href="AboutUs.html#fond-memories">read the essay</a>), and the <a href="Calligraphy.html">Calligraphy Centre</a> page says its students are also given the chance to learn tailoring.',
         'For admission enquiries, contact the Administrative Office through the <a href="Contact.html">contact directory</a>.'),
        single('', 'tailoring', caption='Tailoring Department, Jamia Masjid'))}
<p class="source-note">The original page had no other text. Course length, fees and timings were not given, so none are shown.</p>
</div>'''

admissions = '''<p class="eyebrow">Admissions</p><h1>Admissions</h1><p class="lede">Where to find admission information for each institution of Jame-ul-Uloom, Jamia Masjid, Bangalore.</p>
<div class="prose"><p>Admission rules, documents and fees are published separately for each institution on the original site. They are restored on the pages below, each as printed and with its own date caveat. For current forms, eligibility and fees, contact the respective office listed in the contact directory.</p></div>
<ul class="card-grid portal-cards">
  <li class="card"><h3>Nursery, Primary &amp; High Schools</h3><p>The 2013–14 school diary: rules and admission, discipline, awards and calendars.</p><a class="go" href="AdmissionsDiary.html">Admissions Diary 2013–14 →</a></li>
  <li class="card"><h3>Pre University College for Girls</h3><p>Combinations, fee structure (dated), eligibility and procedure.</p><a class="go" href="PUGirlsCollege/Admissions.html">PU College admissions →</a></li>
  <li class="card"><h3>Degree College (B.Com)</h3><p>Admission procedure and documents.</p><a class="go" href="DegreeGirlsCollege/Admissions.html">Degree College admissions →</a></li>
  <li class="card"><h3>BCA College</h3><p>Admission procedure (the original page repeats the B.Com text).</p><a class="go" href="BCA/Admissions.html">BCA admissions →</a></li>
  <li class="card"><h3>MMI-NCPUL Computer Centre</h3><p>Course structure, fees and intake.</p><a class="go" href="NCPUL/Admissions.html">NCPUL admissions →</a></li>
  <li class="card"><h3>Industrial Training Institute</h3><p>Trades, duration, eligibility and seating.</p><a class="go" href="ITI/Admissions.html">ITI admissions →</a></li>
</ul>
<p><a class="button" href="Contact.html">View Departmental Phone Directory</a> <a class="button" href="Institutions.html">Browse All 14 Institutions</a></p>'''

def institutions_extra():
    return f'''<div class="rc-prose"><h2 id="welcome">Welcome to the Jame ul uloom Group of Institutions</h2>
{quote('I am glad that Jame-ul-uloom English Nursery, Primary and High School, Bangalore is bringing out a school website.', sign='Mr. K. Rahman Khan', role='Greeting printed on the original Institutions page. His signed letter of 15 February 2011, about the school magazine, is on the Recognitions page.')}
{p('Jame-ul-uloom is an Arabic name meaning “Center of Knowledge”. Jame-ul-uloom is housed in the campus of Jamia Mosque, one of the biggest mosques in the state, located in the heart of the Bangalore City. Apart from imparting education, the Institution aims at “character building”. This is achieved through moral education and religious instruction.',
   'Upliftment of the downtrodden in the Minority Community is the aim of Jame-ul-uloom. It also aims in preparing good and useful citizens, so that they can face the situations in this world of competition. To accomplish many such purposes, Jame-ul-uloom has in its fold institutions.')}
<h2 id="trust">The Trust</h2>
{quote('JAMIA MASJID &amp; MUSLIM CHARITABLE FUND TRUST (JM&amp;MCF) is one of the reputed trust. Established in the year 1939 with a mission to support the nation by educating people and to create good society. The trust with a core mission to establish a world class university has started schools, colleges in and around Bangalore.', sign='The Trust’s introduction', role='As printed on the original Institution page. The year is the one that page gives; other pages of the original site give other years (see About Us).')}
<p><a href="Masjid.html">More about Jamia Masjid and the Trust’s charitable activity →</a> · <a href="AboutUs.html">About Us →</a></p></div>'''

def activities_extra():
    return f'''<section class="pv-section" aria-labelledby="pv-functions"><div class="pv-head"><h2 id="pv-functions">Functions and programmes</h2>
<p>Photographs of programmes of the institutions, from the original “Activities” and “Auditorium” pages. No dates or names were printed with them.</p></div>
{gallery('', ['act1', 'act2', 'act3', 'fn6', 'fn7', 'act_col', 'act_nur2', 'act_nur3'])}
<p>More photographs: <a href="Auditorium.html">Auditorium</a> · <a href="Sports.html">Sports</a>.</p></section>'''

COLLEGE_AIMS = f'''<p class="eyebrow">Institutions</p><h1>Colleges: Aims, Mission &amp; Vision</h1><p class="lede">The aims and mission shared by the Pre University, Degree and BCA colleges of Jame-ul-Uloom.</p>
<div class="rc-prose">
<p class="source-note">The same two statements appear, unchanged, on the original “Message” page of the PU College, the Degree College and the BCA College. They are shown once here, and each college links to this page.</p>
<h2>Aims and objectives</h2>
{p('The PU College was established with the sole aim of educating the girl child of our community. Apart from imparting education, the institution aims at “Character Building” which is achieved through moral education. Upliftment of the downtrodden in the minority community is the aim of Jame-ul-uloom Institutions. It also aims in preparing good and responsible citizens, who can compete in today’s challenging world.')}
<h2>Our Mission &amp; Vision</h2>
{p('J U Composite Pre University and Degree College is a nurturing ground for an individual’s holistic development to make effective contribution to the society in a dynamic environment.')}
<h2>The colleges</h2>
<ul class="card-grid portal-cards">
 <li class="card"><h3>Pre University College for Girls</h3><a class="go" href="PUGirlsCollege/home.html">Overview →</a></li>
 <li class="card"><h3>Degree College for Girls (B.Com)</h3><a class="go" href="DegreeGirlsCollege/home.html">Overview →</a></li>
 <li class="card"><h3>Degree College (BCA)</h3><a class="go" href="BCA/home.html">Overview →</a></li>
</ul>
<p><a href="CollegeRegulations.html">Rules and regulations of the colleges and the computer centre →</a></p>
</div>'''

COLLEGE_RULES = f'''<p class="eyebrow">Institutions</p><h1>College Rules &amp; Regulations</h1><p class="lede">The rules printed for the PU, Degree and BCA colleges and for the MMI-NCPUL Computer Centre.</p>
<div class="rc-prose">
<p class="source-note">Four original “Regulations” pages (PU College, Degree College, BCA and NCPUL) carry identical text; it is shown once here. The wording is as printed.</p>
<h2>Rules and Regulations</h2>
<ol>
<li>Students shall abide by all general and specific rules that are in force and that may be made by the institution as regard to their conduct and studies from time to time.</li>
<li>A special emphasis is made on Hijab, Discipline and punctuality. Students should be punctual and regular to the classes; their behavior should be polite and they should show due respect for their teachers.</li>
<li>Students are required to wear modest and decent dress. They are expected to wear salwar kameez and chudidars with dupattas.</li>
<li>Regarding academic progress 75% of attendance is compulsory.</li>
<li>Apart from prescribed examination, they must and should attend periodic tests. This will benefit the academic performance of the students.</li>
<li>Slow learners will be given special attention and extra coaching classes will be conducted to improve their performance in the final examination.</li>
<li>Submission of projects and assignments is compulsory. Records should be maintained neatly.</li>
<li>Parents are requested to make it convenient to visit the college and meet the principal and teachers regarding the progress of their child. They are required to countersign the progress card periodically.</li>
<li>To develop all round qualities in students, extra-curricular activities are conducted; participants are encouraged by awarding prizes.</li>
<li>To enhance students’ knowledge in Deeniyath, Islamic Quiz and seminars are organized…</li>
</ol>
<p class="rc-note">Rule 10 ends with an ellipsis on the original page, as shown.</p>
<p>See also: <a href="Colleges.html">Aims, Mission &amp; Vision</a> · <a href="PUGirlsCollege/home.html">PU College</a> · <a href="DegreeGirlsCollege/home.html">Degree College</a> · <a href="BCA/home.html">BCA</a> · <a href="NCPUL/home.html">NCPUL</a></p>
</div>'''

ROOT_MORE = {
    'Colleges.html': ('Colleges: Aims, Mission & Vision', COLLEGE_AIMS, 'Aims, mission and vision shared by the PU, Degree and BCA colleges of Jame-ul-Uloom.'),
    'CollegeRegulations.html': ('College Rules & Regulations', COLLEGE_RULES, 'Rules and regulations of the colleges and the computer centre of Jame-ul-Uloom.'),
}
