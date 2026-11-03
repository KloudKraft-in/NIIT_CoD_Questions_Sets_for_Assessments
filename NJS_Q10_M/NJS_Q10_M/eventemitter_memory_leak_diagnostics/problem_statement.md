# Node.js Lab: EventEmitter Memory Leak Diagnostics

Duration : 60 Min.

## Scenario

A server endpoint registers custom event listeners to a global event emitter for each API call but fails to remove them, creating a massive memory leak under concurrent load.

## Task Objectives

Perform the following actions inside the `student_workspace` directory:

- Identify the event listener leak inside `server.js` and modify it to register listeners dynamically using once() or clean up properly upon request execution completion.

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

| Test Case     | Requirement                                               | Marks   |
| ------------- | --------------------------------------------------------- | ------- |
| **TC1** | File server.js exists in student workspace                | 2 Marks |
| **TC2** | Express server compiles and starts successfully           | 2 Marks |
| **TC3** | Target route /api/listen returns HTTP 200 OK status       | 2 Marks |
| **TC4** | Global emitter listeners do not grow unbounded under load | 3 Marks |
| **TC5** | Correct usage of once() or removeListener() handlers      | 3 Marks |
| **TC6** | Listener limit warnings do not trigger                    | 3 Marks |
| **TC7** | Request event responses are handled correctly             | 3 Marks |
| **TC8** | Clean shutdown and listener cleanup verified              | 2 Marks |

**Total Score: 20 Marks**
