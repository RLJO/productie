# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Import Stock with Serial number/Lot number in Odoo',
    'version': '14.0.0.2',
    'sequence': 4,
    'summary': 'import data App for import stock inventory adjustment import inventory adjustment import product stock import inventory with lot import stock with lot import serial import inventory data import stock balance import stock with lot import stock with Serial',
    "price": 29,
    "currency": 'EUR',
    'category' : 'Warehouse',
    'description': """
	BrowseInfo developed a new odoo/OpenERP module apps.
	This module is useful for import inventory with serial number from Excel and CSV file .-Import inventory with Serial number/Lot number from CSV and Excel file.
        Its also usefull for import opening stock balance with serial number from XLS or CSV file.
	-Import Stock from CSV and Excel file.
        -Import Stock inventory from CSV and Excel file.
	-Import inventory adjustment import stock balance
	-Import opening stock balance from CSV and Excel file.
        Import stock with Serial number import
    odoo Import stock with lot number import odoo import lot number with stock import
    odoo import serial number with stock import
    odoo import lines import
    odoo import order lines import
    import orders lines import
    import so lines import
    imporr po lines import
    odoo import stock with lot number import stock with serial number
    odoo import stock with lot package import stock with package details
    odoo import stock with serial package import stock with serial number package details odoo
	odoo Inventory import from CSV stock import from CSV Inventory adjustment import Opening stock import. 
    odoo Import warehouse stock Import product stock Manage Inventory import inventory with lot number
    odoo import inventory with serial number import inventory adjustment with serial number import inventory adjustment with lot number
    odoo import inventory data import stock data import opening stock with lot number import lot number import serial number. 
Odoo import transfer import stock transfer import receipt import odoo import stock transfers import tranfers
هذه الوحدة مفيدة لجرد الاستيراد مع الرقم التسلسلي من ملف Excel و CSV.
         لها أيضا مفيدة لتوازن رصيد فتح الواردات مع الرقم التسلسلي من XLS أو ملف CSV.
-استيراد الأسهم من ملف CSV و Excel.
         -استيراد مخزون المخزون من ملف CSV و Excel.
-مستوى الجرد الاستيراد ، رصيد المخزون الاستيراد
-استيراد رصيد المخزون الافتتاحي من ملف CSV و Excel.
الاستيراد -Inventory من CSV ، استيراد الأوراق المالية من CSV ، استيراد تعديل المخزون ، فتح استيراد المخزون. استيراد مخزون المستودع ، استيراد مخزون المنتجات.إدارة المخزون ، جرد الاستيراد مع رقم اللوت ، جرد الاستيراد مع الرقم التسلسلي ، تعديل المخزون الاستيراد مع الرقم التسلسلي ، تعديل المخزون الاستيراد مع عدد الكثير. استيراد بيانات المخزون ، وبيانات المخزون الاستيراد ، فتح مخزون الاستيراد مع رقم الكثير ، ورقم استيراد الكثير ، واستيراد الرقم التسلسلي.

Este módulo es útil para el inventario de importación con el número de serie del archivo Excel y CSV.
         También es útil para la importación de saldos iniciales con número de serie de archivo XLS o CSV.
-Importar Stock desde CSV y archivo de Excel.
         Inventario de acciones de archivo CSV y Excel.
- Ajuste de inventario de importación, balance de stock de importación
-Importar la apertura de stock de CSV y archivo de Excel.
- Inventario importado de CSV, importación de stock desde CSV, importación de ajuste de inventario, apertura de stock de importación. Importar stock de almacén, Importar inventario de producto. Administrar inventario, importar inventario con número de lote, importar inventario con número de serie, importar ajuste de inventario con número de serie, importar ajuste de inventario con número de lote. importar datos de inventario, importar datos de stock, importar stock de apertura con número de lote, número de lote de importación, número de serie de importación.

Ce module est utile pour importer un inventaire avec un numéro de série à partir d'un fichier Excel et CSV.
         Il est également utile pour importer le solde d'ouverture avec le numéro de série du fichier XLS ou CSV.
-Import Stock à partir de fichiers CSV et Excel.
         -Import Stock d'inventaire à partir de fichiers CSV et Excel.
-Ajustement de l'inventaire des importations, importation du solde du stock
- Importer le solde du stock d'ouverture du fichier CSV et Excel.
-Inventaire d'importation de CSV, importation d'actions de CSV, importation d'ajustement d'inventaire, importation d'actions d'ouverture. Stock d'entrepôt d'importation, stock d'importation de produit. Gérer l'inventaire, importer l'inventaire avec le numéro de lot, importer l'inventaire avec le numéro de série, importer l'ajustement d'inventaire avec le numéro de série, importer l'ajustement d'inventaire avec le numéro de lot. importer des données d'inventaire, importer des données de stock, importer des actions d'ouverture avec le numéro de lot, importer le numéro de lot, importer le numéro de série.

Este módulo é útil para inventário de importação com o número de série do arquivo Excel e CSV.
         Também é útil para importar o saldo do estoque de abertura com o número de série do arquivo XLS ou CSV.
-Importar estoque do arquivo CSV e Excel.
         - Inventário de inventário de estoque do arquivo CSV e Excel.
- Ajuste de estoque de importação, saldo de estoque de importação
- Importe o saldo do estoque inicial do arquivo CSV e Excel.
- Importação de inventário de CSV, importação de estoque de CSV, importação de ajuste de estoque, importação de estoque de abertura. Estoque de armazém de importação, estoque de estoque de importação. Estoque de inventário, inventário de importação com número de lote, inventário de importação com número de série, importação de inventário com número de série, importação de inventário com número de lote. importar dados de inventário, importar dados de estoque, importar estoque de abertura com número de lote, importar número de lote, importar número de série.



    """,
    'author': 'BrowseInfo',
    'website': 'https://www.browseinfo.in',
    'depends': ['base','stock','product_expiry'],
    'data': [
            'security/ir.model.access.csv',
            'views/stock_view.xml'],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'live_test_url':'https://youtu.be/qWW-qUfq2RA',
    "images":["static/description/Banner.png"],
}
