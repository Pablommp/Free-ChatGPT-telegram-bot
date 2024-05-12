from config import TELEGRAM_TOKEN
import telebot
from g4f.client import Client
from telebot import apihelper
from telebot import types 
import requests
import threading
import html
import re

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = Client()
user_versions = {} 
user_language = {}
version = "1.2.3"
tu_id = "-1002046951065"

def chatbot_response(user_input, user_id):
    if user_id in user_versions:
        current_version = user_versions[user_id]
    else:
        current_version = "5"
    if current_version == "3.5":
        model = "gpt-3.5-turbo"
    elif current_version == "4":
        model = "gpt-4"
    elif current_version == "5":
        model = "gpt-4-turbo"
    else:
        model = "gpt-4-turbo"
        
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": user_input}]
    )
    return response.choices[0].message.content

# dar formato a los mensajes
def format_code_blocks(text):
    
    code_blocks = re.findall(r'```(.*?)```', text, re.DOTALL)
    
    for block in code_blocks:
        code = html.escape(block.strip())
        text = text.replace(f'```{block}```', f'<pre><code>{code}</code></pre>')
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)

    text = re.sub(r'`(.*?)`', r'<code>\1</code>', text)

    return text

@bot.message_handler(content_types=["photo"])
def bot_mensajes_imagen(message):
    global user_language
    user_id = message.from_user.id  
    if user_id in user_language:
        language = user_language[user_id]
    else:
        language = "english"
    if language == "spanish":
        bot.send_message(message.chat.id, "Lo siento de momento no tengo la capacidad de analizar imagenes :(")
    else:
        bot.send_message(message.chat.id, "Sorry, but I don't have the capability to analyze images at the moment.")
    log(message)
# comandos
@bot.message_handler(commands=["start"])
def cmd_start(message):
    global user_language
    user_id = message.from_user.id  
    if user_id in user_language:
        language = user_language[user_id]
    else:
        language = "english"
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    b1 = types.InlineKeyboardButton(text="Gpt-3.5-turbo ✒", callback_data="version_3.5")
    b2 = types.InlineKeyboardButton(text="Gpt-4 🧠", callback_data="version_4")
    b3 = types.InlineKeyboardButton(text="Gpt-4-turbo 🧠➕", callback_data="version_5")
    markup.add(b1, b2, b3)
    if language == "spanish":
        bot.reply_to(message, """Hola, Bienvenido a FREE ChatGPT Telegram bot.

FREE chatGPT bot implementa una API pública de los modelos más recientes de ChatGPT.

💌 Para comenzar a hablar con él simplemente escribe lo que quieras, el bot es totalmente gratuito e ilimitado.

🧠 El bot usa la API gpt4free, por lo que las respuestas pueden tardar unos segundos dependiendo de la hora del día y el modelo. 

Para más información y contacto usa 
/info. 

Siempre puedes cambiar de modelo usando /model. 

Si necesitas mas ayuda pon /tutorial""", reply_markup=markup)
    else:
        bot.reply_to(message, """Hello, Welcome to FREE ChatGPT Telegram bot.

FREE chatGPT bot implements a public API of the latest ChatGPT models.

💌 To start chatting with it just type whatever you want, the bot is completely free and unlimited.

🧠 The bot uses the gpt4free API, so responses may take a few seconds depending on the time of day and the model.

For more information and contact use /info.

You can always change the model using /model.

If you need more help, put /tutorial.""", reply_markup=markup)
@bot.message_handler(commands=["help"])
def cmd_start(message):
    global user_language
    user_id = message.from_user.id  
    if user_id in user_language:
        language = user_language[user_id]
    else:
        language = "english"
        
    if language == "spanish":
        bot.reply_to(message, """🚀 Comandos del Bot 🤖 🚀

    "/start" ➡️ Iniciar🌍
    ¡Comienza tu viaje aquí!

    "/help" ➡️ Ayuda🛎
    ¿Necesitas asistencia? ¡Estoy aquí para ayudarte!

    "/info" ➡️ Contacto🧭
    ¿Quieres saber más sobre nosotros? ¡Contáctanos aquí!

    "/model" ➡️ Modelo⚙
    Cambia de modelo de IA.

    "/tutorial" ➡️ Tutorial📖
    ¡Aprende cómo sacar el máximo provecho de nuestro bot con nuestro tutorial!

    "/language" ➡️ Opciones de idioma🌐
    Cambia de idioma facilmente.""")
    else:
        bot.reply_to(message, f"""🚀 Bot Commands 🤖 🚀

    "/start" ➡️ Start🌍
    Begin your journey here!

    "/help" ➡️ Help🛎
    Need assistance? I'm here to help!

    "/info" ➡️ Contact🧭
    Want to know more about us? Contact us here!

    "/model" ➡️ Model⚙
    Change AI model.

    "/tutorial" ➡️ Tutorial📖
    Learn how to get the most out of our bot with our tutorial!

    "/language" ➡️ Language Settings🌐
    Set your preferred language.""")
