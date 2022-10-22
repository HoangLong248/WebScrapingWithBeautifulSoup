from bs4 import BeautifulSoup
import requests
import telebot
import json

with open('config.json', 'r') as config_file:
# config_file = open('config.json', 'r')
    token = json.loads(config_file.read())['token']
# config_file.close()
print(token)

bot = telebot.TeleBot("{}".format(token), parse_mode=None) # You can set parse_mode by default. HTML or MARKDOWN

def scraping_data_from_web():
    resp = requests.get("https://ngoctham.com/bang-gia-vang/")
    html = resp.text

    # Write data from response to file
    with open("data.html", 'w', encoding='utf-8') as file:
        file.write(html)

    # Read data from file
    with open("data.html", 'r', encoding='utf-8') as file:
        content = file.read()

        soup = BeautifulSoup(content, 'lxml')
        div_gole_price_page = soup.find_all('div', id="gold-price-page")

        for div_gold_price in div_gole_price_page:
            clean_data = []
            for data in div_gold_price.table.tbody.text.split("\n\n"):
                if data:
                    clean_data.append(data.replace('\n', ';'))
    return clean_data

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "{}".format(scraping_data_from_web()))

if __name__ == "__main__":
    bot.infinity_polling()