"""Restored content of the main portal (root pages).

Text comes from the original site (backup `public_html/`) and is attributed to its writers. Where the original contained an obvious
typing slip the page corrects it silently.
Dates and figures are given exactly as each original page printed them; conflicting figures are never merged, each is labelled with its source.

ROOT: filename -> (title, body, description)  new root pages
OVERRIDES: filename -> body  replaces the body of a page that also exists in the Residential School generator
"""
from html import escape
import recovery_assets as RA
from rc_helpers import (fig, gallery, single, split, p, quote, dated, note, info, sources, table, people, vision, doc_list,
                        scan, logo, phone, img_tag)

DATE_NOTE = ('Dates and figures on this page are quoted as the Trust’s documents give them. The documents do not always agree '
             '(for example on the year the Trust was established), so each figure is shown with the document it comes from.')

# ---------------------------------------------------------------------------------------------------------------------
about = f'''<p class="eyebrow">About Us</p><h1>About Jame-ul-Uloom</h1><p class="lede">The vision, the idea behind the institution and the founding story, and the Founder Secretary’s essays.</p>
<div class="rc-prose">
<h2 id="vision">Our Vision</h2>
{vision([
 'To cherish the quality of simplicity of a person’s behaviour, relationship and lifestyle.',
 'To be always friendly, polite and courteous with everyone everywhere, and cleanliness of the school premises.',
 'To initiate and promote experimentation and innovativeness in education.',
 'To inculcate the habit of punctuality, regularity and discipline.',
 'To pursue excellence and to mould the character.',
 'To develop the spirit of national integration and create a sense of Indianness among children.'])}
<h2 id="movement">A Revolutionary Movement</h2>

<div class="rc-text"><blockquote>
{p('Jamia-ul-uloom was established about twenty years ago with only two students. Since then its growth development and progress has been rapid, astonishing and most exemplary. Today it has grown into a massive institution imparting knowledge to about 3,500 students.',
   'The Jamia-ul-uloom complex has classes from nursery to computer training, and students start coming from 7am and the institute closes at about 10.30pm.',
   'In the Hifze Quran department boys and girls both are becoming Hafiz and Hafiza. In this contest the Jamia-ul-uloom at Jamia Masjid (city) is not just a school it is a revolutionary movement. It is the most glaring example for the Muslims of Karnataka in particular and Muslims of India in general.',
   'The roots of this institute are in Masjid-E-Nabvi, from where knowledge spread to the every part of the world. It is from Masjid-e-Nabvi, the Holy Prophet Hazrath Mohammed (S.A.W) spread the message of universal brotherhood, revealed the Holy Quran and reformed the whole society.',
   'The Holy prophet and his companions underwent every types of hardship, built the Masjid-e-Nabvi, because Namaz is obligatory for all Muslims, a true Muslim just cannot neglect Namaz. And the “Suffa” was constructed to spread knowledge. As a Muslim’s life is waste without Namaz, without knowledge, a Muslim’s life is worst than death. The Holy Prophet (S.A.W) has said, “the life of an ignorant and illiterate person is not life but death.”',
   'The companions of the Holy Prophet would learn about the Holy Quran and various other aspects of life from the Prophet at the Masjid-e-Nabvi.',
   'From these facts we can easily conclude that Masjid-e-Nabvi was not constructed only for Namaz, the other purpose was to spread knowledge from this platform (Suffa), Masjid-e-Nabvi attended to all the problems faced by Muslims. At the time of Namaz all would form rows and say their Namaz and after namaz teaching sessions were conducted at the Masjid-e-Nabvi, and the suffa was the permanent seat of few students, they used to learn about various subjects from the Holy Prophet, they would also undergo training in horse riding and other skills of war. But alas, today the Muslims are ignorant about the role of the Mosque, they think Mosque is meant just for 5 times namaz. This thinking totally wrong and against the philosophy of construction of Masjid-e-Nabvi.',
   'Jamia-ul-uloom situated at Jamia Masjid (city) is a movement, to remind the Muslims about the role of mosque in the society. This movement intends to make the muslims realize that today if muslims are backward in the field of education, it is only because they are staying away from the Mosque. The mosques are abodes of Allah, where Allah is to be remembered, Allah’s message and the message of his Prophet is to be taught, the principles of life and world taught by the Prophet (S.A.W) should be taught, the people should be taught the ways of life taught by Holy Prophet (S.A.W) in the Masjid-e-Nabvi, and all these teachings should be imparted in contemporary methods of teaching. So as to save our younger generations from the evils of the world. Today schools and various institutions are being established to impart western culture and English language, in these places all types of corrupt vulgar thoughts and views are being spread among our children. Is it not our duty to save our children from this moral disaster by establishing schools and institutes to impart the best of education in a total Islamic atmosphere. Let us assemble at the Mosques, let us make these mosque centers of learning, let us spread the Quranic teachings and these Hadees from the Mosques, let us impart education from nursery to Hitech at their centers.',
   'Let us educate our children in a total Islamic atmosphere, let us make them good persons, good doctors and good engineers. All these aims can be realized only if muslims adopt this movement, make every Mosque a true copy of Masjid-e-Nabvi. Today we can proudly say Jamia-Masjid has set an example in this direction and if all Muslims follow this example muslims can progress in the field of education.')}
</blockquote></div>
<h2 id="fond-memories">Jamia-ul-Uloom — Fond Memories</h2>
{split(
 '<p class="source-note">Two essays by <strong>Alhaj Mohammed Ateeq Ahmed</strong>, Founder Secretary, Jame-ul-uloom, Jamia Masjid .</p>'
 '<blockquote>' + p(
  'Among all the sites in the world, the best and the most honoured site is that on which a mosque is built, as the mosque are the most loved homes of Allah. In these mosques we receive peace of mind, soul and conscience. Construction of mosque is a very grand act, as the construction of the mosques has been termed as the best of the deeds of a momin, and Allah gifts a palace, which would be the eternal abode of the momin who constructs a mosque.',
  'A mosque is unique sign of Deen-e-Islam. The Masjid-e-Nabvi (at Madeena) is the most distinguished mosque, as in this mosque the prayers were not just restricted to Namaz, recitation of the Holy Quran and remembrance of Allah, but it was the center of Islamic brotherhood, learning and teaching and all the Islamic activities. As far as learning and teaching in the masjid-e-nabvi is concerned, the institution of Suffa and As’hab-e-Suffa are the most illuminous examples. On this suffa (seat) stood the house of knowledge of the Holy Prophet. Poor and homeless companions of Holy Prophet assembled here, these companions had dedicated their to acquire knowledge. It would be better if the mosques are constructed on the basis of aforesaid objectives, by this way we would also be acting according to sunnath.',
  'To accomplish these objectives the foundation of Jamia Masjid City Bangalore was laid in the heart of the city in 1936. The founders of this mosque wished that this mosque should not just serve the purpose of Namaz and Zikr O Azkar, but muslims and their children should receive education here, because in the city muslim children were going to schools devoid of Islamic atmosphere and they also did not have any system to build the moral and character of muslim child, and a movement to kill the very identity of muslims was spearheaded, by anti Islamic forces. Due to this movement muslim children were becoming unaware of Islam and Islamic teachings. In this context after a discussion and thinking, it was decided to establish a Madrasa and a school under the governor of this mosque to educate and train the muslim child, according to Islamic teachings and to help them to solve the education and economic problems.',
  'To fulfill these objectives, Jamia Masjid and Muslim Charitable Fund Trust was established. The trustees of this trust, keeping in view the objectives of the founder of Jamia Masjid, established a madrasa and a school to impart education to girls and boys separately. So that girls could also come to the school in Hijab and receive education.',
  'Generally the mosque committees are formed only to solve the common problems of the mosque. But “Muslim Charitable Fund Trust” was established along with the trust of the Jamia Masjid City, because we did not want our mosque to be just a mosque, our aim was to make this mosque a center of all muslim activities, mosque should also solve the problems of common muslim and become a learning center for muslims. We wanted to impart education to those muslim children who could not go to school due to financial constraints, we wanted to educate such children with the financial assistance from the muslim charitable fund and educate them in our school and madrasa.',
  '<strong>The beginning of Jamia-ul-uloom:</strong> This madrasa was started in 1982 with only two students. The trust worked hard, and I can never forget the services of Hazrath Moulana Riyazur Rahman Saheb, Khateeb-O-Imam Jamia Masjid, Bangalore city, who motivated people with his sermons, and more and more people come towards Jamia Masjid. The sermons of Moulana were so powerful and so inspiring and that, people who did not want to educate their children admitted their children to Jamia-ul-uloom. In the success of Jamia-ul-uloom, Moulana Riyazur Rehman played the most important role. We pray Allah show his blessings on Moulana.',
  'In 1986, there were two halls in the west side of the mosque. We started Nursery classes in these halls with prayers, this nursery is now a college. Gradually we established a tailoring institute, a calligraphy center and a Computer institute in the mosque.',
  '<strong>Jamia-Ul-Uloom, Shikshanagar (Bannikuppe):</strong> as we felt many hurdles in imparting standard to students in the busy life of the city, the trust plan for establishing a residential school away from the city, that children are educated in a peaceful atmosphere. Allah helped the trust to purchase 52 hectares of land at a cost of only Rs. 13.5 lakhs which is 27 Km from the city.',
 ) + '<p class="rc-sign">Alhaj Mohammed Ateeq Ahmed<small>Founder Secretary, Jame-ul-uloom, Jamia Masjid</small></p></blockquote>',
 single('', 'imam', caption='Late Moulana Riyazur Rahman Rashadi'), flip=False)}
<p>See also: <a href="Team.html">Governing Body</a> · <a href="Trustees.html">Trustees</a> · <a href="Message.html">Chairmen’s Messages</a> · <a href="Institutions.html">Institutions</a> · <a href="Masjid.html">Jamia Masjid</a></p>
</div>'''

