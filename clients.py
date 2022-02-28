'''

Funciones gestion clientes

'''
import traceback
import conexion
from windowaviso import *
import var

class Clientes():
    def validarDNI():
        """

       Método que comprueba si el dni introducido es válido y señala el resultado en la interfaz gráfica.

       """
        try:
            dni = var.ui.txtDNI.text()
            var.ui.txtDNI.setText(dni.upper())
            tabla = 'TRWAGMYFPDXBNJZSQVHLCKE'  # letras dni
            dig_ext = 'XYZ' # digito
            reemp_dig_ext = { 'X': '0', 'Y': '1', 'Z': '2' }
            numeros = '1234567890'
            dni = dni.upper()  # conver la letra mayúsculas
            if len(dni) == 9:
                dig_control = dni[8]
                dni = dni[:8]
                if dni[0] in dig_ext:
                    dni = dni.replace(dni[0], reemp_dig_ext[dni[0]])
                if len(dni) == len([n for n in dni if n in numeros]) and tabla[int(dni) % 23] == dig_control:
                    var.ui.lblValidoDNI.setStyleSheet('QLabel {color: green;}')
                    var.ui.lblValidoDNI.setText('V')
                    var.ui.txtDNI.setStyleSheet('background-color: white;')
                    return True

                else:
                    var.ui.lblValidoDNI.setStyleSheet('QLabel {color: red;}')
                    var.ui.lblValidoDNI.setText('X')
                    var.ui.txtDNI.setStyleSheet('background-color: pink;')
            else:
                var.ui.lblValidoDNI.setStyleSheet('QLabel {color: red;}')
                var.ui.lblValidoDNI.setText('X')
                var.ui.txtDNI.setStyleSheet('background-color: pink;')

        except Exception as error:
            print('Error en módulo validar DNI', error,traceback.format_exc())
        return False
    def cargarFecha(qDate):
        """

        Método que carga la fecha seleccionada en el calendario en el txt de la interfaz.
        Es formateada para ello.

        """
        try:
            data = (str(qDate.day()).zfill(2) + '/' + str(qDate.month()).zfill(2) + '/' + str(qDate.year()))
            if var.ui.tabPrograma.currentIndex() == 0:
                var.ui.txtAltaCli.setText(str(data))
            elif var.ui.tabPrograma.currentIndex() == 1:
                var.ui.txtFechafac.setText(str(data))
            var.dlgcalendar.hide()

        except Exception as error:
            print('Error cargar fecha en txtFecha', error,traceback.format_exc())

    def letraCapital():
        """

        Método que formatea los campos de nombre, apellidos y dirección del cliente para que cada palabra inicie en
        mayúsculas.

        """
        try:
            apel = var.ui.txtApel.text()
            var.ui.txtApel.setText(apel.title())
            nome = var.ui.txtNome.text()
            var.ui.txtNome.setText(nome.title())
            dir = var.ui.txtDir.text()
            var.ui.txtDir.setText(dir.title())

        except Exception as error:
            print('Error en capitalizar datos', error,traceback.format_exc())

    def limpiaFormCli(self):
        """

        Método que vacía los distintos campos de la interfaz de clientes para futuras operaciones.

        """
        try:
            cajas = [var.ui.txtDNI, var.ui.txtApel, var.ui.txtNome, var.ui.txtAltaCli,
                     var.ui.txtDir]
            for i in cajas:
                i.setText('')
            var.ui.lblValidoDNI.setText('')
            var.ui.rbtGroupSex.setExclusive(False)
            var.ui.rbtFem.setChecked(False)
            var.ui.rbtHom.setChecked(False)
            var.ui.rbtGroupSex.setExclusive(True)
            var.ui.chkTarjeta.setChecked(False)
            var.ui.chkTransfe.setChecked(False)
            var.ui.chkEfectivo.setChecked(False)
            var.ui.chkCargocuenta.setChecked(False)
            var.ui.cmbProv.setCurrentIndex(0)
            var.ui.cmbMuni.setCurrentIndex(0)
            var.ui.spinEnvio.setValue(1)
            #conexion.Conexion.cargarTabCli(self)

        except Exception as error:
            print('Error en Limpiar  clientes', error,traceback.format_exc())

    def guardaCli(self):
        """

        Método que gestiona el proceso de guardado de un nuevo cliente en la bbdd y actualiza la interfaz
        en consecuencia.
        Llama a Conexion.altaCli y cargaTabCli.

        """
        if var.ui.lblValidoDNI.text() == 'X':
            print("el dni no es valido")
            return
        try:
            #preparamos el registro
            newcli= []  # base de datos
            cliente = [var.ui.txtDNI, var.ui.txtAltaCli, var.ui.txtApel, var.ui.txtNome, var.ui.txtDir ]   # para base de datos
            tabcli = []   # para tablewidget
            client =[ var.ui.txtDNI, var.ui.txtApel, var.ui.txtNome, var.ui.txtAltaCli ]
            # código para cargar en la tabla el cliente y la forma de pago
            for i in cliente:
                newcli.append(i.text())
            for i in client:
                tabcli.append(i.text())
            newcli.append(var.ui.cmbProv.currentText())
            newcli.append(var.ui.cmbMuni.currentText())
            if var.ui.rbtHom.isChecked():
                newcli.append('Hombre')
            elif var.ui.rbtFem.isChecked():
                newcli.append('Mujer')
            pagos = []
            if var.ui.chkCargocuenta.isChecked():
                pagos.append('Cargo Cuenta')
            if var.ui.chkEfectivo.isChecked():
                pagos.append('Efectivo')
            if var.ui.chkTransfe.isChecked():
                pagos.append('Transferencia')
            if var.ui.chkTarjeta.isChecked():
                pagos.append('Tarjeta')
            pagos = set(pagos)  #evita duplicados
            newcli.append('; '.join(pagos))
            tabcli.append('; '.join(pagos))
            envio = var.ui.spinEnvio.value()
            newcli.append(int(envio))

            #cargamos la tabla
            if Clientes.validarDNI():
                conexion.Conexion.altaCli(newcli) #graba en la tabla de la bbdd
                conexion.Conexion.cargarTabCli(self) #recarga la tabla
            else:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setText('DNI no válido   ')
                msg.exec()

            # código para grabar en la base de datos
        except Exception as error:
            print('Error en guardar clientes', error,traceback.format_exc())

    def modifCli(self):
        """

        Método que guarda las modificaciones realizadas sobre el cliente que se encuentra volcado en la interfaz.
        Usa Conexion.modifCli y cargaTabCli.

        """
        try:
            modcliente = []
            cliente = [var.ui.txtDNI, var.ui.txtAltaCli, var.ui.txtApel, var.ui.txtNome, var.ui.txtDir]
            for i in cliente:
                modcliente.append(i.text())
            modcliente.append(var.ui.cmbProv.currentText())
            modcliente.append(var.ui.cmbMuni.currentText())
            if var.ui.rbtHom.isChecked():
                modcliente.append('Hombre')
            elif var.ui.rbtFem.isChecked():
                modcliente.append('Mujer')
            pagos = []
            if var.ui.chkCargocuenta.isChecked():
                pagos.append('Cargo Cuenta')
            if var.ui.chkEfectivo.isChecked():
                pagos.append('Efectivo')
            if var.ui.chkTransfe.isChecked():
                pagos.append('Transferencia')
            if var.ui.chkTarjeta.isChecked():
                pagos.append('Tarjeta')
            pagos = set(pagos)  # evita duplicados
            modcliente.append('; '.join(pagos))
            envio = var.ui.spinEnvio.value()
            modcliente.append(int(envio))
            conexion.Conexion.modifCli(modcliente)
            conexion.Conexion.cargarTabCli(self)  # recarga la tabla

        except Exception as error:
            print('Error modificar cliente', error,traceback.format_exc())


    def bajaCli(self):
        """

        Método que gestiona el borrado de un cliente de la bbdd y actualiza la interfaz en consecuencia.
        Llama a Conexion.bajaCli y cargaTabCli.

        """
        try:
            dni = var.ui.txtDNI.text()
            conexion.Conexion.bajaCli(dni)
            conexion.Conexion.cargarTabCli(self)

        except Exception as error:
            print('Error en baja cliente', error,traceback.format_exc())

    def cargaCli(self):
        '''
        Carga los aatos del cliente al seleccionar en tabla
        :return:
        '''
        try:
            Clientes.limpiaFormCli(self)
            fila = var.ui.tabClientes.selectedItems()  #seleccionamos la fila
            datos = [var.ui.txtDNI, var.ui.txtApel, var.ui.txtNome, var.ui.txtAltaCli ]
            row = ['']
            if fila:  #cargamos en row todos los datos de la fila
                row = [dato.text() for dato in fila]
            for i, dato in enumerate(datos):
                dato.setText(row[i])   #cargamos en las cajas de texto los datos
            #ahora cargamos los métodos de pago que están en la posición 5 de row
            if 'Efectivo' in row[4]:
                var.ui.chkEfectivo.setChecked(True)
            if 'Transferencia' in row[4]:
                var.ui.chkTransfe.setChecked(True)
            if 'Tarjeta' in row[4]:
                var.ui.chkTarjeta.setChecked(True)
            if 'Cargo' in row[4]:
                var.ui.chkCargocuenta.setChecked(True)
            registro = conexion.Conexion.oneCli(row[0])
            var.ui.txtDir.setText(str(registro[0]))
            var.ui.cmbProv.setCurrentText(str(registro[1]))
            var.ui.cmbMuni.setCurrentText(str(registro[2]))
            if str(registro[3]) == 'Hombre':
                var.ui.rbtHom.setChecked(True)
            elif str(registro[3]) == 'Mujer':
                var.ui.rbtFem.setChecked(True)
            if registro[4]:
                var.ui.spinEnvio.setValue(int(registro[4]))
            if registro[4] == 1:
                var.ui.lblEnvio.setText('Recogida Cliente')
            elif registro[4] == 2:
                var.ui.lblEnvio.setText('Envío nacional ordinario')
            elif registro[4] == 3:
                var.ui.lblEnvio.setText('Envío nacional urgente')
            elif registro[4] == 4:
                var.ui.lblEnvio.setText('Envío interncional')
            Clientes.validarDNI()
            var.ui.txtDNIfac.setText(str(row[0]))
            nombre = row[1] + ', ' + row[2]
            var.ui.lblNomfac.setText(nombre)
        except Exception as error:
            print('Error en cargar datos de un cliente', error,traceback.format_exc())

    def buscaCli(self):
        '''
        Busca el cliente por el dni y muestra los datos en las cajas de texto
        :return:
        '''
        try:
            dni = var.ui.txtDNI.text()
            registro = conexion.Conexion.buscaClie(dni)
            var.ui.txtDNI.setText(str(registro[0]))
            var.ui.txtAltaCli.setText(str(registro[1]))
            var.ui.txtApel.setText(str(registro[2]))
            var.ui.txtNome.setText(str(registro[3]))
            var.ui.txtDir.setText(str(registro[4]))
            var.ui.cmbProv.setCurrentText(str(registro[5]))
            var.ui.cmbMuni.setCurrentText(str(registro[6]))
            if registro[7] == 'Hombre':
                var.ui.rbtHom.setChecked(True)
            else:
                var.ui.rbtFem.setChecked(True)
            if 'Efectivo' in registro[8]:
                var.ui.chkEfectivo.setChecked(True)
            if 'Transferencia' in registro[8]:
                var.ui.chkTransfe.setChecked(True)
            if 'Tarjeta' in registro[8]:
                var.ui.chkTarjeta.setChecked(True)
            if 'Cargo' in registro[8]:
                var.ui.chkCargocuenta.setChecked(True)

        except Exception as error:
            print('error buscar cliente',traceback.format_exc())


