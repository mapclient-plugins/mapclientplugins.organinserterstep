# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'configuredialog.ui'
##
## Created by: Qt User Interface Compiler version 6.9.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QFormLayout, QGridLayout, QGroupBox, QLabel,
    QLineEdit, QSizePolicy, QWidget)

class Ui_ConfigureDialog(object):
    def setupUi(self, ConfigureDialog):
        if not ConfigureDialog.objectName():
            ConfigureDialog.setObjectName(u"ConfigureDialog")
        ConfigureDialog.resize(418, 303)
        self.gridLayout = QGridLayout(ConfigureDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.configGroupBox = QGroupBox(ConfigureDialog)
        self.configGroupBox.setObjectName(u"configGroupBox")
        self.formLayout = QFormLayout(self.configGroupBox)
        self.formLayout.setObjectName(u"formLayout")
        self.labelIdentifier = QLabel(self.configGroupBox)
        self.labelIdentifier.setObjectName(u"labelIdentifier")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.labelIdentifier)

        self.lineEditIdentifier = QLineEdit(self.configGroupBox)
        self.lineEditIdentifier.setObjectName(u"lineEditIdentifier")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.lineEditIdentifier)

        self.labelCommontrunk = QLabel(self.configGroupBox)
        self.labelCommontrunk.setObjectName(u"labelCommontrunk")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.labelCommontrunk)

        self.lineEditCommontrunk = QLineEdit(self.configGroupBox)
        self.lineEditCommontrunk.setObjectName(u"lineEditCommontrunk")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.lineEditCommontrunk)

        self.labelPassthrough = QLabel(self.configGroupBox)
        self.labelPassthrough.setObjectName(u"labelPassthrough")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.labelPassthrough)

        self.lineEditPassthrough = QLineEdit(self.configGroupBox)
        self.lineEditPassthrough.setObjectName(u"lineEditPassthrough")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.lineEditPassthrough)


        self.gridLayout.addWidget(self.configGroupBox, 0, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(ConfigureDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)


        self.retranslateUi(ConfigureDialog)
        self.buttonBox.accepted.connect(ConfigureDialog.accept)
        self.buttonBox.rejected.connect(ConfigureDialog.reject)

        QMetaObject.connectSlotsByName(ConfigureDialog)
    # setupUi

    def retranslateUi(self, ConfigureDialog):
        ConfigureDialog.setWindowTitle(QCoreApplication.translate("ConfigureDialog", u"Configure Step", None))
        self.configGroupBox.setTitle("")
        self.labelIdentifier.setText(QCoreApplication.translate("ConfigureDialog", u"identifier:  ", None))
        self.labelCommontrunk.setText(QCoreApplication.translate("ConfigureDialog", u"common trunk keywords:", None))
#if QT_CONFIG(tooltip)
        self.lineEditCommontrunk.setToolTip(QCoreApplication.translate("ConfigureDialog", u"A comma separated list of keywords that identify organs to be inserted via the common trunk mode. Note that these organ scaffolds will require corresponding templates.", None))
#endif // QT_CONFIG(tooltip)
        self.labelPassthrough.setText(QCoreApplication.translate("ConfigureDialog", u"pass through keywords:", None))
#if QT_CONFIG(tooltip)
        self.lineEditPassthrough.setToolTip(QCoreApplication.translate("ConfigureDialog", u"A comma separated list of keywords which identify scaffolds that are built in the same coordinate system as the whole body and do not require further processing.", None))
#endif // QT_CONFIG(tooltip)
    # retranslateUi