# ---------------------------------------------------------------------------------------------------------------------
def letter(key, heading, by, body_html, key_note=None):
    s = scan('', key)
    return (f'<li class="rc-letter"><div>{s}</div><div class="rc-text"><h2>{heading}</h2><p class="rc-by">{by}</p>{body_html}'
            + (f'<p class="rc-scan-note">{key_note}</p>' if key_note else '') + '</div></li>')

HM_2013 = ['I take this opportunity to express my deep sense of gratitude to the staff, students, management for their consistent efforts in bringing out a wonderful website.',
              'We acknowledge and recognize the fact that every student is unique and we have been given the onerous responsibility of identifying and nurturing inherent talent.',
              'The academic year 2013-2014 will go down into the annals as another eventful year at JUU. Academically our students have done us proud by their brilliant performances. I thank whole heartedly the members of Editorial Committee for their tireless effort in bringing out the website this year.',
              'My best wishes for all the students in their endeavors.']

message = f'''<p class="eyebrow">About Us</p><h1>Chairmen’s Messages</h1><p class="lede">Messages from the Trust’s office-bearers and school heads.</p>
<ul class="rc-letters">
{letter('msg2', 'Message from the Secretary', 'Mohammed Ateeq Ahmed, Secretary',
  quote('I am pleased to learn that the Jame-ul-uloom Institutions are bringing out the new edition of their magazine “Impression”.',
        'I am particularly impressed with the excellent academic result at the SSLC examination. I congratulate the superintendent, the Head Mistress and the motivated staff.',
        'To the students, I want to tell them that there is no substitute for hard work. It is more honorable to fail than cheat. Be gentle with gentle people &amp; be tough with tough. For every enemy there is a friend. Know that a rupee earned fairly is of more value than lakhs earned by unfair means. Try hard to succeed, but also learn to lose and enjoy. Know about the wonder of books and have some quiet time to ponder upon the Mystery of the birds and bees. Have your own ideas even if one tells you they are wrong. Know how to laugh when you are sad, there is no shame in tears. If you are right, stand and fight. I wish you all success in your life.',
        'I am confident in the coming years all our institutions will continue to witness further success and achievement.',
        sign='Mohammed Ateeq Ahmed', role='Secretary'))}
{letter('msg3', 'Message from the President (Kannada)', 'Signed “Adhyakṣaru” (President), Jame-ul-Uloom Muslim Charitable Trust',
  '<p>A Kannada message headed “Shubha Sandesha” (a message of good wishes), with a portrait.</p>')}
{letter('msg4', 'From the Editors’ Desk', 'Syed Murtaza Hussain @ Gufran, Convener &amp; Vice President',
  quote('Penning down my feelings while writing this message can never be fully circumscribed by the words which follow. The aim of this magazine is to capture the various slices of activities, curricular and extracurricular, the tit bits of joys which we have lived passionately as the members of the Jame Ul Uloom family.',
        'Today the JU family is a reference in the educational sector because of all those who are directly and indirectly related and involved with it. Ours is a daily struggle to provide the best to our children and this relentless quest is a journey and not a destination for us. The vibrant young and dedicated staff, the supportive parents, the commitment of the administrative body have fused to usher an excellent working ethos which permeates almost all the activities under taken by Jamia Ululoom.',
        'I want all our students to search for their own perfect ideals and work hard towards reaching them because when you follow your dream, doors open where you would not have thought there would be doors. Education, above all is all about unlocking and unleashing the dormant potential found deep within each student. I am convinced that each one of our student is a precious asset not only for the school or family but for the whole of humanity.',
        'May truth, humility, compassion and a sense of justice guide us in every journey we all under take in life.',
        sign='Syed Murtaza Hussain @ Gufran', role='Convener &amp; Vice President'))}
{letter('msg5', 'Message from the Joint Secretary (Urdu)', 'Syed Noorul Ameen Anwar, Joint Secretary',
  '<p>An Urdu message headed “جامع العلوم قوم کا ایک عظیم ورثہ ہے” (“Jame-ul-Uloom is a great heritage of the community”), signed by Syed Noorul Ameen Anwar, Joint Secretary, with a portrait.</p>')}
{letter('msg6', 'Message from the Treasurer', 'Mohammed Athiulla Khan, Treasurer',
  quote('Education is an ability to meet life’s situations. Knowledge leads to our destinations. To turn events into ideas is the function of literature. Work satisfaction is closely related to life satisfaction. The fines anti doe for w <span class="rc-illegible">[…]</span> … of our Institution all the best in the endeavors in the pursuit of knowledge and to make it as means of their empowerment towards a better world.',
        'I congratulate the Editorial Board for publishing a impressive “Impression”.',
        sign='Mohammed Athiulla Khan', role='Treasurer'))}
{letter('msg7', 'Message from the Superintendent', 'Syed Rasool, Superintendent (school magazine 2010–11)',
  quote('It gives me a great pleasure to present our school magazine for the academic year 2010-11. Our school is striving hard to provide qualitative education to our students and to help them to combat the vices. Our school emblem endorses our goal to aim more knowledge and to reach higher destinations.',
        'I appreciate the nobility, sincerity and honesty of our respected Secretary Alhaj Mohammed Atheeq Ahmed Saheb who has dedicated his life for the welfare of the Institution in particular, and to the community at large in spite of his many other social services. In his endeavor, he gets the full co-operation of the Trustees. We pray for his long and healthy life.',
        'Dear students, you are fortunate to have an efficient Headmistress Mrs. Naveeda Naaz and her learned colleagues.',
        'I desire, you turn each obstacle, you come across, into an opportunity and the opportunity into success.',
        'Dear students my message to you is “STRIVE HARD, NEVER LOSE HOPE AND ACHIEVE”.',
        sign='Syed Rasool', role='Superintendent'))}
{letter('msg8', 'Message from the Head Mistress', 'Naveeda Naaz, Head Mistress (academic year 2010–2011)',
  quote('I take this opportunity to express my deep sense of gratitude to the staff, students, management for their consistent efforts in bringing out a wonderful magazine “Impression”.',
        'We acknowledge and recognize the fact that every student is unique and we have been given the onerous responsibility of identifying and nurturing inherent talent.',
        'The academic year 2010-2011 will go down into the annals as another eventful year at JUU. Academically our students have done us proud by their brilliant performances. I thank whole heartedly the members of the Editorial Committee for their tireless effort in bringing out the “Impression” this year.',
        'My best wishes to all students in their endeavors.',
        sign='Naveeda Naaz', role='Head Mistress'))}
</ul>
<h2 id="head-mistress-2013">Head Mistress’s message, 2013–14</h2>
{split(quote(*HM_2013, sign='Naveeda Naaz (M.A, B.Sc, B.Ed)', role='Head Mistress') + '', single('', 'hm', caption='Head Mistress'))}
<p>The Principal’s message of the Boys Residential School, Banikuppa is on the <a href="ResidentialSchoolBanikuppa/message.html">Banikuppa Principal’s Message page</a>. Letters of appreciation from public figures are on the <a href="Recognitions.html">Recognitions page</a>.</p>'''

