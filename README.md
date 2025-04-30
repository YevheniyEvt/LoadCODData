# Script to collect data in the game Call of Dragons
- Since Call of Dragons does not have an API, I wrote a script that scans🥢 the screen and stores the data in a database.📃
## How it work
- The script takes a screenshot of the screen.
- Then pytesseract scans the screenshot.
- Using alembic creat tables in a PostgreSQL database.
- With SQLAlchemy save that data.
  
#### This project was developed for educational👨‍🎓 purposes and is in the testing stage.
*Сurrently has no graphical interface. Information is output to the terminal and stored in a database*
