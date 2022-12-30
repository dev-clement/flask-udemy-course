"""
blocklist.py

This file just contains all the JWT token for any user. It will be imported
by the app itself and the logout also, so that token can be added to the
blocklist when the user logs out
"""
BLOCKLIST = set()