# ---------------------------------------------------------------------------------------------------------------------
GOV = [('Maqbool Ahmed', 'President'), ('Mohammed Ateeq Ahmed', 'Secretary'), ('Syed Murtuza Husain @ Gufran', 'Vice President'),
       ('Mohammed Athiulla Khan', 'Treasurer'), ('Syed Noorul Ameen @ Anwer', 'Joint Secretary'), ('Syed Abdul Gafoor', 'Internal Auditor')]
team = f'''<p class="eyebrow">About Us</p><h1>Governing Body</h1><p class="lede">The office-bearers of the Jamia Masjid &amp; Muslim Charitable Fund Trust.</p>
<div class="rc-prose">
{split('<h2>Office-bearers</h2>' + people(GOV), single('', 'gov', caption='Governing Body'))}
<h2>Jamia Masjid Trust</h2>
{single('', 'trust_group', big=True, caption='Group photograph labelled “Jamai Masjid Trust”')}
<h2 id="earlier">Earlier Governing Body poster</h2>
{single('', 'gov_old', caption='Governing Body: earlier poster', detail='An earlier poster.')}
<h3 id="earlier-names">Names and designations printed on the earlier poster</h3>
{people([('C.M. Aleemulla Khan · Mushtaq', 'President'), ('Mohammed Ateeq Ahmed', 'Secretary'), ('Maqbool Ahmed', 'Vice President'), ('Mohammed Athiulla Khan', 'Treasurer'), ('Syed Noorul Ameen · Anwar', 'Joint Secretary'), ('Moulana Riyazur Rahman Rashedi', 'Principal in chief'), ('Attar Syed Murtaza Hussain · Gufran', 'Convenor'), ('Syed Abdul Gafoor', 'Internal Auditor')])}
<p>See also the <a href="Trustees.html">Trustees</a> and <a href="Message.html">Chairmen’s Messages</a>.</p>
</div>'''

