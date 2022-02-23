'''
Fichero de eventos generales
'''
import os.path, sys, var, shutil, zipfile, conexion, xlrd, xlwt
from window import *
from datetime import date, datetime
from PyQt5 import QtPrintSupport, QtSql


class Eventos():
    def Salir(self):
        try:
            var.dlgaviso.show()
            if var.dlgaviso.exec():
                sys.exit()
            else:
                var.dlgaviso.hide()
        except Exception as error:
            print('Error en módulo salir ', error)

    def abrircal(self):
        try:
            var.dlgcalendar.show()
        except Exception as error:
            print('Error al abrir el calendario', error)

    def resizeTablaCli(self):
        try:
            header = var.ui.tabClientes.horizontalHeader()
            for i in range(5):
                header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
                if i ==0 or i ==3:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)
        except Exception as error:
            print('Error al redimensionar tabla clientes', error)

    def resizeTablaPro(self):
        try:
            header = var.ui.tabProd.horizontalHeader()
            for i in range(3):
                header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
                if i == 0 or i == 2:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)

        except Exception as error:
            print('Error al redimensionar tabla clientes', error)

    def resizeTablaFac(self):
        try:
            header = var.ui.tabFacturas.horizontalHeader()
            for i in range(3):
                header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)

        except Exception as error:
            print('Error al redimensionar tabla clientes', error)
    def Abrir(self):
        try:
            var.dlgabrir.show()
        except Exception as error:
            print('Error al abrir cuadro dialogo', error)

    def crearBackup(self):
        try:
            fecha = datetime.today()
            fecha = fecha.strftime('%Y.%m.%d.%H.%M.%S')
            var.copia = (str(fecha) + '_backup.zip')
            option = QtWidgets.QFileDialog.Options()
            directorio, filename = var.dlgabrir.getSaveFileName(None, 'Guardar Copia', var.copia,
                                                                '.zip', options = option)
            if var.dlgabrir.Accepted and filename != '':
                fichzip = zipfile.ZipFile(var.copia, 'w')
                fichzip.write(var.filedb, os.path.basename(var.filedb), zipfile.ZIP_DEFLATED)
                fichzip.close()
                shutil.move(str(var.copia), str(directorio))

                msg = QtWidgets.QMessageBox()
                msg.setModal(True)
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText('Copia de Seguridad Creada ')
                msg.exec()
        except Exception as error:
            print('Error Crear Backup: ', error)

    def restaurarBackup(self):
        try:

            option = QtWidgets.QFileDialog.Options()
            filename = var.dlgabrir.getOpenFileName(None, 'Restaurar Copia de Seguridade','','*.zip;;All Files',
                                                        options=option)
            if var.dlgabrir.Accepted and filename != '':
                file = filename[0]
                print(file)
                with zipfile.ZipFile(str(file), 'r') as bbdd:
                    bbdd.extractall(pwd=None)
                bbdd.close()
            conexion.Conexion.db_connect(var.filedb)
            conexion.Conexion.cargarTabCli(self)
            conexion.Conexion.cargarTabPro(self)
            #conexion.Conexion.mostrarFacturas(self)

            msg = QtWidgets.QMessageBox()
            msg.setModal(True)
            msg.setWindowTitle('Aviso')
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText('Copia de Seguridad Restaurada')
            msg.exec()

        except Exception as error:
            print('Error Restaurar Backup')

    def Imprimir(self):
        try:
            printDialog = QtPrintSupport.QPrintDialog()
            if printDialog.exec_():
                printDialog.show()
        except Exception as error:
            print('Error Abrir Ventana Impresora')

    def importaDatos(self):
        """

        Módulo que importa desde una hoja de excel, los datos de los clientes a la bd

        """
        try:
            option = QtWidgets.QFileDialog.Options()
            filename = var.dlgabrir.getOpenFileName(None, 'Importar Datos', '', '*.xls;;All Files',
                                                    options=option)
            if var.dlgabrir.Accepted and filename != '':
                file = filename[0]
                documento = xlrd.open_workbook(file)
                datos = documento.sheet_by_index(0)
                filas = datos.nrows
                columnas = datos.ncols
                newcli = []
                for i in range(1,filas):
                    newcli = []
                    for j in range(9):
                        newcli.append(str(datos.cell_value(i,j)))
                        if conexion.Conexion.comprobardni(newcli[0]):
                            conexion.Conexion.altaCliexcel(newcli)
                conexion.Conexion.cargarTabCli(self)
                msg = QtWidgets.QMessageBox()
                msg.setModal(True)
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText('Hoja de datos cargada')
                msg.exec()
                # for i in filas:
                #     print(str(datos.cell_value(i,0)))

        except Exception as error:
            print('error cargar datos', error)

    def exportarDatos(self):
        """

        Módulo que exporta a una hoja de excel los datos de todos los clientes

        """
        try:
            fecha = datetime.today()
            fecha = fecha.strftime('%Y.%m.%d.%H.%M.%S')
            var.copia = (str(fecha) + '_Clientes.xls')
            option = QtWidgets.QFileDialog.Options()
            directorio, filename = var.dlgabrir.getSaveFileName(None, 'Exportar datos', var.copia,
                                                    '(*.xls);;All files (*.*)', options=option)
            wb = xlwt.Workbook()
            # add_sheet is used to create sheet.
            sheet1 = wb.add_sheet('Clientes')

            # Cabeceras
            sheet1.write(0, 0, 'DNI')
            sheet1.write(0, 1, 'FECHA ALTA')
            sheet1.write(0, 2, 'APELIDOS')
            sheet1.write(0, 3, 'NOME')
            sheet1.write(0, 4, 'DIRECCION')
            sheet1.write(0, 5, 'PROVINCIA')
            sheet1.write(0, 6, 'MUNICIPIO')
            sheet1.write(0, 7, 'SEXO')
            sheet1.write(0, 8, 'FORMAS PAGO')
            sheet1.write(0, 9, 'ENVIO')
            f = 1
            query = QtSql.QSqlQuery()
            query.prepare('SELECT *  FROM clientes order by apellidos, nombre')
            if query.exec_():
                while query.next():
                    sheet1.write(f, 0, query.value(0))
                    sheet1.write(f, 1, query.value(1))
                    sheet1.write(f, 2, query.value(2))
                    sheet1.write(f, 3, query.value(3))
                    sheet1.write(f, 4, query.value(4))
                    sheet1.write(f, 5, query.value(5))
                    sheet1.write(f, 6, query.value(6))
                    sheet1.write(f, 7, query.value(7))
                    sheet1.write(f, 8, query.value(8))
                    sheet1.write(f, 9, query.value(9))
                    f += 1
            wb.save(directorio)

        except Exception as error:
            print('Error en conexion para exportar excel ', error)

    def resizeTablaFac(self):
        try:
            header = var.ui.tabFacturas.horizontalHeader()
            for i in range(2):
                header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)
                if i == 2:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)

        except Exception as error:
            print('Error al redimensionar tabla clientes', error)

    def resizeTablaVen(self):
        try:
            header = var.ui.tabVentas.horizontalHeader()
            for i in range(5):
                header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
                if i == 1 or i == 3:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)

        except Exception as error:
            print('Error al redimensionar tabla clientes', error)

    def modoEnvio(self):
        try:
            reg = var.ui.spinEnvio.value()
            if reg == 1:
                var.ui.lblEnvio.setText('Recogida Cliente')
            elif reg == 2:
                var.ui.lblEnvio.setText('Envío nacional ordinario')
            elif reg == 3:
                var.ui.lblEnvio.setText('Envío nacional urgente')
            elif reg == 4:
                var.ui.lblEnvio.setText('Envío interncional')
        except Exception as error:
            print('Error en spinbox', error)

