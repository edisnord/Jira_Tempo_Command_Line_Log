# Tempo command line time logging tool

This app's intent is to make logging time on Tempo's annoying UI easier using their API. 
The program works by inserting your API Key(can be created from the settings inside Tempo) into a 
text file called data.txt in the same directory with the script in the format:

API Key:$API_KEY <br />
Issue:$ISSUE_CODE <br />
Date:$DATE (Optionally another date to create a range) <br />
Hours:$HOURS <br />
Billable Hours:$BILLABLE_HOURS <br />


In that specific order(do not write comments in between lines or change the order, the text before the : character can be changed though).
You can also write comments and have spaces above the config, but don't put spaces/comments between the data lines.
The script also asks for your display name and a day when you have logged somethign in Tempo, because the 
API does not have a feature which tells you what user created the API key, so I had to take the uglier path to fixing the issue.
