import csv
import os
import sqlite3
import traceback

from PyQt5 import QtSql, QtWidgets, Qt
import conexion, events, productos
import facturas
import var
from window import *
import locale
locale.setlocale( locale.LC_ALL, '' )

class Conexion():

    def create_db(filename):
        """

        Crea los directorios necesarios
        :rtype: String nombre fichero
        Recibe el nombre de la base de datos

        """
        try:
            con = sqlite3.connect(database=filename)
            cur = con.cursor()
            cur.execute(
                'CREATE TABLE if not exists clientes (dni	TEXT NOT NULL, alta	TEXT, apellidos	TEXT, nombre TEXT, direccion TEXT, '
                'provincia	TEXT, municipio	NUMERIC, sexo	TEXT, pago	TEXT, envio	INTEGER, PRIMARY KEY(dni))')
            con.commit()

            cur.execute(
                "CREATE TABLE if not exists facturas (codigo	INTEGER NOT NULL, dni	TEXT NOT NULL, fechafac	TEXT NOT NULL, "
                "PRIMARY KEY(codigo AUTOINCREMENT), FOREIGN KEY(dni) REFERENCES clientes(dni) on delete cascade)")
            con.commit()

            cur.execute(
                "CREATE TABLE if not exists municipios (provincia_id	INTEGER NOT NULL, municipio	TEXT NOT NULL, "
                "id	INTEGER NOT NULL, PRIMARY KEY(id))")
            con.commit()

            cur.execute("CREATE TABLE if not exists productos (codigo	INTEGER NOT NULL, nombre	TEXT, "
                        "precio	NUMERIC, PRIMARY KEY(codigo))")
            con.commit()

            cur.execute(
                "CREATE TABLE if not exists provincias (id INTEGER NOT NULL, provincia	TEXT NOT NULL UNIQUE, PRIMARY KEY(id))")
            con.commit()

            cur.execute(
                "CREATE TABLE if not exists ventas (codventa INTEGER NOT NULL, codfac INTEGER NOT NULL, codprod	INTEGER NOT NULL, "
                "cantidad REAL, precio	REAL NOT NULL, FOREIGN KEY(codfac) REFERENCES facturas(codigo), "
                "FOREIGN KEY(codprod) REFERENCES productos(codigo), PRIMARY KEY (codventa AUTOINCREMENT))")
            con.commit()

            cur.execute('select count() from provincias')
            numero = cur.fetchone()[0]
            con.commit()

            if int(numero) == 0:
                print()
                with open('provincias.csv', 'r', encoding="utf-8") as fin:
                    dr = csv.DictReader(fin)
                    to_db = [(i['id'], i['provincia']) for i in dr]
                cur.executemany('insert into provincias (id, provincia) VALUES (?,?);', to_db)
                con.commit()
            con.close()

            # Creación de directorios
            if not os.path.exists('.\\informes'):
                os.mkdir('.\\informes')
            if not os.path.exists('.\\img'):
                os.mkdir('.\\img')
            if not os.path.exists('.\\copias'):
                os.mkdir('.\\copias')

        except Exception as error:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle('Aviso')
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setText(str(error))
            msg.exec()

    def db_connect(filedb):
        """

       Realiza la conexión con la base de datos al ejecutar el programa
       :rtype: boolean
       Recibe: String

       """
        try:
            db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
            db.setDatabaseName(filedb)
            if not db.open():
                QtWidgets.QMessageBox.critical(None, 'No se puede abrir la base de datos. \nHaz click para continuar.',
                                               QtWidgets.QMessageBox.Cancel)
                return False
            print('Conexión establecida')
            return True
        except Exception as error:
            print('Problemas en conexion ', error,traceback.format_exc())
    '''
    Módulos gestión db clientes
    '''


    def altaCli(newcli):
        """

        Módulo que busca el DNI en la base de datos
        :rtype: boolean, True si existe

        """
        try:
            query = QtSql.QSqlQuery()
            if var:
                query.prepare('insert into clientes (dni, alta, apellidos, nombre, direccion, provincia, municipio,'
                              'sexo, pago, envio) VALUES (:dni, :alta, :apellidos, :nombre, :direccion, :provincia, :municipio,'
                              ':sexo, :pago, :envio)')
                query.bindValue(':dni', str(newcli[0]))
                query.bindValue(':alta', str(newcli[1]))
                query.bindValue(':apellidos', str(newcli[2]))
                query.bindValue(':nombre', str(newcli[3]))
                query.bindValue(':direccion', str(newcli[4]))
                query.bindValue(':provincia', str(newcli[5]))
                query.bindValue(':municipio', str(newcli[6]))
                query.bindValue(':sexo', str(newcli[7]))
                query.bindValue(':pago', str(newcli[8]))
                query.bindValue(':envio', int(newcli[9]))
                if query.exec_():
                    msg = QtWidgets.QMessageBox()
                    msg.setWindowTitle('Aviso')
                    msg.setIcon(QtWidgets.QMessageBox.Information)
                    msg.setText('Cliente dado de Alta')
                    msg.exec()
                else:
                    msg = QtWidgets.QMessageBox()
                    msg.setWindowTitle('Aviso')
                    msg.setIcon(QtWidgets.QMessageBox.Warning)
                    msg.setText(query.lastError().text())
                    msg.exec()
        except Exception as error:
            print('Problemas en altaCliente', error,traceback.format_exc())

    def altaCliexcel(newcli):
        """

        Módulo que se ejecuta para insertar un cliente en la bd cuando importamos desde una hoja de cálculo excel

        """
        try:
            query = QtSql.QSqlQuery()
            if var:
                query.prepare('insert into clientes (dni, alta, apellidos, nombre, direccion, provincia, municipio,'
                              'sexo, pago, envio) VALUES (:dni, :alta, :apellidos, :nombre, :direccion, :provincia, :municipio,'
                              ':sexo, :pago, :envio)')
                query.bindValue(':dni', str(newcli[0]))
                query.bindValue(':alta', str(newcli[1]))
                query.bindValue(':apellidos', str(newcli[2]))
                query.bindValue(':nombre', str(newcli[3]))
                query.bindValue(':direccion', str(newcli[4]))
                query.bindValue(':provincia', str(newcli[5]))
                query.bindValue(':municipio', str(newcli[6]))
                query.bindValue(':sexo', str(newcli[7]))
                query.bindValue(':pago', str(newcli[8]))
                query.bindValue(':envio', int(newcli[9]))
                if query.exec_():
                    print("Inserción Correcta")
                #Conexion.mostrarClientes(None)
        except Exception as error:
            print('Problemas en altaCliente', error,traceback.format_exc())

    def bajaCli(dni):
        """

       Módulo que recibe DNI cliente y lo elimina de la BD

       """
        try:
            query = QtSql.QSqlQuery()
            query.prepare('delete from clientes where dni = :dni')
            query.bindValue(':dni', str(dni))
            if query.exec_():
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText('Cliente con dado de Baja')
                msg.exec()
            else:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setText(query.lastError().text())
                msg.exec()

        except Exception as error:
            print("Error baja cliente en conexion ", error,traceback.format_exc())

    def cargarTabCli(self=None):
        """

       Módulo que toma datos de los clientes y los carga en la tabla de la ui

       """
        try:

            index = 0
            query = QtSql.QSqlQuery()
            query.prepare('select dni, apellidos, nombre, alta, pago from clientes order by apellidos, nombre')
            if query.exec_():
                while query.next():
                    dni = query.value(0)
                    apellidos = query.value(1)
                    nombre = query.value(2)
                    alta = query.value(3)
                    pago = query.value(4)
                    var.ui.tabClientes.setRowCount(index+1) #creamos la fila y luego cargamos datos
                    var.ui.tabClientes.setItem(index,0,QtWidgets.QTableWidgetItem(dni))
                    var.ui.tabClientes.setItem(index, 1, QtWidgets.QTableWidgetItem(apellidos))
                    var.ui.tabClientes.setItem(index, 2, QtWidgets.QTableWidgetItem(nombre))
                    var.ui.tabClientes.setItem(index, 3, QtWidgets.QTableWidgetItem(alta))
                    var.ui.tabClientes.setItem(index, 4, QtWidgets.QTableWidgetItem(pago))
                    index += 1
        except Exception as error:
            print('Problemas mostrar tabla clientes', error,traceback.format_exc())


    def oneCli(dni):
        """

       Módulo que selecciona un cliente y lo devuelve a su función cargaCli del fichero clientes
       :return: Lista
       :rtype: Object

       """
        try:
            record = []
            query = QtSql.QSqlQuery()
            query.prepare('select direccion, provincia, municipio, sexo, envio from clientes '
                          'where dni = :dni')
            query.bindValue(':dni', dni)
            if query.exec_():
                while query.next():
                    for i in range(5):
                        record.append(query.value(i))
            return record

        except Exception as error:
            print('Problemas devolver cliente marcado', error,traceback.format_exc())

    def cargaProv(self):
        """

        Módulo que carga las provincias en el combo de la interfaz gráfica del panel clientes
        :return:
        :rtype:

        """
        try:
            var.ui.cmbProv.clear()
            query = QtSql.QSqlQuery()
            query.prepare('select provincia from provincias')
            if query.exec_():
                var.ui.cmbProv.addItem('')
                while query.next():
                    var.ui.cmbProv.addItem(query.value(0))
        except Exception as error:
            print('Problemas cargar combo ', error,traceback.format_exc())


    def cargaMuni(self):
        """

       Módulo que carga municipios dada una provincia y los carga en el panel clientes

       """
        try:
            #busco el código de la provincia
            id_prov = 0
            var.ui.cmbMuni.clear()
            prov = var.ui.cmbProv.currentText()
            query = QtSql.QSqlQuery()
            query.prepare('select id from provincias where provincia = :prov')
            query.bindValue(':prov', str(prov))
            if query.exec_():
                while query.next():
                    id_prov = query.value(0)
            #cargo los municipios con ese código
            query1 = QtSql.QSqlQuery()
            query1.prepare('select municipio from municipios where provincia_id = :id')
            query1.bindValue(':id', int(id_prov))
            if query1.exec_():
                var.ui.cmbMuni.addItem('')
                while query1.next():
                    var.ui.cmbMuni.addItem(query1.value(0))

        except Exception as error:
            print('Problemas cargar combo municipio ', error,traceback.format_exc())

    def modifCli(modcliente):
        """

       Módulo que recibe los datos del cliente a modificar y los guarda en la BD

       """
        try:
            query = QtSql.QSqlQuery()
            query.prepare('update clientes set alta =:alta, apellidos = :apellidos, nombre = :nombre, '
                          'direccion = :direccion, provincia = :provincia, municipio = :municipio, '
                          'sexo = :sexo, pago = :pago, envio = :envio where dni = :dni')
            query.bindValue(':dni', str(modcliente[0]))
            query.bindValue(':alta', str(modcliente[1]))
            query.bindValue(':apellidos', str(modcliente[2]))
            query.bindValue(':nombre', str(modcliente[3]))
            query.bindValue(':direccion', str(modcliente[4]))
            query.bindValue(':provincia', str(modcliente[5]))
            query.bindValue(':municipio', str(modcliente[6]))
            query.bindValue(':sexo', str(modcliente[7]))
            query.bindValue(':pago', str(modcliente[8]))
            query.bindValue(':envio', int(modcliente[9]))
            if query.exec_():
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText('Datos modificados de Cliente')
                msg.exec()
            else:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setText(query.lastError().text())
                msg.exec()

        except Exception as error:
            print('Problemas modificar cliente ', error,traceback.format_exc())


    def comprobardni(dni):
        """

        Método que recibe el dni de un cliente y comprueba si está en la bd
        :rtype: bool

        """
        try:
            var.msg = True
            query = QtSql.QSqlQuery()
            query.prepare('select dni from clientes')
            if query.exec_():
                while query.next():
                    if str(query.value(0)) == str(dni):
                        var.msg = False
                        return var.msg
            return var.msg

        except Exception as error:
            print('Problemas comprobar dni ', error,traceback.format_exc())

    def buscaClie(dni):
        """

        Módulo que se ejecuta con el botón busca. Devuelve datos del cliente para el panel facturación

        """
        try:
            if dni != '':
                registro = []
                query = QtSql.QSqlQuery()
                query.prepare('select dni, alta, apellidos, nombre, direccion, provincia,'
                            ' municipio, sexo, pago, envio from clientes where dni = :dni')
                query.bindValue(':dni', str(dni))
                var.ui.tabClientes.setRowCount(0)
                var.ui.tabClientes.insertRow(0)
                if query.exec_():
                    while(query.next()):
                        for i in range (10):
                            registro.append(str(query.value(i)))
                        var.ui.tabClientes.setItem(0,0, QtWidgets.QTableWidgetItem(str(registro[0])))
                        var.ui.tabClientes.setItem(0,1, QtWidgets.QTableWidgetItem(str(registro[2])))
                        var.ui.tabClientes.setItem(0,2, QtWidgets.QTableWidgetItem(str(registro[3])))
                        var.ui.tabClientes.setItem(0,3, QtWidgets.QTableWidgetItem(str(registro[1])))
                        var.ui.tabClientes.setItem(0,4, QtWidgets.QTableWidgetItem(str(registro[8])))

                return registro
            else:
                Conexion.cargarTabCli()
        except Exception as error:
            print('Búsqueda de un cliente: ', error,traceback.format_exc())

    def cargarTabPro(self):
        """
       Módulo que recorre la tabla productos de la BD para isertarlos en la tabla de la interfaz gráfica

       """
        try:
            index = 0
            query = QtSql.QSqlQuery()
            query.prepare('select codigo, producto, precio from productos order by producto')
            if query.exec_():
                while query.next():
                    codigo = query.value(0)
                    producto = query.value(1)
                    precio = query.value(2)
                    var.ui.tabProd.setRowCount(index + 1)  # creamos la fila y luego cargamos datos
                    var.ui.tabProd.setItem(index, 0, QtWidgets.QTableWidgetItem(str(codigo)))
                    var.ui.tabProd.setItem(index, 1, QtWidgets.QTableWidgetItem(producto))
                    var.ui.tabProd.setItem(index, 2, QtWidgets.QTableWidgetItem(precio))
                    var.ui.tabProd.item(index,2).setTextAlignment(QtCore.Qt.AlignRight)
                    var.ui.tabProd.item(index, 0).setTextAlignment(QtCore.Qt.AlignCenter)
                    index += 1
        except Exception as error:
            print('Problemas mostrar tabla productos', error,traceback.format_exc())

    '''
    gestión facturación
    '''

    def buscaClifac(dni):
        """

        Busca los datos del cliente a facturar
        :return: Datos cliente a facturar
        :rtype: Object

        """
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare('select dni, apellidos, nombre from clientes where dni =:dni')
            query.bindValue(':dni', str(dni))
            if query.exec_():
                while query.next():
                    registro.append(query.value(1))
                    registro.append(query.value(2))
            return registro
        except Exception as error:
            print('error en conexión buscar cliente', error,traceback.format_exc())

    def altaFac(registro):
        """

        Dado el cliente a facturar se da de alta una factura en la BD a nombre de ese cliente

        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare('insert into facturas (dnifac, fechafac) VALUES (:dni, :fecha)')
            query.bindValue(':dni', str(registro[0]))
            query.bindValue(':fecha', str(registro[1]))
            if query.exec_():
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText('Factura dada de alta.')
                msg.exec()
            else:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setText(query.lastError().text())
                msg.exec()
        except Exception as error:
            print('Error en conexión alta fac', error,traceback.format_exc())

    def cargaTabfacturas(self):
        """

        Módulo que se ejecuta siempre cada vez que se da de alta/baja/modificar una factura
        recargando en el panel de gestión de facturación la tabla factura

        """
        try:
            var.ui.tabFacturas.clearContents()
            index = 0
            query = QtSql.QSqlQuery()
            query.prepare('select codigo, fechafac from facturas order by date(fechafac) desc ')
            if query.exec_():
               while query.next():
                    codigo = query.value(0)
                    fechafac = query.value(1)
                    var.btnfacdel = QtWidgets.QPushButton()
                    icopapelera = QtGui.QPixmap("img/papelera.png")
                    var.btnfacdel.setFixedSize(26,26)
                    var.btnfacdel.setIcon(QtGui.QIcon(icopapelera))
                    var.ui.tabFacturas.setRowCount(index + 1)  # creamos la fila y luego cargamos datos
                    var.ui.tabFacturas.setItem(index, 0, QtWidgets.QTableWidgetItem(str(codigo)))
                    var.ui.tabFacturas.setItem(index, 1, QtWidgets.QTableWidgetItem(fechafac))
                    cell_widget = QtWidgets.QWidget()
                    lay_out = QtWidgets.QHBoxLayout(cell_widget)
                    lay_out.setContentsMargins(0,0,0,0)
                    lay_out.addWidget(var.btnfacdel)
                    var.btnfacdel.clicked.connect(Conexion.bajaFac)
                    var.ui.tabFacturas.setCellWidget(index, 2, cell_widget)
                    var.ui.tabFacturas.item(index, 0).setTextAlignment(QtCore.Qt.AlignCenter)
                    var.ui.tabFacturas.item(index, 1).setTextAlignment(QtCore.Qt.AlignCenter)
                    index = index + 1
        except Exception as error:
            print('Error en carga listado facturas ', error,traceback.format_exc())

    def buscaDNIFac(numfac):
        """

        Módulo que busca del DNI de la tabla facturas en la BD
        :return: DNI
        :rtype: String

        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare('select dnifac from facturas where codigo = :numfac')
            query.bindValue(':numfac', int(numfac))
            if query.exec_():
                while query.next():
                    return query.value(0)
            return ''
        except Exception as error:
            print('Error en carga listado facturas ', error,traceback.format_exc())

    def bajaFac(self):
        """

        Módulo que dado el número factura, la da de baja.
        Además llama al módulo borrar ventas para que elimine todas las ventas asociadas a esa factura de
        la tabla ventas de la BD

        """
        try:
            numfac = var.ui.lblNumfac.text()
            query = QtSql.QSqlQuery()
            query.prepare('delete from ventas where codfac = :codfac')
            query.bindValue(':codfac', int(numfac))
            if query.exec_():
                print("ventas eliminadas de la factura ",numfac)
            query.prepare('delete from facturas where codigo = :numfac')
            query.bindValue(':numfac', int(numfac))

            # msg = QtWidgets.QMessageBox()
            # msg.setWindowTitle('Aviso')
            # msg.setText('Va a dar baja la factura ', numfac)
            # msg.setIcon(QtWidgets.QMessageBox.Warning)
            # msg.setText(query.lastError().text())
            #if msg.exec():
            if query.exec_():
                msg1 = QtWidgets.QMessageBox()
                msg1.setWindowTitle('Aviso')
                msg1.setIcon(QtWidgets.QMessageBox.Information)
                msg1.setText('Factura dada de Baja')
                msg1.exec()
                Conexion.cargaTabfacturas(self)
                facturas.Facturas.vaciarTabVentas()
        except Exception as error:
            print('Error módulo baja factura', error,traceback.format_exc())

    def cargarCmbProducto(self):
        """

        Módulo que toma los datos de los nombres de los productos de la BD  y los carga en el panel de la tabla ventas

        """
        try:
            var.cmbProducto.clear()
            query = QtSql.QSqlQuery()
            var.cmbProducto.addItem('')
            query.prepare('select producto from productos order by producto')
            if query.exec_():
                while query.next():
                    var.cmbProducto.addItem(str(query.value(0)))
        except Exception as e:
            print(e,traceback.format_exc())

    def obtenerCodPrecio(articulo):
        """

        Módulo que dado el nombre del producto obtiene el precio
        :return: Precio
        :rtype: list

        """
        try:
            dato = []
            query = QtSql.QSqlQuery()
            query.prepare('select codigo, precio from productos where producto = :producto')
            query.bindValue(':producto',str(articulo))
            if query.exec_():
                while query.next():
                    dato.append(str(query.value(0)))
                    var.codpro = dato[0]
                    dato.append(str(query.value(1)))
            return dato

        except Exception as e:
            print(e,traceback.format_exc())

    def cargarVenta(venta):
        """

        Carga el registro de una venta realizada en la tabla ventas de la BD

        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare('select codigo from facturas where codigo=:codfac ')
            query.bindValue(':codfac',int(venta[0]))
            if query.exec_():
                if not query.next():
                    print("no existe la factura!")
                    return

            query.prepare('insert into ventas (codfac,codpro,precio,cantidad) values '
                          ' (:codfac,:codpro,:preci,:cantidad)')
            query.bindValue(':codfac', int(venta[0]))
            query.bindValue(':codpro', int(venta[1]))
            query.bindValue(':preci', float(venta[2]))
            query.bindValue(':cantidad', float(venta[3]))
            if query.exec_():
                var.ui.lblVenta.setText('venta realizada')
                var.ui.lblVenta.setStyleSheet('QLabel {color: green;}')
            else:
                var.ui.lblVenta.setStyleSheet('Qlabel {color: red;}')
                var.ui.lblVenta.setText('error venta')
        except Exception as e:
            print(e,traceback.format_exc())

    def buscaCodfac(self):
        """

        Módulo que selecciona el código de la factura con número más alto
        :return: Numero factura
        :rtype: int

        """
        try:
            query = QtSql.QSqlQuery()
            dato = ''
            query.prepare('select codigo from facturas order by codigo desc limit 1')
            if query.exec_():
                while query.next():
                    dato = query.value(0)
            return dato
        except Exception as e:
            print(e,traceback.format_exc())

    def buscaArt(cod):
        """

        Módulo que busca el código de un artículo para usarlo en las ventas
        :return: Nombre del artículo
        :rtype: String

        """
        query2 = QtSql.QSqlQuery()
        query2.prepare('select producto from productos where codigo = :codpro')
        query2.bindValue(':codpro', int(cod))
        if query2.exec_():
            while query2.next():
                return query2.value(0)
        return ''

    def getNombreArticulo(codpro):

        """
        Método que devuelve el nombre del artículo al que corresponde el código que recibe.
        :return: Nombre del artículo
        :rtype: String

        """
        try:
            nombre = ''
            query = QtSql.QSqlQuery()
            query.prepare('select producto from productos where codigo = :codpro')
            query.bindValue(':codpro', int(codpro))
            if query.exec_():
                while query.next():
                    return query.value(0)
            return nombre
        except Exception:
            print(traceback.format_exc())


    def cargarLineasVenta(codfac):
        """

        Módulo que carga todas las ventas asociadas a una factura en la interfaz gráfica

        """
        try:
            subtotal = 0.0
            index = 1
            query = QtSql.QSqlQuery()
            query.prepare('select codventa,precio,cantidad,codpro from ventas where codfac = :codfac')

            query.bindValue(':codfac', int(codfac))
            if query.exec_():
                while query.next():
                    codventa = query.value(0)
                    precio = query.value(1)
                    cantidad = query.value(2)
                    total_venta = round(cantidad*precio,2)
                    subtotal += total_venta
                    pro = query.value(3)
                    producto = Conexion.getNombreArticulo(int(pro))
                    var.ui.tabVentas.setRowCount(index + 1)
                    var.ui.tabVentas.setItem(index, 0, QtWidgets.QTableWidgetItem(str(codventa)))
                    var.ui.tabVentas.setItem(index, 1, QtWidgets.QTableWidgetItem(str(producto)))
                    var.ui.tabVentas.setItem(index, 2, QtWidgets.QTableWidgetItem(str(precio)))
                    var.ui.tabVentas.setItem(index, 3, QtWidgets.QTableWidgetItem(str(cantidad)))
                    var.ui.tabVentas.setItem(index, 4, QtWidgets.QTableWidgetItem(str(total_venta)))
                    var.ui.tabVentas.item(index, 0).setTextAlignment(QtCore.Qt.AlignCenter)
                    index += 1

            iva = subtotal * .21
            var.ui.lblSubtotalCalculo.setText(str(round(subtotal,2)))
            var.ui.lblIVAcalculo.setText(str(round(iva, 2)))
            var.ui.lblTotalCalculo.setText(str(round(iva+subtotal, 2)))
        except Exception as error:
            print('error cargar las lineas de factura', error,traceback.format_exc())


    def borraVenta(self):
        """

        Módulo que elimina una venta de una factura

        """
        try:
            row = var.ui.tabVentas.selectedItems()
            if not row:
                return
            codVenta = row[0].text()
            query = QtSql.QSqlQuery()
            query.prepare('delete from ventas where codventa = :codventa')
            query.bindValue(':codventa', int(codVenta))
            if query.exec_():
                facturas.Facturas.cargaFac(self)
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText('Venta eliminada')
                msg.exec()

        except Exception as error:
            print('Error al borrar una venta ', error,traceback.format_exc())



    def delVentaFac(codfac):
        """

        Módulo que dado el número factura, la da de baja.
        Además llama al módulo borrar ventas para que elimine todas las ventas asociadas a esa factura de
        la tabla ventas de la BD

        """
        try:
            ventas = []
            query = QtSql.QSqlQuery()
            query.prepare('select codventa from ventas where codfac=:numfac')
            query.bindValue(':numfac', codfac)
            if query.exec_():
                while query.next():
                    ventas.append(query.value(0))
            for dato in ventas:
                query1 = QtSql.QSqlQuery()
                query1.prepare('delete from ventas where codventa = :dato')
                query1.bindValue(':dato',int(dato))
                if query1.exec_():
                    var.ui.tabVentas.clearContent()
                    var.ui.lblIva.setText('')
                    var.ui.lblSubtotal.setTYext('')
                    var.ui.lblTotalCalculo.setText('')
        except Exception as e:
            print(e,traceback.format_exc())




