# JunQi-battle-chess
Git clone this repository, do `pip install -r requirements.txt`, and enter the game by clicking the file "PLAYGAME.py"

If you have any problems, feel free to submit an issue!
# The game needs two players, one is red and the other is black. Like other chess rules, the two players take turns to move their chess, following JunQi's specific rules:  
1. high ranking piece eats low ranking piece ('司令'>'军长'>'师长'>'旅长'>'团长'>'营长'>'连长'>'排长'>'工兵')  
2. '炸弹' destroys everything (except '军旗') and itself  
3. only '工兵' or '炸弹' can eat '地雷'  
4. the smallest ranking piece can eat '军旗'  
5. only after removing all the '地雷's, one can eat the other's '军旗'  
6. if the piece moves into the camp (the circle on the chess board), it is protected, and no one can eat it  
7. '地雷' and '军旗' cannot move  
8. normally a piece can move one step each turn, but if it is on the 'zebra line', it can move in a straight line (no turning) as long as it is on the 'zebra line'  
9. By winning, one needs to either i.eat up all the moving pieces of the opponent or ii.eat the opponent's '军旗'  
  
# How to play my game  
1. click enter file PLAYGAME.py
2. click the left button on the mouse to select or move the piece  
3. the first click on a piece reveals its rank, the afterwards clicks move the piece. Then click the position to which you want your piece to go. (you cannot go to a position where there
is a covered piece  
4. if you click a piece to move but want to cancel the move, click the right button on the mouse, and the piece will go back to its original position  
5. if you want to redo a move, press 'F' on the keyboard  
6. if you want to admit defeat or make a tie, click the lower left corner  
7. once the game is over, press 'R' on the keyboard to start a new game  
8. press 'Enter' on the keyboard to switch on and off the Fullscreen display  
9. press 'Esc' on the keyboard to exit the game  
  
The sound and image of victory are my recordings from Command and Conquer Generals: Zero Hour  
 
This is my first project written in Pygame as a newbie in Python. I started learning Python a few months ago, following the book Python Crash Course by ehMatthes.  
This JunQi program is a practice of my understanding of Python basics and Pygame. (I would appreciate it if you can give me some constructive advice on my code :))
  
Thanks for reading!  
I hope you get inspired!
