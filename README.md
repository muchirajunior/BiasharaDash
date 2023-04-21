# Biashara Dash
A monolith dashboard 

### user roles
- account user roles
```
    admin | manager | user
```

### installations
- to install all the requirements run the command
```
    pip install -r requiremets.txt
```

### setup and migrate the database
- on main.py file replace with your database connection string
```python
app.config['SQLALCHEMY_DATABASE_URI']="your_database_connection_string"
```
- note this only works with sql databases

- initialize migrations by running following command
```
    flask db init
```
- set up your first migration 

```
    flask db migrate -m "InitialMigration"
```
- update the database
```
    flask db upgrade
```

### create a super/admin user
- to create admin user run following command. replace admin and 1234 with your username and password
```
    python config.py --email admin@mail.com --password 1234
```

### Adding models
- add your model to models folder
- also add view to the admin view on config.py file
```python
    admin.add_view( AdminModelView(ModelClassName, db.session))
```

### adding controller
- in the controllers folder create a new file and initialize with a new blueprint
```python
    from flask import Blueprint, render_template

    blueprintName=Blueprint("blueprintName",__name__,url_prefix="/blueprintName",template_folder="../templates/blueprintName")
     # add routes
    @blueprintName.route("/route")
    # add @login_required decorator for protected routes
    def function_name():
        return render_template("page.html")
``` 
- import and register the controller on the app.py file
```python
    from controllers.controller_name import blueprintName

    app.register_blueprint(blueprintName)
```
