## Commit Monitor Bot
bot than monitors new commits in the specified repository, and notifies via Telegram

## Setup

### Configuring Bot

The fist step is cheat a telegram Bot, to learn how creat acess (this link)

## Usage 
### Runing commit-Bot.py

After the creating of a Telegram Bot, you must run commit-Bot.py in a python interpreter with your Token, and install all library

![token](https://user-images.githubusercontent.com/72465364/112782518-9a2fa180-9023-11eb-8103-214635b5c55d.jpg)


## Using commands 

commands that can be used to speak the bot

| command  | description | how to use |
| -------- |------------ | ---------- |
| /subscribe | This command is used to start monitor a repository | **/subscribe aconut_name repository_name branch_name**|
| /unsubscribe | Used to stop monitoring a repository | ** /unsubscribe /subscribe aconut_name repository_name** |
| /sleep | Used to specify how often to check the repository, default 10 seconds | /sleep seconds in intereble | 
| /list | Show all repository beingn monitored | /list |
| /menu | Show the menu | /menu |

### Monitor a repository 

![photo_2021-03-29_00-22-25](https://user-images.githubusercontent.com/72465364/112783100-e3ccbc00-9024-11eb-8418-f2e1bae0c196.jpg)

---

![retorno](https://user-images.githubusercontent.com/72465364/112782659-eda1ef80-9023-11eb-8421-f8c79e6ed11e.jpg)


### [full code](https://github.com/wesley587/checking_commitBot/blob/main/Commit-Bot.py)
