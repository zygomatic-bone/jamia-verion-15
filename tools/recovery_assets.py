"""Phase 9: photographs, scans and documents recovered from the original server backup.

Every entry maps one authentic file in the original `public_html/` to its place in the deployed site.

    key -> (original path, destination under public/portal-assets/images/, alt text, caption)

* Files are copied byte-for-byte (so they stay provably authentic). The only change made is that CMYK JPEGs, which some
  browsers and phones render with wrong colours, are converted to RGB.
* Destination names are lower-case (the host is case sensitive). Identical pictures that the old site copied into
  every institution folder are stored ONCE and shared by key.
* `tools/import_recovered_assets.py` performs the copy; `tools/recovery_manifest.py` writes the manifest CSV.
"""

R = 'portal-assets/images/'            # folder (inside public/) that holds every recovered image
DOC = 'portal-assets/documents/'          # original PDFs

# key: (source in backup, destination below R, alt text, caption)
IMAGES = {
    # ---- Chairmen's messages (scanned letters, originally homeimages/Message2..8.jpeg) ------------------------------
    'msg2': ('homeimages/Message2.jpeg', 'messages/message-2-secretary.jpeg', 'Message from Mohammed Ateeq Ahmed, Secretary, on a blue snowflake background with his portrait', 'Message 2 · Secretary'),
    'msg3': ('homeimages/Message3.jpeg', 'messages/message-3-president-kannada.jpeg', 'Kannada-language message headed “Shubha Sandesha”, signed by the President of the Jame-ul-Uloom Muslim Charitable Trust, with his portrait', 'Message 3 · President (Kannada)'),
    'msg4': ('homeimages/Message4.jpeg', 'messages/message-4-convener.jpeg', 'Message “From the Editors desk” by Syed Murtaza Hussain @ Gufran, Convener and Vice President, with his portrait', 'Message 4 · Convener & Vice President'),
    'msg5': ('homeimages/Message5.jpeg', 'messages/message-5-joint-secretary-urdu.jpeg', 'Urdu-language message signed by Syed Noorul Ameen Anwar, Joint Secretary, with his portrait', 'Message 5 · Joint Secretary (Urdu)'),
    'msg6': ('homeimages/Message6.jpeg', 'messages/message-6-treasurer.jpeg', 'Message from Mohammed Athiulla Khan, Treasurer, on a parchment background with his portrait', 'Message 6 · Treasurer'),
    'msg7': ('homeimages/Message7.jpeg', 'messages/message-7-superintendent.jpeg', 'Message from Syed Rasool, Superintendent, on a blue background with his portrait', 'Message 7 · Superintendent'),
    'msg8': ('homeimages/Message8.jpeg', 'messages/message-8-head-mistress.jpeg', 'Message from Naveeda Naaz, Head Mistress', 'Message 8 · Head Mistress'),

    # ---- J.U Darul Quran Arabic College (image-only "About Us" pages and plan) ---------------------------------------
    'dq_en': ('homeimages/AboutEng.jpg', 'darul-quran/about-english.jpg', 'Printed English page headed “J.U Darul Quran Arabic College, Bangalore” with the history of Jame-ul-Uloom, the Arabic College and an appeal', 'About Us (English)'),
    'dq_ur': ('homeimages/Shobaehifz.jpg', 'darul-quran/about-urdu.jpg', 'Printed Urdu page headed “J.U Darul Quran Arabic College, Bangalore” carrying the Urdu version of the college history and appeal', 'About Us (Urdu)'),
    'dq_plan': ('homeimages/Proposed.jpg', 'darul-quran/proposed-plan.jpg', 'Architect’s drawing “Proposed J.U Darul Quran & Arabic College, Bangalore”: front elevation and ground-floor plan', 'Proposed building: front elevation and ground-floor plan'),

    # ---- Portraits and group photographs of the main portal ----------------------------------------------------------
    'imam': ('homeimages/ImamSab.jpg', 'people/moulana-riyazur-rahman-rashadi.jpg', 'Portrait of Late Moulana Riyazur Rahman Rashadi seated at a desk', 'Late Moulana Riyazur Rahman Rashadi'),
    'trust_group': ('homeimages/Team.jpg', 'people/jamia-masjid-trust-group.jpg', 'Group photograph of fourteen members of the Jamia Masjid Trust standing and seated in two rows', 'Group photograph labelled “Jamai Masjid Trust”'),

    # ---- Calligraphy Centre -------------------------------------------------------------------------------------------
    'cal_intro': ('homeimages/Caligraphy1.jpg', 'calligraphy/calligraphy-1.jpg', 'Calligraphy artwork: a basket of fruit with Arabic lettering and the word “Calligraphy”', 'Calligraphy Centre'),
    'cal1': ('homeimages/cali1.jpg', 'calligraphy/calligraphy-0-emblem.jpg', 'Calligraphy Centre artwork: a palm tree and a mosque inside a circle above the words JAME-UL-ULOOM, with lines of Urdu lettering beside it', 'Calligraphy Centre artwork “Cali1”'),
    'cal2': ('homeimages/cali2.jpg', 'calligraphy/calligraphy-2.jpg', 'Calligraphy artwork: Urdu verse in green and red lettering on a brown panel', 'Calligraphy Centre gallery'),
    'cal3': ('homeimages/Cali3.GIF', 'calligraphy/calligraphy-3.gif', 'Calligraphy artwork: a Naskh calligraphy handicraft pot', 'Calligraphy Centre gallery'),
    'cal4': ('homeimages/Cali4.GIF', 'calligraphy/calligraphy-4.gif', 'Calligraphy artwork: an Arabic phrase engraved in relief on a grey surface', 'Calligraphy Centre gallery'),
    'cal5': ('homeimages/Cali5.GIF', 'calligraphy/calligraphy-5.gif', 'Calligraphy artwork: Arabic lettering in gold relief', 'Calligraphy Centre gallery'),
    'cal6': ('homeimages/Cali6.GIF', 'calligraphy/calligraphy-6.gif', 'Calligraphy artwork: an Urdu title panel with a decorative floral frame', 'Calligraphy Centre gallery'),
    'cal7': ('homeimages/Cali7.GIF', 'calligraphy/calligraphy-7.gif', 'Calligraphy artwork: Arabic lettering over a basket of fruit', 'Calligraphy Centre gallery'),
    'cal8': ('homeimages/cali8.jpg', 'calligraphy/calligraphy-8.jpg', 'Calligraphy artwork: Urdu verses with a quill and ink pot', 'Calligraphy Centre gallery'),
    'tailoring': ('homeimages/Tailoring3.gif', 'tailoring/tailoring-class.gif', 'Women seated at sewing machines in the Tailoring Department hall', 'Tailoring Department, Jamia Masjid'),

    # ---- Transport, functions and activities --------------------------------------------------------------------------
    'veh1': ('homeimages/Vehicle1.jpg', 'transport/vehicle-1.jpg', 'Three yellow Jame-ul-uloom school buses parked side by side', 'School buses'),
    'veh2': ('homeimages/Vehicle2.jpg', 'transport/vehicle-2.jpg', 'A yellow Jame-ul-uloom school bus seen from the front left', 'School bus'),
    'veh3': ('homeimages/Vehicle3.jpg', 'transport/vehicle-3.jpg', 'A yellow Jame-ul-uloom English Nursery, Primary and High School bus seen from the side', 'School bus'),
    'fn5': ('homeimages/audi5.jpg', 'events/function-1.jpg', 'Stage of a Jame-ul-uloom function with dignitaries seated in a row under a banner', 'Function of the institutions'),
    'fn6': ('homeimages/audi6.jpg', 'events/function-2.jpg', 'Dignitaries and award recipients standing on a red-draped stage holding certificates and trophies', 'Function of the institutions'),
    'fn7': ('homeimages/audi7.jpg', 'events/function-3.jpg', 'A guest in a shawl presenting a memento to an elderly gentleman in a cap on stage', 'Function of the institutions'),
    'act1': ('homeimages/Activ1.jpg', 'events/activity-schools-1.jpg', 'Children performing on a decorated stage at a school programme', 'School programme'),
    'act2': ('homeimages/Activ2.jpg', 'events/activity-2.jpg', 'Girls speaking at microphones on the stage of a school programme under a “JAMIA-U…” banner', 'School programme'),
    'act3': ('homeimages/Activ3.jpg', 'events/activity-3.jpg', 'A dignitary presenting a trophy to a student at a prize-giving', 'Prize distribution'),
    'act_col': ('BCA/images/Activ1.jpg', 'events/activity-colleges-1.jpg', 'Rows of students in white head-scarves seated in a hall, with a banner behind them', 'College programme'),
    'act_nur2': ('EngNurSchoolDEL/images/Activ2.jpg', 'events/activity-nursery-2.jpg', 'Young children performing a group song on a pink-curtained stage', 'Nursery programme'),
    'act_nur3': ('EngNurSchoolDEL/images/Activ3.jpg', 'events/activity-nursery-3.jpg', 'A child performing on stage in front of a gold-embroidered backdrop', 'Nursery programme'),

    # ---- Library and classrooms shared by several original pages (the old Jamia Masjid pictures were replaced in Phase 9.3 by the owner's new photographs in tools/masjid/) --------------------------------------------
    'lib1': ('homeimages/Lib1.jpg', 'library/library-1.jpg', 'Students in green-and-white uniform reading beside the library shelves', 'School library'),
    'lib2': ('homeimages/Lib2.jpg', 'library/library-2.jpg', 'Students in green-and-white uniform seated on the floor reading', 'School library'),
    'lib3': ('homeimages/Lib3.jpg', 'library/library-3.jpg', 'Students in green-and-white uniform seated around a large blue carpet reading', 'School library'),
    'gov_old': ('BCA/images/Team.jpg', 'people/governing-body-earlier.jpg', 'An earlier printed poster headed Governing Body: eight portrait photographs and a mosque picture, each with a printed name and designation', 'Governing Body: earlier poster'),
    'trustees_old': ('EngBoysHighSchool/images/Trustees.jpg', 'people/trustees-earlier.jpg', 'An earlier printed poster headed Trustees: nineteen portrait photographs in blue frames with a printed name under each', 'Trustees: earlier poster'),
    'cls1': ('homeimages/Classroom.jpg', 'colleges/classroom-pu-1.jpg', 'A classroom with wooden desks, a green board and a projector', 'Classroom'),
    'cls2': ('homeimages/Classroom1.jpg', 'colleges/classroom-pu-2.jpg', 'A classroom with benches, a whiteboard and a green board', 'Classroom'),
    'cls3': ('homeimages/Classroom2.jpg', 'colleges/classroom-pu-3.jpg', 'A classroom with a large green board and desks', 'Classroom'),

    # ---- Colleges (PU, Degree, BCA) -----------------------------------------------------------------------------------
    'col_comp': ('BCA/images/CompLab.jpg', 'colleges/computer-lab-1.jpg', 'Girl students working at computers in the computer laboratory', 'Computer laboratory'),
    'col_comp2': ('PUGirlsCollege/images/CompLab.jpg', 'colleges/computer-lab-2.jpg', 'Students seated in rows at computers in a laboratory', 'Computer laboratory'),
    'col_lib': ('BCA/images/Libr.jpg', 'colleges/library-1.jpg', 'Girl students reading and writing at tables in the college library', 'College library'),
    'col_lib2': ('PUGirlsCollege/images/Libr.jpg', 'colleges/library-2.jpg', 'Girl students seated at tables in a library with shelves of books', 'College library'),
    'bca_cls': ('BCA/images/Classroom.jpg', 'colleges/classroom-bca.jpg', 'A classroom with benches and a whiteboard', 'BCA classroom'),
    'deg_cls1': ('DegreeGirlsCollege/images/Classroom.jpg', 'colleges/classroom-degree-1.jpg', 'A classroom with long wooden benches and a projector', 'Degree College classroom'),
    'deg_cls2': ('DegreeGirlsCollege/images/Classroom1.jpg', 'colleges/classroom-degree-2.jpg', 'A classroom with a whiteboard and a projector on the ceiling', 'Degree College classroom'),
    'pu_lab1': ('PUGirlsCollege/images/Sciencelab.jpg', 'colleges/science-lab-1.jpg', 'II PU girl students with their lecturer in the chemistry laboratory; caption printed on the photograph', 'Chemistry Lab, II PU students with Mr. Ziaulla Khan (Lecturer)'),
    'pu_lab2': ('PUGirlsCollege/images/Sciencelab1.jpg', 'colleges/science-lab-2.jpg', 'Three photographs of PUC students in the chemistry, biology and physics laboratories, with captions', 'Chemistry Lab II PUC · Biology Lab II PUC · Physics Lab I PUC'),
    'pu_prin': ('PUGirlsCollege/images/PrincipalBig.jpg', 'colleges/principal-pu.jpg', 'The Principal of the Pre University College seated at her desk', 'Principal, Pre University College for Girls'),
    'pu_staff': ('PUGirlsCollege/images/Staff.jpeg', 'colleges/staff-pu.jpeg', 'PUC staff members with the Principal, seated and standing in two rows; names printed on the photograph', 'PUC staff members with Principal'),
    'pu_school': ('PUGirlsCollege/images/SchoolPhoto.jpg', 'colleges/group-pu.jpg', 'Group photographs from a college function: students wearing sashes beside staff on the left, a large group of women staff and students on the right', 'Pre University College'),
    'deg_prin': ('BCA/images/PrincipalBig.jpg', 'colleges/principal-degree-bca.jpg', 'The Principal of the Degree and BCA colleges seated at her desk with a telephone and papers', 'Principal, Degree and BCA colleges'),
    'deg_staff': ('BCA/images/Staff.jpeg', 'colleges/staff-degree-bca.jpeg', 'Women faculty members of the Degree and BCA colleges seated and standing in a classroom', 'Faculty of the Degree and BCA colleges'),
    'deg_staff_names': ('BCA/images/STNames.jpeg', 'colleges/staff-degree-bca-names.jpeg', 'The printed caption naming the faculty members in the photograph above', 'Names of the faculty in the photograph'),

    # ---- NCPUL --------------------------------------------------------------------------------------------------------
    'ncpul_aw': ('NCPUL/images/Awards.jpeg', 'ncpul/awards.jpeg', 'Two photographs of certificates being handed over to women students on stage', 'Certificate presentation'),
    'ncpul_cls': ('NCPUL/images/Classroom.jpg', 'ncpul/classroom.jpg', 'Girl students taking notes in the computer centre classroom', 'Classroom'),
    'ncpul_lab1': ('NCPUL/images/CompLab.jpg', 'ncpul/computer-lab-1.jpg', 'Girl students at computers in the NCPUL computer laboratory', 'Computer laboratory'),
    'ncpul_lab2': ('NCPUL/images/CompLab1.jpeg', 'ncpul/computer-lab-2.jpeg', 'Women students working at computers in the computer centre', 'Computer laboratory'),
    'ncpul_staff': ('NCPUL/images/Staff.jpeg', 'ncpul/staff.jpeg', 'Four women staff members of the computer centre standing beside a sign reading “staff members”', 'Staff members'),

    # ---- ITI ----------------------------------------------------------------------------------------------------------
    'iti_prin': ('ITI/ITIimages/principal.jpg', 'iti/principal.jpg', 'The Principal of the Industrial Training Institute seated at his desk writing', 'Principal, ITI'),
    'iti_campus': ('ITI/ITIimages/iti1.jpg', 'iti/campus.jpg', 'The Industrial Training Institute building: a two-storey building with arched windows beside a landscaped garden', 'ITI campus'),
    'iti_fit1': ('ITI/ITIimages/Fit1.jpg', 'iti/fitter-1.jpg', 'Trainees working on a bench in the Fitter workshop', 'Fitter workshop'),
    'iti_fit2': ('ITI/ITIimages/Fit2.jpg', 'iti/fitter-2.jpg', 'Trainees and an instructor gathered around a bench in the Fitter workshop', 'Fitter workshop'),
    'iti_fit3': ('ITI/ITIimages/Fit3.jpg', 'iti/fitter-3.jpg', 'Trainees filing metal at vices in the Fitter workshop', 'Fitter workshop'),
    'iti_fit4': ('ITI/ITIimages/Fit4.jpg', 'iti/fitter-4.jpg', 'Trainees and an instructor examining a vehicle lighting assembly', 'Fitter workshop'),
    'iti_mmv': ('ITI/ITIimages/iti5.jpg', 'iti/mmv-lab.jpg', 'Instructor and trainees working on a vehicle engine in the Mechanic Motor Vehicle workshop', 'MMV laboratory'),
    'iti_work': ('ITI/ITIimages/iti2.jpg', 'iti/workshop.jpg', 'Trainees and instructors gathered around machinery in the ITI workshop', 'ITI workshop'),
    'iti_play1': ('ITI/ITIimages/itiPlaygroud.jpg', 'iti/playground-1.jpg', 'The open playground of the ITI campus', 'ITI playground'),
    'iti_play2': ('ITI/ITIimages/itiPlaygroud1.jpg', 'iti/playground-2.jpg', 'An elderly gentleman in white greeting boys in navy blazers on a sports ground, with onlookers behind', 'Prize distribution'),
    'iti_play3': ('ITI/ITIimages/itiPlaygroud2.jpg', 'iti/playground-3.jpg', 'Men in white caps handing over trophies to a boy at an outdoor prize distribution', 'Prize distribution'),
    # ---- Phase 9.2: photographs published after review of the unreferenced originals ---------------------------------
    'iti_dsc1': ('ITI/ITIimages/DSC02796.JPG', 'iti/prize-distribution-full-1.jpg', 'Boys in navy blazers and white trousers standing in a line on open ground while an elderly man in white shakes hands with one of them; palm trees behind', 'Prize distribution: full photograph'),
    'iti_dsc2': ('ITI/ITIimages/DSC03089.JPG', 'iti/prize-distribution-full-2.jpg', 'A boy in a white shirt and red wristband holds a gold trophy beside a table of trophies while a crowd of children and men watches', 'Prize distribution: full photograph'),
    'iti_dsc3': ('ITI/ITIimages/DSC03090.JPG', 'iti/prize-distribution-full-3.jpg', 'An elderly man in white presents an award to a boy in a white shirt beside a table of trophies, with a crowd of onlookers', 'Prize distribution: full photograph'),
    'bca_cls2': ('BCA/images/Classroom1.jpg', 'colleges/classroom-bca-2.jpg', 'A classroom with wooden benches, a blackboard and green curtains', 'A second BCA classroom photograph'),
    'boys_cls2': ('EngBoysHighSchool/images/Classroom1.jpg', 'schools/classroom-boys-2.jpg', 'A classroom with a ceiling projector, a whiteboard, a green blackboard and wooden benches', 'A second classroom photograph, Boys High School'),
    'iti_cls': ('ITI/ITIimages/Classroom.jpg', 'iti/classroom.jpg', 'A classroom with a whiteboard, two blackboards, a ceiling fan and wooden benches', 'ITI classroom'),

    # ---- English schools ----------------------------------------------------------------------------------------------
    'hm': ('homeimages/HeadMiss.jpg', 'schools/head-mistress.jpg', 'The Head Mistress seated at her desk in front of a bank of security monitors', 'Head Mistress'),
    'nur_group': ('EngNurSchoolDEL/images/SchoolPhoto.jpg', 'schools/nursery-group.jpg', 'Nursery children in white uniforms and head-scarves posing in rows with their teachers', 'English Nursery School'),
    'hp_group': ('homeimages/HPrimPhoto.jpeg', 'schools/higher-primary-group.jpeg', 'Group photograph of Higher Primary pupils in green blazers with teachers and trustees, beside a speaker at a lectern', 'English Higher Primary School'),
    'boys_group': ('EngBoysHighSchool/images/SchoolPhoto.jpg', 'schools/boys-high-group.jpg', 'Boys of the High School in green blazers seated in rows with staff and trustees, beside a speaker at a lectern', 'English Boys High School'),
    'girls_group': ('EngGirlsHighSchool/images/SchoolPhoto.jpg', 'schools/girls-high-group.jpg', 'High School girls in white head-scarves seated in rows with teachers, beside girls reading on a blue carpet', 'English Girls High School'),
    'school_staff': ('EngBoysHighSchool/images/Staff.jpg', 'schools/staff-high-1.jpg', 'Staff members of the English High Schools seated and standing in a hall', 'Staff of the English High Schools'),
    'school_staff2': ('EngGirlsHighSchool/images/Staff1.jpg', 'schools/staff-high-2.jpg', 'Women staff members of the English Girls High School seated on a red carpet with a gentleman', 'Staff of the English Girls High School'),
    'boys_cls': ('EngBoysHighSchool/images/Classroom.jpg', 'schools/classroom-boys.jpg', 'A classroom with benches, a whiteboard and loudspeakers', 'English Boys High School classroom'),
    'girls_cls': ('EngGirlsHighSchool/images/Classroom.jpg', 'schools/classroom-girls.jpg', 'Interior of a classroom with benches and a green board', 'English Girls High School classroom'),
    'girls_comp': ('EngGirlsHighSchool/images/CompLab.jpg', 'colleges/computer-lab-2.jpg', 'Girls seated in rows at computers', 'English Girls High School computer laboratory'),

    # ---- Awards ----------------------------------------------------------------------------------------------------
    'award_trophy': ('homeimages/6.jpg', 'recognitions/udyog-rattan-award-trophy.jpg', 'A glass trophy on a black base held in two hands, engraved “Udyog Rattan Award”', 'Udyog Rattan Award trophy'),

    # ---- Institution logo banners (originally Institutions/*Logo.jpg, 316x81) ---------------------------------------
    'logo_iti': ('Institutions/ITILogo.jpg', 'logos/iti.jpg', 'Jame ul uloom crest with the words Industrial Training Institute (ITI)', 'Industrial Training Institute (ITI)'),
    'logo_pu': ('Institutions/PUGirlsLogo.jpg', 'logos/pu-girls-college.jpg', 'Jame ul uloom crest with the words Pre University College for Girls', 'Pre University College for Girls'),
    'logo_bcom': ('Institutions/BCOMLogo.jpg', 'logos/degree-college.jpg', 'Jame ul uloom crest with the words Bachelor of Commerce (B.Com)', 'Degree College for Girls (B.Com)'),
    'logo_bca': ('Institutions/BCALogo.jpg', 'logos/bca.jpg', 'Jame ul uloom crest with the words Bachelor of Computer Application', 'Bachelor of Computer Application (BCA)'),
    'logo_eghs': ('Institutions/EngGirlsHScLogo.jpg', 'logos/english-girls-high-school.jpg', 'Jame ul uloom crest with the words English Girls High School', 'English Girls High School'),
    'logo_ebhs': ('Institutions/EngBoysHScLogo.jpg', 'logos/english-boys-high-school.jpg', 'Jame ul uloom crest with the words English Boys High School', 'English Boys High School'),
    'logo_ehps': ('Institutions/EngHPScLogo.jpg', 'logos/english-higher-primary-school.jpg', 'Jame ul uloom crest with the words English Higher Primary School', 'English Higher Primary School'),
    'logo_ens': ('Institutions/EngNurScLogo.jpg', 'logos/english-nursery-school.jpg', 'Jame ul uloom crest with the words English Nursery School', 'English Nursery School'),
    'logo_ncpul': ('Institutions/NCPULLOGO.jpg', 'logos/ncpul-computers.jpg', 'Jame ul uloom crest with the words NCPUL Computers', 'MMI-NCPUL Computer Centre'),
    'logo_tail': ('Institutions/Tailoring.jpg', 'logos/tailoring.jpg', 'Jame ul uloom crest with the word Tailoring', 'Tailoring School for Women'),
    'logo_cal': ('Institutions/Caligraphy.jpg', 'logos/calligraphy.jpg', 'Jame ul uloom crest with the word Calligraphy', 'Calligraphy Centre'),
    'logo_hifz': ('Institutions/Shoba-e-hifz.jpg', 'logos/shoba-e-hifz.jpg', 'Jame ul uloom crest with the words Shoba-e-Hifz', 'Shoba-e-Hifz'),
    'logo_alim': ('Institutions/Shoba-e-Alimiyath.jpg', 'logos/shoba-e-alimiyath.jpg', 'Jame ul uloom crest with the words Shoba-e-Alimiyath', 'Shoba-e-Alimiyath'),
}

