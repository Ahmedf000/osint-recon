# 106 Google dorks for domain and person reconnaissance
DORKS = {
    'files': {
        'documents': {
            1: ("PDF Files", "site:{target} filetype:pdf", "domain"),
            2: ("Word Documents", "site:{target} filetype:docx", "domain"),
            3: ("Spreadsheets", "site:{target} filetype:xlsx", "domain"),
            4: ("Presentations", "site:{target} filetype:pptx", "domain"),
        },
        'configs': {
            5: ("ENV Files", "site:{target} filetype:env", "domain"),
            6: ("Backup Files", "site:{target} filetype:bak", "domain"),
            7: ("Config Files", "site:{target} filetype:conf", "domain"),
            8: ("Log Files", "site:{target} filetype:log", "domain"),
        },
        'database': {
            9: ("SQL Dumps", "site:{target} filetype:sql", "domain"),
            10: ("Database Backups", "site:{target} filetype:db", "domain"),
        }
    },

    'webapp': {
        'admin': {
            11: ("Login Pages", "site:{target} inurl:login", "domain"),
            12: ("Admin Panels", "site:{target} inurl:admin", "domain"),
            13: ("Dashboard Pages", "site:{target} intitle:dashboard", "domain"),
            14: ("Password Reset", "site:{target} inurl:reset", "domain"),
        },
        'api': {
            15: ("API Endpoints", "site:{target} inurl:api", "domain"),
            16: ("Swagger Docs", "site:{target} intitle:swagger", "domain"),
            17: ("GraphQL", "site:{target} inurl:graphql", "domain"),
        },
        'cms': {
            18: ("WordPress", "site:{target} inurl:wp-content", "domain"),
            19: ("CMS Detection", 'site:{target} "powered by"', "domain"),
        },
        'errors': {
            20: ("Directory Listings", 'site:{target} intitle:"index of"', "domain"),
            21: ("500 Errors", 'site:{target} intitle:"500 Internal Server Error"', "domain"),
            22: ("403 Forbidden", 'site:{target} intitle:"403 Forbidden"', "domain"),
        }
    },

    'infrastructure': {
        'subdomains': {
            23: ("All Subdomains", "site:*.{target}", "domain"),
            24: ("Staging", "site:staging.{target}", "domain"),
            25: ("Development", "site:dev.{target}", "domain"),
            26: ("Testing", "site:test.{target}", "domain"),
            27: ("UAT", "site:uat.{target}", "domain"),
        },
        'cloud': {
            28: ("S3 Buckets", 'site:s3.amazonaws.com "{target}"', "domain"),
            29: ("Azure Blobs", 'site:blob.core.windows.net "{target}"', "domain"),
        }
    },

    'secrets': {
        'github': {
            30: ("GitHub Secrets", 'site:github.com "{target}" (password OR secret OR api_key)', "domain"),
            31: ("GitHub ENV", 'site:github.com "{target}" filename:.env', "domain"),
        },
        'credentials': {
            32: ("Password Files", "site:{target} (password OR passwd OR pwd) (filetype:xls OR filetype:xlsx OR filetype:csv)", "domain"),
        }
    },

    'intel': {
        'tech': {
            33: ("Job Postings", "site:{target} inurl:careers", "domain"),
            34: ("Tech Stack", 'site:{target} "we use" OR "built with"', "domain"),
        },
        'security': {
            35: ("Bug Bounty", 'site:{target} "bug bounty" OR "responsible disclosure"', "domain"),
            36: ("Security Page", "site:{target} inurl:security", "domain"),
        }
    },

    # ============================================================
    # PERSON-BASED DORKS (For individual reconnaissance)
    # ============================================================

    'person_documents': {
        'professional': {
            51: ("Resume/CV", '"{target}" filetype:pdf (resume OR cv OR curriculum)', "person"),
            52: ("Cover Letters", '"{target}" filetype:pdf "cover letter"', "person"),
            53: ("Portfolio", '"{target}" filetype:pdf portfolio', "person"),
            54: ("Certifications", '"{target}" filetype:pdf (certificate OR certification)', "person"),
            55: ("Transcripts", '"{target}" filetype:pdf transcript', "person"),
        },
        'academic': {
            56: ("Research Papers", '"{target}" filetype:pdf (author OR published)', "person"),
            57: ("Thesis/Dissertation", '"{target}" filetype:pdf (thesis OR dissertation)', "person"),
            58: ("Conference Papers", '"{target}" filetype:pdf (conference OR proceedings)', "person"),
            59: ("Publications List", '"{target}" (publications OR bibliography)', "person"),
        },
        'personal': {
            60: ("Personal Documents", '"{target}" filetype:pdf (personal OR private)', "person"),
            61: ("Tax Documents", '"{target}" filetype:pdf (tax OR w2 OR 1099)', "person"),
            62: ("Financial Docs", '"{target}" filetype:pdf (bank OR financial OR statement)', "person"),
        }
    },

    'person_social': {
        'profiles': {
            63: ("LinkedIn Profile", '"{target}" site:linkedin.com', "person"),
            64: ("Twitter/X", '"{target}" site:twitter.com OR site:x.com', "person"),
            65: ("Facebook", '"{target}" site:facebook.com', "person"),
            66: ("Instagram", '"{target}" site:instagram.com', "person"),
            67: ("GitHub Profile", '"{target}" site:github.com', "person"),
            68: ("Stack Overflow", '"{target}" site:stackoverflow.com', "person"),
            69: ("Reddit", '"{target}" site:reddit.com', "person"),
            70: ("Medium/Blogs", '"{target}" site:medium.com', "person"),
        },
        'professional_networks': {
            71: ("AngelList", '"{target}" site:angel.co', "person"),
            72: ("Crunchbase", '"{target}" site:crunchbase.com', "person"),
            73: ("Indeed", '"{target}" site:indeed.com', "person"),
            74: ("Glassdoor", '"{target}" site:glassdoor.com', "person"),
        }
    },

    'person_contact': {
        'email': {
            75: ("Email Discovery", '"{target}" "@" -site:linkedin.com', "person"),
            76: ("Gmail", '"{target}" "@gmail.com"', "person"),
            77: ("Work Email Pattern", '"{target}" "@*.com"', "person"),
            78: ("Email in Documents", '"{target}" filetype:pdf email', "person"),
        },
        'phone': {
            79: ("Phone Numbers", '"{target}" (phone OR mobile OR cell)', "person"),
            80: ("Contact Info", '"{target}" (contact OR "contact information")', "person"),
        },
        'location': {
            81: ("Address", '"{target}" (address OR location OR "lives in")', "person"),
            82: ("Maps/Geolocation", '"{target}" site:maps.google.com', "person"),
        }
    },

    'person_media': {
        'images': {
            83: ("Profile Photos", '"{target}" filetype:jpg OR filetype:png', "person"),
            84: ("Image Search", '"{target}" site:images.google.com', "person"),
        },
        'videos': {
            85: ("YouTube", '"{target}" site:youtube.com', "person"),
            86: ("Vimeo", '"{target}" site:vimeo.com', "person"),
            87: ("TikTok", '"{target}" site:tiktok.com', "person"),
        },
        'presentations': {
            88: ("SlideShare", '"{target}" site:slideshare.net', "person"),
            89: ("Speaker Deck", '"{target}" site:speakerdeck.com', "person"),
        }
    },

    'person_professional': {
        'work_history': {
            90: ("Company History", '"{target}" (worked OR "previously at" OR "formerly")', "person"),
            91: ("Current Employer", '"{target}" (works OR "currently at" OR employee)', "person"),
            92: ("Job Titles", '"{target}" (CEO OR CTO OR developer OR engineer OR manager)', "person"),
        },
        'skills': {
            93: ("Technical Skills", '"{target}" (Python OR Java OR JavaScript OR skills)', "person"),
            94: ("Certifications", '"{target}" (certified OR certification)', "person"),
        },
        'mentions': {
            95: ("News Mentions", '"{target}" site:news.google.com', "person"),
            96: ("Press Releases", '"{target}" "press release"', "person"),
            97: ("Interviews", '"{target}" (interview OR "spoke with")', "person"),
        }
    },

    'person_background': {
        'education': {
            98: ("Universities", '"{target}" (university OR college OR graduated)', "person"),
            99: ("Alumni", '"{target}" alumni', "person"),
            100: ("Student Records", '"{target}" student', "person"),
        },
        'affiliations': {
            101: ("Organization Membership", '"{target}" (member OR "member of")', "person"),
            102: ("Board Member", '"{target}" (board OR "board member" OR director)', "person"),
            103: ("Volunteer Work", '"{target}" volunteer', "person"),
        },
        'legal': {
            104: ("Court Records", '"{target}" (court OR lawsuit OR plaintiff OR defendant)', "person"),
            105: ("Arrest Records", '"{target}" (arrest OR arrested OR "criminal record")', "person"),
            106: ("Property Records", '"{target}" (property OR deed OR owner)', "person"),
        }
    }
}