TRUSTEES = ['Abbas Khan', 'Naveed Ahmed', 'Syed Sadaqath Peeran', 'J. Shafiulla', 'Moin Abdul Kareem', 'Zaheeruddin Ahmed', 'Mohammed Saifulla', 'L. Mohamed Farooq',
            'Zafrulla Khan', 'Allah Bakash Khan', 'Ashfaq Ahmed', 'Allah Bakash', 'B. Md. Ghouse Qureshi', 'Syed Hussain', 'Mir Qamar Hussain', 'Abdulla Basha', 'Iqbal Ahmed']
trustees = f'''<p class="eyebrow">About Us</p><h1>Trustees</h1><p class="lede">The Trustees of the Jamia Masjid &amp; Muslim Charitable Fund Trust.</p>
<div class="rc-prose">
{split('<h2>Trustees</h2>' + people([(n, '') for n in TRUSTEES]).replace('<span></span>', ''), single('', 'trustees', caption='Trustees'))}
<h2 id="earlier">Earlier Trustees poster</h2>
{single('', 'trustees_old', caption='Trustees: earlier poster', detail='An earlier poster.')}
<p>See also the <a href="Team.html">Governing Body</a>.</p>
</div>'''

# ---------------------------------------------------------------------------------------------------------------------
calligraphy = f'''<p class="eyebrow">Institutions</p><h1>Calligraphy Centre</h1><p class="lede">The Calligraphy Centre run at the Jamia Masjid premises.</p>
<div class="rc-prose">
{logo('', 'logo_cal')}
{split(
 '<h2>Calligraphy Centre being run at Jamia Masjid premises</h2>' + p(
  'The center for learning urdu language and urdu calligraphy was started in the year 1981. It was felt that the students learning in government and private schools are not having an opportunity to learn urdu language and the art of urdu calligraphy, hence Majlis-e-Millia Islamia with the help from the Bureau for Promotion of Urdu, Ministry of Human Resources, New Delhi started this course.',
  'Though NCPUL has withdrawn the support, MMI is running this course which consists of a 2 years calligraphy training along with learning urdu language and use of computers where students can learn basics in computer and DTP and use of urdu software.',
  'The students also are given a chance to learn diniyat and tailoring and also pottery painting. This course is very useful for those who have failed in 10th std. or who don’t want to continue their studies after passing their 10th std. Muslim girls can come in full purdah and they have a secure learning atmosphere in the Mosque along with a very good library. The students can also get jobs and help their family financially. All this facility is free of cost. No fee is charged and all the expenditure is borne by MMI and Jamia-Ul-Uloom. The students and their parents can take full advantage of this facility to learn our own urdu language and also get themselves skilled and fit to be appointed.'),
 single('', 'cal_intro', caption='Calligraphy Centre'))}
{info('For current course details and fees, please contact the office (<a href="Contact.html">Contact</a>).')}
<h2>Gallery</h2>
{gallery('', ['cal1', 'cal2', 'cal3', 'cal4', 'cal5', 'cal6', 'cal7', 'cal8'])}
</div>'''

