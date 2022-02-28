'''
Gestión Facturación
'''
import traceback

from reportlab.pdfgen import canvas

import conexion
import facturas
import var
from PyQt5 import QtWidgets, QtCore

class Facturas():
    def vaciarTabVentas(self=None):
        """

        Método que vacía la tabla y los campos referentes a las lineas de venta en la interfaz para futuras operaciones.

        """
        try:
            var.ui.tabVentas.clearContents()
            var.cmbProducto = QtWidgets.QComboBox()
            var.txtCantidad = QtWidgets.QLineEdit()
            var.txtCantidad.editingFinished.connect(facturas.Facturas.totalLineaVenta)
            var.cmbProducto.currentIndexChanged.connect(facturas.Facturas.procesoVenta)
            facturas.Facturas.cargarLineaVenta(self)
            var.ui.lblSubtotalCalculo.setText('')
            var.ui.lblIVAcalculo.setText('')
            var.ui.lblTotalCalculo.setText('')
        except Exception as error:
            print('Error en vaciarTabVentas: ', error,traceback.format_exc())

    def buscaCli(self):
        """

        Método que carga los datos de cliente en la interfaz de facturación tomando su dni desde la información de
        la factura y consultando Conexion.buscaCliFac.

        """
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
            print('error buscar cliente en facturas', error,traceback.format_exc())

    def facturar(self):
        """

        Método que lanza el proceso de guardar una nueva factura y actualiza la interfaz.
        Llama a Conexion.altaFac, cargaTabFac y buscaCodFac.

        """
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
            print('error alta en facturas', error,traceback.format_exc())

    def cargaFac(self):
        """

        Método que consulta los datos de una factura seleccionada en tabla con Conexion.buscaDatosFac
        y rellena sus respectivos campos en la interfaz.
        Tambien carga sus lineas de venta con Conexion.cargarLineasVenta.

        """
        try:
            fila = var.ui.tabFacturas.selectedItems()  # seleccionamos la fila
            datos = [var.ui.lblNumfac, var.ui.txtFechafac]
            if fila:  # cargamos en row todos los datos de la fila
                row = [dato.text() for dato in fila]
            else:
                print("no tiene sentido")
                var.ui.tabFacturas.setRowCount(0)
                return
            for i, dato in enumerate(datos):
                dato.setText(row[i])
            dni = conexion.Conexion.buscaDNIFac(row[0])
            var.ui.txtDNIfac.setText(dni)
            registro = conexion.Conexion.buscaClifac(dni)
            if registro:
                nombre = registro[0] + ', ' + registro[1]
                var.ui.lblNomfac.setText(nombre)
            Facturas.cargarLineaVenta(self)
            conexion.Conexion.cargarLineasVenta(str(var.ui.lblNumfac.text()))

        except Exception as error:
            print('error alta en factura', error,traceback.format_exc())


    def cargarLineaVenta(self):
        """

        Método que carga una línea de venta en la fila de la tabla indicada por index
        :return: última línea de la tabla que carga las ventas de una factura
        :rtype: int

        """

        try:
            index = 0

            conexion.Conexion.cargarCmbProducto(self)

            var.txtCantidad.setAlignment(QtCore.Qt.AlignCenter)
            var.ui.tabVentas.setRowCount(index + 1)
            var.ui.tabVentas.setCellWidget(index, 1, var.cmbProducto)
            var.ui.tabVentas.setCellWidget(index, 3, var.txtCantidad)
            var.cmbProducto.setFixedSize(170, 25)
            var.cmbProducto.setFixedWidth(170)
            var.cmbProducto.setFixedHeight(25)
            var.txtCantidad.setFixedSize(80, 25)
            var.txtCantidad.setFixedWidth(80)
            var.txtCantidad.setFixedHeight(25)

        except Exception as error:
            print('Error al cargar linea venta ', error,traceback.format_exc())


    def procesoVenta(self):
        """

        Método que guarda todos los datos de la linea de venta al procesarla.

        """
        try:
            articulo = var.cmbProducto.currentText()
            if articulo:
                dato = conexion.Conexion.obtenerCodPrecio(articulo)
                row = var.ui.tabVentas.currentRow()
                var.codpro = dato[0]
                var.ui.tabVentas.setItem(row, 2, QtWidgets.QTableWidgetItem(dato[1]))
                var.ui.tabVentas.item(row, 2).setTextAlignment(QtCore.Qt.AlignCenter)
                var.precio = dato[1].replace('€', '').replace(',', '.').replace(' ','')
        except Exception as error:
            print('error en procesoVenta en invoice', error,traceback.format_exc())

    def totalLineaVenta(self=None):
        """

        Método que calcula el total de una linea de venta y llama a Conexion.cargarVenta para guardarla en la base de
        datos. También actualiza la interfaz en consecuencia.

        """
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
            if var.ui.lblVenta.text() == 'venta realizada':
                Facturas.vaciarTabVentas()
                conexion.Conexion.cargarLineasVenta(str(var.ui.lblNumfac.text()))

        except Exception as e:
            print(e,traceback.format_exc())




