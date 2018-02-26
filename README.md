# off-line-interview
## Enviroment
- Windows 8
- Python 3.5.2 | Anaconda 4.2.0 (64-bit)
## Tasks
### Task 1
- **Description**：Write a Python program that can detect the language of console input from users. (use the language identification service provided by MeaningCloud)

- **Running from command line**:  
```
    C:\interview>python task1.py
```
### Task 2
- **Description**：Write a Python programme that can detect the language of the content of a text file. (use the language identification service provided by MeaningCloud)

- **Running from command line**:  
```
    C:\interview>python task2.py filename
```

- **Running Example**:  
```
    C:\interview>python task2.py input.txt
    English
```
### Task 3
- **Description**：Write a bash script to iterate your Python program in task 2 for detecting language of a directory of text files.

- **Running from command line**:  
```
    C:\interview>task3.sh foldername/
```

- **Running Example**:  
```
    C:\interview>task3.sh input/
    input//Chinese.txt:
    Mandarin Chinese
    input//English.txt:
    English
    input//Spanish.txt:
    Spanish
    Press any key to continue.
```
### Task 4
- **Description**：Develop a Flask project. In essence, implement a website allowing users to input texts, upload text files and displaying detected results. This webside can also investigate other language detection APIs (e.g. Language Detection), and compare the result to the same task of MeaningCloud by collecting users'feedback. It can also visualise the comparison by bar chart.

- **Running Example**:   
```
    C:\interview>cd task4
    C:\interview\task4>python task4.py
```
![image](https://github.com/yuanziinlondon/off-line-interview/tree/master/readme_images/1.png)
