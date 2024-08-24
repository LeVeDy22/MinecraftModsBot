import os
import json
import asyncio
from dotenv import load_dotenv
from aiogram.fsm.context import FSMContext
from aiogram import Bot, Dispatcher, F, types
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import CommandStart, Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

load_dotenv()
BOT_TOKEN = os.getenv('TOKEN')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

PATHS = {
    'all': 'C:\\Users\\Professional\\Desktop\\Python\\MyBots\\MyFirstBot\\all_mods\\mods',
    'forge': 'C:\\Users\\Professional\\Desktop\\Python\\MyBots\\MyFirstBot\\all_mods\\mods_forge',  
    'fabric': 'C:\\Users\\Professional\\Desktop\\Python\\MyBots\\MyFirstBot\\all_mods\\mods_fabric'
}

keyboard_start = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Start working with the bot / Почати роботу з ботом')]],
                                        resize_keyboard=True,
                                        input_field_placeholder='Waiting... / Чекаємо...')

@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Welcome to the bot "Minecraft Mods"! This bot is able to issue popular mods according to the given parameters. / Ласкаво просимо до боту "Майнкрафт моди"! Цей бот вміє видавати популярні моди по заданим параметрам.', reply_markup=keyboard_start)

@dp.message(F.text == 'Start working with the bot / Почати роботу з ботом')
async def start(message: Message):
    await message.answer('You started working with the bot. / Ви почали роботу з ботом.', reply_markup=types.ReplyKeyboardRemove())

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='All loaders / Усі навантажувачі', callback_data='loader_mods')],
        [InlineKeyboardButton(text='Forge / Фордж', callback_data='loader_forge')],
        [InlineKeyboardButton(text='Fabric / Фабрік', callback_data='loader_fabric')]
])
     
    await message.answer('Select loader: / Виберіть навантажувач:', reply_markup=keyboard)

@dp.callback_query(lambda c: c.data and c.data.startswith('loader_')) 
async def handle_loader(callback_query: types.CallbackQuery): 
    global loader
    loader = callback_query.data.split('_')[1]

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='All categories / Усі категорії', callback_data='category_all'), InlineKeyboardButton(text='Adventure / Пригоди', callback_data='category_adventure')],
        [InlineKeyboardButton(text='Decoration / Прикраси', callback_data='category_decoration'), InlineKeyboardButton(text='Food / Їжа', callback_data='category_food'),
        InlineKeyboardButton(text='Magic / Магія', callback_data='category_magic')],
        [InlineKeyboardButton(text='Mobs / Моби', callback_data='category_mobs'), InlineKeyboardButton(text='Optimization / Оптимізація', callback_data='category_optimization'),
        InlineKeyboardButton(text='Storage / Сховище', callback_data='category_storage')],
        [InlineKeyboardButton(text='Technology / Технології', callback_data='category_technology'), InlineKeyboardButton(text='Transportation / Транспорт', callback_data='category_transportation'),
        InlineKeyboardButton(text='World Generetion / Генерація світу', callback_data='category_worldgen')]
])
    
    
    await bot.send_message(callback_query.from_user.id, 'Select category: / Виберіть категорію:', reply_markup=keyboard)
        
@dp.callback_query(lambda c: c.data and c.data.startswith('category_')) 
async def handle_category(callback_query: types.CallbackQuery): 
    global category
    category = callback_query.data.split('_')[1]

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='3', callback_data='quantity_3'), InlineKeyboardButton(text='5', callback_data='quantity_5')],
        [InlineKeyboardButton(text='10', callback_data='quantity_10'), InlineKeyboardButton(text='20', callback_data='quantity_20')],
        [InlineKeyboardButton(text='50', callback_data='quantity_50'), InlineKeyboardButton(text='100', callback_data='quantity_100')],
])

    await bot.send_message(callback_query.from_user.id, f'Select the number of mods: / Виберіть кількість модів:', reply_markup=keyboard)

@dp.callback_query(lambda c: c.data and c.data.startswith('quantity_')) 
async def handle_year(callback_query: types.CallbackQuery):
    global quantity
    quantity = int(callback_query.data.split('_')[1])

    file = f'{category}_{loader}.json'
    if loader == 'mods':
        os.chdir('mods')
    else:
        os.chdir(f'mods_{loader}')

    with open(file, 'r', encoding='utf-8') as json_file: 
        mods = json.load(json_file)
                
        for i in range(quantity):
            mod = mods['mods'][i]
            await bot.send_photo(callback_query.from_user.id,
                f'{mod['image']}',
                caption=f'{mod['name']}\n\n{mod['description']}\n\nDownloads: {mod['downloads']}\nFollowers: {mod['followers']}\n\nLink: {mod['link']}')

    os.chdir('..')

    if quantity != 3:            
        await bot.send_message(callback_query.from_user.id, f'Top {quantity} mods in this category are listed. / Топ {quantity} модів цієї категорії виведено', reply_markup=keyboard_start)
    else:
        await bot.send_message(callback_query.from_user.id, f'Top {quantity} mods in this category are listed. / Топ {quantity} моди цієї категорії виведено', reply_markup=keyboard_start)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('The bot is disabled.')