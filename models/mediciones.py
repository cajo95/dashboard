from app import db

# Los modelos son clases de Python que representan tablas en tu base de datos. 
# Puedes definir modelos utilizando clases y heredando de la clase db.Model de SQLAlchemy. 
# Cada atributo de la clase representa una columna en la tabla.

class potencia_activa_m1(db.Model):
    id_acti    = db.Column(db.String(50), primary_key=True)
    pot_ac_L1  = db.Column(db.Float)
    pot_ac_L2  = db.Column(db.Float)
    pot_ac_L3  = db.Column(db.Float)
    fecha_hora = db.Column(db.DateTime)

class potencia_activa_m2(db.Model):
    __bind_key__ = 'medidor2'
    id_acti    = db.Column(db.String(50), primary_key=True)
    pot_ac_L1  = db.Column(db.Float)
    pot_ac_L2  = db.Column(db.Float)
    pot_ac_L3  = db.Column(db.Float)
    fecha_hora = db.Column(db.DateTime)

class potencia_reactiva_m1(db.Model):
    id_reac    = db.Column(db.String(50), primary_key=True)
    pot_rea_L1 = db.Column(db.Float)
    pot_rea_L2 = db.Column(db.Float)
    pot_rea_L3 = db.Column(db.Float)
    fecha_hora = db.Column(db.DateTime)

class potencia_reactiva_m2(db.Model):
    __bind_key__ = 'medidor2'
    id_reac    = db.Column(db.String(50), primary_key=True)
    pot_rea_L1 = db.Column(db.Float)
    pot_rea_L2 = db.Column(db.Float)
    pot_rea_L3 = db.Column(db.Float)
    fecha_hora = db.Column(db.DateTime)

class factor_potencia_m1(db.Model):
    id_fac     = db.Column(db.String(50), primary_key=True)
    fac_pot_L1 = db.Column(db.Float)
    fac_pot_L2 = db.Column(db.Float)
    fac_pot_L3 = db.Column(db.Float)
    fecha_hora = db.Column(db.DateTime)

class factor_potencia_m2(db.Model):
    __bind_key__ = 'medidor2'
    id_fac     = db.Column(db.String(50), primary_key=True)
    fac_pot_L1 = db.Column(db.Float)
    fac_pot_L2 = db.Column(db.Float)
    fac_pot_L3 = db.Column(db.Float)
    fecha_hora = db.Column(db.DateTime)

class corriente_fase_m1(db.Model):
    id_cor = db.Column(db.String(50), primary_key=True)
    corriente_L1 = db.Column(db.Float)
    corriente_L2 = db.Column(db.Float)
    corriente_L3 = db.Column(db.Float)
    fecha_hora   = db.Column(db.DateTime)

class corriente_fase_m2(db.Model):
    __bind_key__ = 'medidor2'
    id_cor = db.Column(db.String(50), primary_key=True)
    corriente_L1 = db.Column(db.Float)
    corriente_L2 = db.Column(db.Float)
    corriente_L3 = db.Column(db.Float)
    fecha_hora   = db.Column(db.DateTime)

class tension_x_lineas_m1(db.Model):
    id_tension    = db.Column(db.String(50), primary_key=True)
    tension_L1_L2 = db.Column(db.Float)
    tension_L2_L3 = db.Column(db.Float)
    tension_L3_L1 = db.Column(db.Float)
    fecha_hora    = db.Column(db.DateTime)

class tension_x_lineas_m2(db.Model):
    __bind_key__ = 'medidor2'
    id_tension    = db.Column(db.String(50), primary_key=True)
    tension_L1_L2 = db.Column(db.Float)
    tension_L2_L3 = db.Column(db.Float)
    tension_L3_L1 = db.Column(db.Float)
    fecha_hora    = db.Column(db.DateTime)