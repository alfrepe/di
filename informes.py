import os, var
import traceback

from reportlab.pdfgen import canvas
from PyQt5 import QtSql
from datetime import datetime

import conexion


class Informes():
    def listadoClientes(self):
        """

        Método que dibuja el el informe de listado de clientes y lo guarda en formato pdf.
        Usa los métodos cabecera y pie para dibujar dichas partes.

        """
        try:
            var.cv = canvas.Canvas('informes/listadoclientes.pdf')
            var.cv.setTitle('Listado Clientes')
            var.cv.setAuthor('Departamento de Administración')

            rootPath = '.\\informes'
            var.cv.setFont('Helvetica-Bold', size = 12)
            textotitulo = 'LISTADO CLIENTES'
            Informes.cabecera(self)
            Informes.pie(textotitulo)
            var.cv.drawString(255,690,textotitulo)
            var.cv.line(40,685,530,685)
            items = ['DNI', 'Nombre', 'Formas de Pago']
            var.cv.drawString(65,675,items[0])
            var.cv.drawString(210,675,items[1])
            var.cv.drawString(400,675,items[2])
            var.cv.line(40,670,530,670)
            query = QtSql.QSqlQuery()
            query.prepare('select dni, apellidos, nombre, pago from clientes order by'
                          ' apellidos, nombre')
            var.cv.setFont('Helvetica', size = 8)
            if query.exec_():
                i = 50
                j = 655
                while query.next():
                    if j <= 80:
                        var.cv.drawString(460,30, 'Página siguiente...')
                        var.cv.showPage()
                        Informes.cabecera(self)
                        Informes.pie(textotitulo)
                        var.cv.drawString(255, 690, textotitulo)
                        var.cv.line(40, 685, 530, 685)
                        items = ['DNI', 'Nombre', 'Formas de Pago']
                        var.cv.drawString(65, 675, items[0])
                        var.cv.drawString(210, 675, items[1])
                        var.cv.drawString(400, 675, items[2])
                        var.cv.line(40, 670, 530, 670)
                        i = 50
                        j = 655
                    var.cv.setFont('Helvetica', size=8)
                    var.cv.drawString(i,j, str(query.value(0)))
                    var.cv.drawString(i+140,j, str(query.value(1) + ', ' + query.value(2)))
                    var.cv.drawString(i+310,j, str(query.value(3)))
                    j = j - 20
            var.cv.save()
            cont = 0
            for file in os.listdir(rootPath):
                if file.endswith('clientes.pdf'):
                    os.startfile('%s/%s' % (rootPath, file))
                cont = cont +1
        except Exception as error:
            print('Error en informes clientes, ', error,traceback.format_exc())

    def cabecera(self):
        """

        Método que dibuja la cabecera común a todos los informes con los datos de la empresa.

        """
        try:
            logo = '.\\img\logo.png'
            var.cv.line(40,800,530,800)
            var.cv.setFont('Helvetica-Bold', 14)
            var.cv.drawString(50,785, 'Import-Export Vigo')
            var.cv.setFont('Helvetica', 10)
            var.cv.drawString(50,770, 'CIF: A0000000H')
            var.cv.drawString(50, 755, 'Dirección: Avenida Galicia,101')
            var.cv.drawString(50, 740, 'Vigo - 36216 - Spain')
            var.cv.drawString(50, 725, 'e-mail: micorreo@mail.com')
            var.cv.drawImage(logo,425,735)
            var.cv.line(40, 710, 530, 710)
        except Exception as error:
            print('Error en cabecera informe', error,traceback.format_exc())

    def pie(texto):
        """

        Método que dibuja el pie del informe con un formato común.
        Recibe el título del informe para printarlo.

        """
        try:
            var.cv.line(50, 50, 530, 50)
            fecha = datetime.today()
            fecha = fecha.strftime('%d.%m.%Y  %H.%M.%S')
            var.cv.setFont('Helvetica', size = 6)
            var.cv.drawString(70, 40, str(fecha))
            var.cv.drawString(255, 40, str(texto))
            var.cv.drawString(500, 40, str('Página %s ' %var.cv.getPageNumber()))
        except Exception as error:
            print('Error creación de pie de informe clientes', error)

    def listadoProductos(self):
        """

        Método que dibuja el el informe de listado de productos y lo guarda en formato pdf.
        Usa los métodos cabecera y pie para dibujar dichas partes.

        """
        try:
            var.cv = canvas.Canvas('informes/listadoproductos.pdf')
            var.cv.setTitle('Listado Artículos')
            var.cv.setAuthor('Departamento de Administración')

            rootPath = '.\\informes'
            var.cv.setFont('Helvetica-Bold', size = 12)
            textotitulo = 'LISTADO ARTÍCULOS'
            Informes.cabecera(self)
            Informes.pie(textotitulo)
            var.cv.drawString(255,690,textotitulo)
            var.cv.line(40,685,530,685)
            items = ['Código', 'Artículo', 'Precio/Kg']
            var.cv.drawString(60,675,items[0])
            var.cv.drawString(210,675,items[1])
            var.cv.drawString(430,675,items[2])
            var.cv.line(40,670,530,670)
            query = QtSql.QSqlQuery()
            query.prepare('select codigo, producto, precio from productos order by'
                          ' producto')
            var.cv.setFont('Helvetica', size = 8)
            if query.exec_():
                i = 50
                j = 655
                while query.next():
                    if j <= 80:
                        var.cv.drawString(460,30, 'Página siguiente...')
                        var.cv.showPage()
                        Informes.cabecera(self)
                        Informes.pie(textotitulo)
                        var.cv.drawString(255, 690, textotitulo)
                        var.cv.line(40, 685, 530, 685)
                        items = ['Código', 'Artículo', 'Precio/Kg']
                        var.cv.drawRightString(60, 675, items[0])
                        var.cv.drawString(210, 675, items[1])
                        var.cv.drawString(430, 675, items[2])
                        var.cv.line(40, 670, 530, 670)
                        i = 50
                        j = 655
                    var.cv.setFont('Helvetica', size=8)
                    var.cv.drawRightString(i+20,j, str(query.value(0)))
                    var.cv.drawString(i+140,j, str(query.value(1)))
                    var.cv.drawString(i+380,j, str(query.value(2)))
                    j = j - 20
            var.cv.save()
            cont = 0
            for file in os.listdir(rootPath):
                if file.endswith('productos.pdf'):
                    os.startfile('%s/%s' % (rootPath, file))
                cont = cont +1
        except Exception as error:
            print('Error en informes productos, ', error,traceback.format_exc())

    def factura(self):
        """

        Método que dibuja la factura seleccionada y la guarda en formato pdf.
        Usa los métodos cabecera y pie para dibujar dichas partes.

        """
        try:
            var.cv = canvas.Canvas('informes/factura.pdf')
            var.cv.setTitle('Factura')
            var.cv.setAuthor('Departamento de Administración')
            rootPath = '.\\informes'
            var.cv.setFont('Helvetica-Bold', 10)
            textotitulo = 'FACTURA'
            Informes.cabeceraFactura()
            Informes.pie(textotitulo)
            codfac = var.ui.lblNumfac.text()
            # var.cv.drawString(255, 690, textotitulo + ': ' + str(codfac))
            var.cv.line(40, 685, 530, 685)
            items = ['Venta', 'Artículo', 'Precio', 'Cantidad', 'Total']
            var.cv.setFont('Helvetica-Bold', 10)
            var.cv.drawString(60, 675, items[0])
            var.cv.drawString(150, 675, items[1])
            var.cv.drawString(290, 675, items[2])
            var.cv.drawString(390, 675, items[3])
            var.cv.drawString(490, 675, items[4])
            var.cv.line(40, 670, 530, 670)
            suma = 0.0
            query = QtSql.QSqlQuery()
            query.prepare('select codventa,precio,cantidad, codpro from ventas where codfac = :codfac')
            query.bindValue(':codfac', int(codfac))
            i = 50
            j = 655
            if query.exec_():
                while query.next():
                    if j <= 80:
                        # Para saltar de página y colocar pie y cabecera en la nueva
                        var.cv.drawString(460, 65,
                                          'Página siguiente...')  # Ellos están poniendo esta línea más abajo
                        var.cv.showPage()  # Avanza la página
                        var.cv.setFont('Helvetica', 6)
                        var.cv.setFont('Helvetica-Bold', 9)
                        var.cv.line(40, 685, 530, 685)
                        items = ['Venta', 'Artículo', 'Precio', 'Cantidad', 'Total']
                        var.cv.drawString(60, 675, items[0])
                        var.cv.drawString(150, 675, items[1])
                        var.cv.drawString(290, 675, items[2])
                        var.cv.drawString(390, 675, items[3])
                        var.cv.drawString(490, 675, items[4])
                        var.cv.line(40, 670, 530, 670)
                        Informes.cabeceraFactura()
                        Informes.pie(textotitulo)
                        i = 50
                        j = 655
                        var.cv.setFont('Helvetica', 6)
                    codventa = query.value(0)
                    precio = str('{:.2f}'.format(round(query.value(1), 2)))
                    cantidad = str('{:.2f}'.format(round(query.value(2), 2)))
                    articulo = conexion.Conexion.getNombreArticulo(str(query.value(3)))
                    suma = suma + (round(query.value(1), 2) * round(query.value(2), 2))
                    total = str('{:.2f}'.format(round(query.value(1) * query.value(2), 2))).replace(',', '.') + ' €'

                    var.cv.setFont('Helvetica', size=8)
                    var.cv.drawCentredString(i + 20, j, str(codventa))
                    var.cv.drawString(i + 100, j, str(articulo))
                    var.cv.drawString(i + 230, j, str(precio) + '€')
                    var.cv.drawString(i + 350, j, str(cantidad))
                    var.cv.drawString(i + 440, j, str(total))
                    j = j - 20
            Informes.totalFactura(j)
            var.cv.save()
            cont = 0
            for file in os.listdir(rootPath):
                if file.endswith('factura.pdf'):
                    os.startfile('%s/%s' % (rootPath, file))
                cont = cont + 1
        except Exception as error:
            print('Error en informes facturas, ', error,traceback.format_exc())

    def cabeceraFactura(self=None):
        """

        Método que dibuja la cabecera con los datos del cliente de específicos que se añaden en el caso de una factura.

        """
        try:
            logo = '.\\img\logo.png'
            var.cv.drawImage(logo, 425, 722)
            var.cv.line(40, 800, 530, 800)
            var.cv.setFont('Helvetica-Bold', 14)
            var.cv.drawString(50, 785, 'Import-Export Vigo')
            var.cv.setFont('Helvetica-Bold', 10)
            var.cv.drawString(220, 785, 'DATOS CLIENTE:')
            var.cv.setFont('Helvetica', 10)
            var.cv.drawString(50, 770, 'CIF: A0000000H')
            var.cv.drawString(50, 755, 'Dirección: Av. Galicia, 101')
            var.cv.drawString(50, 740, 'Vigo - 36216 - Spain')
            var.cv.drawString(50, 725, 'nohaynadie@algocreible.cow')
            # Datos del cliente:
            query = QtSql.QSqlQuery()
            dni = var.ui.txtDNIfac.text()
            query.prepare('select apellidos,nombre, direccion, envio from clientes where dni = :dni')
            query.bindValue(':dni', dni)
            if query.exec_():
                while query.next():
                    apellidos = query.value(0)
                    nombre = query.value(1)
                    direccion = query.value(2)
                    cliente = str(apellidos + ', ' + nombre)
                    envio = query.value(3)

            fecha = var.ui.txtFechafac.text()
            if (envio == 0):
                formaEnvio = ('Recogida Cliente')
            elif envio == 1:
                formaEnvio = ('Envío Nacional Urgente')
            elif envio == 2:
                formaEnvio = ('Envío Nacional Normal')
            else:
                formaEnvio = ('Envío Internacional')
            formaEnvio = str('Forma de envío: ' + formaEnvio)
            fecha = str('Factura emitida a fecha: ' + fecha)
            dni = str('DNI: ' + dni)
            direccion = str('Dirección: ' + direccion)
            cliente = str('Cliente: ' + cliente)
            codfac = var.ui.lblNumfac.text()
            var.cv.drawString(220, 770, dni)
            var.cv.drawString(220, 755, cliente)
            var.cv.drawString(220, 740, direccion)
            var.cv.drawString(220, 725, formaEnvio)
            var.cv.line(40, 718, 530, 718)

            var.cv.setFont('Helvetica', 8)
            var.cv.setFont('Helvetica-Bold', 10)
            var.cv.drawString(40, 690, 'Código de Factura: ' + str(codfac))
            var.cv.drawString(170, 690, fecha)
        except Exception as error:
            print('Error en cabecera informe ', error,traceback.format_exc())

    def totalFactura(altura):
        """

        Método que añade a la factura el cálculo del subtotal, iva y total tras haber añadido las lineas de venta.
        Recibe la altura a la que debe printarse para decidir si debe cambiar de página.

        """
        try:
            if altura <= 120:
                # Para saltar de página y colocar pie y cabecera en la nueva
                var.cv.drawString(460, altura, 'Página siguiente...')  # Ellos están poniendo esta línea más abajo
                var.cv.showPage()  # Avanza la página
                var.cv.setFont('Helvetica-Bold', 10)
                Informes.cabeceraFactura()
                altura = 655
                var.cv.setFont('Helvetica', 6)
                var.cv.line(40, 685, 530, 685)
                items = ['Venta', 'Artículo', 'Precio', 'Cantidad', 'Total']
                var.cv.drawString(60, 675, items[0])
                var.cv.drawString(150, 675, items[1])
                var.cv.drawString(290, 675, items[2])
                var.cv.drawString(390, 675, items[3])
                var.cv.drawString(490, 675, items[4])
                var.cv.line(40, 670, 530, 670)
                Informes.pie('FACTURA')
                altura=655

            alturaPie=altura
            var.cv.line(40,alturaPie,530,alturaPie)
            subtotal=var.ui.lblSubtotalCalculo.text()
            iva=var.ui.lblIVAcalculo.text()
            total=var.ui.lblTotalCalculo.text()
            subtotal = str('SUBTOTAL: '+subtotal)
            iva = str('IVA:               '+iva)
            total = str('TOTAL:     '+total)
            var.cv.setFont('Helvetica',10)
            #var.cv.drawString(70,40,str(fecha))
            #var.cv.drawString(255,40,str(texto))
            #var.cv.drawString(500,40,str('Página %s '%var.cv.getPageNumber()))
            var.cv.drawString(420, alturaPie-10, subtotal)
            var.cv.drawString(420, alturaPie - 25, iva)
            var.cv.setFont('Helvetica-Bold', 12)
            var.cv.drawString(420, alturaPie - 40, total)
        except Exception as error:
            print('Error al crear pie de informe facura ',error)
