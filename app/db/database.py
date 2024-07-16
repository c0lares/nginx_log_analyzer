from peewee import *

db = MySQLDatabase(
    'log_check',
    user='root',
    password='bp1234',
    host='mysql',
    port=3306
)

# Definicao das modelos de access_log

class UserAgent(Model):
    browser = CharField(null=True)
    browser_version = CharField(null=True)
    os = CharField(null=True)
    os_version = CharField(null=True)
    device = CharField(null=True)

    class Meta:
        database = db
        table_name = 'user_agent'
        
class GeoIp(Model):
    continent_code = CharField(null=True)
    city = CharField(null=True)
    country = CharField(null=True)
    latitude = FloatField(null=True)
    longitude = FloatField(null=True)
    time_zone = CharField(null=True)
    state_iso_code = CharField(null=True)
    autonomous_system_organization = CharField(null=True)
    network = CharField(null=True)
    
    class Meta:
        database = db
        table_name = 'geo_ip'    

class Request(Model):
    ip = CharField()
    date_time_utc = DateTimeField()
    requisition_type = CharField(null=True)
    requisition_status = IntegerField(null=True)
    requisition_size = FloatField(null=True)
    url_requested = CharField(null=True)
    user_agent = ForeignKeyField(UserAgent, backref='posts')
    geo_ip = ForeignKeyField(GeoIp, backref='posts')
    hashcode = CharField()

    class Meta:
        database = db



#Definindo as classes para o error_log
class ErrorLog(Model):
    priority = IntegerField()
    log_level = CharField()
    date_time = DateTimeField()
    process_id = CharField(null=True)
    connection_id = CharField(null=True)
    message = CharField(null=True)
    client = CharField(null=True)
    request = CharField(null=True)
    host = CharField(null=True)
    server = CharField(null=True)
    hashcode = CharField()
    
    class Meta:
        database = db
        table_name = 'error_log'
        
class SecurityInform(Model):
    information = TextField()
    last_datetime = DateTimeField()
    hashcode = CharField()

    class Meta:
        database = db
        table_name = 'security_inform'

#Funcoes do banco de dados
def initialize_database():
    db.connect()
    db.create_tables([UserAgent, Request, GeoIp, ErrorLog, SecurityInform], safe=True)
    return db

def close_datase(db):
    if isinstance(db, Database):
        db.close()
    else:
        raise TypeError("O argumento fornecido nao e uma instancia valida de banco de dados.")
