# Node.js Lab: Sync Offloading / Worker Pool

Duration : 120 Min.

## Scenario

A server handling user password hashing gets blocked under concurrent load because CPU-intensive PBKDF2 operations block the event loop thread.

## Task Objectives

Perform the following actions inside the `student_workspace` directory:

- Rewrite the Express endpoint in `server.js` to offload PBKDF2 password hashing to a background thread script `worker.js` utilizing the Node.js `worker_threads` Worker pool.

## Instructions to Perform the Task

1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Navigate to and click the specific files mentioned in the Task Objectives.
3. Make the necessary code edits in the editor.
4. Press `Ctrl + S` (Windows) or `Cmd + S` (Mac) to save your changes.
5. If you need to run commands, open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.

## Validation

Once you have saved your files and are ready to submit, return to the platform dashboard and click the **"Run Test" / "Verify"** button. This will automatically evaluate your changes and generate your score!

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case     | Requirement                                                        | Marks   |
| ------------- | ------------------------------------------------------------------ | ------- |
| **TC1** | File server.js exists in workspace                                 | 0 Marks |
| **TC2** | File worker.js exists in workspace                                 | 0 Marks |
| **TC3** | Worker pools utilized for processing CPU-intensive operations      | 3 Marks |
| **TC4** | Main execution threads remain non-blocked during hashing execution | 3 Marks |
| **TC5** | Asynchronous response payloads correctly formatted                 | 3 Marks |
| **TC6** | Worker data pbkdf2 properties configurations matched               | 3 Marks |
| **TC7** | System handles thread messaging error events                       | 4 Marks |
| **TC8** | Node.js worker_threads module integrated successfully              | 4 Marks |

**Total Score: 20 Marks**
