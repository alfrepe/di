'''
Gestión Facturación
'''
from reportlab.pdfgen import canvas

import conexion
import invoice
import var
from PyQt5 import QtWidgets, QtCore

class Facturas():
    def buscaCli(self):
        try:
            dni = var.ui.txtDNIfac.text().upper()
            var.ui.txtDNIfac.setText(dni)
            registro = conexion.Conexion.buscaClifac(dni)
            if registro:
                nombre = registro[0] + ', ' + registro[1]
                var.ui.lblNomfac.setText(nombre)
            else:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText('No existe el cliente')
                msg.exec()


        except Exception as error:
            print('error buscar cliente en facturas', error)

    def facturar(self):
        try:
            registro = []
            dni = var.ui.txtDNIfac.text().upper()
            registro.append(str(dni))
            var.ui.txtDNIfac.setText(dni)
            fechafac = var.ui.txtFechafac.text()
            registro.append(str(fechafac))
            conexion.Conexion.altaFac(registro)
            conexion.Conexion.cargaTabfacturas(self)
            codfac = conexion.Conexion.buscaCodfac(self)
            var.ui.lblNomfac.setText(str(codfac))
        except Exception as error:
            print('error alta en facturas', error)

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
            conexion.Conexion.cargarLineasVenta(str(var.ui.lblNumfac.text()))

        except Exception as error:
            print('error alta en factura', error)


    def cargarLineaVenta(index):
        """

        Método que carga una línea de venta en la fila de la tabla indicada por index
        :return: última línea de la tabla que carga las ventas de una factura
        :rtype: int

        """
        try:
            var.cmbProducto = QtWidgets.QComboBox()
            var.cmbProducto.currentIndexChanged.connect(Facturas.procesoVenta)
            var.cmbProducto.setFixedSize(170, 25)
            conexion.Conexion.cargarCmbProducto(self=None)
            var.txtCantidad = QtWidgets.QLineEdit()
            var.txtCantidad.editingFinished.connect(Facturas.totalLineaVenta)
            var.txtCantidad.setFixedSize(80, 25)
            var.txtCantidad.setAlignment(QtCore.Qt.AlignCenter)
            var.ui.tabVentas.setRowCount(index + 1)
            var.ui.tabVentas.setCellWidget(index, 1, var.cmbProducto)
            var.ui.tabVentas.setCellWidget(index, 3, var.txtCantidad)
        except Exception as error:
            print('Error al cargar linea venta ', error)


    def procesoVenta(self):
        try:
            if var.cmbProducto.currentText() != '':
                articulo = var.cmbProducto.currentText()
                dato = conexion.Conexion.obtenerCodPrecio(articulo)
                row = var.ui.tabVentas.currentRow()
                precio = dato[1].replace('€', '').replace(',', '.')
                var.precio = precio
                var.codpro = dato[0]
                var.ui.tabVentas.setItem(row, 2, QtWidgets.QTableWidgetItem(dato[1]))
                var.ui.tabVentas.item(row, 2).setTextAlignment(QtCore.Qt.AlignCenter)
        except Exception as error:
            print('error en procesoVenta en invoice', error)

    def totalLineaVenta():
        try:
            venta = []
            row = var.ui.tabVentas.currentRow()
            cantidad = float(var.txtCantidad.text().replace(',','.'))
            total_venta = round(float(var.precio) *float(cantidad),2)
            var.ui.tabVentas.setItem(row,4,QtWidgets.QTableWidgetItem(str(total_venta)))
            var.ui.tabVentas.item(row,4).setTextAlignment(QtCore.Qt.AlignRight)
            codfac = var.ui.lblNumfac.text()

            venta.append(int(codfac))
            venta.append(float(var.codpro))

            venta.append(float(var.precio))
            venta.append(float(cantidad))

            conexion.Conexion.cargarVenta(venta)

        except Exception as e:
            print(e)




