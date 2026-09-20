# The Unofficial Guide

<!-- Replace this line with your name and which corpus you picked. -->
# Khaled Ismael, campus_life

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Unit 1

## What This Does
This project is a RAG application that uses the `campus_life` corpus to answer questions about campus policies, housing, courses, dining, and student services. It retrieves relevant document chunks and uses them to generate an answer. The system can answer questions when the information is covered by the corpus and refuses questions that are not sufficiently supported by the documents.

## Chunking Strategy
I split the `campus_life` documents at paragraph boundaries with a **400-character maximum** and **no overlap**. I kept the document title in each chunk so the chunk has enough context to stand on its own.

**Chunk size:** and **Overlap:**
I chose a 400-character chunk size with 0 overlap because the campus_life documents I read in Milestone 1 are mostly short, focused posts rather than long guides. The baseline run showed an average document length of about 317 characters, with the longest at 549 characters, and many documents already formed a complete thought without needing to be split. However, some documents contain multiple paragraphs with separate facts, so I wanted to split those at paragraph boundaries rather than cutting through sentences. I also noticed that character-based overlap could cut words across chunk boundaries, so I removed overlap for this strategy. I kept the document title in each chunk so that a retrieved chunk still has enough context to identify what it is about.


## Sample Chunks
**Chunk 1** — source: `admin_add_drop_deadline.txt` — produced by: `split_documents`

```
======================================================================
Chunk 1  |  source: admin_add_drop_deadline.txt#0  |  produced by: chunker.py::split_documents
======================================================================
On the add/drop deadline

You can add a course through the end of the second week. Dropping is a longer window — through the end of week six — but a drop after week two shows as a W on your transcript. Nothing anywhere on the registrar's site says this plainly,and students find out from each other.

```

**Chunk 2** — source: `course_cs_210.txt` — produced by: `split_documents`

```
======================================================================
Chunk 2  |  source: course_cs_210.txt#0  |  produced by: chunker.py::split_documents
======================================================================
CS 210 Data Structures

I'm a junior and I've done this twice now. Format is lecture with weekly labs; slides go up after class, not before. Assessment: two midterms and a final, all drawn from lecture material rather than the textbook. Midterms are curved, the final is not.

Expect 8 to 10 hours a week outside class.
```

**Chunk 3** — source: `course_math_220_workload` — produced by: `split_documents`

```
======================================================================
Chunk 3  |  source: course_math_220_workload.txt#0  |  produced by: chunker.py::split_documents
======================================================================
Workload for MATH 220 Linear Algebra

People keep asking so: 6 to 8 hours a week, almost all of it on problem sets. That's real time, not optimistic time.

It's front-loaded — the first month is heavier than the rest, partly because you're learning the format.

```

**Chunk 4** — source: `dining_the_ridgeway_cafe_followup.txt` — produced by: `split_documents`

```
======================================================================
Chunk 4  |  source: dining_the_ridgeway_cafe_followup.txt#0  |  produced by: chunker.py::split_documents
======================================================================
Re: The Ridgeway Café

Adding to what people have said about The Ridgeway Café. The wait figure of 10 to 15 minutes at 12:30 matches what I've seen. If you're trying to eat between classes, go before 11:45 and it's a different building entirely.

Also worth saying: seating is tight; about 40 seats for a building of 900. Nobody tells you this at orientation.
```

**Chunk 5** — source: `housing_morrow_house.txt` — produced by: `split_documents`

```
======================================================================
Chunk 5  |  source: housing_morrow_house.txt#0  |  produced by: chunker.py::split_documents
======================================================================
Morrow House — what it's actually like

Just finished a year in this building. Built 1954, partially renovated 2008. Rooms are singles and doubles, hall bathrooms.

The good: cheapest housing tier by about $900 a year, and the singles are real singles.

The bad: known damp problem on the ground floor; two rooms were taken offline in 2024.
```

## Sample Answer

<!-- One complete question and answer, pasted as text, with the source line
     visible. Milestone 4. -->
**Question:**
When does dropping a course put a W on your transcript?

