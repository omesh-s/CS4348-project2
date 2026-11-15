# CS 4348 Project 2 | Bank Simulation

## Files

| File | Role |
| --- | --- |
| `project2.py` | Runs the bank simulation. |
| `devlog.md` | Records the plan, changes, and results for each session. |
| `README.md` | Explains how to run, check, and package the project. |

The `.git` folder holds the commit history.

## Run and check

Open a terminal in the `project2` folder. Use Python 3. No build or extra
packages are needed.

```bash
python3 project2.py
```

On campus Linux, run these commands to save the output and check it.

```bash
timeout 10s python3 project2.py > ../bank-output.txt
grep -c 'leaves the bank$' ../bank-output.txt
grep -c 'leaving for the day$' ../bank-output.txt
tail -n 1 ../bank-output.txt
```

The counts should be `50` and `3`. The last line should be
`The bank closes for the day.` The order of many lines can change each run.

On Windows PowerShell, use `py -3 project2.py` to run it. If your install
uses the `python` command, use `python project2.py`.

## How the simulation works

- Three teller threads report ready before the main thread starts 50 customer
  threads.
- Customers enter a first-in, first-out line. A teller takes the next visit.
  A semaphore protects the line and another counts the customers in it.
- Each visit has a shared record with its customer ID, teller ID, and
  transaction. The teller and customer use semaphores to signal each step.
- The door and safe each have two permits. The manager has one. Only tellers
  handling a withdrawal visit the manager.
- The main thread waits for all customers to leave, wakes the tellers, and
  waits for them to exit.

## Add your own work and submit

1. Check the due date in eLearning. The bundled project sheet says Spring
   2026 and lists April 17 at 11:59 p.m.
2. Before your own review or test session, add a dated heading to the end
   of `devlog.md`. Write what you know and what you plan to check. Commit
   that entry. If needed, use `git config user.name "Your Name"` and
   `git config user.email "your-email@example.com"` in this folder first.
3. Run the checks. Add a second dated entry with the results you saw, what
   you learned, and any fix you made. Commit the log and any source changes.
4. From inside `project2`, run the commands below. The first should report
   a clean working tree, and the second should show your commits.

```bash
git status
git log --oneline
```

5. From the parent folder, create a fresh ZIP and confirm it contains the
   Git history.

```bash
cd ..
python3 -m zipfile -c project2-submission.zip project2
unzip -l project2-submission.zip | grep 'project2/\.git/HEAD'
```

In PowerShell, use `py -3 -m zipfile -c project2-submission.zip project2`
and `tar -tf project2-submission.zip | Select-String 'project2/.git/HEAD'`.
Upload `project2-submission.zip` to eLearning.
