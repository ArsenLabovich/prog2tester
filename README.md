
---
<h1>Requirements</h1>

_**- Python (version 3.6+)**_

**_- GCC (version 7.5+, optional: Cygwin, use the same GCC as in your IDE)_**

**_- \*\*Hands growing not from the ass\*\*_**

--- 

### **TASK 2 ONLY**
### **Starting Guide** 

In the working directory , there should be a package `/src` with  a compilable C file named `main.c` or `z2.c`
and an unpacked folder with tests downloaded from the site `prog2.dev`.
Or you can create your own tests with the same structure.

### **Structure Example (only for 1st task, then will be updated)**
```
stdin/
├── scenar_1/
│   ├── (1st input for the first scenario)
│   ...
├── scenar_2/
│   ├── (1st input for the second scenario)
│   ...
├── ....
stdout/
├── scenar_1/
│   ├── (1st output for the first scenario)
│   ...
├── scenar_2/
│   ├── (1st output for the second scenario)
│   ...
include/
├── data.h
├── functions.h
src/
├── data.c
├── functions.c
├── (main.c or z2.c) 
tester.py
```
---
### **How to use?**
To run tests you need to go to directory where 
the script,tests and C file are located and run the following command:

```bash
python tester.py
``` 

### **Show Difference Mode**
You can use the `-s` or `--show-diff` program argument to run tests in show\_difference mode.
By default, the script will run tests in the usual mode (--show-diff = False).

---
 
```bash
python tester.py -s 
``` 
```bash
python tester.py --show-diff
``` 
Tester will run tests and show the difference between the expected and actual output.


---
Example of the output:
---

Example 1

![example1](example_pictures/compilation_failed_example.png)
---
---

Example 2

![example2](example_pictures/passed_and_failed_tests_example.png)
---
---

Example 3

![Example3](example_pictures/show_difference_example.png)
---
---

#### *Author - Arsen Labovich*

#### *All rights reserved. Unauthorized copying or use of this document is prohibited.*

---


#### Contact me in case of problems:

- **Telegram:** [@Laboviiich](https://t.me/Laboviiich)
- **Email:** [arsen.labovich@gmail.com](mailto:arsen.labovich@gmail.com)
- **Discord:** [medved9762] [medved9762]
]
