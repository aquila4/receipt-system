import app

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

app.config['MAIL_USERNAME'] = 'gmcrealty27@gmail.com'
app.config['MAIL_PASSWORD'] = 'jlhnlhbwingrocpi'
app.config['MAIL_DEFAULT_SENDER'] = 'gmcrealty27@gmail.com'
app.config["SECRET_KEY"] = "receipt-system-super-secret-123"