@bot.message_handler(commands=["info"])
def cmd_start(message):
    global user_language
    user_id = message.from_user.id  
    if user_id in user_language:
        language = user_language[user_id]
    else:
        language = "english"
        
    if language == "spanish":
        bot.reply_to(message, f"Este bot es la versión {version}\n\nGithub: https://github.com/PabloMarpen\n\nTelegram: https://t.me/Void_1212\n\nIA API: https://github.com/xtekky/gpt4free")
    else:
        bot.reply_to(message, f"This bot is the version {version}\n\nGithub: https://github.com/PabloMarpen\n\nTelegram: https://t.me/Void_1212\n\nIA API: https://github.com/xtekky/gpt4free")

@bot.message_handler(commands=["model", "version"])
def cmd_start(message):
    global user_language
    user_id = message.from_user.id  
    if user_id in user_language:
        language = user_language[user_id]
    else:
        language = "english"
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    b1 = types.InlineKeyboardButton(text="Gpt-3.5-turbo ✒", callback_data="version_3.5")
    b2 = types.InlineKeyboardButton(text="Gpt-4 🧠", callback_data="version_4")
    b3 = types.InlineKeyboardButton(text="Gpt-4-turbo 🧠➕", callback_data="version_5")
    markup.add(b1, b2, b3)
    if language == "spanish":
        bot.reply_to(message, "🤖 ¿Quieres cambiar de version? 🤖", reply_markup=markup)
    else:
        bot.reply_to(message, "🤖 Do you want to change the version? 🤖", reply_markup=markup)
    
@bot.message_handler(commands=["tutorial"])
def cmd_start(message):
    global user_language
    user_id = message.from_user.id  
    if user_id in user_language:
        language = user_language[user_id]
    else:
        language = "english"
    
    gif_path = "../static/tuto.gif"
    gif_file = open(gif_path, "rb")
    bot.send_document(message.chat.id, gif_file)
    if language == "spanish":
        bot.reply_to(message, "Bienvenido al Tutorial de Uso de FREE ChatGPT Telegram Bot\n\n¡Hola! Gracias por usar el bot de Telegram FREE ChatGPT. Este bot te permite interactuar con modelos de inteligencia artificial para generar respuestas basadas en tus entradas. A continuación, te mostraré cómo utilizar algunas de las funciones básicas del bot.\n\nResponder a Mensajes Anteriores:\n\nPara responder a un mensaje anterior, simplemente menciona el mensaje arrastrándolo hacia la izquierda y luego escribes tu respuesta. El bot detectará automáticamente a qué mensaje estás respondiendo y generará una respuesta en consecuencia.\n\nComandos Básicos:\n\n1. /model: Este comando te permite cambiar el modelo de inteligencia artificial que el bot está utilizando. Puedes elegir entre diferentes versiones del modelo, como GPT-3.5, GPT-4, y GPT-4 Turbo. Una vez que ejecutes el comando, el bot te proporcionará opciones para seleccionar el modelo deseado.\n\n2. /info: Con este comando, puedes obtener información sobre el bot, su versión y el creador. Además, también puedes obtener detalles sobre la API de inteligencia artificial que el bot utiliza. Simplemente ejecuta el comando y el bot te proporcionará la información solicitada.\n\nOtros Comandos:\n\n- /changelog: Este comando te permite ver los cambios recientes en el bot, como nuevas características añadidas o correcciones de errores. Siempre es útil estar al tanto de las actualizaciones del bot.\n\n¡Y eso es todo! Ahora estás listo para comenzar a usar el bot y disfrutar de conversaciones interesantes con la inteligencia artificial. Si tienes alguna pregunta o necesitas ayuda adicional, no dudes en ponerte en contacto con el creador del bot.\n\n¡Gracias por usar el bot de Telegram FREE ChatGPT!")
    else:
        bot.reply_to(message, """Welcome to the FREE ChatGPT Telegram Bot Usage Tutorial

Hello! Thank you for using the FREE ChatGPT Telegram bot. This bot allows you to interact with artificial intelligence models to generate responses based on your inputs. Below, I will show you how to use some of the basic functions of the bot.

Replying to Previous Messages:

To reply to a previous message, simply mention the message by swiping it to the left and then write your response. The bot will automatically detect which message you are responding to and generate a response accordingly.

Basic Commands:

/model: This command allows you to change the artificial intelligence model that the bot is using. You can choose between different versions of the model, such as GPT-3.5, GPT-4, and GPT-4 Turbo. Once you execute the command, the bot will provide you with options to select the desired model.

/info: With this command, you can get information about the bot, its version, and the creator. Additionally, you can also get details about the artificial intelligence API that the bot uses. Simply execute the command and the bot will provide you with the requested information.

Other Commands:

/changelog: This command allows you to view recent changes in the bot, such as new features added or bug fixes. It's always useful to stay informed about the bot's updates.
And that's it! Now you're ready to start using the bot and enjoy interesting conversations with artificial intelligence. If you have any questions or need additional help, feel free to contact the bot's creator.

Thank you for using the FREE ChatGPT Telegram bot!""")

