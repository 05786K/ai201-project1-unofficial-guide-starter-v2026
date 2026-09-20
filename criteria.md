# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:**
While reading the campus_life documents in Milestone 1, I noticed several administrative documents cover closely related, deadline-adjacent policies — `admin_add_drop_deadline.txt`, `admin_withdrawal_deadline.txt`, `admin_pass_fail_option.txt`, and `admin_grade_appeals.txt` all discuss similar transcript/registration territory. Most documents are short and single-topic, so I expect retrieval to usually find the right one, but I'm allowing one miss for cases where two of these adjacent policy docs get confused with each other.


---

## 2. Every answer names a source
Every answer the system produces names at least one source document.

**Why this target:**
The generation stage of my pipeline attaches a `Source:` line to every answer by construction. This criterion isn't testing retrieval quality — it's checking that the pipeline never silently drops that field, e.g. if generation fails or the gate is bypassed unexpectedly.


---

## 3. The relevance gate stops out-of-corpus questions
When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

**Why this target:**
I haven't measured my own cutoff yet — that's Milestone 4 — so for now I'm relying on config.py's documented default of 0.6 as a reasonable starting point. campus_life's documents are narrowly about this specific university's policies and buildings, so I expect a genuinely unrelated question to score clearly higher than an in-scope one, but I'm not assuming the default is perfectly tuned for this corpus until I've actually checked it, which is why I'm not requiring 5 of 5.


---

## 4. Chunk Size
At least 4 of the 5 sampled chunks are between 150 and 500 characters, matching the scale of a single campus_life post.

**Why this target:**
corpora/README.md reports that campus_life documents average about 317 characters, and the ones I read in Milestone 1 ranged from short single-paragraph notices to slightly longer multi-paragraph posts. I expect a good chunk here to be about the size of a typical post: not a one-sentence fragment, and not padded out much longer than what a real post looks like.


---

## 5. The cited source actually supports the answer
For at least 4 of 5 test questions, the source document named in the answer contains the information used to answer the question.

**Why this target:**
Each campus_life document covers one topic (e.g. `admin_add_drop_deadline.txt` only discusses the add/drop deadline), so checking "does the named source actually contain the cited fact" is a direct single-document check, not a judgment call. I'm allowing one miss because retrieval could occasionally name a topically adjacent document (see criterion 1) whose content overlaps enough to look right without actually being the source of the specific fact used.


---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