# ---------------------------------------------------------------------------------------------------------------------
classroom = f'''<p class="eyebrow">Facilities</p><h1>Smart Classrooms</h1><p class="lede">Computerised classroom teaching at Jame-ul-uloom School.</p>
<div class="rc-prose">
{p('An opportunity has been created by Jame-ul-uloom School for the students who can access a unique way of computerised education in their curriculum. Hoping that the students shall enhance their knowledge and make learning more interactive and interesting.',
   'Digital classes play a crucial role in the life of a student as well as teachers and cover the subjects like English, Mathematics, Science, Social Sciences, Comprehension passages, nursery rhymes with animations, videos and examination guidelines etc. Thus the school has worked a massive project to develop an information which will cater to the needs of the students in all subjects.')}
{gallery('', ['cls1', 'cls2', 'cls3'])}
<p>Classroom photographs of individual institutions are on their own Facilities pages: <a href="PUGirlsCollege/Facilities.html">PU College</a> · <a href="DegreeGirlsCollege/Facilities.html">Degree College</a> · <a href="BCA/Facilities.html">BCA</a> · <a href="EngBoysHighSchool/Facilities.html">Boys High School</a> · <a href="EngGirlsHighSchool/Facilities.html">Girls High School</a>.</p>
</div>'''

computerlab = f'''<p class="eyebrow">Facilities</p><h1>Computer Laboratory</h1><p class="lede">The college computer laboratory.</p>
<div class="rc-prose">
{p('The college is housed in a spacious building with well furnished and ventilated class rooms, well equipped laboratories and library with good collection of books. Magazines and News papers are also subscribed for the benefit of the students. The computer lab is provided with internet facility. A spacious auditorium is also under construction. We aim to provide canteen facility for our students. A nationalized bank (Canara Bank) is also located in the same building.')}
{gallery('', ['col_comp', 'col_comp2'], captions={'col_comp': 'Computer laboratory (BCA / Degree college)', 'col_comp2': 'Computer laboratory (PU college)'})}
<p>School computer education (from 1st to 10th standard) is described on the <a href="EngGirlsHighSchool/Facilities.html">English High School Facilities</a> pages. The <a href="NCPUL/home.html">MMI-NCPUL Computer Centre</a> has its own pages.</p>
</div>'''

library = f'''<p class="eyebrow">Facilities</p><h1>Library</h1><p class="lede">Photographs of the school library.</p>
<div class="rc-prose">
<p>Descriptions of the libraries of individual institutions are on their own pages: <a href="PUGirlsCollege/Facilities.html">PU College</a> · <a href="DegreeGirlsCollege/Facilities.html">Degree College</a> · <a href="BCA/Facilities.html">BCA</a> · <a href="NCPUL/Library.html">NCPUL</a> · <a href="ITI/Library&amp;CompLab.html">ITI</a>.</p>
{gallery('', ['lib1', 'lib2', 'lib3'])}
</div>'''

auditorium = f'''<p class="eyebrow">Facilities</p><h1>Auditorium</h1><p class="lede">Functions of the Jame ul uloom Group of Institutions.</p>
<div class="rc-prose">

{gallery('', ['audi1', 'fn5', 'audi2', 'fn6', 'fn7'])}
<p>More photographs of annual-day and house programmes are on the <a href="Activities.html">Activities</a> page.</p>
</div>'''

SPORTS_TEXT = ('The students are grouped into four houses and each house is under the supervision of the house masters who planned co-curricular and sports activities. '
               'Fridays are used to conduct literary activities such as debates, essay writing, poem recitation, seminars, drawing, quiz competitions and Leadership training. '
               'These activities culminate in annual school day competition and the successful students are awarded certificates and trophies on annual day celebrations. '
               'Certificates are also awarded for good academic performance, good behavior and cent percent attendance. Inter house competitions are held in football, volley ball, cricket, kabadi and Athletic events. '
               'Winners and runners are awarded certificates and medals. The students also participate in taluk, district and state level competitions earn name and fame and bring laurels to the school.')
sports = f'''<p class="eyebrow">Students</p><h1>Co-Curricular Activities &amp; Sports</h1><p class="lede">Co-curricular activities and sports at the Residential Higher &amp; Primary School, Banikuppa.</p>
<div class="rc-prose">
{p(SPORTS_TEXT)}
<h2>Photographs</h2>
{gallery('', ['iti_play1'], captions={'iti_play1': 'Playground of the ITI campus'})}
<p>Sports-day and house photographs from the Banikuppa campus are in <a href="Activities.html#pv-activities">Activities in pictures</a>. The annual calendar of school competitions is on the <a href="Activities.html">Activities</a> page.</p>
</div>'''