@bot.callback_query_handler(func=lambda call: call.data.startswith("version_"))
def callback_query(call):
    global user_language
    user_id = call.from_user.id  
    if user_id in user_language:
        language = user_language[user_id]
    else:
        language = "english"
        
    version = call.data.split("_")[1]  # Extraer la versión seleccionada
    user_id = call.from_user.id
    user_versions[user_id] = version  # Asignar la versión seleccionada al usuario
    if version == "3.5":
        if language == "spanish":
            bot.send_message(call.message.chat.id, """Se ha seleccionado la versión gpt 3.5 ✒️

🚅 Velocidad:     🟢🟢🟢⚪️

🧠 Inteligencia:  🟢🟢⚪️⚪️""")
        else:
          bot.send_message(call.message.chat.id, """Version gpt 3.5 has been selected ✒️

🚅 Speed: 🟢🟢🟢⚪️

🧠 Intelligence: 🟢🟢⚪️⚪️""")
    elif version == "4":
        if language == "spanish":
            bot.send_message(call.message.chat.id, """Se ha seleccionado la versión gpt 4 🧠

🚅 Velocidad:     🟢🟢⚪️⚪️

🧠 Inteligencia:  🟢🟢🟢⚪️""")
        else:
            bot.send_message(call.message.chat.id, """Version gpt 4 has been selected 🧠

🚅 Speed: 🟢🟢⚪️⚪️

🧠 Intelligence: 🟢🟢🟢⚪️""")
    elif version == "5":
        if language == "spanish":
            bot.send_message(call.message.chat.id, """Se ha seleccionado la version gpt 4 turbo 🧠➕

🚅 Velocidad:     🟢🟢⚪️⚪️

🧠 Inteligencia:  🟢🟢🟢🟢""")
        else:
            bot.send_message(call.message.chat.id, """Version gpt 4 turbo has been selected 🧠➕

🚅 Speed: 🟢🟢⚪️⚪️

🧠 Intelligence: 🟢🟢🟢🟢""")
@bot.message_handler(commands=["language"])
def cmd_start(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    b1 = types.InlineKeyboardButton(text="spanish 🇪🇸", callback_data="language_spanish")
    b2 = types.InlineKeyboardButton(text="english 🇬🇧", callback_data="language_english")
    markup.add(b1, b2)
    bot.reply_to(message, "Select your language", reply_markup=markup)
    
@bot.callback_query_handler(func=lambda call: call.data.startswith("language_"))
def callback_query(call):
    global user_language
    language = call.data.split("_")[1]  # Extraer el idioma seleccionado
    user_id = call.from_user.id
    
    user_language[user_id] = language
        
    if language == "spanish":
        bot.send_message(call.message.chat.id, "🇪🇸 Se ha seleccionado Español 🇪🇸") 
    elif language == "english":
        bot.send_message(call.message.chat.id, "🇬🇧 You selected English 🇬🇧")
                
# API https://github.com/eternnoir/pyTelegramBotAPI
# Función para manejar las solicitudes de los usuarios
def handle_message(message):
    global user_language
    user_id = message.from_user.id  
    if user_id in user_language:
        language = user_language[user_id]
    else:
        language = "english"
    
    if message.reply_to_message:  
        handle_reply(message)  
    elif message.text.startswith("/"):
        if language == "spanish":
            bot.send_message(message.chat.id, "Eso es un comando, que aún no existe.")
        else:
            bot.send_message(message.chat.id, "That command doesn't exist yet.")
    else:
        if language == "spanish":
            temp_message = bot.send_message(message.chat.id, "⏳ Generando respuesta... ⏳\n\n⚠ Este proceso puede tardar entre 2 segundos a 1 minuto ⚠", disable_notification=True)
        else:
            temp_message = bot.send_message(message.chat.id, "⏳ Generating response... ⏳\n\n⚠ This process may take between 2 seconds to 1 minute ⚠", disable_notification=True)
      
        try:
   
            respuesta = chatbot_response(message.text, user_id) 

            respuesta_formateada = format_code_blocks(respuesta)

            bot.edit_message_text(
                chat_id=temp_message.chat.id, 
                message_id=temp_message.message_id, 
                text=respuesta_formateada,
                reply_markup=None, 
                disable_web_page_preview=True,
                parse_mode="HTML" 
            )
            log(message)

        except apihelper.ApiTelegramException as e:
            if language == "spanish":
                bot.send_message(message.chat.id, "No se pudo generar tu prompt por un error inesperado")
            else:
                bot.send_message(message.chat.id, "Couldn't generate your prompt due to an unexpected error.")
            print("Error al enviar el mensaje a Telegram:", e)

# función para manejar los mensajes a los que se responde
def handle_reply(message):
    global user_language
    user_id = message.from_user.id  
    if user_id in user_language:
        language = user_language[user_id]
    else:
        language = "english"
        
    if language == "spanish":
        temp_message = bot.send_message(message.chat.id, "⏳ Generando respuesta... ⏳\n\n⚠ Este proceso puede tardar entre 2 segundos a 1 minuto ⚠", disable_notification=True)
    else:
        temp_message = bot.send_message(message.chat.id, "⏳ Generating response... ⏳\n\n⚠ This process may take between 2 seconds to 1 minute ⚠", disable_notification=True)
       
    user_input = message.reply_to_message.text
    bot_input = message.text
    # Combinar los dos mensajes en un solo mensaje
    combined_message = f"{bot_input} {user_input}"
   
    user_id = message.reply_to_message.from_user.id  
    respuesta = chatbot_response(combined_message, user_id)

    try:
        # Formatear bloques de código y texto en negrita
        respuesta_formateada = format_code_blocks(respuesta)

        bot.edit_message_text(
            chat_id=temp_message.chat.id, 
            message_id=temp_message.message_id, 
            text=respuesta_formateada, 
            reply_markup=None, 
            disable_web_page_preview=True,
            parse_mode="HTML"  # Usar HTML como formato
        )
        log(message)
    except apihelper.ApiTelegramException as e:
        # Manejo de la excepción aquí
        if language == "spanish":
            bot.send_message(message.chat.id, "No se pudo generar tu prompt por un error inesperado")
        else:
            bot.send_message(message.chat.id, "Couldn't generate your prompt due to an unexpected error.")
        print("Error al enviar el mensaje a Telegram:", e) 

@bot.message_handler(content_types=["text"])
def bot_mensajes_texto(message):
    thread = threading.Thread(target=handle_message, args=(message,))
    thread.start()

@bot.message_handler(func=lambda message: True)
def log(message):
    bot.forward_message(chat_id=tu_id, from_chat_id=message.chat.id, message_id=message.message_id)

# MAIN ############################################
if __name__ == '__main__':
    bot.set_my_commands([

        telebot.types.BotCommand("/start", "Start🤖"),
        telebot.types.BotCommand("/help", "Help 🛎"),
        telebot.types.BotCommand("/info", "Contact 🧭"),
        telebot.types.BotCommand("/model", "Model ⚙"),
        telebot.types.BotCommand("/tutorial", "Tutorial 📖"),
        telebot.types.BotCommand("/language", "language 🌍")
    ])
    print('iniciando el bot')
    bot.infinity_polling()
    print('apagando el bot')
