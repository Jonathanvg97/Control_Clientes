from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import date
# from tkinter import messagebox

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:JADMEC06@localhost/CLIENTES'
db = SQLAlchemy(app)

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    saldo = db.Column(db.Float, nullable=False)
    porcentaje = db.Column(db.Integer, nullable=False)

    def __init__(self, nombre, saldo,porcentaje):
        self.nombre = nombre
        self.saldo = saldo
        self.porcentaje=porcentaje

class Abono(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    monto = db.Column(db.Float, nullable=False)

    def __init__(self, cliente_id, fecha, monto):
        self.cliente_id = cliente_id
        self.fecha = fecha
        self.monto = monto

@app.route('/')
def index():
    clientes = Cliente.query.all()
    return render_template('index.html', clientes=clientes)

@app.route('/cliente/<int:id>')
def ver_cliente(id):
    cliente = Cliente.query.get(id)
    abonos = Abono.query.filter_by(cliente_id=id).all()
    return render_template('cliente.html', cliente=cliente, abonos=abonos)

@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        nombre = request.form['nombre']
        saldo = float(request.form['saldo'])
        porcentaje =int(request.form['porcentaje'])
        saldo_con_porcentaje = saldo * porcentaje/100 + (saldo)
        cliente = Cliente(nombre=nombre, saldo=saldo_con_porcentaje, porcentaje=porcentaje)
        db.session.add(cliente)
        db.session.commit()

        return redirect('/')
    else:
        return render_template('agregar.html')
    

@app.route('/abonar/<int:id>', methods=['GET', 'POST'])
def abonar(id):
    cliente = Cliente.query.get(id)

    if request.method == 'POST':
        monto = float(request.form['monto'])
        abono = Abono(cliente_id=id, fecha=date.today(), monto=monto)
        cliente.saldo -= monto

        db.session.add(abono)
        db.session.commit()

        return redirect('/cliente/{}'.format(id))
    else:
        return render_template('abonar.html', cliente=cliente)
    
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_cliente(id):
    cliente = Cliente.query.get(id)

    if request.method == 'POST':
        cliente.nombre = request.form['nombre']
        cliente.saldo = float(request.form['saldo'])
        cliente.porcentaje=int(request.form['porcentaje'])
        db.session.commit()
        return redirect('/cliente/{}'.format(id))

    return render_template('editar.html', cliente=cliente)

@app.route('/eliminar/<int:id>')
def eliminar_cliente(id):
    cliente = Cliente.query.get(id)
    abono = Abono.query.filter_by(cliente_id=id).first()

    if abono is not None:
        abono.visible = False  
# Eliminar el abono primero
        db.session.commit()
        cliente.visible=False
        db.session.commit()
        # return "El cliente y su abono se eliminaron correctamente."
        return render_template('index.html')
    
    else:
        abono.visible=True
        db.session.commit()
        
        cliente.visible=True
        db.session.commit()
       
    return render_template('index.html')




if __name__ == '__main__':
    app.run(debug=True)
    
    
