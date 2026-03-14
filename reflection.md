# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.



## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

My answer: From the first glance after starting running the app using streamlit service on local host, I noticed the guessing game is not working properly. For instance, when I enter 99 it tells me to go higher when I enter 100 which is the maximum guessing number, the hint messages still says "go higher!" while the secret number is 20, so this is incorrect.

In more details of the bugs present in app.py code, there are several I have observed:
1) In the get_range_for_difficulty function, line 8, if difficulty == "Hard":
    return 1, 50  # BUG: Hard should be harder (larger range), not 1–50
"Hard" returns 1–50, which is easier than Normal's 1–100. Should likely be 1–200 or similar.

2) The New Game button is not responding and the game is not reset/refreshed, I have to manually refresh the webpage to reset the game.


3) Check_guess Hints are backwards: I expected to see the correct hints
if guess > secret:
    return "Too High", "ð Go HIGHER!"   # BUG: should say "Go LOWER!"
else:
    return "Too Low", "ð Go LOWER!"     # BUG: should say "Go HIGHER!"
When the guess is too high, the message tells the player to go higher, which is the opposite of correct.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).


- I used Claude built-in agent (access is provided by Codepath). Claude debugging results indicates that the function check_guess() is incorrectly implemented due to hint bug, if guess number is greater than the secret number, it is expected for the hint to say "go lower", but the logic gives the oppsite. 

if g > secret:
    return "Too High", "ð Go HIGHER!"  # BUG: same backwards hint
return "Too Low", "ð Go LOWER!"
Same inverted hint bug in the string comparison path.

 - Claude suggests that I implemented below fix: swapped with 50 for the range for normal and 100 for the hard level, this is correct implementation.

 def get_range_for_difficulty(difficulty: str):
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal": 
        return 1, 50 # FIXME: Logic breaks here, swapped 100 with 50
    if difficulty == "Hard":
        return 1, 100 # FIXME: Logic breaks here, swapped 50 with 100
    return 1, 100 

- Claude suggested below incorrect implementation after I updated with above code logic:
if difficulty == "Normal":
    return 1, 100
if difficulty == "Hard":
    return 1, 50
which is the reverting back to original incorrect code, this is AI hallucination.



---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?


- I asked claude to list all the bugs for each code file and provide solutions summary:

For example for app.py, below are the fixes:

Fix	Line	Change
1	7-10	Swapped Normal/Hard ranges back to 100/50
2	38-40	Inverted hints: Too High → LOWER, Too Low → HIGHER
3	45-47	Same hint fix in string fallback path
4	52	Removed + 1 from win score formula
5	135	New game resets attempts to 1 not 0
6	136	New game uses randint(low, high) not randint(1, 100)
7	110	Info bar shows {low} and {high} instead of hardcoded 100

I went through the fix one by one and verify the results accordingly with the result.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

- Streamlit Reruns
Imagine Streamlit like a whiteboard that gets erased and redrawn from top to bottom every single time something happens — a button click, a text input change, a checkbox toggle — anything.

This is called a rerun. Every interaction causes the entire Python script to re-execute from line 1.

- Session State
Because the whole script reruns on every click, regular Python variables reset to their default values every time. That's a problem — if you store the secret number in a normal variable, it picks a new random number on every rerun!

st.session_state is Streamlit's solution — a persistent backpack that survives reruns:


# Normal variable — RESETS every rerun (bug!)
secret = random.randint(1, 100)  # new number every click 

# Session state — SURVIVES reruns (correct)
if "secret" not in st.session_state:
    st.session_state.secret = random.randint(1, 100)  # set only once 
Think of it like the difference between:

Writing something on a paper (normal variable) — erased when the whiteboard resets
Putting something in your backpack (session_state) — stays with you across reruns


# This runs top to bottom... every single time you click a button
st.title("My App")
difficulty = st.sidebar.selectbox(...)  # re-executes
raw_guess = st.text_input(...)          # re-executes
if submit:                              # re-executes
    ...
This feels strange at first since most programs only run once. In Streamlit, our script is more like a live recipe that gets cooked fresh on every interaction.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.


- My answer: One habit or strategy from this project I'd like to reuse is to document all the bugs and flag each comment with #FIXME and a message next to it, also make a summary list of the bugs for record keeping before asking agent to suggest the bug fix solutions, then generate a list of suggested fix and save as a list before reviewing each bug and suggested bug fix one by one and verify accuracy and results. 

- One thing I would do differently: Verify AI-generated code by reading it line by line before running it, rather than trusting it works just because it runs without errors.

This project was a perfect example of why that matters. The AI-generated game:

Ran without crashing — no syntax errors, no exceptions on startup
Looked correct at a glance — the logic structure made sense
Still had 7+ bugs — all of them silent, behavioral bugs that only appeared during actual gameplay
The hardest bugs to catch were the ones that seemed intentional:


# Looks like a reasonable scoring formula...
points = 100 - 10 * (attempt_number + 1)  # but the +1 was wrong

# Looks like it's handling a type safety edge case...
if attempts % 2 == 0:
    secret = str(st.session_state.secret)  # but it was making the game unwinnable
What to do differently next time:

Before running AI-generated code, trace through it manually with a concrete example — pick a specific input (e.g., "guess = 60, secret = 50") and follow each line step by step to verify the output matches expectations.

This catches inverted logic, off-by-one errors, and type bugs that automated tools and even a quick glance will miss. Think of it as code review before execution, not just debugging after something breaks.

- This project taught me that AI-generated code can be confidently wrong — it looks polished, runs without errors, and follows correct structure, but can contain subtle logic bugs that only surface when you actually play the game. I now treat AI code the way I'd treat code from a new teammate: read it carefully, trace through it with real examples, and always verify behavior with tests before trusting it.

