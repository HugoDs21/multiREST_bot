<p align="center">
    <img src="https://img.shields.io/github/stars/HugoDs21/multiREST_bot?style=social">
    <img src="https://img.shields.io/github/forks/HugoDs21/multiREST_bot?style=social">
    <img src="https://img.shields.io/github/workflow/status/HugoDs21/multiREST_bot/Docker">
</p>
 
# multiREST_bot

Discord bot that informs about the menus of the [Multirest](http://multirest.eu/) restaurants at FCUP and FEUP.

***

## Installation 

You can get this project in two ways:

- cloning the repo
- download one of the releases

### Cloning the repo

1. `git clone https://github.com/HugoDs21/multiREST_bot.git`
1. `cd multiRest_bot`
1. Create an `.env` file like the sample file `.env.sample`
1. `docker-compose up -d`

### Releases

1. Download the latest [release](https://github.com/HugoDs21/multiREST_bot/releases/latest)
2. Rename the folder and remove the version (no need but let's keep it simple)
3. Create an `.env` file like the sample file `.env.sample` inside `multiREST_bot`
4. `docker-compose up -d`

## Usage

- Default prefix is `!`
- Use commands `multirest` and `mr` to interact with the bot
- Restaurantes available - `fcup`, `feup` 
- **Help** - `!mr help`
- **Today's menu** - `!mr fcup hoje`
- **Tomorrow's menu** - `!mr feup amanha`
- **Weekly menu** - `!mr fcup semana`
- Aliases available - `ajuda, h, sem, hj, am`

# Todo
 - ~~Complete base bot~~
 - ~~Actually dockerize it~~
 - ~~Write a proper README~~
 - Multi-lingual support for erasmus students
 - Be able to specify the date 
