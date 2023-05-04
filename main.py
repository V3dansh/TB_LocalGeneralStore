import telebot
from telebot.types import Message
from typing import List, Tuple

#initialize the bot
API_KEY = '6236712239:AAH56r1k6uDKwE5kPNBqWkcxKuAT8v2-7us'
# define the bot and start the connection
bot = telebot.TeleBot(API_KEY)
#Checking the connection
if(bot):
        print("Connection established")
else:
    print("Connection Failed")

#starting the bot
@bot.message_handler(commands=['start'])
def start_handler(message:Message)->None:
    print("Bot is live")
    storeStart="Welcome to our Local General Store\nClick on below commands to carry on your shopping\n\n /menu-Show Menu\n /add_item_X- Add items to your cart,where X=item numbers\n /cart -View yoour cart\n /checkout -To checkout your itmes in your cart"
    bot.reply_to(message,storeStart)

# define the inventory items as a list of tuples containing item name, price and remaining quantity
inventory_items: List[Tuple[str, float, int]] = [('Item 1', 10.0, 10), ('Item 2', 5.0, 20), ('Item 3', 2.5, 15),
                                                ('Item 4', 7.0, 5), ('Item 5', 12.5, 8), ('Item 6', 8.0, 18),
                                                ('Item 7', 3.5, 12), ('Item 8', 6.0, 3), ('Item 9', 9.0, 6),
                                                ('Item 10', 4.5, 9)]

# define a dictionary to store the user's cart
cart = {}

# define a function to format the inventory items
def format_item(item: Tuple[str, float, int]) -> str:
    return f"{item[0]}\t\t\t\t\t\t\t\t\t\t\t\t${item[1]}\t\t\t\t\t\t\t\t\t{item[2]}"

# define a function to display the inventory to the user
@bot.message_handler(commands=['menu'])
def send_menu(message: Message) -> None:
    menu = "Here's our menu:\n\n"
    menu+="Item_Name\t\t\t\tPrice\t\t\t\t\t\t\tQty\n"
    menu+="---------------------------------------------------\n"
    for item in inventory_items:
        menu += format_item(item) + "\n"
    bot.reply_to(message, menu)

# define a function to add an item to the user's cart
@bot.message_handler(regexp='^/add_item_\d+')
def add_item_to_cart(message: Message) -> None:
    item_index = int(message.text.split('_')[-1])
    item = inventory_items[item_index-1]
    if item[2] == 0:
        bot.reply_to(message, "Sorry, this item is out of stock.")
    else:
        if message.chat.id not in cart:
            cart[message.chat.id] = {}
        if item_index not in cart[message.chat.id]:
            cart[message.chat.id][item_index] = 0
        if item[2] - cart[message.chat.id][item_index] <= 0:
            bot.reply_to(message, "Sorry, you can't order more of this item.")
        else:
            cart[message.chat.id][item_index] += 1
            bot.reply_to(message, f"{item[0]} added to cart.")

# define a function to remove an item from the user's cart
@bot.message_handler(regexp='^/remove_item_\d+')
def remove_item_from_cart(message: Message) -> None:
    item_index = int(message.text.split('_')[-1])
    if message.chat.id not in cart or item_index not in cart[message.chat.id]:
        bot.reply_to(message, "This item is not in your cart.")
    else:
        cart[message.chat.id][item_index] -= 1
        if cart[message.chat.id][item_index] == 0:
            del cart[message.chat.id][item_index]
        item = inventory_items[item_index]
        bot.reply_to(message, f"{item[0]} removed from cart.")

# define a function to display the user's cart
@bot.message_handler(commands=['cart'])
def show_cart(message: Message) -> None:
    if message.chat.id not in cart or not cart[message.chat.id]:
        bot.reply_to(message, "Your cart is empty.")
    else:
        total_price = 0
        checkout_items = "Here's your order:\n\n"
        checkout_items+="Qty\t\t\t\tItem\t\t\t\tPrice\n"
        checkout_items+="-----------------------------------\n"
        for item_index, quantity in cart[message.chat.id].items():
            item = inventory_items[item_index-1]
            item_total_price = item[1] * quantity
            total_price += item_total_price
            checkout_items += f"{quantity}\t\t\t\t\t\t{item[0]}\t\t\t\t\t${item_total_price}\n"
            inventory_items[item_index-1] = (item[0], item[1], item[2] - quantity)
        checkout_items += f"\nTotal price: ${total_price}"
        bot.reply_to(message, checkout_items)

#define a function to check out the user's cart
@bot.message_handler(commands=['checkout'])
def checkout_cart(message: Message) -> None:
    if message.chat.id not in cart or not cart[message.chat.id]:
        bot.reply_to(message, "Your cart is empty.")
    else:
        total_price = 0
        checkout_items = "Your order:\n\n"
        checkout_items+="Qty\t\t\t\tItem\t\t\t\tPrice\n"
        checkout_items+="-----------------------------------\n"
        for item_index, quantity in cart[message.chat.id].items():
            item = inventory_items[item_index-1]
            item_total_price = item[1] * quantity
            total_price += item_total_price
            checkout_items += f"{quantity}\t\t\t\t\t\t{item[0]}\t\t\t\t\t${item_total_price}\n"
            inventory_items[item_index-1] = (item[0], item[1], item[2] - quantity)
        checkout_items += f"\nTotal price: ${total_price}"
        checkout_items+="\nThank you for shopping, Have a nice day"
        del cart[message.chat.id]
        bot.reply_to(message, checkout_items)

#start the bot
bot.polling()
print("Bot has stopped")