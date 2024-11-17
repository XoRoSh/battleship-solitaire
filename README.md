# battleship-solitaire
Constraint Satisfaction Problem that is solved by using **Forward Checking** and **General Arc Consistency**

# Game desciption:
Each cell represents a variable that has a certain domain i.e "1 (part of ship) 0 (water)". By creating constraints we can describe limitations that rules impose on the board.  

**example:**

<img width="553" alt="image" src="https://github.com/user-attachments/assets/c936b053-e68c-4958-a016-406cd2b7873d"> <br />
<img width="431" alt="image" src="https://github.com/user-attachments/assets/26adf4ba-0940-452e-8e91-54601f7516be">


[Try playing](https://lukerissacher.com/battleships) 


# Solving puzzle 

## run code
    python3 solve_battleship_solitaire.py --inputfile <input file> --outputfile <output file>
    
provided few input cases. i.e: <br />
    python3 battle.py --inputfile input_easy1 --outputfile output_easy1

**input file format** <br />
211222<br />
140212<br />
32100<br />
000000<br />
0000S0<br />
000000<br />
000000<br />
00000.<br />
000000<br />

## file format explained: 
**first 3 lines:** <br/>

211222 // row constraints <br />
140212 // column constraints 3rd column is water initially <br />
3210   // number of each ship type: single, double .... <br />
<br />
**So the board would look like:**
<pre>
    1 4 0 2 1 2 
  _____________
2 | < > 0 . . .  
1 | 0 0 0 . S .   
1 | 0 ^ 0 . . .  
2 | 0 M 0 0 . S  
2 | 0 v 0 ^ . . 
2 | 0 0 0 v . S  
</pre>
3 - single <br />
2 - double <br />
1 - tripe  <br />

| 0 - no hint 
| S - submarine 
| . - water
| M - middle 
| < - left 
| > - right 
| ^ - top 
| v - bot 


