# Linux Lab: Working with Directories and File Operations (Local VM)

Duration : 60 Min.

## Scenario

As a systems administrator, you are tasked with managing directory structures and performing file operations on your local Ubuntu system. You need to create a designated workspace directory, generate a temporary file inside it, and move and rename the file into your home directory.

## Task Objectives

Perform the following actions inside your home directory (`~`) of the local Linux system:

### 1. Environment Verification

- Ensure the local VM environment is running with your default home directory (`~`).

### 2. Directory & File Creation

- Create a workspace directory named `workspace` inside your home directory (`~/`).
- Create an empty file named `temp.txt` inside `~/workspace/`.

### 3. File Operations (Move & Rename)

- Move the file `temp.txt` from `~/workspace/` to `~/`.
- Rename `temp.txt` to `final.txt` so that the final file path is `~/final.txt`.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1**   | Local VM Environment active and verified | 0 Marks |
| **TC2**   | Directory `workspace` and file `temp.txt` created successfully | 5 Marks |
| **TC3**   | File `temp.txt` moved and renamed to `~/final.txt` | 5 Marks |

**Total Score: 10 Marks**
