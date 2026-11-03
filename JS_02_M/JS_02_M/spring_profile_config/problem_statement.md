# Java Lab: Spring Profile Configuration Extraction

Duration : 60 Min.

## Scenario
Read and extract specific configuration values from a multi-profile Spring Boot `application.yml` file. You are given a configuration file that contains multiple profiles: `default`, `dev`, and `prod`. The production profile contains a sensitive database password that needs to be extracted for an automated deployment script.

## Task Objectives
Perform the following actions inside the `student_workspace` directory:
- Review the `src/main/resources/application.yml` file to understand its structure.
- Edit the provided `extract.sh` script.
- Your script must parse the YAML file and extract the value of `db.password` under the `prod` profile (e.g., using `grep`, `awk`, `sed`, or `yq`).
- Ensure the script writes the exact password string into a new file named `output.txt` in the `student_workspace` directory.
- Make sure your script is executable (`chmod +x extract.sh`) and runs successfully.

## Instructions to Perform the Task
1. When your workspace loads in **VS Code**, use the **Explorer** panel on the left to locate your files.
2. Navigate to and click the specific files mentioned in the Task Objectives (e.g., `src/main/java/...`).
3. Make the necessary code edits in the editor.
4. Press `Ctrl + S` (Windows) or `Cmd + S` (Mac) to save your changes.
5. If you need to run commands (like `mvn clean`), open the built-in terminal by clicking **Terminal > New Terminal** from the top menu.

## Validation
Once you have saved your files and are ready to submit, return to the platform dashboard and click the **"Run Test" / "Verify"** button. This will automatically evaluate your changes and generate your score!

## Grading Criteria
Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | `extract.sh` has execution permissions and runs successfully | 4 Marks |
| **TC2** | The `output.txt` file is generated | 4 Marks |
| **TC3** | `output.txt` is not empty | 4 Marks |
| **TC4** | `output.txt` contains the correct `db.password` value for the `prod` profile | 4 Marks |
| **TC5** | `output.txt` does NOT contain passwords from the `dev` or `default` profiles | 4 Marks |

**Total Score: 20 Marks**