# ---------------------------------------------------------------------------------------------------------------------
masjid = f'''<p class="eyebrow">Jamia Masjid</p><h1>Jamia Masjid, Bangalore</h1><p class="lede">The mosque at City Market, on whose campus Jame-ul-uloom functions: prayer times, photographs and videos of the halls, library and study rooms, the Trust’s charitable activity and historical documents.</p>
<div class="rc-prose">
@@MASJID_TOP@@
<h2 id="prayer-times">Prayer times</h2>
<ul class="times"><li><strong>Fajar</strong>5:40 AM</li><li><strong>Zohar</strong>1:30 PM</li><li><strong>Asar</strong>5:00 PM</li><li><strong>Magrib</strong>6:35 PM</li><li><strong>Isha</strong>8:15 PM</li></ul>
<p>Prayer times change through the year; please confirm with the masjid office on <a href="tel:0822239495">0822239495</a>.</p>
@@MASJID_SECTIONS@@
<h2>About Jame-ul-uloom</h2>
{p('Jame-ul-uloom is an Arabic name meaning “Center of Knowledge”. Jame-ul-uloom is housed in the campus of Jamia Mosque, one of the biggest mosques in the state, located in the heart of the Bangalore City. Apart from imparting education, the Institution aims at “character building”. This is achieved through moral education and religious instruction.',
   'Upliftment of the downtrodden in the Minority Community is the aim of Jame-ul-uloom. It also aims in preparing good and useful citizens, so that they can face the situations in this world of competition. To accomplish many such purposes, Jame-ul-uloom has in its fold institutions.',
   'The uniqueness of Jame-ul-uloom is that it is probably a single institution which is functioning under the aegis of a mosque imparting modern education along with moral religious education in the light of Holy Quran and Hadith. About a dozen teachers including Hufaz and Moulvies are employed for the purpose. All the classes right from L.K.G to PUC will have one Arabic teaching period on all working days. On every Thursday in the last two periods a religious congregation, “ijtima” is conducted for all the girl students. Separate arrangements are made for adult education by a well qualified teacher outside the working hours of the school.')}
<h2>Charitable activity</h2>
{p('In general a Masjid committee is formed to look after Masjid activity whereas Jamia Masjid has added one more activity, i.e. Charitable activity, which means to take care of muslims educational needs so as to make every muslims future very bright, particularly those who are unable to get educated due to poverty.')}
<p><a href="AboutUs.html">Read the founding story and the Founder Secretary’s essays →</a></p>
<h2 id="documents">Historical documents (Urdu)</h2>
<p>Two Urdu PDF documents about the Jamia Masjid are available to read and download below.</p>
{doc_list('', ['tareeq', 'majalla'])}
</div>'''

# ---------------------------------------------------------------------------------------------------------------------
DIARY_EVENTS = [
 ('May 27.05.2013', 'Monday', 'School reopens'), ('June 25.06.2013', 'Tuesday', 'Shab-e-Barat'), ('July 02.07.2013', 'Tuesday', '1st Round Test, 1st Std. to X Std.'),
 ('Aug 05.08.2013', 'Monday', 'Shab-e-Qadr'), ('09.08.2013', 'Friday', 'Eid-ul-Fitr'), ('15.08.2013', 'Thursday', 'Independence Day'),
 ('September 09.09.2013', 'Tuesday', 'Ganesh Chaturthi'), ('22.09.2013', 'Saturday', 'Mid Term / 1st Semester Exam'),
 ('October 02.10.2013', 'Wednesday', 'Gandhi Jayanthi'), ('04.10.2013', 'Friday', 'Mahalaya Amavasya'), ('14.10.2013', 'Monday', 'Vijaya Dasami'), ('16.10.2013', 'Wednesday', 'Eid-ul-Azha'), ('28th to 31st', 'Mon–Thurs', 'Sports for primary'),
 ('November 01.11.2013', 'Friday', 'Rajyotsava Day'), ('04.11.2013', 'Monday', 'Diwali'), ('19th to 21st', 'Mon–Wed', 'Sports for High School'), ('26.11.2013', 'Monday', '3rd Round Test for High School'),
 ('December 1.12.2013', 'Saturday', 'Kanakadasa Jayanthi'), ('23rd to 25th', 'Mon to Wed', 'Christmas Vacation'), ('27.12.2013', '', 'Sports for Kinder Garden'),
 ('January 2014 14.01.2014', 'Monday', 'Makara Sankranti'), ('15.01.2014', 'Friday', 'Eid-e-Milad'), ('26.01.2014', 'Sunday', 'Republic Day'), ('27.01.2014', 'Monday', 'Fourth Round Test'),
 ('February 2014', 'To be announced', '2nd Round Test for Primary; Preparatory Exam for Std. X'), ('28.02.2014', '', 'Mahashivaratri'),
 ('March 2014', 'To be announced', 'Final Semester Exam'), ('April 2014', '', 'Results of all classes')]
