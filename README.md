# Cobbler
GoogleSheets/CSV -> IPS Patch Bridge for Rom Hacking

Cobbler is a IPS patch generator that given a CSV or GoogleSheets XLSX will generate an IPS patch file.

Currently it only works with DMG-NDJ but it could easily be expanded to more.

# USAGE
./cobbler [--csv|--xlsx]

# Sheets/CSV header format
[Start,	End, Source, Translation, Edited, Word Count, Diff, Allowed Length, Done]

note: if your using XLSX, you'll need a 'Project Progress' sheet that lists your sheets in 'A' and 'Y/N' in 'E' 
if Cobller should include them
