# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
  When I ran the game the first time, it looked fine. The UI loaded fine. I was able to enter the number and submit and got hints.

- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").
  The obvious bugs for me were that the hints were backwards and that the game wasn't reseting when i clicked New Game button.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
  Claude Code
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
It correctly identified that the hint messages in check_guess were swapped — when the guess was too high, the message said "Go HIGHER!", and when too low, it said "Go LOWER!". I verified this by reading the logic directly: if guess > secret means the guess is already too high, so the correct instruction is to go lower. The messages were simply attached to the wrong branches. Once I swapped them, the hints pointed in the right direction.
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
When I reported that attempts weren't registering in history, the AI first focused on the wrong cause — it pointed to attempts += 1 happening before the validity check and said invalid inputs were "burning" attempts and polluting history. That was a real issue, but it didn't explain why valid guesses also weren't registering. I had to report the problem again before the AI found the actual root cause: the new_game button wasn't resetting st.session_state.status, so after a game ended, st.stop() was silently blocking every subsequent submit. The first diagnosis was technically true but incomplete and pointed me in the wrong direction.
---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
For logic bugs, I used pytest to verify the fix with concrete inputs and expected outputs. For UI bugs — like the new_game button not resetting status, or the hint message not showing — I had to test manually by running the Streamlit app and stepping through the scenarios (finishing a game, then clicking New Game, then trying to submit a guess).
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
  One test that was particularly useful was test_too_high_message_says_go_lower:


_, msg = check_guess(60, 50)
assert "LOWER" in msg
Before the fix, check_guess(60, 50) returned "Go HIGHER!" — telling the player to go in the wrong direction. After swapping the messages, the test confirmed the hint now correctly said "LOWER". It also showed me that the original tests in the file were broken in a different way: they were asserting result == "Win" against a tuple ("Win", "🎉 Correct!"), so they would have always failed regardless of the bug.
- Did AI help you design or understand any tests? How?
Claude Code helped design the tests by generating one per bug fix and naming them after what the bug was — for example test_win_on_first_attempt_gives_90 includes a comment showing the old wrong calculation (100 - 10*(1+1) = 80) and the expected correct result (90). That made it easy to understand what each test was actually checking and why the old value was wrong.
---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
The secret number was already stable when I started — it was stored in st.session_state so it didn't change between guesses.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
In a normal Python script, code runs once top to bottom and stops. Streamlit is different — every time a user interacts with the page (clicks a button, types in a field, changes a dropdown), the entire script reruns from the top. That means any variable you define normally gets reset to its original value on every interaction.

Session state (st.session_state) is Streamlit's way of remembering things across those reruns. It's like a small dictionary that survives each rerun. So if you store the secret number in st.session_state.secret, it keeps its value even when the page reruns after a button click.
- What change did you make that finally gave the game a stable secret number?
The secret was already stored in st.session_state, so it didn't randomly change between guesses. The actual problem I fixed was that switching difficulty didn't update the secret — the old secret stayed even after the range changed. I added a check that compares the stored difficulty to the current one, and if they differ, it regenerates the secret within the new range and resets the game state
---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