diary = f'''<p class="eyebrow">Admissions</p><h1>Admissions Diary 2013–14</h1><p class="lede">Rules, admission conditions, discipline and calendars from the school diary.</p>
<div class="rc-prose">
{doc_list('', ['diary'])}
<h2>Our Vision</h2>
<p>In our school we take pride in the following:</p>
{vision(['To cherish the quality of simplicity of a person’s behaviour, relationship and lifestyle', 'To be always friendly, polite and courteous with everyone everywhere, and cleanliness of the school premises', 'To initiate and promote experimentation and innovativeness in education.', 'To inculcate the habit of punctuality, regularity and discipline.'])}
<p>The main objectives of Jame-ul-uloom are:</p>
{vision(['To pursue excellence and to mould the character', 'To develop the spirit of national integration and create a sense of Indianness among children.', 'To initiate and promote experimentation and innovativeness in education.', 'To inculcate the habit of punctuality, regularity and discipline.'])}
<h2 id="rules">Rules and Admission</h2>
<ol>
<li>Jame-ul-uloom school is open to both girls and boys.</li>
<li>Admission will be made on the basis of seats in particular class.</li>
<li>Birth Certificate from the Corporation Chief Registrar of Birth, with the child’s name entered should be produced without fail in respect of children seeking admission to the pre-primary standard and above. A transfer certificate from educational institution previously attended by the child should be duly countersigned by the B.E.O of Education Department.</li>
<li>Children who have studied in schools in states other than Karnataka should have their transfer certificate duly countersigned by D.D.P.I of the state or District concerned.</li>
<li>Fees once paid will not be refunded on any account.</li>
</ol>
<h2>Special Features of the School</h2>
<div class="rc-twocol"><ul><li>Career Guidance</li><li>Well equipped laboratory and library</li><li>Exhibition, Sports facilities</li><li>Felicitations for the toppers</li><li>Trips and Excursions</li><li>Medical Check up</li></ul><ul><li>Literary Competitions</li><li>National festivals</li><li>Workshops &amp; Seminars</li><li>Inter Schools Debates</li><li>Graduation</li><li>Many other special programmes for the overall development of students</li></ul></div>
<h2>High-Lights of Jame-Ul-Uloom</h2>
{p('This prestigious School of ours is a linguistic minority institution. This is a recognised institution which was started in the year 1983-84, with just two pupils in the basement of the Musjid. By the grace of Allah, and with the full co-operation of the office bearers and Trustees, the institutions have expanded by leaps and bounds. At present we have around 3,500 pupils, studying in different courses.',
   'This institution of Jame-ul-uloom which is attached to Jamia Masjid, imparts Deeniyath and moral education to all its pupils apart from the formal education. This is to mould the character of the young and to develop in them a desire to live an honourable life in the modern society.')}
<h3>For Primary Classes</h3>
<ol><li>Promotion from class I to IV Std. shall be decided on the basis of continuous comprehensive assessment made every month of the work done in the class and assignments given to the children, in Semester Examination.</li><li>Home work is given to encourage and develop independent study skill.</li><li>Home work time table is given to all students who are required to complete the work as assigned by subject teachers.</li><li>Class assessments are considered to evaluate their overall performance throughout the year. Remedial classes for slow learners are conducted on a regular basis to help and boost their academic performance.</li></ol>
<h3>Jame-ul-uloom High School</h3>
{p('Started in 1990-91 this school has so far sent 20 batches of students for S.S.L.C Examination of them 11 batches gave us 100% results. During the year 2012-2013, 158 students appeared for the SSLC Examination. Out of 158 students 24 students obtained distinctions and the percentage pass was 100 %.')}
<h3>Extra Curricular Activities</h3>
{p('All round development of the personality of a child is the goal of education and besides academics students are given opportunities in extra curricular activities like Quiz, debate, fancy dress, painting, creative writing etc. to develop their own talents. Students attend competitions organised by other schools and DHIE.',
   'Teachers day and children’s day, national festivals like Independence day and Republic day are some of the occasions when the children exhibit their talents in various fields.')}
<h3>Compulsory Computer Education</h3>
{p('It is an accepted fact that in the modern age, life will be blank without computers. With a view to keep our students abreast with the modern information, computer education is made compulsory right from IV Standard. Arrangement for computer education is made separately for girls and boys in different blocks.')}
<h3>Examination &amp; Promotion</h3>
{p('A time table is given a week before a test/Examination. Pupils absent for any reason are not re-examined. In case of an unforeseen holiday, the test/examination of the day will be conducted after the last paper as per the time table.',
   'The final Examination report for all students from 1 Std to IX Std will be issued in April 2014 to confirm the result of the year’s work.',
   '75 % attendance is mandatory for all the students.',
   'Promotion is decided by the head mistress in consultation with teachers. Answer papers of final Examination shall not be given to parents/guardians. Answer papers of other tests/examinations will be shown to parents/guardians.')}
<h2 id="discipline">School Discipline</h2>
<ol>
<li>Our School is known for its values. A man may achieve any height he aspires, but if he is ignorant of the basic values like discipline, punctuality, good mannerism, respect, love, compassion etc., he has not gained much in life.</li>
<li>The School follows certain norms to help the students achieve these goals. All students are expected to be well aware of all the rules and also to follow them without any lapse.</li>
<li>As the medium of instruction is English, children should speak in English in the school premises with their teachers and companions to develop their conversation ability. Parents should encourage their children to talk in English, in addition with their mother-tongue at home with brothers and sisters.</li>
<li>Students should bring the school diary everyday to school. They should bring to the class the necessary text books and note books as per the time table.</li>
<li>It is necessary that the students cultivate the best etiquette and conduct themselves well in school and wherever they go. It is important that the students bear in mind the fact that the school is judged by their conduct, behaviour and performance. They should always greet their teachers, elders and friends in an amiable and audible tone of voice whenever and wherever they meet them in school or outside.</li>
<li>Cellphones are strictly prohibited.</li>
<li>A school canteen is provided in the premises. Students are prohibited to buy eatables from outside the school campus. No student will be sent home in between school hours. In case of emergency the parents should contact the Headmistress.</li>
<li>The school authorities reserve the right to dismiss those students whose progress in studies is unsatisfactory.</li>
<li>Students are responsible for all personal belongings.</li>
<li>Students are expected to be within the school campus by 8.40 a.m. Repeated late-coming and disinterest in studies will not be tolerated. Discipline in the assembly, in the classrooms and in between the periods should be maintained.</li>
<li>Leave of absence will not be granted without prior submission of leave application from the parent or guardian. In case of absence without a leave letter, on returning to school the students must bring the leave note signed by the parent or guardian.</li>
<li>Neatness and cleanliness are insisted; students are expected to come to school daily in freshly laundered uniform with clean socks and well polished shoes. Any student who comes to school in a slovenly condition will be excluded from class or sent home.</li>
<li>Attendance is mandatory on the first and last day of each term.</li>
</ol>
<h3>Assignments</h3>
<p>Students are required to attend assignments that are given to them at the school, the schedule of which is given below.</p>
{table(['Day', 'Subjects'], [['Monday', 'Urdu &amp; Mathematics'], ['Tuesday', 'English &amp; Social Science'], ['Wednesday', 'Kannada &amp; Gen. Science'], ['Thursday', 'Urdu &amp; Social Sciences'], ['Friday', 'English &amp; Gen. Science'], ['Saturday', 'Kannada &amp; Mathematics']])}
<h3>Results</h3>
{p('Pupils who fail in VIII and IX standard will not be permitted to continue their studies in our institution. There is no provision for reconsideration of failures. Result once declared according to the rules of the education department, cannot be altered. Parents are requested not to take the trouble of meeting the Head Mistress or Management for this purpose.')}
<h3>Educational Excursion</h3>
{p('Pupils are taken to visit places of historical or geographical interest. All students are expected to participate in these excursions, whenever such excursions are arranged separately for both boys and girls.')}
<h3>While on the Bus / Van</h3>
<p>The students who are using school transport are expected strictly to adhere to the following rules.</p>
<ol><li>Be on the allotted time at the point of boarding.</li><li>Always be seated till your destination.</li><li>Do not pick up fight or tease the fellow passengers.</li><li>Do not cause inconvenience to others with your belongings in the way.</li><li>Do not damage the bus or van in any way.</li><li>Respect all the rules set by the driver, helper, teacher in charge.</li><li>Maintain perfect discipline with your best behavior.</li></ol>
<h2 id="school-awards">School Awards</h2>
{p('A glittering function was held on 13th December 2012 at Town Hall for the meritorious students of Jame-Ul-Uloom Group of Institutions. Dr. Hans Raj Bharadwaj, Hon’ble Governor, Government of Karnataka, was the Chief Guest. Alijanab R. Roshan Baig Saheb, M.L.A. Jayamahal, Bangalore and Alijanab Abdul Qadeer Sahab, Secretary, Allama Iqbal Education Society and Shaheen Group of Institutions, Bidar were the Guests of Honour.',
   'The Awards and Prizes to meritorious students of Jame-ul-uloom College Bachelor of Computer Application, Composite P.U. College, English High School, Bangalore and Residential High School, Bannikuppe, Industrial Training Institute. Special feature of the function was that awards were given to the City Muslim Organizations. Trustees of Jame-ul-uloom, many dignitaries of the City, parents and other invitees attended the function.',
   'Special prizes are given to the students class wise every year for regular attendance, cleanliness, best performance in studies throughout the year. Literary activities such as debate, quiz, essay writing, sports and athletic and team games are taught and competitions were conducted and prizes are awarded to the winners.')}
<h2>Newspaper in Education</h2>
{p('Deccan Herald in Education programme was introduced in our school since 2004-05. It is a programme designed to help the students identify and harness it as a classroom tool. The newspaper is a vibrant current medium that can be effectively used by the students to relate the textual facts to reality, thus bringing enthusiasm into classroom situations, besides increasing the child’s general awareness it also gives the child a basic reading habit and enhancing his/her knowledge of the changing world hand in hand with the text book.',
   'The DHIE hold workshops on various topics. These workshops are conducted by highly talented and qualified personalities of Deccan Herald. Children participate in these workshops enthusiastically. The child is therefore exposed to a wider range of knowledge, besides the regular curriculum.')}
<h2>Smart Classrooms</h2>
<p>Read about the <a href="Classroom.html">Smart Classrooms</a>.</p>
<h2>Declaration by Parent / Guardian</h2>
<h2>Activity Calendar 2013–2014</h2>
<p>The month-by-month competitions are listed on the <a href="Activities.html">Activities</a> page.</p>
<h2>Calendar of Events</h2>
{table(['Date', 'Day', 'Event'], [[escape(a), escape(b), escape(c)] for a, b, c in DIARY_EVENTS])}
</div>'''

