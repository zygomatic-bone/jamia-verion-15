/* Rules of the website forms: field names, types, limits and choice lists. The Feedback, Admissions and Careers pages use the same names. */
export default {
  "max_body_bytes": 24000,
  "choices": {
    "category": [
      [
        "appreciation",
        "Appreciation"
      ],
      [
        "suggestion",
        "Suggestion"
      ],
      [
        "facilities",
        "Facilities"
      ],
      [
        "academics",
        "Academics"
      ],
      [
        "admissions",
        "Admissions"
      ],
      [
        "other",
        "Other"
      ]
    ],
    "audience": [
      [
        "student",
        "Student"
      ],
      [
        "parent",
        "Parent or guardian"
      ],
      [
        "alumni",
        "Alumnus or alumna"
      ],
      [
        "visitor",
        "Visitor"
      ],
      [
        "community",
        "Community member"
      ],
      [
        "other",
        "Other"
      ]
    ],
    "about": [
      [
        "general",
        "The whole institution"
      ],
      [
        "masjid",
        "Jamia Masjid"
      ],
      [
        "schools",
        "English schools (nursery to high school)"
      ],
      [
        "pu",
        "Pre University College for Girls"
      ],
      [
        "degree",
        "Degree colleges"
      ],
      [
        "ncpul",
        "MMI-NCPUL Computer Centre"
      ],
      [
        "iti",
        "ITI"
      ],
      [
        "hifz",
        "Shoba-e-Hifz and Shoba-e-Alimiyath"
      ],
      [
        "banikuppa",
        "Residential School, Banikuppa"
      ],
      [
        "website",
        "This website"
      ]
    ],
    "programme": [
      [
        "schools",
        "Nursery, primary or high school"
      ],
      [
        "pu",
        "Pre University College for Girls"
      ],
      [
        "degree",
        "Degree college (B.Com / BCA)"
      ],
      [
        "ncpul",
        "MMI-NCPUL Computer Centre"
      ],
      [
        "iti",
        "ITI (Fitter, MRAC, MMV)"
      ],
      [
        "hifz",
        "Shoba-e-Hifz / Shoba-e-Alimiyath"
      ],
      [
        "banikuppa",
        "Residential School, Banikuppa"
      ],
      [
        "unsure",
        "Not sure yet"
      ]
    ],
    "area": [
      [
        "teaching-school",
        "Teaching: schools"
      ],
      [
        "teaching-college",
        "Teaching: colleges"
      ],
      [
        "islamic",
        "Islamic studies and Hifz"
      ],
      [
        "technical",
        "Technical training (ITI)"
      ],
      [
        "computer",
        "Computer education"
      ],
      [
        "admin",
        "Administration and office"
      ],
      [
        "residential",
        "Residential campus, Banikuppa"
      ],
      [
        "other",
        "Another way to contribute"
      ]
    ],
    "experience": [
      [
        "fresher",
        "Starting out"
      ],
      [
        "one-three",
        "1 to 3 years"
      ],
      [
        "three-five",
        "3 to 5 years"
      ],
      [
        "five-plus",
        "More than 5 years"
      ]
    ]
  },
  "forms": {
    "feedback": {
      "label": "Feedback",
      "min": {
        "message": 5
      },
      "fields": [
        {
          "name": "rating",
          "type": "int",
          "required": true,
          "limit": 5,
          "label": "Rating"
        },
        {
          "name": "category",
          "type": "choice",
          "required": true,
          "limit": "category",
          "label": "Topic"
        },
        {
          "name": "message",
          "type": "text",
          "required": true,
          "limit": 2000,
          "label": "Message"
        },
        {
          "name": "about",
          "type": "choice",
          "required": false,
          "limit": "about",
          "label": "About"
        },
        {
          "name": "audience",
          "type": "choice",
          "required": false,
          "limit": "audience",
          "label": "Sender is"
        },
        {
          "name": "name",
          "type": "line",
          "required": false,
          "limit": 80,
          "label": "Name"
        },
        {
          "name": "email",
          "type": "email",
          "required": false,
          "limit": 120,
          "label": "Email"
        }
      ]
    },
    "admissions": {
      "label": "Admissions enquiry",
      "min": {},
      "fields": [
        {
          "name": "guardian",
          "type": "line",
          "required": true,
          "limit": 80,
          "label": "Parent or guardian"
        },
        {
          "name": "phone",
          "type": "phone",
          "required": true,
          "limit": 20,
          "label": "Phone"
        },
        {
          "name": "email",
          "type": "email",
          "required": false,
          "limit": 120,
          "label": "Email"
        },
        {
          "name": "programme",
          "type": "choice",
          "required": true,
          "limit": "programme",
          "label": "Programme"
        },
        {
          "name": "level",
          "type": "line",
          "required": false,
          "limit": 60,
          "label": "Class or year sought"
        },
        {
          "name": "student",
          "type": "line",
          "required": false,
          "limit": 80,
          "label": "Student name"
        },
        {
          "name": "message",
          "type": "text",
          "required": false,
          "limit": 1000,
          "label": "Message"
        },
        {
          "name": "consent",
          "type": "bool",
          "required": true,
          "limit": 0,
          "label": "Agrees to be contacted"
        }
      ]
    },
    "careers": {
      "label": "Careers: expression of interest",
      "min": {},
      "fields": [
        {
          "name": "name",
          "type": "line",
          "required": true,
          "limit": 80,
          "label": "Name"
        },
        {
          "name": "phone",
          "type": "phone",
          "required": true,
          "limit": 20,
          "label": "Phone"
        },
        {
          "name": "email",
          "type": "email",
          "required": true,
          "limit": 120,
          "label": "Email"
        },
        {
          "name": "area",
          "type": "choice",
          "required": true,
          "limit": "area",
          "label": "Area of interest"
        },
        {
          "name": "qualification",
          "type": "line",
          "required": false,
          "limit": 120,
          "label": "Qualification"
        },
        {
          "name": "experience",
          "type": "choice",
          "required": false,
          "limit": "experience",
          "label": "Experience"
        },
        {
          "name": "message",
          "type": "text",
          "required": false,
          "limit": 1500,
          "label": "Message"
        },
        {
          "name": "consent",
          "type": "bool",
          "required": true,
          "limit": 0,
          "label": "Agrees to be contacted"
        }
      ]
    }
  }
};
