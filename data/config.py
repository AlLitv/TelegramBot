import os # работа с Операционной системой


from dotenv import load_dotenv


load_dotenv()


BOT_TOKEN = str(os.getenv('BOT_TOKEN'))


admin_id = [
    864770563,
   # 448768892
]


teacher = 864770563

stiker_id = {
    'start_stiker' : 'CAACAgIAAxkBAAEEjcNiZiMoSTQ4-OE5I0imypxWbNTEygACxxgAArfUeElKxssIBSHQXiQE',
    'help_stiker' : 'CAACAgIAAxkBAAEEjcViZiXBB_Qm6YVxwB7o5aO26sEeTwAC_BQAArLFeEnpVEZYfRxtfiQE'
}