ROOT = {
    'AboutUs.html': ('About Us', about, 'About Jame-ul-Uloom: vision, history, the founding idea and the Founder Secretary’s essays.'),
    'Message.html': ('Chairmen’s Messages', message, 'Messages from the Secretary, President, Convener, Joint Secretary, Treasurer, Superintendent and Head Mistress of Jame-ul-Uloom.'),
    'Team.html': ('Governing Body', team, 'The Governing Body of the Jamia Masjid & Muslim Charitable Fund Trust.'),
    'Trustees.html': ('Trustees', trustees, 'Trustees of the Jamia Masjid & Muslim Charitable Fund Trust.'),
    'Calligraphy.html': ('Calligraphy Centre', calligraphy, 'The Urdu calligraphy and computer centre run at the Jamia Masjid premises.'),
    'Classroom.html': ('Smart Classrooms', classroom, 'Smart classrooms at Jame-ul-uloom School.'),
    'ComputerLab.html': ('Computer Laboratory', computerlab, 'The college computer laboratory at Jame-ul-uloom.'),
    'Library.html': ('Library', library, 'Library photographs of Jame-ul-uloom.'),
    'Auditorium.html': ('Auditorium', auditorium, 'The auditorium and functions of the Jame ul uloom Group of Institutions.'),
    'Sports.html': ('Co-Curricular Activities & Sports', sports, 'Co-curricular activities and sports.'),
    'Masjid.html': ('Jamia Masjid', masjid, 'Jamia Masjid, Bangalore: prayer times, the main and secondary halls, the pathway and water channel, libraries and study halls, charitable activity and historical Urdu documents.'),
    'AdmissionsDiary.html': ('Admissions Diary 2013–14', diary, 'The 2013–14 school diary of Jame-ul-uloom: rules, admission conditions, discipline and calendars.'),
}
