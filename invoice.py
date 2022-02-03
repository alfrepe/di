'''
Gestión Facturación
'''
from reportlab.pdfgen import canvas

import conexion
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

        except Exception as error:
            print('error alta en factura', error)

    def prepararTabFac(self):
        try:
            pass
            # index = 0
            # var.btnfacdel = QtWidgets.QPushButton()
            # var.ui.tabFacturas.setRowCount(index + 1)
            # var.ui.tabFacturas.setItem(index, 0, QtWidgets.QTableWidgetItem())
            # var.ui.tabFacturas.setItem(index, 1, QtWidgets.QTableWidgetItem())
            # var.ui.tabFacturas.setCellWidget(index, 2, var.btnfacdel)
        except Exception as error:
            print("error preparar tabla fact", error)

    def cargarLineaVenta(self):
        try:
            index = 0
            var.cmbProducto = QtWidgets.QComboBox()
            var.txtCantidad = QtWidgets.QLineEdit()
            var.cmbProducto.setFixedSize(180, 25)
            conexion.Conexion.cargarCmbProducto(self)
            var.txtCantidad.setFixedSize(60, 25)
            var.txtCantidad.setAlignment(QtCore.Qt.AlignCenter)
            var.ui.tabVentas.setRowCount(index + 1)
            var.ui.tabVentas.setCellWidget(index, 1, var.cmbProducto)
            var.ui.tabVentas.setCellWidget(index, 3, var.txtCantidad)
            var.cmbProducto.currentIndexChanged.connect(Facturas.procesoVenta)
            var.txtCantidad.editingFinished.connect(Facturas.totalLineaVenta)

        except Exception as error:
            print('error en cargarLineaVenta', error)

    def procesoVenta(self):
        try:
            row = var.ui.tabVentas.currentRow()
            articulo = var.cmbProducto.currentText()
            dato = conexion.Conexion.obtenerCodPrecio(articulo)
            #
            var.ui.tabVentas.setItem(row, 2, QtWidgets.QTableWidgetItem(dato[1]))
            var.ui.tabVentas.item(row, 2).setTextAlignment(QtCore.Qt.AlignCenter)
            precio = dato[1].replace('€','')
            var.precio = precio.replace(',','.')
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




