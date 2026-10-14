# Build

    pip install opencc-python-reimplemented     # only for the zh-HK derivation
    python3 docs/build/build.py                 # writes all pages from content.py
    python3 docs/build/verify.py                # weekly check, exits 1 on any failure

Twin proxy values are injected at build time (public values only):

    TWIN_ENDPOINT=https://<worker>/ TURNSTILE_SITEKEY=<public key> python3 docs/build/build.py

Change `BASE` in content.py if the domain changes. Add a locale by adding an entry to LOCALES and a full S["xx"] block.
