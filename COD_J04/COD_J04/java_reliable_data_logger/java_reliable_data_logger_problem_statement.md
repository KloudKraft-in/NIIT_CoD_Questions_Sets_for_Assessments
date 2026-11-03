# Java: Reliable Data Logger

Implement a Java program to process and validate a series of system log entries. The program should:

* Parse log entries containing a timestamp, log level, and message
* Identify and handle malformed logs using a custom exception
* Use try-with-resources to ensure proper stream management

**Class Description**
Complete the class `LogProcessor` in the editor with the following methods:

* `void processLogs(List<String> rawLogs)`: Iterates through the logs and validates them.
* `boolean isValid(String log)`: A helper method to check if the log follows the format `[TIMESTAMP] LEVEL MESSAGE`.

**Custom Exception**
Implement the `MalformedLogException` class. It should be thrown if:

1. The log does not start with a bracketed timestamp `[...]`.
2. The log level is missing or invalid (Valid levels: INFO, WARN, ERROR).

**Returns**

* For each valid log, print: `Log Processed: {LEVEL}`.
* For each malformed log, catch the exception and print: `Error: {errorMessage}`.

**Constraints**

* $1 \le NumberOfLogs \le 100$.
* Timestamp format: `[HH:mm:ss]`.

**Input Format For Custom Testing**
The first line contains an integer $N$ denoting the number of log entries.
The following $N$ lines contain the raw log strings.

**Sample Case 0**
**Sample Input For Custom Testing**

```text
3
[10:00:00] INFO System Started
10:05:00 WARN Disk space low
[10:10:00] FATAL Memory overflow
```

**Sample Output**

```text
Log Processed: INFO
Error: Log must start with a bracketed timestamp.
Error: Invalid log level: FATAL.
```

**Explanation**
Log 1 is valid.
Log 2 is missing brackets around the timestamp.
Log 3 uses an invalid level "FATAL" (not in INFO/WARN/ERROR).


**Boilerplate :**

```
// student_workspacd/solution.java

import java.util.*;

/* 
 * Implement the 'LogProcessor' class here.
 * The 'MalformedLogException' is already defined in the Harness.
 * DO NOT use access modifiers (e.g.: 'public') in your class declarations.
 */

class LogProcessor {
    public void processLogs(List<String> logs) {
        // Write your code here
    }
}

```


**Solution.java :**

```
// student_workspace/solution.java

import java.util.*;

class LogProcessor {
    public void processLogs(List<String> logs) {
        for (String log : logs) {
            try {
                if (!log.startsWith("[")) {
                    throw new MalformedLogException("Log must start with a bracketed timestamp.");
                }
              
                String[] parts = log.split(" ");
                if (parts.length < 2) {
                    throw new MalformedLogException("Invalid log level: " + log + ".");
                }
              
                String level = parts[1];
                if (!(level.equals("INFO") || level.equals("WARN") || level.equals("ERROR"))) {
                    throw new MalformedLogException("Invalid log level: " + level + ".");
                }
              
                System.out.println("Log Processed: " + level);
              
            } catch (MalformedLogException e) {
                System.out.println("Error: " + e.getMessage());
            }
        }
    }
}

```
