# Database Lab: PostgreSQL Connection String Parsing & Diagnostic Scripting

Duration : 30 Min.

## Scenario
An application fails to connect to PostgreSQL with 'FATAL: password authentication failed for user app_user'. The engineer is handed three distinct connection URI formats: (1) postgresql://app_user:pass@10.0.1.20:5432/app_db?sslmode=require, (2) host=10.0.1.20 port=5432 dbname=app_db user=app_user, and (3) an environment variable based configuration. The engineer must build a diagnostic Python script to parse connection strings, validate target host reachability, and test credentials.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
1. Create a script ~/test_pg_dsn.py that parses a database URI into host, port, dbname, user, and sslmode components.
2. Attempt a socket connection to target host and port to verify network reachability before attempting authentication.
3. Execute a test query 'SELECT current_database(), current_user;' and format output as JSON.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Review the technical objectives and navigate to the specified files or directories.
3. Make the necessary configurations or code edits in the editor.
4. Press `Ctrl + S` (Windows) or `Cmd + S` (Mac) to save your changes.
5. If you need to run commands, open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.
6. Verify your progress locally by executing:
   ```bash
   python run.py
   ```

## Validation
Once you have saved your files and are ready to submit, return to the platform dashboard and click the **"Run Test" / "Verify"** button. This will automatically evaluate your changes and generate your score!

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | URI decomposition: script accurately parses components from PostgreSQL URI and key-value formats | 3 Marks |
| **TC2** | Pre-flight socket check: script verifies TCP port 5432 availability prior to SQL authentication | 4 Marks |
| **TC3** | Execution & formatting: returns valid JSON with database name, user, and connection latency | 3 Marks |

**Total Score: 10 Marks**

## Important Notes
- This is an **Auto-Evaluated** assessment.
- Ensure all required files and configurations are saved in `student_workspace` before submitting.
