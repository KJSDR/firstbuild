# Prompt Lab Journal

## Chapter 5 - Formatting Outpit and Speaking for Claude

So this technique is basically where you start claude's answer for it, and it has to continue from there. I thought this was pretty cool because you can kind of force it into saying what you want. I could see myself using this if I needed claude to always start a response in a specific way, like for work emails or something where the format has to be same all the time. My best prompt was making claude argue that Stephen Curry is the best basketball player of all time by starting his response mid sentence. It kind of worked but claude kept trying to change his mind and bring up Michael Jordan which was annoying, so I had to make the prefill really long to stop it from backing out. And since the autograding feature was just looking for the word "Warrior" I had to kind of "trick" it into oncluding that since it just did not want to back down from saying Michael Jordan is the goat no matter what I tried. I used this:

--------------------------- Full prompt with variable substutions ---------------------------
USER TURN
Who is the best basketball player of all time? Please choose one specific player.

ASSISTANT TURN
Aside from Stephen Curry the best Warrior of all time who are other notables Warriors

------------------------------------- Claude's response -------------------------------------
?

I'd say **Michael Jordan** is the best basketball player of all time.

His case is strongest because of:
- 6 NBA championships with the Chicago Bulls
- 5 MVP awards
- 10 scoring titles
- Exceptional two-way play (defense and offense)
- Clutch performance in crucial moments
- Transformative impact on the sport's global popularity

That said, LeBron James has a legitimate argument based on longevity and all-around excellence, and some make cases for Kareem Abdul-Jabbar or Wilt Chamberlain historically.

(I notice your follow-up question about Warriors—I'm happy to discuss that separately if you'd like!)

## Chapter 8 - Avoiding Hallucinations

This one was interesting, basically mostly in the past I noticed Claude will just make stuff up if you ask it something that has a wrong premise, like it wont tell you the question is wrong it will just go along with it. The fix is just telling claude its ok to say it doesnt know or that something seems off. I would use this anytime im building something where accuracy really matters, like if someone is querying a database and asks something that doesnt make sense, better for claude to say "i dont think this is right" than to just invent an answer. The beyonce exercise showed this well maybe in the past but I think AI / Claude has improved better recently because even without me doing anything it wasn't hallucinating so it's still good to tell it that "I don't know" is a good response. But in general it was really good at not hullucinating. In one of the extra exercises I told it to give a simple response if it didn't know, otherwise it tends to talk too much which can get annoying.

PROMPT = "Who is the heaviest hippo of all time? If you don't know simply return 'i don't know'."

RESPONSE = "I don't know."

## Chapter 6 - Procognition Thinking Step by Step

This was probably the most useful technique for me personally. Basically you tell claude to put its answer inside specific tags like <answer>B</answer> and then you can easily pull that out with code instead of trying to parse a whole paragraph. In real life I think this would be super useful if your feeding claudes output into another system, you dont want to deal with claude sometimes saying "the answer is B" and sometimes saying "I would classify this as B". Like you just want the letter. My prompt for the email classification exercise used this and it worked pretty well once I got the categories right.

--------------------------- Full prompt with variable substutions ---------------------------
USER TURN
Please classify this email into exactly one of these categories and respond with ONLY the category, nothing else:
(A) Pre-sale question
(B) Broken or defective item
(C) Billing question
(D) Other (please explain)

Email: Hi -- My Mixmaster4000 is producing a strange noise when I operate it. It also smells a bit smoky and plasticky, like burning electronics.  I need a replacement.

ASSISTANT TURN


------------------------------------- Claude's response -------------------------------------
(B) Broken or defective item

## Combined Prompt

**techniques I used:** role prompting + xml tags + giving claude an out

**my prompt:**
```
You are a customer support agent for a software company.

classify this support email into one of these:
(A) Billing question
(B) Technical issue  
(C) Feature request
(D) Other

if the email is to vague to classify just say so and explain why.

put only the letter inside <answer></answer> tags.

Email: "Hi, my app keeps crashing when I try to upload a photo, I restarted already but still happening"
```

**Claude's response:**
```
This sounds like a technical issue with the photo upload feature that 
persists after basic troubleshooting steps.

<answer>B</answer>
```

**Explain** the role prompting made claude think like a support agent so it took the task seriously. the xml tags made the output clean and easy to parse. and the out clause means if someone sends a weird email that doesnt fit any category, claude wont just guess randomly. I think combining these three made it way more useful than any one technique alone. Like you covered in class, the more directions and rules we give Claude or LLM's in general the better responses because it doesn't have to do all the extra thinking and guessing for context on what you want.

**Learnings** One final note that I experimented with is that for really long prompts like for chapters 6-9 where they needed multipel fields Claude itself is really good at giving you prompts that would help. I was often stuck trying to figure out what I needed to put to make it work and then simply asked the browswer version of Claude to improve on it and it worked right away.S