import discord
import threading
import aiosqlite
import logging
import yaml
import pytz
import json
from discord import app_commands
from discord.ext import commands
from flask import Flask, session, render_template, request, url_for, redirect, abort

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

embed_color = data["General"]["EMBED_COLOR"]

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)
app.secret_key = 'your_secret_key'

async def check_user_credentials(username, password):
    users = {
        'user1': 'password1',
        'user2': 'password2',
        'user3': 'password3'
    }

    if username in users and users[username] == password:
        return True
    else:
        return False

async def is_user_authenticated():
    return session.get('logged_in', False)

@app.route('/', methods=['GET'])
async def home_page():
    return render_template('home.html')

@app.route('/tz/', methods=['GET'])
async def tz_page():
    if not await is_user_authenticated():
        session['next'] = request.path
        return redirect(url_for('login'))
    str = ""
    for x in pytz.all_timezones:
        str = str + f"{x}<br>"
    return str

@app.route('/users/', methods=['GET'])
async def users_list():
    if not await is_user_authenticated():
        session['next'] = request.path
        return redirect(url_for('login'))
    abort(400, description='Missing required parameter "user_id"')

@app.route('/users/<user_id>', methods=['GET'])
async def users_page(user_id):
    if not await is_user_authenticated():
        session['next'] = request.path
        return redirect(url_for('login'))
    db = await aiosqlite.connect('database.db')
    cursor = await db.execute('SELECT * FROM freelancers WHERE freelancer_id=?', (user_id,))
    a = await cursor.fetchone()
    if a is None:
        await db.close()
        abort(404, description=f'"{user_id}" not found')
    else:
        if a[2] == "NULL":
            description = "N/A"
        else:
            description = a[2]
        if a[3] == "NULL":
            portfolio = "N/A"
        else:
            portfolio = a[3]
        if a[4] == "NULL":
            timezone = "N/A"
        else:
            timezone = a[4]
        if a[5] == "NULL":
            paypal = "N/A"
        else:
            paypal = a[5]
        if a[6] == "NULL":
            paypalme = "N/A"
        else:
            paypalme = a[6]
        payload = {
            "description": description,
            "portfolio": portfolio,
            "timezone": timezone,
            "paypal": paypal,
            "paypalme": paypalme
        }
        await db.close()
        json_payload = json.dumps(payload, indent=2, default=str)
        return json_payload

@app.route('/login', methods=['GET', 'POST'])
async def login():
    if request.method == 'POST':
        if await check_user_credentials(request.form['username'], request.form['password']):
            session['logged_in'] = True
            return redirect(session.get('next', url_for('tz_page')))
        else:
            error = 'Invalid username or password'
            return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/logout')
async def logout():

    session.clear()
    return redirect(url_for('login'))

def run_flask():
    app.run(host='0.0.0.0', port=2000)

class APICog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="api", description="Checks the status of the API!")
    @app_commands.default_permissions(administrator=True)
    async def api(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(description="Running!", color=discord.Color.from_str(embed_color))
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(APICog(bot))

flask_thread = threading.Thread(target=run_flask)
flask_thread.start()