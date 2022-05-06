# merbobot
Bot for controlling the quality of display of goods on the shelves for company EFKA, hackathon URBAN TECH CHALLENGE

 The bot is available at: https://t.me/merbobot.
 

<img src="https://github.com/Neafiol/Merbobot/blob/master/merboTG.gif?raw=true" alt="" style="max-width:100%;">



Bot for Telegram, made at the hackathon URRBAN TECH CHELLENGE. The algorithm is as follows:
1. Having discovered the inadequacy of the display of goods on the shelves of the store, the buyer sends a photo to the bot.
2. A more precise geolocation and the allocation of the store.
3. The photo is checked for spam and the quality of the display of products on the shelf.
4. In case of detection of imperfect display of goods on the shelves, the user gets discount points.
5. Information about the quality of the display of goods is available to store employees on the bot's site.

After receiving the photos are checked for spam with the help of a neural network. Then from each photo using Hough's algorithm the shelves are selected, using gradient boosting methods the presence of extraneous goods on the shelves, gaps between items and unevenly standing products are searched. All photos can later be manually marked up in the web interface and replenish the dataset. At the time of writing, the accuracy of spam detection is 96%, detection of display quality is 73.432%. 

The photo shows graphs of changes in the quality of display of goods in different stores:
![Site kachestvo](https://files.catbox.moe/d2y8bw.png)



In addition to the bot implemented a whole ecosystem of interaction with users: for activity provides remuneration points. Every week there is a lottery and the number of points ~ the probability of winning. It is also possible to conduct small surveys and promptly receive feedback from customers. 
![Site index](https://files.catbox.moe/56al8q.png)

![Site opros](https://files.catbox.moe/zn9hvb.png)

