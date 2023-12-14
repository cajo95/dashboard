from app import app
#from time import time
#from datetime import timedelta
from flask_apscheduler import APScheduler

scheduler = APScheduler()
@scheduler.task('cron', id='my_job', hour='*', minute= 18, second=59)
def tarea_programada():
    #print('prueba')
    with app.app_context():
        from clases.clases import reporte
        reporte().insert_en_db()

if __name__ == '__main__':
    # job_scheduler.init_app(app)
    # job_scheduler.start()
    scheduler.init_app(app)
    scheduler.start()
    app.run(port=5000, debug=True, use_reloader = False)


"""# Configuración de tarea programada.
job_scheduler = APScheduler()
app.config['SCHEDULER_API_ENABLED'] = True 
app.config['JOBS'] = [
    # {
    #     'id': 'job_inicial',
    #     'func': tarea_programada,
    #     'trigger': 'date',  # Ejecutar una vez al iniciar la aplicación
    #     'run_date': '2023-11-30 10:26:59',
    #     'replace_existing': False,
    # },
    {
        'id': f'job_repetitivo_{int(time())}',
        'func': tarea_programada,
        'trigger': 'cron',  # Repetir cada hora después de la primera ejecución
        'hour': '*',  
        'minute': 20,  
        'second': 59,  
        'replace_existing': False,
    }
]

@scheduler.task('interval', id='my_job', seconds=10)
def my_job():

    print('This job is executed every 10 seconds.')"""

