# Claude Code Instructions

## My Context
- I am a graduate student writing a thesis on financial 
  markets and machine learning
- My vault is at C:\Users\johnn\Brain
- My primary focus is my thesis but I also track lectures,
  meetings, and personal tasks

## Daily Morning Routine
When I say "good morning" or "morning briefing" or 
"start my day", do ALL of the following automatically:

1. DAILY NOTE
- Check if today's daily note exists in Tracking/Daily/[todays date].md
- If it doesn't exist, create it using the Daily Template
- If it does exist, update it

2. PULL IN TASKS
- Read all incomplete tasks from Tracking/Daily/TaskForge
- Add any tasks due today to the Day Plan section of 
  today's daily note
- Check for any tasks that were incomplete from 
  yesterday's daily note and carry them forward

3. SYNC GRANOLA
- Pull all new meetings and calls from Granola since 
  yesterday
- Create notes for any new meetings in Meetings/Calls
- If any meetings relate to thesis work add links to 
  Sources/Thesis/Notes
- Add today's scheduled meetings to the Day Plan with 
  their correct times

4. INBOX SWEEP
- Check everything in Inbox
- Sort each item into the correct vault folder
- If anything is unprocessed audio or text, summarize 
  it and file it properly

5. THESIS PULSE
- Check the most recent thesis notes and drafts
- Give me a one paragraph reminder of where I left off
- Suggest the single most important thesis task for today

6. MORNING SUMMARY
- Generate a clean morning briefing note and save it 
  to Tracking/Daily/[todays date].md under a new 
  section called "Morning Briefing"
- The briefing should include:
  * Today's date and day of week
  * Top 3 tasks due today from TaskForge
  * Any meetings scheduled today from Granola
  * One thesis focus suggestion
  * One interesting connection between recent notes
  * Any items that were processed from Inbox

Always end by saying "Good morning John, your vault 
is ready. Here is your day:" and then print the 
morning briefing cleanly

## Weekly Review Instructions
When I say "run weekly review", do the following:

1. Find all daily notes from the past 7 days in 
   Tracking/Daily

2. Read every daily note and extract:
   - Tasks completed vs missed
   - Thesis progress sections
   - Notes and ideas captured
   - Any meetings from Meetings/Calls that week

3. Read everything new added to the vault this week:
   - New files in Sources (any subfolder)
   - New files in Knowledge/Concepts
   - New notes in Notes/Fleeting

4. Generate a comprehensive weekly review note and 
   save it to Tracking/Progress/[YEAR]-W[WEEK NUMBER].md
   using the Weekly Review Template structure

5. Update Tracking/Learning Log.md with:
   - New concepts encountered this week
   - How they connect to existing knowledge
   - Suggested follow-up reading or actions

6. Look across ALL new material this week and find 
   non-obvious connections between:
   - Lecture content and thesis topics
   - Meeting discussions and thesis progress
   - Random notes and existing concepts
   - Add these connections as [[links]] in relevant notes

7. End with a prioritized suggestion list for next week
   based on thesis progress and incomplete tasks
