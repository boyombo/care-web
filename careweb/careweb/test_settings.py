DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'futurecaredb',
        'USER': 'futurecaredbowner',
        'PASSWORD': 'DB@Adm!nPassword',
        'HOST': 'localhost',
        'PORT': '5432',
    },
}

PAYSTACK_PUBLIC_KEY = "pk_test_f80812fc104b4a11284eb634a9fff51afefd029b"
PAYSTACK_SECRET_KEY = "sk_test_cd1751e746ab5a6c70f7ed6ca058a6503b446457"
PAYSTACK_PUBLIC_KEY_LIVE = "pk_live_19f7e9669943ffab64e14ed3135eacd2612a69b9"
PAYSTACK_SECRET_KEY_LIVE = "sk_live_e171530399dd1be42161c3c35f4c389946eea33d"
HASHID_FIELD_SALT = '5!ge-z*s#mh-+9_rky&8#n1$thf@0q(sdhv^6yoc=0f3i26hj!'

POSTMARK = {
    'TOKEN': '9ac9cc38-eb6f-47b5-ab5b-8d68ab5b1ead',
    'TEST_MODE': False,
    'VERBOSITY': 0,
}
