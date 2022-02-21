from datetime import *
import conexion
from window import *
from windowaviso import *
from windowcal import *
import sys, var, events, clients, locale, informes, products, invoice
locale.setlocale(locale.LC_ALL, 'es-ES')


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
class FileDialogAbrir(QtWidgets.QFileDialog):
    def __init__(self):
        '''
        ventana abrir explorador windows
        '''
        super(FileDialogAbrir, self).__init__()

class DialogCalendar(QtWidgets.QDialog):
    def __init__(self):
        '''
        ventana calendario
        '''
        super(DialogCalendar, self).__init__()
        var.dlgcalendar = Ui_windowcal()
        var.dlgcalendar.setupUi(self)
        diaactual = datetime.now().day
        mesactual = datetime.now().month
        anoactual = datetime.now().year
        var.dlgcalendar.Calendar.setSelectedDate((QtCore.QDate(anoactual,mesactual,diaactual)))
        var.dlgcalendar.Calendar.clicked.connect(clients.Clientes.cargarFecha)

class DialogAviso(QtWidgets.QDialog):
    def __init__(self):
        '''

        Clase que instancia la ventana de avisos

        '''
        super(DialogAviso, self).__init__()
        var.dlgaviso = Ui_windowaviso()
        var.dlgaviso.setupUi(self)
        var.dlgaviso.btnBoxAviso.accepted.connect(self.accept)
        var.dlgaviso.btnBoxAviso.rejected.connect(self.reject)


class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        var.ui = Ui_window()
        var.ui.setupUi(self)
        conexion.Conexion.create_DB(var.filedb)
        '''
        Eventos de botón
        '''
        var.ui.btnCalendar.clicked.connect(events.Eventos.abrircal)
        var.ui.btnLimpiaCli.clicked.connect(clients.Clientes.limpiaFormCli)
        var.ui.btnGrabaCli.clicked.connect(clients.Clientes.guardaCli)
        var.ui.btnBajaCli.clicked.connect(clients.Clientes.bajaCli)
        var.ui.btnModifCli.clicked.connect(clients.Clientes.modifCli)
        var.ui.btnBuscaCli.clicked.connect(clients.Clientes.buscaCli)
        var.ui.btnAltapro.clicked.connect(products.Productos.altaPro)
        var.ui.btnBajapro.clicked.connect(products.Productos.bajaPro)
        var.ui.btnModifpro.clicked.connect(products.Productos.modifProd)
        var.ui.btnLimpiaPro.clicked.connect(products.Productos.limpiaFormPro)
        var.ui.btnBuscaPro.clicked.connect(products.Productos.buscaPro)
        var.ui.btnBuscaClifac.clicked.connect(invoice.Facturas.buscaCli)
        var.ui.btnFechaFac.clicked.connect(events.Eventos.abrircal)
        var.ui.btnFacturar.clicked.connect(invoice.Facturas.facturar)
        var.ui.btnPDFcli.clicked.connect(informes.Informes.listadoClientes)
        var.ui.btnReportPro.clicked.connect(informes.Informes.listadoProductos)
        var.ui.btnImprimir.clicked.connect(informes.Informes.factura)
        var.ui.btnBorrarVenta.clicked.connect(conexion.Conexion.borraVenta)

        '''
        Eventos de la barra de menús y de herramientas     
        '''
        var.ui.actionSalir.triggered.connect(events.Eventos.Salir)
        var.ui.actionAbrir.triggered.connect(events.Eventos.Abrir)
        var.ui.actionCrear_Backup.triggered.connect(events.Eventos.crearBackup)
        var.ui.actionRestaurar_Base_de_Datos.triggered.connect(events.Eventos.restaurarBackup)
        var.ui.actionImprimir.triggered.connect(events.Eventos.Imprimir)
        var.ui.actionImportar_Datos.triggered.connect(events.Eventos.importaDatos)
        var.ui.actionExportar_DAtos.triggered.connect(events.Eventos.exportarDatos)
        '''
        Eventos caja de texto
        '''
        var.ui.txtDNI.editingFinished.connect(clients.Clientes.validarDNI)
        var.ui.txtApel.editingFinished.connect(clients.Clientes.letraCapital)
        var.ui.txtNome.editingFinished.connect(clients.Clientes.letraCapital)
        var.ui.txtDir.editingFinished.connect(clients.Clientes.letraCapital)
        var.txtCantidad = QtWidgets.QLineEdit()


        '''
        Eventos QTabWidget
        '''
        events.Eventos.resizeTablaCli(self)
        events.Eventos.resizeTablaPro(self)
        events.Eventos.resizeTablaFac(self)
        events.Eventos.resizeTablaFac(self)
        events.Eventos.resizeTablaVen(self)
        var.ui.tabClientes.clicked.connect(clients.Clientes.cargaCli)
        var.ui.tabClientes.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        var.ui.tabProd.clicked.connect(products.Productos.cargaPro)
        var.ui.tabProd.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        #var.ui.tabFacturas.clicked.connect(invoice.Facturas.cargaFac)
        var.ui.tabFacturas.clicked.connect(conexion.Conexion.cargaFac)
        var.ui.tabProd.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        var.ui.tabVentas.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        #invoice.Facturas.prepararTabFac(self)
        invoice.Facturas.cargarLineaVenta(self)



        '''
        Base de datos
        '''
        conexion.Conexion.db_connect(var.filedb)
        conexion.Conexion.cargarTabCli(self)
        conexion.Conexion.cargarTabPro(self)
        conexion.Conexion.cargaTabfacturas(self)

        '''
        Eventos combobox
        '''
        conexion.Conexion.cargaProv(self)
        var.ui.cmbProv.currentIndexChanged.connect(conexion.Conexion.selMuni)
        conexion.Conexion.cargarCmbProducto(self)


        '''
        barra de estado
        '''
        var.ui.statusbar.addPermanentWidget(var.ui.lblFecha, 1)
        day = datetime.now()
        var.ui.lblFecha.setText(day.strftime('%A, %d de %B de %Y').capitalize())

        '''
        Eventos menú herramientas
        '''
        var.ui.actionbarSalir.triggered.connect(events.Eventos.Salir)
        var.ui.actionbarabrirdirectorio.triggered.connect(events.Eventos.Abrir)
        var.ui.actionbarcrearbackup.triggered.connect(events.Eventos.crearBackup)
        var.ui.actionbarresaturabackup.triggered.connect(events.Eventos.restaurarBackup)
        var.ui.actionbarimprimir.triggered.connect(events.Eventos.Imprimir)
        var.ui.actionListado_Clientes.triggered.connect(informes.Informes.listadoClientes)


        '''
        otros eventos
        '''
        var.ui.spinEnvio.valueChanged.connect(events.Eventos.modoEnvio)




if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Main()
    desktop = QtWidgets.QApplication.desktop()
    x = (desktop.width() - window.width()) // 2
    y = (desktop.height() - window.height()) // 2
    window.move(x, y)
    var.dlgaviso = DialogAviso()
    var.dlgcalendar = DialogCalendar()
    var.dlgabrir = FileDialogAbrir()
    #window.showMaximized()
    window.show()
    sys.exit(app.exec())



