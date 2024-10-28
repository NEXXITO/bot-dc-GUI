import customtkinter as ctk
from tkinter import messagebox
import discord
from discord.ext import commands
import threading
import requests
#MADE BY DARKLINCA & NEXX

TOKEN = ""
intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Funciones de acciones principales
async def kick_user_discord(user_id):
    guild = bot.guilds[0]
    member = guild.get_member(int(user_id))
    if member:
        await member.kick(reason="Kickeado desde la interfaz")
        messagebox.showinfo("Kickear Usuario", f"Usuario {user_id} ha sido kickeado.")
    else:
        messagebox.showwarning("Error", "Usuario no encontrado.")

async def ban_user_discord(user_id):
    guild = bot.guilds[0]
    member = guild.get_member(int(user_id))
    if member:
        await member.ban(reason="Baneado desde la interfaz")
        messagebox.showinfo("Banear Usuario", f"Usuario {user_id} ha sido baneado.")
    else:
        messagebox.showwarning("Error", "Usuario no encontrado.")

async def unban_user_discord(user_id):
    guild = bot.guilds[0]
    user = await bot.fetch_user(int(user_id))
    if user:
        await guild.unban(user, reason="Desbaneado desde la interfaz")
        messagebox.showinfo("Desbanear Usuario", f"Usuario {user_id} ha sido desbaneado.")
    else:
        messagebox.showwarning("Error", "Usuario no encontrado.")

async def send_private_message_discord(user_id, message):
    user = await bot.fetch_user(int(user_id))
    if user:
        await user.send(message)
        messagebox.showinfo("Enviar Mensaje", f"Mensaje enviado a {user_id}.")
    else:
        messagebox.showwarning("Error", "Usuario no encontrado.")

async def send_message_to_channel(channel_id, message):
    channel = bot.get_channel(int(channel_id))
    if channel:
        await channel.send(message)
        messagebox.showinfo("Enviar Mensaje a Canal", f"Mensaje enviado al canal {channel_id}.")
    else:
        messagebox.showwarning("Error", "Canal no encontrado.")

# Generador de embeds
async def send_custom_embed(webhook_url, title, description, color, avatar_url, footer_text, footer_url):
    embed = {
        "title": title,
        "description": description,
        "color": color,
        "footer": {
            "text": footer_text,
            "icon_url": footer_url
        },
        "thumbnail": {
            "url": avatar_url
        }
    }

    data = {
        "embeds": [embed]
    }

    response = requests.post(webhook_url, json=data)
    
    if response.status_code == 204:
        messagebox.showinfo("Enviar Embed", f"Embed enviado correctamente al webhook.")
    else:
        messagebox.showwarning("Error", f"No se pudo enviar el embed. Código de error: {response.status_code}")

# Ejecutar acción seleccionada
def ejecutar_accion():
    user_id = entry_user_id.get()
    channel_id = entry_channel_id.get()
    action = action_var.get()
    
    if action == "Kickear":
        if user_id:
            bot.loop.create_task(kick_user_discord(user_id))
        else:
            messagebox.showwarning("Error", "Por favor, ingresa una ID de usuario.")
    elif action == "Banear":
        if user_id:
            bot.loop.create_task(ban_user_discord(user_id))
        else:
            messagebox.showwarning("Error", "Por favor, ingresa una ID de usuario.")
    elif action == "Unbanear":
        if user_id:
            bot.loop.create_task(unban_user_discord(user_id))
        else:
            messagebox.showwarning("Error", "Por favor, ingresa una ID de usuario.")
    elif action == "Mensaje Privado":
        message = entry_message.get()
        if user_id and message:
            bot.loop.create_task(send_private_message_discord(user_id, message))
        else:
            messagebox.showwarning("Error", "Por favor, ingresa una ID de usuario y un mensaje.")
    elif action == "Mensaje a Canal":
        message = entry_message.get()
        if channel_id and message:
            bot.loop.create_task(send_message_to_channel(channel_id, message))
        else:
            messagebox.showwarning("Error", "Por favor, ingresa una ID de canal y un mensaje.")
    elif action == "Generar Embed":
        open_embed_generator()
    else:
        messagebox.showwarning("Error", "Acción no reconocida.")

