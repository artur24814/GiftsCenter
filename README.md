# GiftsCenter
<hr>

<img src="https://res.cloudinary.com/practicaldev/image/fetch/s--yfF3_q8k--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://thepracticaldev.s3.amazonaws.com/i/f0i5oszdj3gwk686xuc0.JPG">

## Contents
 * <a href="#info"><strong>Info</strong></a><p>Information about the resources used in this project</p>
 * <a href="#GiftsCenter"><strong>GiftsCenter</strong></a><p>gift list website</p>
 * <a href="#clone_project"><strong>Clone and Run a Flask Project</strong></a><p>how run projects in your computer</p>

<hr>

<details><summary id="info" style="font-size: 30px;"> INFO</summary>
<h4>Information about the additional library, external Api used in this project and general information</h4>

<strong>Flask</strong>  is a web framework.

<strong>Pillow</strong> The Python Imaging Library adds image processing capabilities to your Python interpreter.

<strong>pytest</strong> For testing application.

<strong>python-dotenv</strong> For reads key-value pairs from a .env file and can set them as environment variables. 

<strong>Psycopg2binary</strong> Psycopg is the most popular PostgreSQL database adapter for the Python programming language. 

<strong>Flask-Mail</strong> The Flask-Mail extension provides a simple interface to set up SMTP with your Flask application and to send messages from your views and scripts.

</details>

<hr>
<center><h1 id="GiftsCenter"> GiftsCenter <span style='font-size:80px;'><img src="https://img.icons8.com/external-smashingstocks-outline-color-smashing-stocks/66/null/external-gifts-shopping-smashingstocks-outline-color-smashing-stocks.png"/></span></h1></center>

### You have an important celebration and, as usual, you expect that your guests bring some nonsense 🤬 as a gift? <br> Or you're going to a party you don't know what to buy for a gift 🤯?

#### That's why the sites like this exists. I present my version written with  using python framework 'Flask' 

You must have an account for normal work on this site. Without it, on this site you can only search for users and actions, but you will not create your own actions or participate in actions.

<img src="https://user-images.githubusercontent.com/97242088/208264559-f97760c6-b175-48d0-9e2b-b2cac4bbf72f.png" width="600" height="150">
<img src="https://user-images.githubusercontent.com/97242088/208264558-9605ce05-c0ee-4181-b2bb-1b85761ae1dd.png" width="600" height="150">

Once you have an account, you can search for a friend or the action itself, but in our case, we will first search for our friend, just enter a few letters from his name.

<img src="https://user-images.githubusercontent.com/97242088/208264803-0ee72dec-a308-49f4-be51-118da3256169.png" width="1000" height="250">

If you found him, click 'add friend'. But now you can't take part in all his actions yet, it would be strange if you can take part in all actions to which you are not invited, wouldn't it 🤪?<br>
Now he should make his move.

If he accepts you as a friend next he will go into his action and select you and press 'add' and now you are officially invited to the party. Now you will receive invitations via email.<br>
I use an emulated email server, Python provides one that is very handy that you can start in a second terminal with the following command:

```python -m smtpd -n -c DebuggingServer localhost:8025```

And I can see this message in a terminal

<img src="https://user-images.githubusercontent.com/97242088/208265726-2218e599-2c22-4a1d-8823-5dbcc8f53a27.png">

Now go to this action and choose the gift 🎁 you are going to buy to get ahead of others! 
Now this gift on the website will be marked as checked and others will not be able to choose it (You can't book more than one gift, but if you try you'll get a message saying it can't be done and the item won't be checked). 
Next you will receive an email with a confirmation and a reminder for this gift. Don't worry no one will know what you choose and if you choose anything at all, complete anonymity ⛔️

<img src="https://user-images.githubusercontent.com/97242088/208266001-17c44f32-5957-469a-9f28-da310f8e3c66.png" width="700" height="400">

<img src="https://user-images.githubusercontent.com/97242088/208265593-3e4aa70c-60f8-4a61-98c8-f184c24da387.png" alt="example item chosen" width="500" height="400">

Ok, now we create our action and invite friends, we choose a picture, and date (must be later like today otherwise you will receive a message). You shouldn't choose all your friends at once, you can add them at any time.

<img src="https://user-images.githubusercontent.com/97242088/208266701-f9b45457-fd9e-441a-b685-9ff99cdd8068.png" width="700" height="400">

<img src="https://user-images.githubusercontent.com/97242088/208266711-f1a51d76-872c-4d1b-be29-c2f17d0e3b1c.png" alt="example ms invited" width="500" height="430">

Great, all invited people have received invitations, now you are sure that you will not receive nonsense for a gift wait for guests and have a nice time 🥳.

<center><h2 id="clone_project">Clone and Run a Project</h2></center>

Before diving let’s look at the things we are required to install in our system.

To run Flask prefer to use the Virtual Environment

`pip install virtualenv`

Making and Activating the Virtual Environment:-

`virtualenv “name as you like”`

`source env/bin/activate`

Installing Flask:-

`pip install Flask`

Now, we need to clone project from Github:-
<p>Above the list of files, click Code.</p>
<img src="https://docs.github.com/assets/cb-20363/images/help/repository/code-button.png">

Copy the URL for the repository.
<ul>
<li>To clone the repository using HTTPS, under "HTTPS", click</li>
<li>To clone the repository using an SSH key, including a certificate issued by your organization's SSH certificate authority, click SSH, then click</li>
<li>To clone a repository using GitHub CLI, click GitHub CLI, then click</li>
</ul>
<img src="https://docs.github.com/assets/cb-33207/images/help/repository/https-url-clone-cli.png">

Open Terminal.

Change the current working directory to the location where you want the cloned directory.

Type git clone, and then paste the URL you copied earlier.

`$ git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY`

Press Enter to create your local clone.

```
$ git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY
> Cloning into `Spoon-Knife`...<br>
> remote: Counting objects: 10, done.
> remote: Compressing objects: 100% (8/8), done.
> remove: Total 10 (delta 1), reused 10 (delta 1)
> Unpacking objects: 100% (10/10), done.
```

Install the project dependencies:

`pip install -r requirements.txt`

create `.env` in linux  type `touch .env`

open this file and type (it is information about your postgres user):
```python
DB = 'flask_database'
DB_USER = "Your_user"
DB_PASSWORD = "your_password"
DB_HOST = "127.0.0.1"
```

Connect with database

`flask --app core init-db`

Run local python message server

`python -m smtpd -n -c DebuggingServer localhost:8025`
<hr>

<strong>If you prefer to have emails sent for real, you need to use a real email server.</strong>
If you have one, then you just need to set the MAIL_SERVER, MAIL_PORT, MAIL_USE_TLS, MAIL_USERNAME and MAIL_PASSWORD environment variables for it. 
If you want a quick solution, you can use a Gmail account to send email, type this in `.env`:

```python
MAIL_SERVER='smtp.gmail.com'
MAIL_USERNAME='your_email@gmail.com'
MAIL_PASSWORD='your_password'
```
Next in `core/__init__.py` instead of 
```python
app.config['MAIL_SERVER'] = 'localhost'
app.config['MAIL_PORT'] = 8025
```
type
```python
from dotenv import load_dotenv
import os

load_dotenv()
app.config['MAIL_SERVER']=os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
```
<hr>


to start the development server

`flask --app core --debug run`

and open `127.0.0.1:5000` on your browser to view the app.

run tests type

`pytest`

Have fun
<p style="font-size:100px">&#129409;</p>


