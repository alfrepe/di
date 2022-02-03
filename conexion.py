from PyQt5 import QtSql, QtWidgets, Qt
import conexion, events, products
import invoice
import var
from window import *
import locale
locale.setlocale( locale.LC_ALL, '' )

class Conexion():
    def db_connect(filedb):
        try:
            db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
            db.setDatabaseName(filedb)
            if not db.open():
                QtWidgets.QMessageBox.critical(None,
                 'No se puede abrir la base de atos.\n' 'Haz click para continuar',
                        QtWidgets.QMessageBox.Cancel)
                return False
            else:
                print('Conexión establecida')
                return True
        except Exception as error:
            print('Problemas en conexion ', error)
    '''
    Módulos gestión base datos cliente
    '''
    def existeDni(dni):
        try:
            signal = True
            query = QtSql.QSqlQuery()
            query.prepare('select dni from clientes')
            if query.exec_():
                while query.next():
                    if str(dni) == str(query.value(0)):
                        signal == False
            return True

        except Exception as error:
            print('Problemas con dni repetido:', error)


    def altaCli(newcli):
        try:
            query = QtSql.QSqlQuery()
            #var = Conexion.comprobardni
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
            print('Problemas en altaCliente', error)

    def altaCliexcel(newcli):
        try:
            query = QtSql.QSqlQuery()
            #var = Conexion.comprobardni
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
                Conexion.mostrarClientes(None)
        except Exception as error:
            print('Problemas en altaCliente', error)

    def bajaCli(dni):
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
            print("Error baja cliente en conexion ", error)

    def cargarTabCli(self):
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
            print('Problemas mostrar tabla clientes', error)


    def oneCli(dni):
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
            print('Problemas devolver cliente marcado', error)

    def cargaProv(self):
        try:
            var.ui.cmbProv.clear()
            query = QtSql.QSqlQuery()
            query.prepare('select provincia from provincias')
            if query.exec_():
                var.ui.cmbProv.addItem('')
                while query.next():
                    var.ui.cmbProv.addItem(query.value(0))
        except Exception as error:
            print('Problemas cargar combo ', error)

    def selMuni(self):
        try:
            #busco el código de la provincia
            id = 0
            var.ui.cmbMuni.clear()
            prov = var.ui.cmbProv.currentText()
            query = QtSql.QSqlQuery()
            query.prepare('select id from provincias where provincia = :prov')
            query.bindValue(':prov', str(prov))
            if query.exec_():
                while query.next():
                    id = query.value(0)
            #cargo los municipios con ese código
            query1 = QtSql.QSqlQuery()
            query1.prepare('select municipio from municipios where provincia_id = :id')
            query1.bindValue(':id', int(id))
            if query1.exec_():
                var.ui.cmbMuni.addItem('')
                while query1.next():
                    var.ui.cmbMuni.addItem(query1.value(0))

        except Exception as error:
            print('Problemas cargar combo municipio ', error)

    def modifCli(modcliente):
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
            print('Problemas modificar cliente ', error)


    def comprobardni(dni):
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
            print('Problemas comprobar dni ', error)

    def buscaClie(dni):
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
                self = 0
                Conexion.cargarTabCli(self)
        except Exception as error:
            print('Búsqueda de un cliente: ', error)

    '''
    funciones gestión PRODUCTOS
    '''

    def altaProd(registro):
        try:
            query = QtSql.QSqlQuery()
            query.prepare('insert into productos (producto, precio) VALUES '
                         '(:producto, :precio)')
            query.bindValue(':producto', str(registro[0]))
            query.bindValue(':precio', str(registro[1]))
            if query.exec_():
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText('Artículo dado de Alta')
                msg.exec()

        except Exception as error:
            print('Problemas alta producto ', error)


    def cargarTabPro(self):
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
            print('Problemas mostrar tabla productos', error)

    def bajaProd(cod):
        try:
            query = QtSql.QSqlQuery()
            query.prepare('delete from productos where codigo = :cod')
            query.bindValue(':cod', str(cod))
            if query.exec_():
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText('Producto dado de Baja')
                msg.exec()
            else:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setText(query.lastError().text())
                msg.exec()

        except Exception as error:
            print("Error baja cliente en conexion ", error)

    def modifPro(modpro):
        try:
            query = QtSql.QSqlQuery()
            query.prepare('update productos set producto =:producto, precio = :precio where codigo = :cod')
            query.bindValue(':cod',  int(modpro[0]))
            query.bindValue(':producto', str(modpro[1]))
            modpro[2] = modpro[2].replace('€','')
            modpro[2] = modpro[2].replace(',','.')
            modpro[2] = float(modpro[2])
            modpro[2] = round(modpro[2], 2)
            modpro[2] = str(modpro[2])
            modpro[2] = locale.currency(float(modpro[2]))
            query.bindValue(':precio', str(modpro[2]))

            if query.exec_():
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText('Datos modificados de Producto')
                msg.exec()
            else:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setText(query.lastError().text())
                msg.exec()
        except Exception as error:
            print('Error modificar producto en conexion: ', error)

    def buscaPro(producto):
        try:
            if producto != '':
                registro = []
                query = QtSql.QSqlQuery()
                query.prepare('select codigo, producto, precio from productos where producto =:producto')
                query.bindValue(':producto', str(producto))
                var.ui.tabProd.setRowCount(0)
                var.ui.tabProd.insertRow(0)
                if query.exec_():
                    while query.next():
                        codigo = query.value(0)
                        registro.append(str(codigo))
                        var.ui.tabProd.setItem(0, 0, QtWidgets.QTableWidgetItem(str(registro[0])))
                        producto = query.value(1)
                        registro.append(str(producto))
                        var.ui.tabProd.setItem(0, 1, QtWidgets.QTableWidgetItem(str(registro[1])))
                        precio = query.value(2)
                        registro.append(str(precio))
                        var.ui.tabProd.setItem(0, 2, QtWidgets.QTableWidgetItem(str(registro[2])))
                        var.ui.tabProd.item(0, 2).setTextAlignment(QtCore.Qt.AlignRight)
                        var.ui.tabProd.item(0, 0).setTextAlignment(QtCore.Qt.AlignCenter)
            else:
                self = 0
                Conexion.cargarTabPro(self)
            return registro

        except Exception as error:
            print('Error en búsqueda producto: ', error)

    '''
    Gestión Facturación
    '''

    def buscaClifac(dni):
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
            print('error en conexión buscar cliente', error)

    def altaFac(registro):
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
            print('Error en conexión alta fac', error)

    def cargaTabfacturas(self):

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
            print('Error en carga listado facturas ', error)

    def buscaDNIFac(numfac):
        try:
            query = QtSql.QSqlQuery()
            query.prepare('select dnifac from facturas where codigo = :numfac')
            query.bindValue(':numfac', int(numfac))
            if query.exec_():
                while query.next():
                    dni  = query.value(0)
            return dni
        except Exception as error:
            print('Error en carga listado facturas ', error)

    def bajaFac(self):
        try:

            numfac = var.ui.lblNumfac.text()
            query = QtSql.QSqlQuery()
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
        except Exception as error:
            print('Error módulo baja factura', error)

    def cargarCmbProducto(self):
        try:
            var.cmbProducto.clear()
            query = QtSql.QSqlQuery()
            var.cmbProducto.addItem('')
            query.prepare('select producto from productos order by producto')
            if query.exec_():
                while query.next():
                    var.cmbProducto.addItem(str(query.value(0)))
        except Exception as e:
            print(e)

    def obtenerCodPrecio(articulo):
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
            print(e)

    def cargarVenta(venta):
        try:
            query = QtSql.QSqlQuery()
            query.prepare('insert into ventas (codfac,codpro,precio,cantidad) values '
                          ' (:codfac,:codpro,:preci,:cantidad)')
            query.bindValue(':codfac', int(venta[0]))
            query.bindValue(':codpro', int(venta[1]))
            query.bindValue(':preci', float(venta[2]))
            query.bindValue(':cantidad', float(venta[3]))
            if query.exec_():
                var.ui.lblVenta.setText('venta realizada')
            else:
                var.ui.lblVenta.setStyleSheet('Qlabel {color: red;}')
                var.ui.lblVenta.setText('error venta')
        except Exception as e:
            print(e)
    def buscaCodfac(self):
        try:
            query = QtSql.QSqlQuery()
            dato = ''
            query.prepare('select codigo from facturas order by codigo desc limit 1')
            if query.exec_():
                while query.next():
                    dato = query.value(0)
            return dato
        except Exception as e:
            print(e)

    def buscaArt(cod):
        query2 = QtSql.QSqlQuery()
        query2.prepare('select producto from productos where codigo = :codpro')
        query2.bindValue(':codpro', int(cod))
        if query2.exec_():
            while query2.next():
                return query2.value(0)
        return ''
    def cargarLineasVenta(codfac):
        try:
            subtotal = 0.0
            #var.ui.tabVentas.clearContents()
            index = 0
            query2 = QtSql.QSqlQuery()
            query = QtSql.QSqlQuery()
            query.prepare('select codventa,precio,cantidad,codpro from ventas where codfac = :codfac')

            query.bindValue(':codfac', int(codfac))
            row = col = 0
            if query.exec_():
                while query.next():
                    codventa = query.value(0)
                    precio = query.value(1)
                    cantidad = query.value(2)
                    total_venta = round(cantidad*precio,2)
                    subtotal += total_venta
                    query2.prepare('select producto from productos where codigo = :codpro')
                    query2.bindValue(':codpro', int(query.value(3)))
                    var.ui.tabVentas.setRowCount(index + 1)
                    if query2.exec_():
                        while query2.next():
                            var.ui.tabVentas.setItem(index, 1, QtWidgets.QTableWidgetItem(str(query2.value(0))))
                    var.ui.tabVentas.setItem(index, 0, QtWidgets.QTableWidgetItem(str(codventa)))
                    var.ui.tabVentas.setItem(index, col+2, QtWidgets.QTableWidgetItem(str(precio)))
                    var.ui.tabVentas.setItem(index, col + 3, QtWidgets.QTableWidgetItem(str(cantidad)))
                    var.ui.tabVentas.setItem(index, col + 4, QtWidgets.QTableWidgetItem(str(total_venta)))
                    var.ui.tabVentas.item(index, 0).setTextAlignment(QtCore.Qt.AlignCenter)
                    index = index + 1
            iva = subtotal * .21
            var.ui.lblSubtotalCalculo.setText(str(round(subtotal,2)))
            var.ui.lblIVAcalculo.setText(str(round(iva, 2)))
            var.ui.lblTotalCalculo.setText(str(round(iva+subtotal, 2)))
        except Exception as error:
            print('error cargar las lines de factura', error)

    def borraVenta(self):
        try:
            row = var.ui.tabVentas.currentRow()
            codventa = var.ui.tabVentas.item(row, 0).text()
            query = QtSql.QSqlQuery()
            query.prepare('delete from ventas where codventa = :codventa')
            query.bindValue(':codventa', int(codventa))
            if query.exec_():
                while query.next():
                    msg1 = QtWidgets.QMessageBox()
                    msg1.setWindowTitle('Aviso')
                    msg1.setIcon(QtWidgets.QMessageBox.Information)
                    msg1.text('Venta eliminada')
                    msg1.exec()
            codfac = var.ui.lblNumfac.text()
            Conexion.cargarLineasVenta(codfac)
        except Exception as error:
            print('error en baja venta en conexion ', error)

    def cargaFac(self):
        try:
            fila = var.ui.tabFacturas.selectedItems()  # seleccionamos la fila
            datos = [var.ui.lblNumfac, var.ui.txtFechafac]
            if fila:  # cargamos en row todos los datos de la fila
                row = [dato.text() for dato in fila]
            for i, dato in enumerate(datos):
                dato.setText(row[i])
            dni = conexion.Conexion.buscaDNIFac(row[0])
            var.ui.txtDNIfac.setText(dni)
            registro = conexion.Conexion.buscaClifac(dni)
            if registro:
                nombre = registro[0] + ', ' + registro[1]
                var.ui.lblNomfac.setText(nombre)

            invoice.Facturas.cargarLineaVenta(self)
            conexion.Conexion.cargarLineasVenta(str(var.ui.lblNumfac.text()))

        except Exception as error:
            print('error alta en factura', error)



