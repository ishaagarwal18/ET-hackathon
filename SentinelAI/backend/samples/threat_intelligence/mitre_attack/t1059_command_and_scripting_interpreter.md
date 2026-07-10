# MITRE ATT&CK T1059 Command and Scripting Interpreter

Adversaries may abuse command and scripting interpreters to execute commands, run payloads, evade controls, and automate post-compromise activity. Common interpreters include PowerShell, Unix shell, Python, JavaScript, and Windows command shell.

Detection guidance includes monitoring process creation, parent-child process relationships, encoded command arguments, unusual interpreter execution from office applications, and script execution from temporary directories.

Response guidance includes isolating affected hosts, collecting command-line telemetry, reviewing spawned child processes, rotating exposed credentials, and blocking malicious scripts or interpreter abuse patterns.
