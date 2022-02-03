import conexion
import var
import locale
locale.setlocale( locale.LC_ALL, '' )

class Productos():


    def altaPro(self):
        try:
            registro = []
            producto = var.ui.txtProducto.text()
            producto = producto.title()
            registro.append(producto)
            precio = var.ui.txtPrecio.text()
            precio = precio.replace(',', '.') #necesita estar con punto como en américa
            precio = locale.currency(float(precio))
            registro.append(precio)
            conexion.Conexion.altaProd(registro)
            conexion.Conexion.cargarTabPro(self)

        except Exception as error:
            print('Error en alta productos: ', error)

    def cargaPro(self):
        '''
        Carga los aatos del cliente al seleccionar en tabla
        :return:
        '''
        try:

            fila = var.ui.tabProd.selectedItems()  #seleccionamos la fila
            datos = [var.ui.lblPro, var.ui.txtProducto, var.ui.txtPrecio ]
            if fila:  #cargamos en row todos los datos de la fila
                row = [dato.text() for dato in fila]
            for i, dato in enumerate(datos):
                dato.setText(row[i])   #cargamos en las cajas de texto los datos
        except Exception as error:
            print('Error carga producto: ', error)


    def limpiaFormPro(self):
        try:
            cajas = [var.ui.lblPro, var.ui.txtProducto, var.ui.txtPrecio ]
            for i in cajas:
                i.setText('')
            conexion.Conexion.cargarTabPro(self)
        except Exception as error:
            print('Erros limpiar producto: ', error)

    def bajaPro(self):
        try:
            cod = var.ui.lblPro.text()
            conexion.Conexion.bajaProd(cod)
            conexion.Conexion.cargarTabPro(self)

        except Exception as error:
            print('Error en baja cliente', error)

    def modifProd(self):
        try:
            modpro = []
            producto = [var.ui.lblPro, var.ui.txtProducto, var.ui.txtPrecio ]
            for i in producto:
                modpro.append(i.text())
            print(modpro)
            conexion.Conexion.modifPro(modpro)
            conexion.Conexion.cargarTabPro(self)
        except Exception as error:
            print('error modificar producto: ', error)

    def buscaPro(self):
        try:
            producto = var.ui.txtProducto.text()
            registro = conexion.Conexion.buscaPro(producto)

            var.ui.lblPro.setText(str(registro[0]))
            var.ui.txtProducto.setText(str(registro[1]))
            var.ui.txtPrecio.setText(str(registro[2]))

        except Exception as error:
            print('error modificar producto: ', error)