# Original PDFs, copied unchanged: key -> (source, destination below DOC, title, description)
DOCUMENTS = {
    'diary': ('homeimages/Diary Edited-1.pdf', 'admissions-diary-2013-14.pdf', 'Admissions Diary 2013–14', '11-page school diary with rules, admission conditions and calendars (PageMaker, November 2013)'),
    'tareeq': ('masjidimages/Masjid Tareeq.pdf', 'masjid-tareeq.pdf', 'Masjid Tareeq (Urdu)', '23-page Urdu document printed as “Jamia Masjid in the mirror of history”'),
    'majalla': ('masjidimages/majalah qurbani  fainal 1.pdf', 'majalla-qurbani.pdf', 'Majalla Qurbani (Urdu magazine)', '51-page Urdu magazine issue of the Jamia Masjid'),
}


# Existing Phase 8 photographs that are byte-identical to original files: used again instead of storing a second copy.
P8 = 'ResidentialSchoolBanikuppa/assets/images/'
EXISTING = {
    # key: (path inside public/, alt text, caption)
    'gov': (P8 + 'governing.jpeg', 'The Governing Body of the Trust: printed portrait photographs with names and designations', 'Governing Body'),
    'trustees': (P8 + 'trustees.jpg', 'The Trustees: printed portrait photographs with names', 'Trustees'),
    'audi1': (P8 + 'audi1.jpg', 'Boys in green waistcoats and white caps standing in rows in the auditorium, with a large audience behind them', 'Auditorium'),
    'audi2': (P8 + 'audi2.jpg', 'A packed auditorium: women and girls in the balcony and a large audience of students in the stalls', 'Auditorium'),
}
