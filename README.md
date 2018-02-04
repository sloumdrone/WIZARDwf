# Overview
WIZARDwf is a utility for Workfront (a project management/project tracking system). It will automate extending project deadlines. While this may seem like cheating, it became useful and was a requested utility for the company for which it was developed.

## Dependencies
 - Python 2.7.x
 - CHRON or some other automated scheduling system
 - PM Tools (non-foss)
     - This is a tools package developed for the same company as WIZARDwf. The items used by WIZARDwf can be bypassed with a little bit of code alteration: provide your own SMTP mailing code and you can avoid the need for teh mail portion. Either hard code (not recommended) or use some form of hashing or cypher library for the password and username masking. Done deal, non-foss removed.
 