# Generador de embeds (ventana)
def open_embed_generator():
    embed_window = ctk.CTkToplevel(app)
    embed_window.title("Generador de Embed")
    embed_window.geometry("500x600")

    # Campos del generador de embeds
    ctk.CTkLabel(embed_window, text="Título del Embed").pack(pady=5)
    entry_title = ctk.CTkEntry(embed_window, width=400)
    entry_title.pack()

    ctk.CTkLabel(embed_window, text="Descripción").pack(pady=5)
    entry_description = ctk.CTkEntry(embed_window, width=400)
    entry_description.pack()

    ctk.CTkLabel(embed_window, text="Color del Embed (en hexadecimal)").pack(pady=5)
    entry_color = ctk.CTkEntry(embed_window, width=400)
    entry_color.insert(0, "#FFD700")  # Ejemplo: color dorado
    entry_color.pack()

    ctk.CTkLabel(embed_window, text="Avatar URL").pack(pady=5)
    entry_avatar_url = ctk.CTkEntry(embed_window, width=400)
    entry_avatar_url.pack()

    ctk.CTkLabel(embed_window, text="Footer Text").pack(pady=5)
    entry_footer_text = ctk.CTkEntry(embed_window, width=400)
    entry_footer_text.pack()

    ctk.CTkLabel(embed_window, text="Footer URL").pack(pady=5)
    entry_footer_url = ctk.CTkEntry(embed_window, width=400)
    entry_footer_url.pack()

    ctk.CTkLabel(embed_window, text="URL de Webhook").pack(pady=5)
    entry_webhook_url = ctk.CTkEntry(embed_window, width=400)
    entry_webhook_url.pack()

    def enviar_embed():
        webhook_url = entry_webhook_url.get()
        title = entry_title.get()
        description = entry_description.get()
        
        # Convertir el color de hexadecimal a decimal
        color_hex = entry_color.get().lstrip('#')
        color = int(color_hex, 16) if color_hex else 0xFFD700  # Por defecto, dorado

        avatar_url = entry_avatar_url.get()
        footer_text = entry_footer_text.get()
        footer_url = entry_footer_url.get()
        
        if webhook_url:
            bot.loop.create_task(send_custom_embed(webhook_url, title, description, color, avatar_url, footer_text, footer_url))
            embed_window.destroy()
        else:
            messagebox.showwarning("Error", "Por favor, ingresa una URL de Webhook.")
    
    # Botón para enviar el embed
    ctk.CTkButton(embed_window, text="Enviar Embed", command=enviar_embed, fg_color="purple").pack(pady=20)


# Configuración de la interfaz principal
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Gestión de Usuarios")
app.geometry("450x500")

# ID del Usuario
ctk.CTkLabel(app, text="ID del Usuario", font=("Arial", 14)).pack(pady=5)
entry_user_id = ctk.CTkEntry(app, width=250)
entry_user_id.pack(pady=5)

# ID del Canal (solo para enviar mensajes a canales)
ctk.CTkLabel(app, text="ID del Canal", font=("Arial", 14)).pack(pady=5)
entry_channel_id = ctk.CTkEntry(app, width=250)
entry_channel_id.pack(pady=5)

# Menú de selección de acción
action_var = ctk.StringVar(value="Kickear")
ctk.CTkOptionMenu(app, values=["Kickear", "Banear", "Unbanear", "Mensaje Privado", "Mensaje a Canal", "Generar Embed"], variable=action_var).pack(pady=5)

# Campo para mensaje
entry_message = ctk.CTkEntry(app, width=250)
entry_message.pack(pady=5)
entry_message.insert(0, "Escribe el mensaje aquí...")

# Botón para ejecutar la acción seleccionada
ctk.CTkButton(app, text="Ejecutar Acción", command=ejecutar_accion, fg_color="purple").pack(pady=20)

# Función para correr el bot
def run_bot():
    bot.run(TOKEN)
# Añadir copyright en la parte inferior de la ventana principal
ctk.CTkLabel(app, text="© DarKlinca Services", font=("Arial", 10), fg_color="transparent").pack(side="bottom", pady=10)

# Ejecutar bot en un hilo
threading.Thread(target=run_bot).start()
app.mainloop()
