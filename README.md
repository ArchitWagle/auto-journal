# AutoJournal

A simple text to handwriting converter.
## Installation

clone this repository to your local machine
```bash
git clone https://github.com/ArchitWagle/auto-journal.git
```

## Usage

Firstly take a image of your handwriting sample and copy  the image to `images/` folder. 
Name your sample file as `sample_r.jpeg`   
format of sample image is  
  
![The sample](/images/sample_r.jpeg)


#### Note: It is extremely important to follow the image sample format and take a clear photo without shadows.

Now open the file `input.txt` and copy the text you want to convert into the file. I have already filled the file with some random text.

Now execute the following commands

```bash
python3 adjust.py
```
Now you will see a gui window.  At the bottom of the window are 2 scroll bars.  
The first scrollbar adjusts your image contrast. The second scroll bar is like a activation button  
  
move the second scroll bar to the right completely.  
Now adjust the contrast with the first scroll bar, keep adjusting until there is a bounding box around each and every character.  
Once you are done with the above steps hit the `esc` key.

Now execute the following command

```bash
python3 hw.py
```
Your handwritten image would appear. click `esc` to exit

## Contributing
Pull requests are welcome. 
