import traceback

from PyQt5 import QtSql, QtWidgets, QtCore

import conexion
import var
import locale
locale.setlocale( locale.LC_ALL, '' )

class Productos:

    def altaProBD(registro):
        """

        Módulo que recibe un producto y lo guarda en la BD

        """
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
            print('Problemas alta producto ', error,traceback.format_exc())

    def altaPro(self):
        """

       Módulo que llama a cargaPro para guardar el producto en la bd y recarga la tabla productos
       :rtype:

       """
        try:
            registro = []
            producto = var.ui.txtProducto.text()
            producto = producto.title()
            registro.append(producto)
            precio = var.ui.txtPrecio.text()
            precio = precio.replace(',', '.').replace('€','')
            precio = locale.currency(float(precio))
            registro.append(precio)
            Productos.altaProBD(registro)
            conexion.Conexion.cargarTabPro(self)

        except Exception as error:
            print('Error en alta productos: ', error,traceback.format_exc())

    def cargaPro(self):
        '''
        Carga los aatos del cliente al seleccionar en tabla
        :return:
        '''
        try:

            fila = var.ui.tabProd.selectedItems()  # seleccionamos la fila
            datos = [var.ui.lblPro, var.ui.txtProducto, var.ui.txtPrecio ]
            row = ''
            if fila:  #cargamos en row todos los datos de la fila
                row = [dato.text() for dato in fila]
            for i, dato in enumerate(datos):
                dato.setText(row[i])   #cargamos en las cajas de texto los datos
        except Exception as error:
            print('Error carga producto: ', error,traceback.format_exc())

    def bajaProdBD(cod):
        """

        Módulo que recibe el codigo de un producto y lo busca en la BD para eliminarlo
        :rtype:
        """
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
            print("Error baja producto en conexion ", error,traceback.format_exc())

    def limpiaFormPro(self):
        """

       Módulo que limpia el formulario de los datos de producto
       :rtype:

       """
        try:
            cajas = [var.ui.lblPro, var.ui.txtProducto, var.ui.txtPrecio ]
            for i in cajas:
                i.setText('')
            conexion.Conexion.cargarTabPro(self)
        except Exception as error:
            print('Erros limpiar producto: ', error,traceback.format_exc())

    def bajaPro(self):
        """

       Módulo que da de baja un producto y recarga la tabla de productos
       :rtype:

       """
        try:
            cod = var.ui.lblPro.text()
            Productos.bajaProdBD(cod)
            conexion.Conexion.cargarTabPro(self)

        except Exception as error:
            print('Error en bajaPro', error,traceback.format_exc())

    def modifProd(self):
        """

        Módulo que coge los datos de los labels asociados a modificar producto y llama a modifProBD para su modificación en la bd y la recarga de la tabla productos
        :rtype:

        """
        try:
            modpro = []
            producto = [var.ui.lblPro, var.ui.txtProducto, var.ui.txtPrecio ]
            for i in producto:
                modpro.append(i.text())
            print(modpro)
            Productos.modifProBD(modpro)
            conexion.Conexion.cargarTabPro(self)
        except Exception as error:
            print('error modificar producto: ', error,traceback.format_exc())

    def modifProBD(modpro):
        """

        Módulo que recibe los datos del producto a modificar y los guarda en la BD
        :rtype:

        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare('update productos set producto =:producto, precio = :precio where codigo = :cod')
            query.bindValue(':cod', int(modpro[0]))
            query.bindValue(':producto', str(modpro[1]))
            modpro[2] = modpro[2].replace('€', '')
            modpro[2] = modpro[2].replace(',', '.')
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
            print('Error modificar producto en conexion: ', error,traceback.format_exc())



    def buscaPro(self):
        """

       Módulo asociado al botón buscar de articulos que busca un producto en la bd

       """
        try:
            producto = var.ui.txtProducto.text()
            registro = Productos.buscaProDB(producto)
            if registro:
                var.ui.lblPro.setText(str(registro[0]))
                var.ui.txtProducto.setText(str(registro[1]))
                var.ui.txtPrecio.setText(str(registro[2]))

        except Exception as error:
            print('error modificar producto: ', error,traceback.format_exc())

    def buscaProDB(producto):
        """

        Módulo que recibe el nombre de un producto para buscarlo en la BD

        """
        registro = []
        try:
            if producto != '':
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
                conexion.Conexion.cargarTabPro(self=None)
            return registro

        except Exception as error:
            print('Error en búsqueda producto: ', error,traceback.format_exc())