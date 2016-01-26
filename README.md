# CnC-Botnet-in-Python
C&#38;C Botnet written in Python

<h2>Description</h2>
Simple botnet written in Python using fabric. 
<p>
The author is not responsible for the use of this code.

<h2>Hosts</h2>
It is possible to load hosts from a file _hosts.txt_ included in the main directory of the project.
The default format for this file is:
```bash
username@host:port password
```

If the port number is not declared, port 22 is used:
```bash
username@host password
```
SSH connection is the default authentication way, so if the host knows the public key of the user, it is not necessary to indicate the password:
```bash
username@host
```

<h2>Usage</h2>
To start the application, simply download the repository
```bash
git clone https://github.com/marcorosa/CC-Botnet-in-Python
cd CC-Botnet-in-Python
```
Create the _hosts.txt_ file (optional, see above), and run the start script
```bash
python start.py
```

<h2>Example</h2>
```
=================================
MENU
=================================
[0] Load host from external file
[1] Add a new host
[2] Print selected hosts
[3] Check active hosts
[4] Select only active hosts
[5] Select bots
[6] Execute command locally
[7] Execute command on bots
[8] Run external script
[9] Open shell in a host
[10] Exit
>>> 
```
