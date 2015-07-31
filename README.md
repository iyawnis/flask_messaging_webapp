# README
Install virtualenv (https://pypi.python.org/pypi/virtualenv)
and mongodb http://www.mongodb.org/ 

```sh
$ apt-get install python-virtualenv
$ apt-get install mongodb
```

Create a new virtual env and activate it  
```sh
$ virtualenv <new_env_name>
$ source <new_env_name>/bin/activate
```
(`<virtual_env_name>`) should show infront of terminal line

cd to Webapp directory

Pull application dependencies: 
```sh
$ pip install -r requirements.txt
```
Server startup is handled by `manage.py`.
Execute `python manage.py` to see available options.

####Managing MongoDB

*dropping and populating the DB can now be handeled by the startup script manage.py*


- Open shell by: `mongo`
- See existing databases: `show dbs`
- Use db: `use <db_name>`
- Show existing collections: `show collections`
- Delete collection: `db.<collection_name>.drop()`
- `exit`
