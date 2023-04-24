## LeetConnect
---

LeetConnect is a program that lets you do LeetCode, Codewars, and HackerRank challenges from your IDE, text editor, and whatever else you have that can write to a file. <br>
It uses Selenium WebDriver to accomplish this.

Now that you're interested, I have to let you know the unfortunate reality of the situation. <br> LeetConnect only supports Codewars at the moment (very ironic), so the previous statement may only be 1/3 accurate, however, LeetCode support should be coming in the very near future.

I made this program for myself to use and rushed it *real bad*, so right now the only driver option is Chrome, and I'm not *entirely* sure if it works on Linux. I tried to make it compatible, but I haven't gotten around to testing it yet.

---


## Features:

1. Effortless cookie management, LeetConnect makes it as simple as possible to deal with cookies in WebDrivers. Simply run the setup for your target platforms once and LeetConnect will take care of the storing and adding of cookies to the WebDriver for all your configured platforms.

2. Customizable solution parser. Easily add your own functions to take care of parsing solutions before they're ran on the target platform, using solution_parser.py

3. Solution result parsing and output specifically designed to look good in terminals, it's got colors!
---

## Danger ahead, take heed!

LeetConnect has had a tendency to not close the Chrome WebDrivers all too well during development. 

 I suspect most of this is really just down to all the Exceptions and unexpected terminations faced during development, and that it *should* work mostly fine in actual use, but I've not used it more than a couple hours myself.

 If the server terminates unexpectedly, just check the task manager for ay WebDrivers that may still be running and kill the processes.
 
  Not a major problem if you don't, but it won't really be helpful to leave them running if your computer is already not very performant.

---

## Using LeetConnect
LeetConnect is used by launching it with arguments, there aren't very many.

### Requirements:
1. Python
2. Selenium
3. Chrome WebDriver (or just Google Chrome on Windows.)
```
Run the `leetconnect.py` script with the appropriate command-line arguments to perform the desired action. Here is a list of available arguments:

- `-o, --open`: Opens a new LeetConnect server configured for the target platform.
- `-r, --run`: Runs the solution file on the target platform and shows the results.
- `-s, --submit`: Submits the solution file on the target platform and shows the submission results.
- `-i, --import`: Imports code from the target platform's embedded editor.
- `--setup`: Perform cookie setup on the target platform.
- `-p, --port`: Port to listen on or send commands to (default is 9000).
- `-c, --close`: Closes the active LeetConnect server.
- `--status`: Returns whether the previous session is still active.
```

Example usage:
```
starts the cookie setup process for the target platform
leetconnect.py --setup codewars

open a server with Codewars as the target platform on the default port
leetconnect.py -o codewars 

overwrite your file with the code from the platform's embedded editor
leetconnect.py -i my_solution.py

run/test your code on the target platform
leetconnect.py -r my.solution.py

same as above but submits it instead
leetconnect.py -s my.solution.py

close the server and WebDriver
leetconnect.py -c
```
---

## FAQ
###### No one has asked any questions, I've made it all up!

---

### **Q: Do I have to follow that style to contribute?**
**A:** No, use whatever style you want, use as many different styles as you want, I don't really care as long as it runs, this isn't a world changing project or passion of mine, I just want to do my Codewars in an IDE (or VSCode, mostly VSCode). 

<br>

### **Q: Dear God why does your code look like that???**
**A:** I like it. PEP8 is for employable programmers, I try my best to not be one.

<br>

### **Q: Will LeetConnect ever support X platform/browser/os?**
**A:** If someone adds support for it and sends a PR, sure.

<br>

### **Q: Why am I encountering XYZ error?**
**A:** Don't know, works on my computer.

----

## Contributing
Feel free, just don't add more dependencies or change the style of existing code.