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


I used Claude built-in agent (access is provided by Codepath). Claude debugging results indicates that the function check_guess() is incorrectly implemented due to hint bug, if guess number is greater than the secret number, it is expected for the hint to say "go lower", but the logic gives the oppsite. 

if g > secret:
    return "Too High", "ð Go HIGHER!"  # BUG: same backwards hint
return "Too Low", "ð Go LOWER!"
Same inverted hint bug in the string comparison path.




---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