**Answer:**
```
(best distance 0.236, cutoff 0.6)

Dropping a course puts a W on your transcript after week two (through the end of week six). 

Source: admin_add_drop_deadline.txt

Sources retrieved: admin_add_drop_deadline.txt, admin_grade_appeals.txt, admin_pass_fail_option.txt, admin_transcript_requests.txt, admin_withdrawal_deadline.txt

1 model calls this session, 529 tokens (495 in, 34 out)
```

**Question:**
When does dropping a course put a W on your transcript?

**Answer:**

```
#   distance   source                           preview
----------------------------------------------------------------------------------------------------
1   0.2356     admin_add_drop_deadline.txt      On the add/drop deadline  You can add a course throu...
2   0.4633     admin_withdrawal_deadline.txt    On the withdrawal deadline  Withdrawal is a differen...
3   0.4998     admin_transcript_requests.txt    On the transcript requests  Official transcripts cos...
4   0.5670     admin_pass_fail_option.txt       On the pass/fail option  Any course outside your maj...
5   0.6092     admin_grade_appeals.txt          On the grade appeals  A grade appeal starts with the...

Gate: best distance 0.236 is under the 0.6 cutoff

Lower is better. 0.3 is a close match, 0.9 is unrelated.
Milestone 4: run your five questions, then the five in OUT_OF_SCOPE
that your documents clearly don't cover, and look for the gap
between the two groups. Your cutoff goes in that gap.
```

**My relevance cutoff:**
The five in-scope questions had best distances between **0.2036 and 0.2916**. The five out-of-scope questions had best distances between **0.8246 and 0.9340**. This leaves a large gap between the two groups: the highest in-scope distance was **0.2916**, while the lowest out-of-scope distance was **0.8246**.

Therefore, I placed the cutoff at **0.6**, which falls between the two groups. With this cutoff, all five in-scope questions passed the relevance gate, while all five out-of-scope questions were rejected. I kept 0.6 rather than setting the cutoff closer to either group because it provides room for some variation in retrieval distances while still separating the questions the corpus covers from clearly unrelated questions.
```
| Question | In corpus? | Best distance |
|---|---|---:|
| When does dropping a course put a W on your transcript? | Yes | 0.2356 |
| How does the housing lottery determine priority for juniors and seniors? | Yes | 0.2036 |
| How many times can you change your meal plan tier, and when is the deadline? | Yes | 0.2377 |
| What happens to unused dining dollars at the end of the academic year? | Yes | 0.2916 |
| How much does an official electronic transcript cost? | Yes | 0.2486 |
| What is the capital of Mongolia? | No | 0.8246 |
| How do I change the oil in a diesel engine? | No | 0.9340 |
| Who won the 1994 World Cup? | No | 0.8859 |
| What is the recommended dosage of ibuprofen for a headache? | No | 0.8442 |
| How do I write a for loop in Rust? | No | 0.8960 |

```


## How I Used AI
Two specific moments I used Claude:

**1.**
I asked Claude for help deciding how to chunk the `campus_life` documents. Claude suggested I use a fixed character size with character-based overlap. After looking at the actual documents and testing the chunker, I noticed that some documents were already short and complete, while longer documents contained separate facts in different paragraphs. I also found that character-based overlap could split a word across a chunk boundary, such as turning `"Expect"` into `"pect"`. I changed the approach to split on paragraph boundaries instead of character positions. 


**2.**
I gave Claude my five in-scope best distances (0.2036–0.2916) and five out-of-scope best distances (0.8246–0.9340) and asked where it would put the relevance cutoff and what I might get wrong at that number. It said the gap was wide enough that, for these ten questions, roughly 0.35 to 0.75 would separate them correctly. I kept the cutoff at 0.6 because it sits roughly in the middle of the gap and also matches the starter's reasonable default range.

Claude also pointed out a limitation in my test set. My five out-of-scope questions were clearly unrelated to campus life, so they produced very high distances. A more realistic failure case would be a question that shares campus-life vocabulary but asks about information that is not actually covered by the corpus, such as asking whether the school has a pool or asking about a dorm that is not mentioned in the documents. Those questions could potentially retrieve a superficially similar chunk and fall below the 0.6 cutoff.


<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
